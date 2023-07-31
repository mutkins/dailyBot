import logging
from Trello.api_client import send_request

# Configure logging
logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


def add_card(idList, key, token, name, card_id=None, is_done=False, **kwargs):
    r"""Adds a new trello card on the list or update existing.
        :param idList: card's list
        :param key: trello key
        :param token: trello token
        :param name: card's name
        :param card_id: card's id (if card already exists)
        :param kwargs: desc, pos, due, start, dueComplete, idMembers, idLabels, urlSource, fileSource, mimeType,
         idCardSource, keepFromSource, address, locationName, coordinates
        :return: None
        """
    try:
        if card_id:
            update_card(id=card_id, idList=idList, key=key, token=token, name=name, **kwargs)
        else:
            create_card(idList=idList, key=key, token=token, name=name, **kwargs)
    except Exception as e:
        log.error(e)
        raise e


def create_card(idList, key, token, name, **kwargs):
    r"""Creates trello card.
    :param idList: card's list
    :param key: trello key
    :param token: trello token
    :param name: card's name
    :param kwargs: desc, pos, due, start, dueComplete, idMembers, idLabels, urlSource, fileSource, mimeType,
     idCardSource, keepFromSource, address, locationName, coordinates
    :return: None
    """
    params = {
        "idList": idList,
        "key": key,
        "token": token,
        "name": name
    }
    params.update(kwargs)
    try:
        send_request(method='post', params=params, path='/cards/')
    except Exception as e:
        log.error(e)
        raise e


def update_card(id, idList, key, token, name, **kwargs):
    r"""Updates trello card.
    :param id: card's id
    :param idList: card's list
    :param key: trello key
    :param token: trello token
    :param name: card's name
    :param kwargs: desc, pos, due, start, dueComplete, idMembers, idLabels, urlSource, fileSource, mimeType,
     idCardSource, keepFromSource, address, locationName, coordinates
    :return: None
    """
    params = {
        "idList": idList,
        "key": key,
        "token": token,
        "name": name
    }
    params.update(kwargs)
    try:
        send_request(method='put', params=params, path=f'/cards/{id}')
    except Exception as e:
        log.error(e)
        raise e


def is_card_name_exist_in_list(idList, name, key, token):
    cards = get_cards_in_list(idList=idList, key=key, token=token)
    for card in cards:
        if card.get('name') == name:
            return card.get('id')
    return False


def get_card_by_name(idList, name, key, token):
    cards = get_cards_in_list(idList=idList, key=key, token=token)
    for card in cards:
        if card.get('name') == name:
            return card
    return False


def get_cards_in_list(idList, key, token):
    params = {
        "key": key,
        "token": token,
    }
    try:
        return send_request(method='get', params=params, path=f'/lists/{idList}/cards').json()
    except Exception as e:
        log.error(e)
        raise e


def get_cards_on_board(board_id, key, token):
    params = {
        "key": key,
        "token": token,
    }
    try:
        return send_request(method='get', params=params, path=f'/boards/{board_id}/cards').json()
    except Exception as e:
        log.error(e)
        raise e


def get_card_by_id(id, key, token):
    params = {
        "key": key,
        "token": token,
    }
    try:
        return send_request(method='get', params=params, path=f'/cards/{id}').json()
    except Exception as e:
        log.error(e)
        raise e



