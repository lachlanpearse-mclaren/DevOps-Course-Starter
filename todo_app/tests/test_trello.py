import datetime
from todo_app.data.trello_api import TrelloCard, ViewModel

class TestTrello:

    @staticmethod
    def test_get_todo():        

        card_list = [
            TrelloCard(1, 'Card Name 1', 123, datetime.datetime.today(), 'Dummy card number 1'),
            TrelloCard(2, 'Card Name 1', 133, datetime.datetime.today(), 'Dummy card number 2'),
            TrelloCard(3, 'Card Name 1', 133, datetime.datetime.today(), 'Dummy card number 3'),
            TrelloCard(4, 'Card Name 1', 123, datetime.datetime.today(), 'Dummy card number 4'),
            TrelloCard(5, 'Card Name 1', 123, datetime.datetime.today(), 'Dummy card number 5')
        ]
        trello_list_ids = {'todo':123,'doing':133,'done':143}

        todo_list_id = trello_list_ids['todo']
        view_model = ViewModel(card_list, trello_list_ids)

        todo_items = view_model.todo_items

        for i in todo_items:
            assert todo_list_id == i.idList
        
