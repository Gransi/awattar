import datetime
import json
import dataclasses
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
@click.pass_obj
@click.option("--start", type=click.DateTime(), default=None)
@click.option("--end", type=click.DateTime(), default=None)
def fetch(obj: CliContext, start: Optional[datetime.datetime], end: Optional[datetime.datetime]):
    """Fetch hourly energy prices"""
    today = datetime.date.today()
    if not start:
        start = datetime.datetime.combine(
            today, datetime.time.min, tz.tzlocal()
        )
    if not end:
        end = datetime.timedelta(1) + start
    items = obj.client.request(start, end)
    print(json.dumps([item.to_json_dict() for item in items], indent=4))
