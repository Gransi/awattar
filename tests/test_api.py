import datetime

from tzlocal import get_localzone

from awattar.client import AwattarClient
from awattar.marketitem import MarketItem


def test_basic_api_today() -> None:
    client = AwattarClient("AT")
    data = client.today()

    assert len(data) == 23
    assert data[0].start_datetime == datetime.datetime.now(tz=datetime.timezone.utc).replace(hour=1, minute=0, second=0, microsecond=0, tzinfo=get_localzone())


def test_basic_api_min_and_max() -> None:
    client = AwattarClient("AT")
    data = client.request(datetime.datetime(2023, 10, 17, 12, 0, 0, tzinfo=get_localzone()), datetime.datetime(2023, 10, 17, 18, 0, 0, tzinfo=get_localzone()))

    assert len(data) == 6
    assert data[0].start_datetime == datetime.datetime(2023, 10, 17, 12, 0, 0, tzinfo=get_localzone())

    # get min slot
    min_slot = client.min()
    assert isinstance(min_slot, MarketItem)
    assert min_slot.start_datetime == datetime.datetime(2023, 10, 17, 12, 0, 0, tzinfo=get_localzone())
    assert min_slot.end_datetime == datetime.datetime(2023, 10, 17, 13, 0, 0, tzinfo=get_localzone())
    assert min_slot.marketprice == 110.93

    # get max slot
    max_slot = client.max()
    assert isinstance(max_slot, MarketItem)
    assert max_slot.start_datetime == datetime.datetime(2023, 10, 17, 17, 0, 0, tzinfo=get_localzone())
    assert max_slot.end_datetime == datetime.datetime(2023, 10, 17, 18, 0, 0, tzinfo=get_localzone())
    assert max_slot.marketprice == 164.9


def test_basic_api_min_and_max2() -> None:
    client = AwattarClient("AT")
    data = client.request(datetime.datetime(2023, 8, 8, 0, 0, 0, tzinfo=get_localzone()), datetime.datetime(2023, 8, 9, 0, 0, 0, tzinfo=get_localzone()))

    assert len(data) == 24
    assert data[0].start_datetime == datetime.datetime(2023, 8, 8, 0, 0, 0, tzinfo=get_localzone())

    # get min slot
    min_slot = client.min()
    assert isinstance(min_slot, MarketItem)
    assert min_slot.start_datetime == datetime.datetime(2023, 8, 8, 2, 0, 0, tzinfo=get_localzone())
    assert min_slot.end_datetime == datetime.datetime(2023, 8, 8, 3, 0, 0, tzinfo=get_localzone())
    assert min_slot.marketprice == -18.59

    # get max slot
    max_slot = client.max()
    assert isinstance(max_slot, MarketItem)
    assert max_slot.start_datetime == datetime.datetime(2023, 8, 8, 21, 0, 0, tzinfo=get_localzone())
    assert max_slot.end_datetime == datetime.datetime(2023, 8, 8, 22, 0, 0, tzinfo=get_localzone())
    assert max_slot.marketprice == 89.18


def test_basic_api_mean() -> None:
    client = AwattarClient("AT")
    data = client.request(datetime.datetime(2023, 8, 8, 0, 0, 0, tzinfo=get_localzone()), datetime.datetime(2023, 8, 9, 0, 0, 0, tzinfo=get_localzone()))

    assert len(data) == 24
    assert data[0].start_datetime == datetime.datetime(2023, 8, 8, 0, 0, 0, tzinfo=get_localzone())

    # get mean slot
    mean_slot = client.mean()
    assert isinstance(mean_slot, MarketItem)
    assert mean_slot.start_datetime == datetime.datetime(2023, 8, 8, 0, 0, 0, tzinfo=get_localzone())
    assert mean_slot.end_datetime == datetime.datetime(2023, 8, 9, 0, 0, 0, tzinfo=get_localzone())
    assert mean_slot.marketprice == 17.729166666666668


