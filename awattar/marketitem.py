import datetime
from dateutil import tz

class MarketItem(object):
    def __init__(self,
                 start_datetime : datetime,
                 end_datetime : datetime,
                 marketprice,
                 unit
                 ):
        """Construct a new aWATTarClient item object."""

        self._start_datetime = start_datetime 
        self._end_datetime = end_datetime
        self._marketprice = marketprice
        self._unit = unit

    @classmethod
    def by_timestamp(cls,
                 start_timestamp,
                 end_timestamp,
                 marketprice,
                 unit
                 ):
        """
        Create new instance with timestamp

        Parameters
        ----------
        start_timestamp
            Start timestamp
        end_timestamp
            End timestamp        

        """  

        return cls(
            datetime.datetime.utcfromtimestamp(start_timestamp / 1000).replace(tzinfo=datetime.timezone.utc),
            datetime.datetime.utcfromtimestamp(end_timestamp / 1000).replace(tzinfo=datetime.timezone.utc),
            marketprice,
            unit)

        self._start_datetime = datetime.datetime.utcfromtimestamp(start_timestamp / 1000).replace(tzinfo=datetime.timezone.utc) 
        self._end_datetime = datetime.datetime.utcfromtimestamp(end_timestamp / 1000).replace(tzinfo=datetime.timezone.utc) 
        self._marketprice = marketprice
        self._unit = unit     

    @property
    def start_datetime(self):

        #return in local timezone
        return self._start_datetime.astimezone(tz.tzlocal()) 
    
    @property
    def end_datetime(self):

        #return in local timezone
        return self._end_datetime.astimezone(tz.tzlocal()) 

    @property
    def marketprice(self):
        return self._marketprice

    @property
    def unit(self):
        return self._unit;        