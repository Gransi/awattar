import datetime

from tzlocal import get_localzone

from awattar.client import AwattarClient
from awattar.marketitem import MarketItem


def test_basic_api_today() -> None:
    client = AwattarClient("AT")
    data = client.today()

    assert len(data) == 23
    assert data[0].start_datetime == datetime.datetime.now(tz=datetime.timezone.utc).replace(hour=1, minute=0, second=0, microsecond=0, tzinfo=get_localzone())


def test_basic_api_past() -> None:
    client = AwattarClient("AT")
    data = client.request(datetime.datetime(2023, 10, 17, 12, 0, 0, tzinfo=get_localzone()), datetime.datetime(2023, 10, 17, 18, 0, 0, tzinfo=get_localzone()))

    assert len(data) == 6
    assert data[0].start_datetime == datetime.datetime(2023, 10, 17, 12, 0, 0, tzinfo=get_localzone())

    # test negative results; wrong timerange
    best_slot = client.best_slot(1, datetime.datetime(2020, 10, 17, 12, 0, 0, tzinfo=get_localzone()), datetime.datetime(2020, 10, 17, 18, 0, 0, tzinfo=get_localzone()))
    assert best_slot is None

    # get best slot
    best_slot = client.best_slot(1, datetime.datetime(2023, 10, 17, 12, 0, 0, tzinfo=get_localzone()), datetime.datetime(2023, 10, 17, 18, 0, 0, tzinfo=get_localzone()))
    assert isinstance(best_slot, MarketItem)
    assert best_slot.marketprice == 125.35


def test_basic_api_past2() -> None:
    client = AwattarClient("AT")
    data = client.request(datetime.datetime(2023, 10, 17, 3, 0, 0, tzinfo=get_localzone()), datetime.datetime(2023, 10, 17, 18, 0, 0, tzinfo=get_localzone()))

    assert len(data) == 15

    assert data[0].start_datetime == datetime.datetime(2023, 10, 17, 3, 0, 0, tzinfo=get_localzone())
    assert data[0].end_datetime == datetime.datetime(2023, 10, 17, 4, 0, 0, tzinfo=get_localzone())
    assert data[0].energy_unit == "MWh"
    assert data[0].price_per_kWh == 0.10409
    assert data[0].marketprice == 104.09
    assert data[0].unit == "Eur/MWh"

    assert data[3].start_datetime == datetime.datetime(2023, 10, 17, 6, 0, 0, tzinfo=get_localzone())
    assert data[3].end_datetime == datetime.datetime(2023, 10, 17, 7, 0, 0, tzinfo=get_localzone())
    assert data[3].energy_unit == "MWh"
    assert data[3].price_per_kWh == 0.15369999999999998
    assert data[3].marketprice == 153.7
    assert data[3].unit == "Eur/MWh"

    assert data[6].start_datetime == datetime.datetime(2023, 10, 17, 9, 0, 0, tzinfo=get_localzone())
    assert data[6].end_datetime == datetime.datetime(2023, 10, 17, 10, 0, 0, tzinfo=get_localzone())
    assert data[6].energy_unit == "MWh"
    assert data[6].price_per_kWh == 0.15925999999999998
    assert data[6].marketprice == 159.26
    assert data[6].unit == "Eur/MWh"

    assert data[10].start_datetime == datetime.datetime(2023, 10, 17, 13, 0, 0, tzinfo=get_localzone())
    assert data[10].end_datetime == datetime.datetime(2023, 10, 17, 14, 0, 0, tzinfo=get_localzone())
    assert data[10].energy_unit == "MWh"
    assert data[10].price_per_kWh == 0.11425
    assert data[10].marketprice == 114.25
    assert data[10].unit == "Eur/MWh"

    assert data[14].start_datetime == datetime.datetime(2023, 10, 17, 17, 0, 0, tzinfo=get_localzone())
    assert data[14].end_datetime == datetime.datetime(2023, 10, 17, 18, 0, 0, tzinfo=get_localzone())
    assert data[14].energy_unit == "MWh"
    assert data[14].price_per_kWh == 0.16490000000000002
    assert data[14].marketprice == 164.9
    assert data[14].unit == "Eur/MWh"
