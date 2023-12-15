import datetime
import sys

from tzlocal import get_localzone

from awattar import AwattarClient


def main(argv: list[str]) -> None:
    print("Connect to aWATTar")
    client = AwattarClient("AT")

    print("-----------------------------------------------------------------")
    print("Get Market data from API")
    data = client.request()

    for item in data:
        print(f"{item.start_datetime:%Y-%m-%d %H:%M:%S} - {item.end_datetime:%Y-%m-%d %H:%M:%S} - {(item.marketprice / 1000):.4f} EUR/kWh")

    print("-----------------------------------------------------------------")
    print("Get Market data from API - today")
    data = client.today()

    for item in data:
        print(f"{item.start_datetime:%Y-%m-%d %H:%M:%S} - {item.end_datetime:%Y-%m-%d %H:%M:%S} - {(item.marketprice / 1000):.4f} EUR/kWh")

    print("-----------------------------------------------------------------")
    print("Get Market data from API - tomorrow")
    data = client.tomorrow()

    for item in data:
        print(f"{item.start_datetime:%Y-%m-%d %H:%M:%S} - {item.end_datetime:%Y-%m-%d %H:%M:%S} - {(item.marketprice / 1000):.4f} EUR/kWh")

    print("-----------------------------------------------------------------")
    print("Get Market data from 2020-05-17")
    data = client.request(datetime.datetime(2020, 5, 17, tzinfo=get_localzone()))
    for item in data:
        print(f"{item.start_datetime:%Y-%m-%d %H:%M:%S} - {item.end_datetime:%Y-%m-%d %H:%M:%S} - {(item.marketprice / 1000):.4f} EUR/kWh")

    print("-----------------------------------------------------------------")
    print("Get Market data between 2020-05-18 and 2020-05-19")
    data = client.request(datetime.datetime(2020, 5, 18, tzinfo=get_localzone()), datetime.datetime(2020, 5, 19, tzinfo=get_localzone()))
    for item in data:
        print(f"{item.start_datetime:%Y-%m-%d %H:%M:%S} - {item.end_datetime:%Y-%m-%d %H:%M:%S} - {(item.marketprice / 1000):.4f} EUR/kWh")

    print("-----------------------------------------------------------------")
    print("Get Market data from API - today with min/max/mean")
    data = client.request()
    for item in data:
        print(f"{item.start_datetime:%Y-%m-%d %H:%M:%S} - {item.end_datetime:%Y-%m-%d %H:%M:%S} - {(item.marketprice / 1000):.4f} EUR/kWh")

    min_item = client.min()
    print(f"Min: {min_item.start_datetime:%Y-%m-%d %H:%M:%S} - {min_item.end_datetime:%Y-%m-%d %H:%M:%S} - {(min_item.marketprice / 1000):.4f} EUR/kWh")

    max_item = client.max()
    print(f"Max: {max_item.start_datetime:%Y-%m-%d %H:%M:%S} - {max_item.end_datetime:%Y-%m-%d %H:%M:%S} - {(max_item.marketprice / 1000):.4f} EUR/kWh")

    mean_item = client.mean()
    print(f"Mean: {mean_item.start_datetime:%Y-%m-%d %H:%M:%S} - {mean_item.end_datetime:%Y-%m-%d %H:%M:%S} - {(mean_item.marketprice / 1000):.4f} EUR/kWh")

    print("-----------------------------------------------------------------")
    print("Get Market data from API - today's best slot")
    data = client.request()

    best_slot = client.best_slot(3)
    if best_slot is None:
        print("No slot found")
    else:
        print(f"Best slot for 3 hours: {best_slot.start_datetime:%Y-%m-%d %H:%M:%S} - {best_slot.end_datetime:%Y-%m-%d %H:%M:%S} - {(best_slot.marketprice / 1000):.4f} EUR/kWh")


if __name__ == "__main__":
    main(sys.argv[1:])
