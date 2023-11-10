import datetime
import sys

from tzlocal import get_localzone

from awattar import AwattarClient


def main(argv: str) -> None:
    print("Connect to aWATTar")
    client = AwattarClient("AT")

    print("Get Market data from API")
    data = client.request()

    for item in data:
        print(f"{item.start_datetime:%Y-%m-%d %H:%M:%S} - {item.end_datetime:%Y-%m-%d %H:%M:%S} - {(item.marketprice / 1000):.4f} EUR/kWh")

    print("Get Market data from 2020-05-17")
    data = client.request(datetime.datetime(2020, 5, 17, tzinfo=get_localzone()))
    for item in data:
        print(f"{item.start_datetime:%Y-%m-%d %H:%M:%S} - {item.end_datetime:%Y-%m-%d %H:%M:%S} - {(item.marketprice / 1000):.4f} EUR/kWh")

    print("Get Market data between 2020-05-18 and 2020-05-19")
    data = client.request(datetime.datetime(2020, 5, 18, tzinfo=get_localzone()), datetime.datetime(2020, 5, 19, tzinfo=get_localzone()))
    for item in data:
        print(f"{item.start_datetime:%Y-%m-%d %H:%M:%S} - {item.end_datetime:%Y-%m-%d %H:%M:%S} - {(item.marketprice / 1000):.4f} EUR/kWh")


if __name__ == "__main__":
    main(sys.argv[1:])
