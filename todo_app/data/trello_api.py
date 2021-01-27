import requests
import os

class TrelloCard:
    def __init__(self, id, name, idList):
        self.id = id
        self.name = name
        self.idList = idList


def get_trello_keys():
    
    auth_keys = []
    auth_keys.append(os.getenv('TRELLO_AUTH'))
    auth_keys.append(os.getenv('TRELLO_TOKEN'))
        
    return auth_keys

def get_trello_board_id():
    board_id = os.getenv('TRELLO_BOARD_ID')
    return board_id

def get_trello_list_id(list_name):
    trello_auth_key = get_trello_keys()
    trello_board_id = get_trello_board_id()
    response = requests.get(f'https://api.trello.com/1/boards/{trello_board_id}/lists?key={trello_auth_key[0]}&token={trello_auth_key[1]}')
    
    all_lists = response.json()

    for i in all_lists:
        if i['name'] == list_name:
            list_id = i['id']
    
    return list_id

def get_trello_cards():
    trello_auth_key = get_trello_keys()
    trello_board_id = get_trello_board_id()
    response = requests.get(f'https://api.trello.com/1/boards/{trello_board_id}/cards?key={trello_auth_key[0]}&token={trello_auth_key[1]}')

    card_list = []
    for card in response.json():
        existing_card = TrelloCard(card['id'], card['name'], card['idList'])

        card_list.append(existing_card)

    return card_list

def move_trello_card(card_id, new_list_id):
    trello_auth_key = get_trello_keys()
    requests.put(f'https://api.trello.com/1/cards/{card_id}?key={trello_auth_key[0]}&token={trello_auth_key[1]}&idList={new_list_id}')

def create_trello_card(card_name):
    trello_auth_key = get_trello_keys()
    trello_list_id = get_trello_list_id("To Do")
    requests.post(f'https://api.trello.com/1/cards/?key={trello_auth_key[0]}&token={trello_auth_key[1]}&idList={trello_list_id}&name={card_name}')

def archive_trello_card(card_id):
    trello_auth_key = get_trello_keys()
    requests.put(f'https://api.trello.com/1/cards/{card_id}?key={trello_auth_key[0]}&token={trello_auth_key[1]}&closed=true')
