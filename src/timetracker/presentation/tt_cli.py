import configparser
from pathlib import Path
from time import time
from typing import Tuple, Type
import click
from datetime import datetime

from domain.DomainCtlImp import DomainCtlImpl as DomainCtl
from utils.parsers import parse_timestamp, parse_tags
from utils.config import load_config, DATE_FORMAT, TIME_FORMAT


def validate_time(ctx, param, value) -> float:
    try:
        return parse_timestamp(value)
    except ValueError:
        raise click.BadParameter(
            f"Got {value}. Format must be  {DATE_FORMAT} {TIME_FORMAT} or {TIME_FORMAT}."
        )
    except TypeError:
        # Its ok to be None
        return None


def validate_tags(ctx, param, value) -> Tuple[str]:
    try:
        return parse_tags(value)
    except TypeError:
        # Its ok to be None
        return tuple()


@click.group()
def cli():
    """A CLI wrapper for the TimeTracker Application"""
    pass


@cli.group()
def task():
    """Task related operations"""
    pass


@click.option(
    "-c",
    "--creation-time",
    type=click.UNPROCESSED,
    callback=validate_time,
    default=time(),
    help=f"Creation time as a timestamp, a string like {DATE_FORMAT} {TIME_FORMAT} or like {TIME_FORMAT} (using standard 1989 C standard format codes) for the task. If not specified, creation_time is the current time",
)
@click.option(
    "-s",
    "--start-time",
    type=click.UNPROCESSED,
    callback=validate_time,
    help=f"Start time as a timestamp, a string like {DATE_FORMAT} {TIME_FORMAT} or like {TIME_FORMAT} (using standard 1989 C standard format codes) for the task. If not specified, start_time is the same as creation time",
)
@click.option(
    "-e",
    "--end-time",
    type=click.UNPROCESSED,
    callback=validate_time,
    help=f"End time as a timestamp, a string like {DATE_FORMAT} {TIME_FORMAT} or like {TIME_FORMAT} (using standard 1989 C standard format codes) for the task. If not specified, this field is left empty",
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
    type=click.UNPROCESSED,
    callback=validate_tags,
    help="Comma-separated list of tags to include in the task. If not specified, this field is left empty.",
)
@click.option(
    "-n",
    "--notes",
    type=str,
    default="",
    help="Notes for thye task. If not specified, this field is left empty.",
)
@task.command()
@click.pass_context
def create(
    ctx,
    creation_time: float,
    start_time: float,
    end_time: float,
    pause: float,
    tags: str,
    notes: str,
):
    """Create a Task"""

    config = load_config()
    ctx.domainCtl = DomainCtl(config)

    if not start_time:
        start_time = creation_time

    task = ctx.domainCtl.create_task(
        creation_time, start_time, end_time, pause, tags, notes
    )
    click.echo(task)


@click.option(
    "-c",
    "--creation-time",
    type=click.UNPROCESSED,
    callback=validate_time,
    default=time(),
    help=f"Creation time as a timestamp, a string like {DATE_FORMAT} {TIME_FORMAT} or like {TIME_FORMAT} (using standard 1989 C standard format codes) for the task. If not specified, creation_time is the current time",
)
@click.option(
    "-s",
    "--start-time",
    type=click.UNPROCESSED,
    callback=validate_time,
    help=f"Start time as a timestamp, a string like {DATE_FORMAT} {TIME_FORMAT} or like {TIME_FORMAT} (using standard 1989 C standard format codes) for the task. If not specified, start_time is the same as creation time",
)
@click.option(
    "-t",
    "--tags",
    type=click.UNPROCESSED,
    callback=validate_tags,
    help="Comma-separated list of tags to include in the task. If not specified, this field is left empty.",
)
@click.option(
    "-n",
    "--notes",
    type=str,
    default="",
    help="Notes for thye task. If not specified, this field is left empty.",
)
@task.command()
@click.pass_context
def start(
    ctx,
    creation_time: float,
    start_time: float,
    tags: str,
    notes: str,
):
    """Start a Task"""
    end_time = None
    pause = 0

    config = load_config()
    ctx.domainCtl = DomainCtl(config)

    if not start_time:
        start_time = creation_time

    task = ctx.domainCtl.create_task(
        creation_time, start_time, end_time, pause, tags, notes
    )
    click.echo(task)


