import datetime
from typing import Any, TypeVar

from dateutil import tz

T = TypeVar("T", bound="MarketItem")


class MarketItem:
    _marketprice: float
    _currency: str
    _energy_unit: str
    _price_per_kWh: float

    def __init__(
        self,
        start_datetime: datetime.datetime,
        end_datetime: datetime.datetime,
        marketprice: float,
        unit: str,
    ) -> None:
        """Construct a new aWATTarClient item object."""

        self._start_datetime = start_datetime
        self._end_datetime = end_datetime
        self._marketprice = float(marketprice)
        self._unit = unit

    def to_json_dict(self) -> dict[str, Any]:
        return {"start": self.start_datetime.isoformat(), "end": self.end_datetime.isoformat(), "price": self.marketprice, "unit": self.unit, "currency": self.currency, "energy_unit": self.energy_unit, "price_per_kWh": self.price_per_kWh}

    @classmethod
    def by_timestamp(
        cls: type[T],
        start_timestamp: float,
        end_timestamp: float,
        marketprice: float,
        unit: str,
    ) -> T:
        """
        Create new instance with timestamp

        Parameters
        ----------
        start_timestamp
            Start timestamp
        end_timestamp
            End timestamp

        """
        return cls(datetime.datetime.fromtimestamp(start_timestamp / 1000.0, datetime.timezone.utc), datetime.datetime.fromtimestamp(end_timestamp / 1000.0, datetime.timezone.utc), marketprice, unit)

    @property
    def start_datetime(self) -> datetime.datetime:
        # return in local timezone
        return self._start_datetime.astimezone(tz.tzlocal())

    @property
    def end_datetime(self) -> datetime.datetime:
        # return in local timezone
        return self._end_datetime.astimezone(tz.tzlocal())

    @property
    def marketprice(self) -> float:
        return self._marketprice

    @property
    def unit(self) -> str:
        return self._unit

    @property
    def price_per_kWh(self) -> float:
        try:
            return self._price_per_kWh
        except AttributeError:
            if self.energy_unit.startswith("M"):
                self._price_per_kWh = self.marketprice / 1000
        return self._price_per_kWh

    @property
    def currency(self) -> str:
        try:
            return self._currency
        except AttributeError:
            self._currency = self.unit.split("/")[0]
        return self._currency

    @property
    def energy_unit(self) -> str:
        try:
            return self._energy_unit
        except AttributeError:
            self._energy_unit = self.unit.split("/")[1]
        return self._energy_unit
