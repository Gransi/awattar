import sys

import datetime
from datetime import timedelta
import statistics 
import numpy
sys.path.append("..")
from awattar.client import AwattarClient

def main(argv):

    print ('Connect to aWATTar')
    client = AwattarClient('AT')

    print ('Get Market data from API')
    client.request()
    
    min_item = client.min()
    print(f'Min: {min_item.start_datetime:%Y-%m-%d %H:%M:%S} - {min_item.end_datetime:%Y-%m-%d %H:%M:%S} - {(min_item.marketprice / 1000):.4f} EUR/kWh')

    max_item = client.max()
    print(f'Max: {max_item.start_datetime:%Y-%m-%d %H:%M:%S} - {max_item.end_datetime:%Y-%m-%d %H:%M:%S} - {(max_item.marketprice / 1000):.4f} EUR/kWh')

    mean_item = client.mean()
    print(f'Mean: {mean_item.start_datetime:%Y-%m-%d %H:%M:%S} - {mean_item.end_datetime:%Y-%m-%d %H:%M:%S} - {(mean_item.marketprice / 1000):.4f} EUR/kWh')


    best_slot = client.best_slot(3)
    if best_slot is None:
        print("No slot found")
    else:        
        print(f'Best slot1: {best_slot.start_datetime:%Y-%m-%d %H:%M:%S} - {best_slot.end_datetime:%Y-%m-%d %H:%M:%S} - {(best_slot.marketprice / 1000):.4f} EUR/kWh')

    best_slot = client.best_slot(1,datetime.datetime(2020, 10, 17, 12, 0, 0),datetime.datetime(2020, 10, 17, 18, 0, 0))
    if best_slot is None:
        print("No slot found")
    else:        
        print(f'Best slot2: {best_slot.start_datetime:%Y-%m-%d %H:%M:%S} - {best_slot.end_datetime:%Y-%m-%d %H:%M:%S} - {(best_slot.marketprice / 1000):.4f} EUR/kWh')

    starttime_slot = datetime.datetime.now()
    starttime_slot = starttime_slot.replace(hour=12)	
    endtime_slot = starttime_slot + timedelta(hours=6)

    best_slot = client.best_slot(1,starttime_slot,endtime_slot)
    if best_slot is None:
        print("No slot found")
    else:        
        print(f'Best slot3: {best_slot.start_datetime:%Y-%m-%d %H:%M:%S} - {best_slot.end_datetime:%Y-%m-%d %H:%M:%S} - {(best_slot.marketprice / 1000):.4f} EUR/kWh')

 

    #print ('Get Market data from API')
    #data = client.request()
    
    #maxitem = max(data, key=lambda p: p.marketprice)

    #print(f'Max: {maxitem.start_datetime:%Y-%m-%d %H:%M:%S} - {maxitem.end_datetime:%Y-%m-%d %H:%M:%S} - {(maxitem.marketprice / 1000):.4f} EUR/kWh')

    #minitem = min(data, key=lambda p: p.marketprice)

    #print(f'Min: {minitem.start_datetime:%Y-%m-%d %H:%M:%S} - {minitem.end_datetime:%Y-%m-%d %H:%M:%S} - {(minitem.marketprice / 1000):.4f} EUR/kWh')



    #i_want_object_of_test = [test(test_obj.val.lower()) for test_obj in test_lst]
    #attr=(data, key=lambda p: p.marketprice)
    #print(vars(attr))
    #medianitem = numpy.median(attr)

    #print(f'Median: {medianitem} EUR/kWh')

    #List of data
    #for item in data:
    #    print(f'{item.start_datetime:%Y-%m-%d %H:%M:%S} - {item.end_datetime:%Y-%m-%d %H:%M:%S} - {(item.marketprice / 1000):.4f} EUR/kWh')
         

if __name__ == "__main__":
	main(sys.argv[1:])