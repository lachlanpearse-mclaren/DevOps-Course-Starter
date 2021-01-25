import requests

def get_trello_keys():
    with open('./todo_app/data/trello_key.txt','r') as f:
        f.seek(0)
        key_line = f.readline()
        auth_keys = key_line.split(',',1)
        
        return auth_keys

def get_trello_board_id():
    return '600ede7caeb0c67b818ec912'

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

    return response.json()