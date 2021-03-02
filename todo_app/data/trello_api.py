import requests, os, datetime, json

class TrelloCard:

    def __init__(self, id, name, idList, due_date, description, modified):
        self.id = id
        self.name = name
        self.idList = idList
        self.due_date = due_date
        self.description = description
        self.modified = modified
    
    def get_date_string(self):
        return datetime.datetime.strftime(self.due_date, '%Y-%m-%d')
    
    def get_user_facing_date(self):
        return datetime.datetime.strftime(self.due_date, '%d/%m/%Y')

    def get_modified_date_string(self):
        return datetime.datetime.strftime(self.modified, '%Y-%m-%d')
    
    def get_modified_user_facing_date(self):
        return datetime.datetime.strftime(self.modified, '%d/%m/%Y')

class ViewModel:
    def __init__(self, items, trello_list_ids):
        self._items = items
        self._trello_list_ids = trello_list_ids

    @property
    def items(self):
        return self._items

    @property
    def trello_list_ids(self):
        return self._trello_list_ids

    @property
    def todo_items(self):
        items = []
        for item in self._items:
            if item.idList == self.trello_list_ids['todo']:
                items.append(item)
        return items
    
    @property
    def doing_items(self):
        items = []
        for item in self._items:
            if item.idList == self.trello_list_ids['doing']:
                items.append(item)
        return items
    
    @property
    def done_items(self):
        items = []
        for item in self._items:
            if item.idList == self.trello_list_ids['done']:
                items.append(item)
        return items

    @property
    def recent_done_items(self):
        items = []
        for item in self._items:
            if item.idList == self.trello_list_ids['done'] and item.modified == datetime.date.today():
                items.append(item)
        return items

    @property
    def older_done_items(self):
        items = []
        for item in self._items:
            if item.idList == self.trello_list_ids['done'] and item.modified != datetime.date.today():
                items.append(item)
        return items

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

    #card_list = [TrelloCard(card['id'], card['name'], card['idList'], datetime.datetime.strptime(card['due'], '%Y-%m-%dT%H:%M:%S.%fZ'), card['desc']) for card in response.json()]
    card_list = []
    for card in response.json():
        if card['due'] == None:
            due_date = datetime.datetime.strftime(datetime.datetime.today() + datetime.timedelta(365), '%Y-%m-%dT%H:%M:%S.%fZ')

        else:
            due_date = card['due']

        card_list.append(TrelloCard(card['id'], card['name'], card['idList'], datetime.datetime.strptime(due_date, '%Y-%m-%dT%H:%M:%S.%fZ'), card['desc'], datetime.datetime.strptime(card['dateLastActivity'], '%Y-%m-%dT%H:%M:%S.%fZ').date()))
        
    return card_list

def move_trello_card(card_id, new_list_id):
    trello_auth_key = get_trello_keys()
    requests.put(f'https://api.trello.com/1/cards/{card_id}?key={trello_auth_key[0]}&token={trello_auth_key[1]}&idList={new_list_id}')

def create_trello_card(new_card):
    trello_auth_key = get_trello_keys()
    requests.post(f'https://api.trello.com/1/cards/?key={trello_auth_key[0]}&token={trello_auth_key[1]}&idList={new_card.idList}&name={new_card.name}&desc={new_card.description}&due={new_card.get_date_string()}')

def archive_trello_card(card_id):
    trello_auth_key = get_trello_keys()
    requests.put(f'https://api.trello.com/1/cards/{card_id}?key={trello_auth_key[0]}&token={trello_auth_key[1]}&closed=true')
