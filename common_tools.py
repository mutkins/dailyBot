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


def get_hf_date_diff(date):
    date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%fZ')
    diff = get_days_diff(date1=date)
    hf_date = get_count_days_name(diff)
    return hf_date


def get_days_diff(date1, date2=datetime.now()):
    return (date1 - date2).days


def get_count_days_name(count):
    match count:
        case 0:
            name = 'Сегодня'
        case 1:
            name = 'Завтра'
        case 2:
            name = 'Послезавтра'
        case _:
            name = f'{count}д.'
    return name
