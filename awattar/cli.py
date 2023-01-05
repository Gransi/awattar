import datetime
import json

import click
from dateutil import tz

from awattar.client import AwattarClient


@click.group
def cli():
    pass


@cli.command
def fetch():
    """Fetch hourly energy prices for Germany provided via aWATTar's API."""
    today = datetime.date.today()
    start: datetime.datetime = datetime.datetime.combine(
        today, datetime.time.min, tz.tzlocal()
    )
    end: datetime.datetime = datetime.timedelta(1) + start
    print(start)
    print(end)
    client = AwattarClient("DE")
    items = client.request(start, end)
    item = items[0]
    print(item)
    print(json.dumps([item.to_json_dict() for item in items], indent=4))
