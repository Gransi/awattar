import datetime
from dateutil import tz

class MarketItem(object):
    def __init__(self,
                 start_timestamp,
                 end_timestamp,
                 marketprice,
                 unit
                 ):
        """Construct a new aWATTarClient item object."""

        self._start_timestamp = start_timestamp
        self._end_timestamp = end_timestamp
        self._marketprice = marketprice
        self._unit = unit

    @property
    def start_datetime(self):

        #get datetime in utc
        value = datetime.datetime.utcfromtimestamp(self._start_timestamp / 1000).replace(tzinfo=datetime.timezone.utc) 

        #return in local timezone
        return value.astimezone(tz.tzlocal()) 
    
    @property
    def end_datetime(self):
        #get datetime in utc
        value = datetime.datetime.utcfromtimestamp(self._end_timestamp / 1000).replace(tzinfo=datetime.timezone.utc) 

        #return in local timezone
        return value.astimezone(tz.tzlocal()) 

    @property
    def marketprice(self):
        return self._marketprice

    @property
    def unit(self):
        return self._unit;        