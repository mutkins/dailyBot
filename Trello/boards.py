import logging
from Trello.api_client import send_request

# Configure logging
logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


def get_daily_board_id(key, token):
    list_id = search_daily_board(key=key, token=token)
    if not list_id:
        list_id = add_daily_board(key, token).get('id')
    return list_id


def search_daily_board(key, token):
    boards = get_boards(key=key, token=token)
    for board in boards:
        if board.get('name') == 'Daily':
            return board.get('id')


def get_boards(key, token):
    params = {
        "key": key,
        "token": token,
    }
    try:
        return send_request(method='get', params=params, path=f'/members/me/boards').json()
    except Exception as e:
        log.error(e)
        raise e


def add_daily_board(key, token):
    params = {
        "name": 'Daily',
        "key": key,
        "token": token,
    }
    try:
        return send_request(method='post', params=params, path=f'/boards').json()
    except Exception as e:
        log.error(e)
        raise e

