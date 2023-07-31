import logging
from Trello.api_client import send_request

# Configure logging
logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


def get_list_id_by_name(board_id, key, token, name):
    list_id = search_list(board_id=board_id, key=key, token=token, name=name)
    if not list_id:
        list_id = add_todo_list(board_id, key, token).get('id')
    return list_id


def search_list(board_id, key, token, name):
    lists = get_lists_on_board(board_id, key, token)
    for list in lists:
        if list.get('name') == name:
            return list.get('id')


def get_lists_on_board(board_id, key, token):
    params = {
        "key": key,
        "token": token,
        "board_id": board_id
    }
    try:
        return send_request(method='get', params=params, path=f'/boards/{board_id}/lists').json()
    except Exception as e:
        log.error(e)
        raise e


def add_todo_list(board_id, key, token):
    params = {
        "name": 'To Do',
        "key": key,
        "token": token,
        "idBoard": board_id
    }
    try:
        return send_request(method='post', params=params, path=f'/lists').json()
    except Exception as e:
        log.error(e)
        raise e

