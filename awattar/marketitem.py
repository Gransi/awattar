import datetime
from dateutil import tz

class MarketItem(object):

    marketprice : float

    def __init__(self,
                 start_datetime : datetime,
                 end_datetime : datetime,
                 marketprice : float,
                 unit : str
                 ):
        """Construct a new aWATTarClient item object."""

        self._start_datetime = start_datetime 
        self._end_datetime = end_datetime
        self._marketprice = float(marketprice)
        self._unit = unit

    def to_json_dict(self):
        return {
                "start": self.start_datetime.isoformat(),
                "end": self.end_datetime.isoformat(),
                "price": self.marketprice,
                "unit": self.unit,
                "currency": self.currency,
                "energy_unit": self.energy_unit,
                "price_per_kWh": self.price_per_kWh
            }

    @classmethod
    def by_timestamp(cls,
                 start_timestamp : datetime,
                 end_timestamp : datetime,
                 marketprice : float,
                 unit : str
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

    @property
    def price_per_kWh(self):
        try:
            return self._price_per_kWh
        except AttributeError:
            assert self.energy_unit.startswith("M")
            self._price_per_kWh = self.marketprice / 1000
        return self._price_per_kWh

    @property
    def currency(self):
        try:
            return self._currency
        except AttributeError:
            self._currency = self.unit.split("/")[0]
        return self._currency

    @property
    def energy_unit(self):
        try:
            return self._energy_unit
        except AttributeError:
            self._energy_unit = self.unit.split("/")[1]
        return self._energy_unit
