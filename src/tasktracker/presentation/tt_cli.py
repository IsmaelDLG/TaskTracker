from distutils import log
from pathlib import Path
from time import time
from typing import Tuple, Type
import click
from datetime import datetime
from tasktracker.domain.DomainCtlImp import DomainCtlImp as DomainCtl
from tasktracker import getCustomLogger, CONFIG

logger = getCustomLogger("presentation.tt_cli")


def validate_tags(ctx, param: str, value: str) -> Tuple[str]:
    try:
        logger.debug(f":validate_tags {param}: {value}")
        if not param:
            e = TypeError("Cannot parse None to tags!")
            logger.exception(e)
            raise e
        if isinstance(value, tuple):
            return value
        elif isinstance(value, str):
            return tuple(value.split(","))
        else:
            return ()
    except TypeError:
        # Its ok to be None
        return tuple()


@click.group()
def cli():
    """A CLI wrapper for the TimeTracker Application"""
    pass


@cli.group()
def tasks():
    """Task related operations"""
    pass


@click.option(
    "-s",
    "--start-time",
    type=click.DateTime(formats=[CONFIG["DATES"]["datetime_format"]]),
    default=None,
    help=f"Start time as a timestamp or a string-like date. If not specified, now is used.",
)
@click.option(
    "-e",
    "--end-time",
    type=click.DateTime(formats=[CONFIG["DATES"]["datetime_format"]]),
    help=f"End time as a timestamp or a string-like date. If not specified, this field is left empty",
)
@click.option(
    "-p",
    "--pause",
    type=float,
    default=0,
    help="Time spent in seconds of pause in this task. If not specified, this field is 0.",
)
@click.option(
    "-t",
    "--tags",
    type=str,
    callback=validate_tags,
    help="Comma-separated list of tags to include in the task. If not specified, this field is left empty.",
)
@click.option(
    "-n",
    "--notes",
    type=str,
    default="",
    help="Notes for the task. If not specified, this field is left empty.",
)
@tasks.command()
def create(
    start_time: float,
    end_time: float,
    pause: float,
    tags: str,
    notes: str,
):
    """Create a Task"""

    domainCtl = DomainCtl()

    if not start_time:
        start_time = datetime.utcnow()

    task = domainCtl.create_task(
        start_time.timestamp(),
        end_time.timestamp() if end_time else None,
        pause,
        tags,
        notes,
    )

    click.echo(task)


@click.argument("id", nargs=1, type=click.INT)
@click.option(
    "-s",
    "--start-time",
    type=click.DateTime(formats=[CONFIG["DATES"]["datetime_format"]]),
    default=None,
    help=f"Start time as a timestamp or a string-like date. If not specified, time() is used.",
)
@click.option(
    "-e",
    "--end-time",
    type=click.DateTime(formats=[CONFIG["DATES"]["datetime_format"]]),
    help=f"End time as a timestamp or a string-like date. If not specified, this field is left empty",
)
@click.option(
    "-p",
    "--pause",
    type=float,
    default=0,
    help="Time spent in seconds of pause in this task. If not specified, this field is 0.",
)
@click.option(
    "-t",
    "--tags",
    type=str,
    callback=validate_tags,
    help="Comma-separated list of tags to include in the task. If not specified, this field is left empty.",
)
@click.option(
    "-n",
    "--notes",
    type=str,
    default="",
    help="Notes for the task. If not specified, this field is left empty.",
)
@tasks.command()
def edit(
    id: int,
    start_time: float,
    end_time: float,
    pause: float,
    tags: tuple,
    notes: str,
):
    """Edit a task"""

    domainCtl = DomainCtl()

    try:
        task = domainCtl.edit_task(id, start_time, end_time, pause, tags, notes)
    except KeyError as e:
        click.echo(str(e))
        return 1


@click.option(
    "-k",
    "--id",
    type=click.INT,
    default=None,
    help="ID of the task. If not specified, this method will return the last task created.",
)
@tasks.command()
def get(id: int):
    """Get a task"""
    domainCtl = DomainCtl()
    if id:
        try:
            task = domainCtl.get_task(id)
        except KeyError as e:
            click.echo(str(e))
            return 1
    else:
        try:
            task = domainCtl.get_last_task()
        except KeyError as e:
            click.echo(str(e))
            return 1
    click.echo(task)


@click.argument("id", nargs=1, type=click.INT)
@tasks.command()
def delete(id: int):
    """Delete a task"""
    domainCtl = DomainCtl()
    try:
        task = domainCtl.delete_task(id)
    except KeyError as e:
        click.echo(f"Task {id} does not exist")
        return 1

    click.echo(f"Deleted task: {task}")


@tasks.command()
def get_all():
    """Get all tasks in the database"""

    domainCtl = DomainCtl()
    current = None
    try:
        current = domainCtl.get_last_task()
        click.echo(current)
    except KeyError as e:
        click.echo("No tasks were found!")
        return

    i = current.id - 1
    while i > 0:
        try:
            current = domainCtl.get_task(i)
            click.echo(current)
        except KeyError as e:
            pass
        i -= 1


@tasks.command()
@click.argument("path", type=click.Path(exists=True), default=str(Path(".").absolute()))
@click.argument("name", type=str, default=f"tasks-{int(round(time()))}.csv")
@click.option(
    "--headers",
    is_flag=True,
    default=False,
    help="Set this option to tell tt_cli the CSV file needs to have headers.",
)
@click.option(
    "--human-readable",
    is_flag=True,
    default=False,
    help="Set this option to tell tt_cli the CSV file needs to be human readable (affects dates and numbers).",
)
def export(path, name, headers, human_readable):
    """Export all tasks as a CSV file."""

    domainCtl = DomainCtl()

    pathp = Path(path)
    namep = Path(name)
    domainCtl.export_as_csv(pathp / namep, headers, human_readable)


@tasks.command("import")
@click.argument("file", type=click.Path(exists=True))
@click.option(
    "--headers",
    is_flag=True,
    default=False,
    help="Set this option to tell tt_cli the CSV file has headers.",
)
def imp(file, headers):
    """Import all tasks from a CSV file."""
    domainCtl = DomainCtl()

    filep = Path(file)
    domainCtl.import_from_csv(filep, headers)
