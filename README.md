# awattar

##  Installation

```sh
$ pip install awattar
```

This package is tested with Python 3.10 

## Command line

Use the command `awattar --help` and `awattar fetch-prices --help` to get more information.

```shell
$ awattar --help
Usage: awattar [OPTIONS] COMMAND [ARGS]...

  Access aWATTar's energy prices API.

Options:
  --country [DE|AT]  the API's target country (either Germany or Austria),
                     default: AT
  --help             Show this message and exit.

Commands:
  fetch-prices  Fetch hourly energy prices
```

### Command line example

```shell
$  awattar --country AT fetch-prices --day 2023-02-20
[
    {
        "start": "2023-02-20T00:00:00+01:00",
        "end": "2023-02-20T01:00:00+01:00",
        "price": 85.96,
        "unit": "Eur/MWh",
        "currency": "Eur",
        "energy_unit": "MWh",
        "price_per_kWh": 0.08596
    },
    ...
]
```

##  Examples

```python
    from awattar.client import AwattarClient

    print ('Connect to aWATTar')
    client = AwattarClient('AT') # or DE for Germany

    print ('Get marketdata from API')
    data =  client.request()
    
    for item in data:
        print(f'{item.start_datetime:%Y-%m-%d %H:%M:%S} - {item.end_datetime:%Y-%m-%d %H:%M:%S} - {(item.marketprice / 1000):.4f} EUR/kWh')

```

Output
```
Connect to aWATTar
Get marketdata from API
2020-08-11 13:00:00 - 2020-08-11 14:00:00 - 0.0350 EUR/kWh
2020-08-11 14:00:00 - 2020-08-11 15:00:00 - 0.0341 EUR/kWh
2020-08-11 15:00:00 - 2020-08-11 16:00:00 - 0.0340 EUR/kWh
2020-08-11 16:00:00 - 2020-08-11 17:00:00 - 0.0387 EUR/kWh
2020-08-11 17:00:00 - 2020-08-11 18:00:00 - 0.0417 EUR/kWh
2020-08-11 18:00:00 - 2020-08-11 19:00:00 - 0.0430 EUR/kWh
2020-08-11 19:00:00 - 2020-08-11 20:00:00 - 0.0465 EUR/kWh
2020-08-11 20:00:00 - 2020-08-11 21:00:00 - 0.0413 EUR/kWh
2020-08-11 21:00:00 - 2020-08-11 22:00:00 - 0.0400 EUR/kWh
2020-08-11 22:00:00 - 2020-08-11 23:00:00 - 0.0369 EUR/kWh
2020-08-11 23:00:00 - 2020-08-12 00:00:00 - 0.0309 EUR/kWh
```

##  Usage

### Initialize Awattar Client

Currently only Austria and Germany are supported

```python
    client = AwattarClient('AT') # or DE for Germany
```

### Get Market data

Get current Market data
```python
    data = client.request()
```

Get Market data from 2020-05-17
```python
    data = client.request(datetime.datetime(2020, 5, 17))
```

Get Market data between 2020-05-18 and 2020-05-19
```python
    data = client.request(datetime.datetime(2020, 5, 18), datetime.datetime(2020, 5, 19))
```

### Analyse Market data

```python
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
        print(f'Best slot 1: {best_slot.start_datetime:%Y-%m-%d %H:%M:%S} - {best_slot.end_datetime:%Y-%m-%d %H:%M:%S} - {(best_slot.marketprice / 1000):.4f} EUR/kWh')

    best_slot = client.best_slot(1,datetime.datetime(2020, 10, 5, 0, 0, 0),datetime.datetime(2020, 10, 6, 3, 0, 0))
    if best_slot is None:
        print("No slot found")
    else:        
        print(f'Best slot 2: {best_slot.start_datetime:%Y-%m-%d %H:%M:%S} - {best_slot.end_datetime:%Y-%m-%d %H:%M:%S} - {(best_slot.marketprice / 1000):.4f} EUR/kWh')
```

Output
```
Connect to aWATTar
Get Market data from API
Min: 2020-10-06 03:00:00 - 2020-10-06 04:00:00 - 0.0107 EUR/kWh
Max: 2020-10-05 19:00:00 - 2020-10-05 20:00:00 - 0.0544 EUR/kWh
Mean: 2020-10-05 17:00:00 - 2020-10-06 17:00:00 - 0.0349 EUR/kWh
Best slot 1: 2020-10-06 02:00:00 - 2020-10-06 05:00:00 - 0.0149 EUR/kWh
Best slot 2: 2020-10-06 02:00:00 - 2020-10-06 03:00:00 - 0.0190 EUR/kWh
```

# Source code
The source code is currently available on Github: [https://github.com/Gransi/awattar](https://github.com/Gransi/awattar)
