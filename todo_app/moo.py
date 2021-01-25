from data.trello_api import get_trello_list_id

trello_list_ids = {}
trello_list_ids['todo'] = get_trello_list_id('To Do')
trello_list_ids['doing'] = get_trello_list_id('Doing')
trello_list_ids['done'] = get_trello_list_id('Done')

print(trello_list_ids)