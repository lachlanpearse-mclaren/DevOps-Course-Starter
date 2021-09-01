import datetime,pytest
from todo_app.data.todo import ToDoCard, ViewModel

@pytest.fixture
def card_list():
    card_list = [
            ToDoCard(1, 'Card Name 1', 123, datetime.date.today() + datetime.timedelta(-8), 'Dummy card number 1', datetime.date.today() + datetime.timedelta(-8)),
            ToDoCard(2, 'Card Name 2', 133, datetime.date.today() + datetime.timedelta(-7), 'Dummy card number 2', datetime.date.today() + datetime.timedelta(-7)),
            ToDoCard(3, 'Card Name 3', 143, datetime.date.today() + datetime.timedelta(-6), 'Dummy card number 3', datetime.date.today() + datetime.timedelta(-2)),
            ToDoCard(4, 'Card Name 4', 143, datetime.date.today() + datetime.timedelta(-6), 'Dummy card number 4', datetime.date.today() + datetime.timedelta(-3)),
            ToDoCard(5, 'Card Name 5', 143, datetime.date.today() + datetime.timedelta(-5), 'Dummy card number 5', datetime.date.today() + datetime.timedelta(-2)),
            ToDoCard(6, 'Card Name 6', 123, datetime.date.today() + datetime.timedelta(-4), 'Dummy card number 6', datetime.date.today() + datetime.timedelta(-2)),
            ToDoCard(7, 'Card Name 7', 143, datetime.date.today() + datetime.timedelta(-3), 'Dummy card number 7', datetime.date.today()),
            ToDoCard(8, 'Card Name 8', 143, datetime.date.today() + datetime.timedelta(-1), 'Dummy card number 8', datetime.date.today())
        ]
    return card_list

@pytest.fixture
def list_ids():
    list_ids = {'todo':123,'doing':133,'done':143}
    return list_ids

class TestTrello:

    @staticmethod
    def test_get_todo(card_list,list_ids):        

        todo_list_id = list_ids['todo']
        view_model = ViewModel(card_list, list_ids)

        todo_items = view_model.todo_items

        for i in todo_items:
            assert todo_list_id == i.idList
        
    @staticmethod
    def test_get_doing(card_list,list_ids):        

        todo_list_id = list_ids['doing']
        view_model = ViewModel(card_list, list_ids)

        doing_items = view_model.doing_items

        for i in doing_items:
            assert todo_list_id == i.idList
    
    @staticmethod
    def test_get_done(card_list,list_ids):        

        todo_list_id = list_ids['done']
        view_model = ViewModel(card_list, list_ids)

        done_items = view_model.done_items

        for i in done_items:
            assert todo_list_id == i.idList

    @staticmethod
    def test_recent_done_items(card_list,list_ids):        

        view_model = ViewModel(card_list, list_ids)

        recent_done_items = view_model.recent_done_items
        
        assert len(recent_done_items) == 2

    @staticmethod
    def test_older_done_items(card_list,list_ids):        

        view_model = ViewModel(card_list, list_ids)

        older_done_items = view_model.older_done_items

        assert len(older_done_items) == 3

        

