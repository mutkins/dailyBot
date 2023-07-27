from datetime import datetime
from dateutil.relativedelta import relativedelta
from calendar import Calendar
import calendar
import logging

# Configure logging
logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


def get_month_days(iterator=0):
    c = Calendar(firstweekday=0)
    date = date_iterator(iterator=iterator)
    return c.itermonthdays3(year=date.year, month=date.month)


def get_month_name(iterator=0):
    date = date_iterator(iterator=iterator)
    return calendar.month_name[date.month]


def get_year(iterator=0):
    date = date_iterator(iterator=iterator)
    return date.year


def date_iterator(iterator=0):
    return datetime.now() + relativedelta(months=iterator)