def test_basic_api_best_slot() -> None:
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
    assert best_slot.start_datetime == datetime.datetime(2023, 10, 17, 12, 0, 0, tzinfo=get_localzone())
    assert best_slot.end_datetime == datetime.datetime(2023, 10, 17, 13, 0, 0, tzinfo=get_localzone())
    assert best_slot.marketprice == 110.93

    best_slot = client.best_slot(2, datetime.datetime(2023, 10, 17, 12, 0, 0, tzinfo=get_localzone()), datetime.datetime(2023, 10, 17, 18, 0, 0, tzinfo=get_localzone()))
    assert isinstance(best_slot, MarketItem)
    assert best_slot.start_datetime == datetime.datetime(2023, 10, 17, 12, 0, 0, tzinfo=get_localzone())
    assert best_slot.end_datetime == datetime.datetime(2023, 10, 17, 14, 0, 0, tzinfo=get_localzone())
    assert best_slot.marketprice == 112.59

    best_slot = client.best_slot(3, datetime.datetime(2023, 10, 17, 12, 0, 0, tzinfo=get_localzone()), datetime.datetime(2023, 10, 17, 18, 0, 0, tzinfo=get_localzone()))
    assert isinstance(best_slot, MarketItem)
    assert best_slot.start_datetime == datetime.datetime(2023, 10, 17, 12, 0, 0, tzinfo=get_localzone())
    assert best_slot.end_datetime == datetime.datetime(2023, 10, 17, 15, 0, 0, tzinfo=get_localzone())
    assert best_slot.marketprice == 116.84333333333332

    best_slot = client.best_slot(1, datetime.datetime(2023, 10, 17, 16, 0, 0, tzinfo=get_localzone()), datetime.datetime(2023, 10, 17, 18, 0, 0, tzinfo=get_localzone()))
    assert isinstance(best_slot, MarketItem)
    assert best_slot.start_datetime == datetime.datetime(2023, 10, 17, 16, 0, 0, tzinfo=get_localzone())
    assert best_slot.end_datetime == datetime.datetime(2023, 10, 17, 17, 0, 0, tzinfo=get_localzone())
    assert best_slot.marketprice == 150

    best_slot = client.best_slot(1, datetime.datetime(2023, 10, 17, 17, 0, 0, tzinfo=get_localzone()), datetime.datetime(2023, 10, 17, 18, 0, 0, tzinfo=get_localzone()))
    assert isinstance(best_slot, MarketItem)
    assert best_slot.start_datetime == datetime.datetime(2023, 10, 17, 17, 0, 0, tzinfo=get_localzone())
    assert best_slot.end_datetime == datetime.datetime(2023, 10, 17, 18, 0, 0, tzinfo=get_localzone())
    assert best_slot.marketprice == 164.9

    best_slot = client.best_slot(1, datetime.datetime(2023, 10, 17, 18, 0, 0, tzinfo=get_localzone()), datetime.datetime(2023, 10, 17, 19, 0, 0, tzinfo=get_localzone()))
    assert best_slot is None


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

    assert data[9].start_datetime == datetime.datetime(2023, 10, 17, 12, 0, 0, tzinfo=get_localzone())
    assert data[9].end_datetime == datetime.datetime(2023, 10, 17, 13, 0, 0, tzinfo=get_localzone())
    assert data[9].energy_unit == "MWh"
    assert data[9].price_per_kWh == 0.11093
    assert data[9].marketprice == 110.93
    assert data[9].unit == "Eur/MWh"

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


