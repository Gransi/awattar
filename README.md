# awattar



###  Installation

```sh
$ pip install awattar
```

This package is tested with Python 3.8.1 

###  Examples

```python

    print ('Connect to aWATTar')
    client = AwattarClient('AT') # or DE for Germany

    print ('Get marketdata from API')
    data =  client.get_data_24hours()
    
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

###  Usage

#### Initialize Awattar Client

Currently only Austria and Germany are supported

```python
    client = AwattarClient('AT') # or DE for Germany
```

#### Get Market data

Get current Market data
```python
    data = client.get_data()
```

Get Market data from 2020-05-17
```python
    data = client.request(datetime.datetime(2020, 5, 17))
```

Get Market data between 2020-05-18 and 2020-05-19
```python
    data = client.request(datetime.datetime(2020, 5, 18), datetime.datetime(2020, 5, 19))
```

# Source code
The source code is currently available on Github:[https://github.com/Gransi/awattar](https://github.com/Gransi/awattar)
