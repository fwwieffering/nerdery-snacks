from dateutil.relativedelta import relativedelta
import datetime


def get_next_month() -> datetime.datetime:
    """
    Returns a datetime object of the first day of the next month
    """
    today: datetime.date = datetime.date.today()
    minus_days: int = today.day - 1
    next_month: datetime.datetime = datetime.datetime.combine(
        today + relativedelta(months=+1, days=-minus_days),
        datetime.datetime.min.time()
    )
    return next_month
