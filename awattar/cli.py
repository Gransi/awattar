import csv
import dataclasses
import datetime
import json
import sys
from typing import Optional

import click
from dateutil import tz

from awattar.client import AwattarClient


@dataclasses.dataclass
class CliContext:
    """Used as click's context object"""

    client: AwattarClient


@click.group
@click.pass_context
@click.option(
    "--country",
    type=click.Choice(["DE", "AT"]),
    default="AT",
    help="the API's target country (either Germany or Austria), default: AT",
)
def cli(ctx, country):
    """Access aWATTar's energy prices API."""
    ctx.obj = CliContext(AwattarClient(country=country))


@cli.command
@click.option("--start", type=click.DateTime(), default=None, help="the start date in local time of the interval for which to fetch the prices")
@click.option("--end", type=click.DateTime(), default=None, help="the end date in local time of the interval for which to fetch the prices")
@click.option(
    "--year",
    type=click.DateTime(["%Y"]),
    default=None,
    help="year in local time for which to fetch the prices",
)
@click.option(
    "--month",
    type=click.DateTime(["%Y-%m"]),
    default=None,
    help="year and month in local time for which to fetch the prices",
)
@click.option(
    "--day",
    type=click.DateTime(["%Y-%m-%d"]),
    default=None,
    help="year, month, and day in local time for which to fetch the prices",
)
@click.option(
    "--format",
    type=click.Choice(["json", "json-pretty", "csv", "csv-pretty"]),
    default="json-pretty",
)
@click.option("--today", is_flag=True, default=False, help="fetch today's (local time) prices")
@click.option("--tomorrow", is_flag=True, default=False, help="fetch tomorrow's (local time) prices (will only work after they've been published at 12:55 GMT")
@click.argument("FILE", type=click.File(mode="w"), default="-")
def fetch_prices(
    start: Optional[datetime.datetime],
    end: Optional[datetime.datetime],
    year: Optional[datetime.datetime],
    month: Optional[datetime.datetime],
    day: Optional[datetime.datetime],
    today: bool,
    tomorrow: bool,
    format: str,
    file: click.File,
):
    """Fetch hourly energy prices"""
    # validate parameter combination
    single = list(map(bool, [day, month, year, today, tomorrow]))
    if sum(single) > 1:
        raise click.UsageError(
            "--day, --month, --year, --today, and --tomorrow are mutually exclusive parameters. Please specify at most one of them."
        )
    if any(single) and (start or end):
        raise click.UsageError(
            "--start and --end parameters are mutually exclusiv with any of --day, --month, --year, --today, and --tomorrow."
        )
    # The API allows supplying a value for end without one for start as well as
    # an end date earlier than start date, and returns default data (current
    # day UTC) in these cases. However, this is not really intuitive and should
    # probably better be prevented in the first place.
    if not start and end:
        raise click.BadOptionUsage("--end", "--end cannot be supplied without --start")
    if start and end and not (start < end):
        raise click.BadParameter(
            "--start not earlier than --end", param_hint=["--start", "--end"]
        )

    # fetch data
    if day:
        items = _get_for_day(day.astimezone(tz.tzlocal()))
    elif month:
        items = _get_for_month(month.astimezone(tz.tzlocal()))
    elif year:
        items = _get_for_year(year.astimezone(tz.tzlocal()))
    elif today:
        date = datetime.datetime.combine(
            datetime.date.today(), datetime.time.min, tz.tzlocal()
        )
        items = _get_for_day(date)
    elif tomorrow:
        date = datetime.date.today() + datetime.timedelta(1)
        date = datetime.datetime.combine(date, datetime.time.min, tz.tzlocal())
        items = _get_for_day(date)
    else:
        items = _get_for_period(start, end)

    # make sure we got some data from the API
    if not items:
        click.echo("Error when fetching data: no data received", sys.stderr)
        raise click.Abort()

    # write data to the provided file (or print to stdout)
    out_items = [item.to_json_dict() for item in items]
    if format == "json":
        file.write(json.dumps(out_items))
    elif format == "json-pretty":
        file.write(json.dumps(out_items, indent=4))
    else:
        dialect = "excel-tab" if "pretty" in format else "excel"
        # default lineterminator led to duplicate newlines in file when running from git bash on Windows
        writer = csv.DictWriter(
            file,
            out_items[0].keys() if out_items else [],
            lineterminator="\n",
            dialect=dialect,
        )
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
