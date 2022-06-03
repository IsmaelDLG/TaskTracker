from pathlib import Path
from time import time
from typing import Tuple, Type
import click
from datetime import datetime
from tasktracker.domain.DomainCtlImp import DomainCtlImp as DomainCtl
from tasktracker import getCustomLogger, CONFIG


def validate_time(ctx, param, value) -> float:
    return param.timestamp()


def validate_tags(ctx, param, value) -> Tuple[str]:
    try:
        logger.debug(f"tags: {param}")
        if not param:
            raise TypeError("Cannot parse None to tags!")
        if isinstance(param, tuple):
            return param
        elif isinstance(param, str):
            return tuple(param.split(","))
        else:
            return ""
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
    "-c",
    "--creation-time",
    type=click.DateTime(formats=[CONFIG["DATES"]["datetime_format"]]),
    default=datetime.utcnow(),
    help=f"Creation time as a timestamp or a string-like date. If not specified, creation_time is the current time",
)
@click.option(
    "-s",
    "--start-time",
    type=click.DateTime(formats=[CONFIG["DATES"]["datetime_format"]]),
    default=None,
    help=f"Start time as a timestamp or a string-like date. If not specified, start_time is the same as creation time",
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
    creation_time: float,
    start_time: float,
    end_time: float,
    pause: float,
    tags: str,
    notes: str,
):
    """Create a Task"""

    domainCtl = DomainCtl()

    if not creation_time:
        creation_time = datetime.utcnow().timestamp()
    if not start_time:
        start_time = creation_time

    task = domainCtl.create_task(
        creation_time.timestamp(),
        start_time.timestamp(),
        end_time.timestamp(),
        pause,
        tags,
        notes,
    )
    click.echo(task)


@click.option(
    "-c",
    "--creation-time",
    type=click.DateTime(formats=[CONFIG["DATES"]["datetime_format"]]),
    default=datetime.utcnow(),
    help=f"Creation time as a timestamp or a string-like date. If not specified, creation_time is the current time",
)
@click.option(
    "-s",
    "--start-time",
    type=click.DateTime(formats=[CONFIG["DATES"]["datetime_format"]]),
    help=f"Start time as a timestamp or a string-like date. If not specified, start_time is the same as creation time",
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
def start(
    creation_time: float,
    start_time: float,
    tags: str,
    notes: str,
):
    """Start a Task"""
    end_time = None
    pause = 0

    domainCtl = DomainCtl()

    if not start_time:
        start_time = creation_time

    task = domainCtl.create_task(
        creation_time.timestamp(),
        start_time.timestamp(),
        end_time.timestamp(),
        pause,
        tags,
        notes,
    )
    click.echo(task)


@click.option("-k", "--id", type=click.INT, help="ID of the task to end.")
@click.option(
    "-e",
    "--end-time",
    type=click.DateTime(formats=[CONFIG["DATES"]["datetime_format"]]),
    help=f"End time as a timestamp or a string-like date. If not specified, this field is left empty",
)
@click.option(
    "-p",
    "--pause",
    type=click.FLOAT,
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
    type=click.STRING,
    default="",
    help="Notes for the task. If not specified, this field is left empty.",
)
@tasks.command()
def end(
    id: int,
    end_time: float,
    pause: float,
    tags: str,
    notes: str,
):
    """End a Task in progress"""

    domainCtl = DomainCtl()
    click.echo("TODO")
    # domainCtl.update_task(id, end_time.timestamp(), pause, tags, notes)


@click.option("-k", "--id", type=click.INT, help="ID of the task to end.")
@click.option(
    "-e",
    "--end-time",
    type=click.DateTime(formats=[CONFIG["DATES"]["datetime_format"]]),
    help=f"End time as a timestamp or a string-like date. If not specified, this field is left empty",
)
@click.option(
    "-p",
    "--pause",
    type=click.FLOAT,
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
    type=click.STRING,
    default="",
    help="Notes for the task. If not specified, this field is left empty.",
)
@tasks.command()
def end_last(
    end_time: float,
    pause: float,
    tags: str,
    notes: str,
):
    """End a last Task in progress"""

    domainCtl = DomainCtl()
    click.echo("TODO")
    # ctx.domainCTl.update_task(LAST??, end_time.timestamp(), pause, tags, notes)


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
        task = domainCtl.get_task(id)
    else:
        task = domainCtl.get_last_task()
    click.echo(task)


@click.option(
    "-c",
    "--creation-time",
    type=click.DateTime(formats=[CONFIG["DATES"]["datetime_format"]]),
    default=datetime.utcnow(),
    help=f"Creation time as a timestamp or a string-like date. If not specified, creation_time is the current time",
)
@click.option(
    "-s",
    "--start-time",
    type=click.DateTime(formats=[CONFIG["DATES"]["datetime_format"]]),
    help=f"Start time as a timestamp or a string-like date. If not specified, start_time is the same as creation time",
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
def update(
    creation_time: float,
    start_time: float,
    end_time: float,
    pause: float,
    tags: str,
    notes: str,
):
    """Create a Task"""

    domainCtl = DomainCtl()
    click.echo("TODO")
    # domainCtl.update_task(creation_time.timestamp(), start_time.timestamp(), end_time.timestamp(), pause, tags, notes)


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


logger = getCustomLogger("presentation.tt_cli")

if __name__ == "__main__":
    cli()
