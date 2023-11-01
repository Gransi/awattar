
import sys

import datetime
from awattar import AwattarClient

def print_data (data):
    for item in data:
        print(f'{item.start_datetime:%Y-%m-%d %H:%M:%S} - {item.end_datetime:%Y-%m-%d %H:%M:%S} - {(item.marketprice / 1000):.4f} EUR/kWh')

def main(argv):

    print ('Connect to aWATTar')
    client = AwattarClient('AT')

    print ('Get Market data from API')
    data = client.request()
    print_data(data)    

    print ('Get Market data from API for today')
    data = client.today()
    print_data(data)    

    print ('Get Market data from API for tomorrow')
    data = client.tomorrow()
    print_data(data)    

    print ('Get Market data from 2020-05-17')
    data = client.request(datetime.datetime(2020, 5, 17))
    print_data(data)    

    print ('Get Market data between 2020-05-18 and 2020-05-19')
    data = client.request(datetime.datetime(2020, 5, 18), datetime.datetime(2020, 5, 19))
    print_data(data)    

if __name__ == "__main__":
	main(sys.argv[1:])