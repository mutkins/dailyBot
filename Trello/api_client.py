from requests import Request
from requests import Session
from requests import exceptions
import configparser
import logging

# Configure logging
logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")

config = configparser.ConfigParser()
config.read('settings.ini')

base_url = config['TRELLO']['base_url']
header = {"Content-Type": "application/json"}


def send_request(method='get', params=None, path='/me/boards'):
    url = base_url + path
    request = Request(method=method, url=url, headers=header, params=params)
    with Session() as session:
        prepared_request = session.prepare_request(request)
        try:
            r = session.send(request=prepared_request)
            r.raise_for_status()
            return r
        except exceptions.RequestException as e:
            log.error(e)
            raise e
