from datetime import datetime


def get_day_month_year_string(**kwargs):
    timestamp = datetime.timestamp(datetime.now())
    offset = kwargs.get("offset", None)
    self = kwargs.get("self", None)
    if self:
        timestamp = self.year
    if offset:
        timestamp += offset

    date = datetime.fromtimestamp(timestamp / 1000)  # Divide by 1000 to convert from milliseconds to seconds

    print("get_day_month_year_string:", date.strftime("%d-%m-%Y"))
    return date.strftime("%d-%m-%Y")  # Format the date as day-month-year
