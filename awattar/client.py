import asyncio
import datetime
import math
import socket
from typing import TYPE_CHECKING, Any, Optional, cast

import aiohttp
import async_timeout
import requests
from aiohttp.client import ClientError, ClientSession
from typing_extensions import Self

from awattar.marketitem import MarketItem


class AwattarError(Exception):
    """Generic aWATTar exception."""


class AwattarConnectionError(AwattarError):
    """aWATTar - connection exception."""


class AwattarNoDataError(AwattarError):
    """aWATTar - no data exception."""


class AwattarClient:
    def __init__(self, country: str = "AT") -> None:
        """Construct a new AwattarClient object."""

        self._country = country

    def _make_url(self, start_time: Optional[datetime.datetime] = None, end_time: Optional[datetime.datetime] = None) -> str:
        # set params
        params = ""
        if start_time is not None:
            # remove microseconds
            start_time = start_time.replace(microsecond=0)

            params = "?start=" + str(int(start_time.timestamp())) + "000"

            if end_time is not None:
                # remove microseconds
                end_time = end_time.replace(microsecond=0)

                # set end timestamp
                params = params + "&end=" + str(int(end_time.timestamp())) + "000"

        # build url
        if self._country == "AT":
            url = "https://api.awattar.com/v1/marketdata" + params
        elif self._country == "DE":
            url = "https://api.awattar.de/v1/marketdata" + params

        return url

    def _set_data(self, jsondata):
        self._data = [MarketItem.by_timestamp(**k) for k in jsondata["data"]]

    def request(
        self,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None,
    ) -> list[MarketItem]:
        """
        Get Market data between start time and end time

        Parameters
        ----------
        start_time : datetime
            Start time
        end_time : datetime
            End time

        Returns
        -------
        MarketItem:
            Returns list of MarketItem

        """

        # send request
        req = requests.get(self._make_url(start_time, end_time), timeout=20)

        if req.status_code != requests.codes.ok:
            raise Exception(f"no data received, status code {req.status_code}")

        jsondata = req.json()
        self._set_data(jsondata)

        return self._data

    def min(self) -> MarketItem:
        """
        Get Market item with lowest price from last request

        Returns
        -------
        MarketItem:
            Returns MarketItem with lowest price

        """

        min_item = self._data[0]

        for item in self._data:
            if item.marketprice < min_item.marketprice:
                min_item = item

        return min_item

    def max(self) -> MarketItem:
        """
        Get Market item with highest price from last request

        Returns
        -------
        MarketItem:
            Returns MarketItem with highest price

        """
        if not hasattr(self, "_data"):
            self.request()

        max_item = self._data[0]

        for item in self._data:
            if item.marketprice > max_item.marketprice:
                max_item = item

        return max_item

    def mean(self) -> MarketItem:
        """
        Get mean price of market of the last request

        Returns
        -------
        MarketItem:    Returns mean price of market

        """

        mean_value = float((sum(a.marketprice for a in self._data)) / len(self._data))

        return MarketItem(self._data[0].start_datetime, self._data[len(self._data) - 1].end_datetime, mean_value, self._data[0].unit)

    def for_timestamp(self, timestamp: datetime.datetime) -> MarketItem | None:
        """Get MarketItem for given timestamp.

        Parameters
        ----------
        timestamp : datetime
            Timestamp must be between start_datetime and end_datetime of MarketItem

        Returns
        -------
        MarketItem: The MarketItem for the given timestamp or None if not found
        """

        for item in self._data:
            if item.start_datetime <= timestamp < item.end_datetime:
                return item

        return None

    def best_slot(self, duration: int, start_datetime: Optional[datetime.datetime] = None, end_datetime: Optional[datetime.datetime] = None) -> MarketItem | None:
        """
        Get the best slot.

        Parameters
        ----------
        duration : int
            Duration of usage[hour]
        start_datetime : datetime
            Start time
        end_datetime : datetime
            End time

        Returns
        -------
        int
            Returns the best starting point

        """
        durationround = math.ceil(duration)
        best_slot = None

        # clean up start_datetime
        if start_datetime is not None:
            start_datetime = start_datetime.replace(minute=0, second=0)

        # clean up end_datetime
        if end_datetime is not None:
            end_datetime = end_datetime.replace(minute=0, second=0)

        datalenght = len(self._data) - (durationround - 1)

        for i in range(datalenght):
            item = self._data[i]

            if start_datetime is None or item.start_datetime >= start_datetime:

                # get end
                if i < datalenght - 1 and end_datetime is not None and self._data[i + durationround- 1].end_datetime > end_datetime:
                    break

                sum_slot = 0.0
                for x in range(durationround):
                    sum_slot += self._data[i + x].marketprice

                mean_slot_price = sum_slot / durationround

                if best_slot is None or best_slot.marketprice > (mean_slot_price):
                    best_slot = MarketItem(item.start_datetime, item.start_datetime + datetime.timedelta(hours=durationround), mean_slot_price, item.unit)

        return best_slot

    def today(self) -> list[MarketItem]:
        """
        Get Market data for today

        Returns
        -------
        MarketItem:
            Returns list of MarketItem

        """

        starttime = datetime.datetime.now(tz=datetime.timezone.utc)
        starttime = starttime.replace(hour=0, minute=0, second=0)
        endtime = starttime.replace(hour=23, minute=0, second=0)

        return self.request(starttime, endtime)

    def tomorrow(self) -> list[MarketItem]:
        """
        Get Market data for tomorrow

        Returns
        -------
        MarketItem:
            Returns list of MarketItem

        """

        starttime = datetime.datetime.now(tz=datetime.timezone.utc)
        starttime = starttime.replace(hour=23, minute=00, second=00)
        endtime = starttime.replace(hour=23, minute=0, second=0) + datetime.timedelta(days=1)

        return self.request(starttime, endtime)


