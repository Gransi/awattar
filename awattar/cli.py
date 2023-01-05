import datetime
import json
import dataclasses

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
def fetch(obj: CliContext):
    """Fetch hourly energy prices"""
    today = datetime.date.today()
    start: datetime.datetime = datetime.datetime.combine(
        today, datetime.time.min, tz.tzlocal()
    )
    end: datetime.datetime = datetime.timedelta(1) + start
    items = obj.client.request(start, end)
    print(json.dumps([item.to_json_dict() for item in items], indent=4))