def test_basic_api_best_slot2() -> None:
    client = AwattarClient("AT")
    data = client.request(datetime.datetime(2023, 8, 8, 0, 0, 0, tzinfo=get_localzone()), datetime.datetime(2023, 8, 9, 0, 0, 0, tzinfo=get_localzone()))

    assert len(data) == 24
    assert data[0].start_datetime == datetime.datetime(2023, 8, 8, 0, 0, 0, tzinfo=get_localzone())
    assert data[23].end_datetime == datetime.datetime(2023, 8, 9, 0, 0, 0, tzinfo=get_localzone())

    # test negative results; wrong timerange
    best_slot = client.best_slot(1, datetime.datetime(2020, 8, 8, 12, 0, 0, tzinfo=get_localzone()), datetime.datetime(2020, 8, 8, 18, 0, 0, tzinfo=get_localzone()))
    assert best_slot is None

    # get best slot
    best_slot = client.best_slot(1, datetime.datetime(2023, 8, 8, 0, 0, 0, tzinfo=get_localzone()), datetime.datetime(2023, 8, 9, 0, 0, 0, tzinfo=get_localzone()))
    assert isinstance(best_slot, MarketItem)
    assert best_slot.start_datetime == datetime.datetime(2023, 8, 8, 2, 0, 0, tzinfo=get_localzone())
    assert best_slot.end_datetime == datetime.datetime(2023, 8, 8, 3, 0, 0, tzinfo=get_localzone())
    assert best_slot.marketprice == -18.59

    best_slot = client.best_slot(1, datetime.datetime(2023, 8, 8, 12, 0, 0, tzinfo=get_localzone()), datetime.datetime(2023, 8, 8, 18, 0, 0, tzinfo=get_localzone()))
    assert isinstance(best_slot, MarketItem)
    assert best_slot.start_datetime == datetime.datetime(2023, 8, 8, 14, 0, 0, tzinfo=get_localzone())
    assert best_slot.end_datetime == datetime.datetime(2023, 8, 8, 15, 0, 0, tzinfo=get_localzone())
    assert best_slot.marketprice == -10.01

    best_slot = client.best_slot(2, datetime.datetime(2023, 8, 8, 12, 0, 0, tzinfo=get_localzone()), datetime.datetime(2023, 8, 8, 18, 0, 0, tzinfo=get_localzone()))
    assert isinstance(best_slot, MarketItem)
    assert best_slot.start_datetime == datetime.datetime(2023, 8, 8, 13, 0, 0, tzinfo=get_localzone())
    assert best_slot.end_datetime == datetime.datetime(2023, 8, 8, 15, 0, 0, tzinfo=get_localzone())
    assert best_slot.marketprice == -8.655

    best_slot = client.best_slot(3, datetime.datetime(2023, 8, 8, 12, 0, 0, tzinfo=get_localzone()), datetime.datetime(2023, 8, 8, 18, 0, 0, tzinfo=get_localzone()))
    assert isinstance(best_slot, MarketItem)
    assert best_slot.start_datetime == datetime.datetime(2023, 8, 8, 13, 0, 0, tzinfo=get_localzone())
    assert best_slot.end_datetime == datetime.datetime(2023, 8, 8, 16, 0, 0, tzinfo=get_localzone())
    assert best_slot.marketprice == -7.2299999999999995

    best_slot = client.best_slot(1, datetime.datetime(2023, 8, 8, 16, 0, 0, tzinfo=get_localzone()), datetime.datetime(2023, 8, 8, 18, 0, 0, tzinfo=get_localzone()))
    assert isinstance(best_slot, MarketItem)
    assert best_slot.start_datetime == datetime.datetime(2023, 8, 8, 16, 0, 0, tzinfo=get_localzone())
    assert best_slot.end_datetime == datetime.datetime(2023, 8, 8, 17, 0, 0, tzinfo=get_localzone())
    assert best_slot.marketprice == 0.09

    best_slot = client.best_slot(1, datetime.datetime(2023, 8, 8, 17, 0, 0, tzinfo=get_localzone()), datetime.datetime(2023, 8, 8, 18, 0, 0, tzinfo=get_localzone()))
    assert isinstance(best_slot, MarketItem)
    assert best_slot.start_datetime == datetime.datetime(2023, 8, 8, 17, 0, 0, tzinfo=get_localzone())
    assert best_slot.end_datetime == datetime.datetime(2023, 8, 8, 18, 0, 0, tzinfo=get_localzone())
    assert best_slot.marketprice == 11.7

    best_slot = client.best_slot(1, datetime.datetime(2023, 8, 8, 18, 0, 0, tzinfo=get_localzone()), datetime.datetime(2023, 8, 8, 19, 0, 0, tzinfo=get_localzone()))
    assert isinstance(best_slot, MarketItem)
    assert best_slot.start_datetime == datetime.datetime(2023, 8, 8, 18, 0, 0, tzinfo=get_localzone())
    assert best_slot.end_datetime == datetime.datetime(2023, 8, 8, 19, 0, 0, tzinfo=get_localzone())
    assert best_slot.marketprice == 34.61

    best_slot = client.best_slot(1, datetime.datetime(2023, 8, 8, 23, 0, 0, tzinfo=get_localzone()), datetime.datetime(2023, 8, 9, 0, 0, 0, tzinfo=get_localzone()))
    assert isinstance(best_slot, MarketItem)
    assert best_slot.start_datetime == datetime.datetime(2023, 8, 8, 23, 0, 0, tzinfo=get_localzone())
    assert best_slot.end_datetime == datetime.datetime(2023, 8, 9, 0, 0, 0, tzinfo=get_localzone())
    assert best_slot.marketprice == 59.98

    best_slot = client.best_slot(24, datetime.datetime(2023, 8, 8, 0, 0, 0, tzinfo=get_localzone()), datetime.datetime(2023, 8, 9, 0, 0, 0, tzinfo=get_localzone()))
    assert isinstance(best_slot, MarketItem)
    assert best_slot.start_datetime == datetime.datetime(2023, 8, 8, 0, 0, 0, tzinfo=get_localzone())
    assert best_slot.end_datetime == datetime.datetime(2023, 8, 9, 0, 0, 0, tzinfo=get_localzone())
    assert best_slot.marketprice == 17.729166666666668
    assert best_slot.price_per_kWh == 0.017729166666666667