class AsyncAwattarClient(AwattarClient):
    def __init__(self, country: str = "AT", session=None):
        """Construct a new AsyncAwattarClient object."""
        super().__init__(country=country)
        if session:
            self.session = session
            self._close_session = False
        else:
            self.session = ClientSession()
            self._close_session = True

        self.request_timeout = 10

    async def request(self, start_time=None, end_time=None):
        """
        Get Market data between start time and end time async

        Parameters
        ----------
        start_time : datetime
            Start time
        end_time : datetime
            End time

        Returns
        -------
        MarketItem:
            Returns list of MarketItem

        """

        try:
            async with async_timeout.timeout(self.request_timeout):
                response = await self.session.get(self._make_url(start_time, end_time))
                response.raise_for_status()
        except asyncio.TimeoutError as exception:
            msg = "Timeout occurred while connecting to the API."
            raise AwattarConnectionError(
                msg,
            ) from exception
        except (ClientError, socket.gaierror) as exception:
            msg = "Error occurred while communicating with the API."
            raise AwattarConnectionError(
                msg,
            ) from exception

        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            text = await response.text()
            msg = "Unexpected content type response from the easyEnergy API"
            raise AwattarError(
                msg,
                {"Content-Type": content_type, "response": text},
            )

        self._set_data(cast(dict[str, Any], await response.json()))
        return self._data

    async def today(self):
        """
        Get Market data for today

        Returns
        -------
        MarketItem:
            Returns list of MarketItem

        """

        starttime = datetime.datetime.now(tz=datetime.timezone.utc)
        starttime = starttime.replace(hour=0, minute=0, second=0)
        endtime = starttime.replace(hour=23, minute=0, second=0)

        return await self.request(starttime, endtime)

    async def tomorrow(self):
        """
        Get Market data for tomorrow

        Returns
        -------
        MarketItem:
            Returns list of MarketItem

        """

        starttime = datetime.datetime.now(tz=datetime.timezone.utc)
        starttime = starttime.replace(hour=23, minute=00, second=00)
        endtime = starttime.replace(hour=23, minute=0, second=0) + datetime.timedelta(days=1)

        return await self.request(starttime, endtime)

    async def close(self) -> None:
        """Close open client session."""
        if self.session and self._close_session:
            await self.session.close()

    async def __aenter__(self) -> Self:
        """Async enter.

        Returns
        -------
            The EasyEnergy object.
        """
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        """Async exit.

        Args:
        ----
            _exc_info: Exec type.
        """
        await self.close()
