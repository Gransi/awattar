import pytest
import click
import datetime
import pytz
from datetime import timedelta
from tzlocal import get_localzone

from awattar.client import AwattarClient
from awattar.marketitem import MarketItem

def test_basic_api_today():
    client = AwattarClient('AT')
    data = client.today()

    assert len(data) == 23
    assert data[0].start_datetime == datetime.datetime.now().replace(hour=1, minute=0,second=0,microsecond=0, tzinfo=get_localzone())

def test_basic_api_past():
    client = AwattarClient('AT')    
    data = client.request(datetime.datetime(2023, 10, 17, 12, 0, 0),datetime.datetime(2023, 10, 17, 18, 0, 0))

    assert len(data) == 6
    assert data[0].start_datetime == datetime.datetime(2023, 10, 17, 12, 0, 0, tzinfo=get_localzone()) 

    # get best slot
    best_slot = client.best_slot(1,datetime.datetime(2020, 10, 17, 12, 0, 0),datetime.datetime(2020, 10, 17, 18, 0, 0))
    assert best_slot is None

    # get best slot
    best_slot = client.best_slot(1,datetime.datetime(2023, 10, 17, 12, 0, 0),datetime.datetime(2023, 10, 17, 18, 0, 0))  
    assert isinstance(best_slot, MarketItem)  
    assert best_slot.marketprice == 125.35