@click.option("-k", "--id", type=click.INT, help="ID of the task to end.")
@click.option(
    "-e",
    "--end-time",
    type=click.UNPROCESSED,
    callback=validate_time,
    help=f"End time as a timestamp, a string like {DATE_FORMAT} {TIME_FORMAT} or like {TIME_FORMAT} (using standard 1989 C standard format codes) for the task. If not specified, this field is left empty",
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
    type=click.UNPROCESSED,
    callback=validate_tags,
    help="Comma-separated list of tags to include in the task. If not specified, this field is left empty.",
)
@click.option(
    "-n",
    "--notes",
    type=click.STRING,
    default="",
    help="Notes for thye task. If not specified, this field is left empty.",
)
@task.command()
@click.pass_context
def end(
    ctx,
    id: int,
    end_time: float,
    pause: float,
    tags: str,
    notes: str,
):
    """End a Task in progress"""

    config = load_config()
    ctx.domainCtl = DomainCtl(config)
    click.echo("TODO")
    # ctx.domainCtl.update_task(id, end_time, pause, tags, notes)


@click.option("-k", "--id", type=click.INT, help="ID of the task to end.")
@click.option(
    "-e",
    "--end-time",
    type=click.UNPROCESSED,
    callback=validate_time,
    help=f"End time as a timestamp, a string like {DATE_FORMAT} {TIME_FORMAT} or like {TIME_FORMAT} (using standard 1989 C standard format codes) for the task. If not specified, this field is left empty",
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
    type=click.UNPROCESSED,
    callback=validate_tags,
    help="Comma-separated list of tags to include in the task. If not specified, this field is left empty.",
)
@click.option(
    "-n",
    "--notes",
    type=click.STRING,
    default="",
    help="Notes for thye task. If not specified, this field is left empty.",
)
@task.command()
@click.pass_context
def end_last(
    ctx,
    end_time: float,
    pause: float,
    tags: str,
    notes: str,
):
    """End a last Task in progress"""

    config = load_config()
    ctx.domainCtl = DomainCtl(config)
    click.echo("TODO")
    # ctx.domainCTl.update_task(LAST??, end_time, pause, tags, notes)


@click.option(
    "-c",
    "--creation-time",
    type=click.UNPROCESSED,
    callback=validate_time,
    default=time(),
    help=f"Creation time as a timestamp, a string like {DATE_FORMAT} {TIME_FORMAT} or like {TIME_FORMAT} (using standard 1989 C standard format codes) for the task. If not specified, creation_time is the current time",
)
@click.option(
    "-s",
    "--start-time",
    type=click.UNPROCESSED,
    callback=validate_time,
    help=f"Start time as a timestamp, a string like {DATE_FORMAT} {TIME_FORMAT} or like {TIME_FORMAT} (using standard 1989 C standard format codes) for the task. If not specified, start_time is the same as creation time",
)
@click.option(
    "-e",
    "--end-time",
    type=click.UNPROCESSED,
    callback=validate_time,
    help=f"End time as a timestamp, a string like {DATE_FORMAT} {TIME_FORMAT} or like {TIME_FORMAT} (using standard 1989 C standard format codes) for the task. If not specified, this field is left empty",
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
    type=click.UNPROCESSED,
    callback=validate_tags,
    help="Comma-separated list of tags to include in the task. If not specified, this field is left empty.",
)
@click.option(
    "-n",
    "--notes",
    type=str,
    default="",
    help="Notes for thye task. If not specified, this field is left empty.",
)
@task.command()
@click.pass_context
def update(
    ctx,
    creation_time: float,
    start_time: float,
    end_time: float,
    pause: float,
    tags: str,
    notes: str,
):
    """Create a Task"""

    config = load_config()
    ctx.domainCtl = DomainCtl(config)
    click.echo("TODO")
    # ctx.domainCtl.update_task(creation_time, start_time, end_time, pause, tags, notes)


@task.command()
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
@click.pass_context
def export(ctx, path, name, headers, human_readable):
    """Export all tasks as a CSV file."""
    config = load_config()
    ctx.domainCtl = DomainCtl(config)

    pathp = Path(path)
    namep = Path(name)
    ctx.domainCtl.export_as_csv(pathp / namep, headers, human_readable)


@task.command("import")
@click.argument("file", type=click.Path(exists=True))
@click.option(
    "--headers",
    is_flag=True,
    default=False,
    help="Set this option to tell tt_cli the CSV file has headers.",
)
@click.pass_context
def imp(ctx, file, headers):
    """Import all tasks from a CSV file."""
    config = load_config()
    ctx.domainCtl = DomainCtl(config)

    filep = Path(file)
    ctx.domainCtl.import_from_csv(filep, headers)


if __name__ == "__main__":
    cli()
