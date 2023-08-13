from datetime import datetime
from dateutil.relativedelta import relativedelta
from calendar import Calendar
import calendar
import logging
import re

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
    return get_count_days_name(diff)


def get_days_diff(date1, date2=datetime.now()):
    date2=datetime.now()
    print(f'Calculating date dif... datenow={date2}, date2={date1}')
    log.debug(f'Calculating date dif... datenow={date2}, date2={date1}')
    return (date1.date() - date2.date()).days


def get_count_days_name(count):
    match count:
        case -1:
            name = 'Вчера'
        case -2:
            name = 'Позавчера'
        case 0:
            name = 'Сегодня'
        case 1:
            name = 'Завтра'
        case 2:
            name = 'Послезавтра'
        case _ if count < 0:
            name = f'{count*-1}д. назад'
        case _:
            name = f'{count}д.'
    print(f'count days name = {name}')
    log.debug(f'count days name = {name}')
    return name


def extract_card_id(message_text):
    r = re.search('id:\S*', message_text).group(0)
    return r[3:]
