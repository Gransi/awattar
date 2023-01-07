import csv
import dataclasses
import datetime
import json
from typing import Optional

import click
from dateutil import tz

from awattar.client import AwattarClient


@dataclasses.dataclass
class CliContext:
    client: AwattarClient


@click.group
@click.pass_context
@click.option(
    "--country",
    type=click.Choice(["DE", "AT"]),
    default="DE",
    help="the API's target country (either Germany or Austria), default: DE",
)
def cli(ctx, country):
    """Access aWATTar's energy prices API."""
    ctx.obj = CliContext(AwattarClient(country=country))


@cli.command
@click.option("--start", type=click.DateTime(), default=None)
@click.option("--end", type=click.DateTime(), default=None)
@click.option(
    "--year",
    type=click.DateTime(["%Y"]),
    default=None,
    help="the year for which to fetch the data",
)
@click.option(
    "--month",
    type=click.DateTime(["%Y-%m"]),
    default=None,
    help="the year and month for which to fetch the data",
)
@click.option(
    "--day",
    type=click.DateTime(["%Y-%m-%d"]),
    default=None,
    help="the year, month, and day for which to fetch the data",
)
@click.option("--format",type=click.Choice(["json", "csv"]), default="json")
@click.argument("FILE", type=click.File(mode="w"), default="-")
def fetch(
    start: Optional[datetime.datetime],
    end: Optional[datetime.datetime],
    year: Optional[datetime.datetime],
    month: Optional[datetime.datetime],
    day: Optional[datetime.datetime],
    format: str,
    file: click.File,
):
    """Fetch hourly energy prices"""
    if day:
        items = _get_for_day(day.astimezone(tz.tzlocal()))
    elif month:
        items = _get_for_month(month.astimezone(tz.tzlocal()))
    elif year:
        items = _get_for_year(year.astimezone(tz.tzlocal()))
    else:
        today = datetime.date.today()
        if not start:
            start = datetime.datetime.combine(today, datetime.time.min, tz.tzlocal())
        if not end:
            end = start + datetime.timedelta(1)
        items = _get_for_period(start, end)
    out_items = [item.to_json_dict() for item in items]
    if format == "json":
        file.write(json.dumps(out_items, indent=4))
    else:
        # default lineterminator led to duplicate newlines in file when running from git bash on Windows
        writer = csv.DictWriter(file, out_items[0].keys(), lineterminator="\n", dialect="excel-tab")
        writer.writeheader()
        writer.writerows(out_items)


def _get_for_period(start: datetime.datetime, end: datetime.datetime):
    return (
        click.get_current_context().find_object(CliContext).client.request(start, end)
    )


def _get_for_year(year: datetime.datetime):
    return _get_for_period(year, year.replace(year=year.year + 1))


def _get_for_month(month: datetime.datetime):
    try:
        return _get_for_period(month, month.replace(month=month.month + 1))
    except ValueError:
        return _get_for_period(month, month.replace(year=month.year + 1, month=1))


def _get_for_day(day: datetime.datetime):
    return _get_for_period(day, day + datetime.timedelta(1))
