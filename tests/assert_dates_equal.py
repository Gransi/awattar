import datetime  # noqa: INP001

from tzlocal import get_localzone


class AssertDatesEqual:
    def assert_dates_equal(self, date_from_request: datetime.datetime, destination_year: int, destination_month: int, destination_day: int, destination_hour: int) -> None:
        destination_date = self.convert_to_utc(self.create_local_datetime(destination_year, destination_month, destination_day, destination_hour))

        if type(date_from_request) != type(destination_date):
            raise AssertionError("date_from_request is of type: ", type(date_from_request), " and destination_date is of type: ", type(destination_date))

        request_date = self.convert_to_utc(date_from_request)

        if request_date != destination_date:
            raise AssertionError(f"Dates not equal {request_date} - {destination_date}")

    def convert_to_utc(self, date: datetime.datetime) -> datetime.datetime:
        return date.astimezone(datetime.timezone.utc)

    def create_local_datetime(self, year: int, month: int, day: int, hour: int) -> datetime.datetime:
        return datetime.datetime(year, month, day, hour, 0, 0, tzinfo=get_localzone())
