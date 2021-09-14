import datetime,pytest
from todo_app.data.todo import ToDoCard, ViewModel

@pytest.fixture
def card_list():
    card_list = [
            ToDoCard(1, 'Card Name 1', 'todo', datetime.date.today() + datetime.timedelta(-8), 'Dummy card number 1', datetime.date.today() + datetime.timedelta(-8)),
            ToDoCard(2, 'Card Name 2', 'todo', datetime.date.today() + datetime.timedelta(-7), 'Dummy card number 2', datetime.date.today() + datetime.timedelta(-7)),
            ToDoCard(3, 'Card Name 3', 'doing', datetime.date.today() + datetime.timedelta(-6), 'Dummy card number 3', datetime.date.today() + datetime.timedelta(-2)),
            ToDoCard(4, 'Card Name 4', 'doing', datetime.date.today() + datetime.timedelta(-6), 'Dummy card number 4', datetime.date.today() + datetime.timedelta(-3)),
            ToDoCard(5, 'Card Name 5', 'doing', datetime.date.today() + datetime.timedelta(-5), 'Dummy card number 5', datetime.date.today() + datetime.timedelta(-2)),
            ToDoCard(6, 'Card Name 6', 'done', datetime.date.today() + datetime.timedelta(-4), 'Dummy card number 6', datetime.date.today() + datetime.timedelta(-2)),
            ToDoCard(7, 'Card Name 7', 'done', datetime.date.today() + datetime.timedelta(-3), 'Dummy card number 7', datetime.date.today()),
            ToDoCard(8, 'Card Name 8', 'done', datetime.date.today() + datetime.timedelta(-1), 'Dummy card number 8', datetime.date.today())
        ]
    return card_list


class TestTrello:

    @staticmethod
    def test_get_todo(card_list):        

        todo_list_id = 'todo'
        view_model = ViewModel(card_list)

        todo_items = view_model.todo_items

        for i in todo_items:
            assert todo_list_id == i.idList
        
    @staticmethod
    def test_get_doing(card_list):        

        todo_list_id = 'doing'
        view_model = ViewModel(card_list)

        doing_items = view_model.doing_items

        for i in doing_items:
            assert todo_list_id == i.idList
    
    @staticmethod
    def test_get_done(card_list):        

        todo_list_id = 'done'
        view_model = ViewModel(card_list)

        done_items = view_model.done_items

        for i in done_items:
            assert todo_list_id == i.idList

    @staticmethod
    def test_recent_done_items(card_list):        

        view_model = ViewModel(card_list)

        recent_done_items = view_model.recent_done_items
        
        assert len(recent_done_items) == 2

    @staticmethod
    def test_older_done_items(card_list):        

        view_model = ViewModel(card_list)

        older_done_items = view_model.older_done_items

        assert len(older_done_items) == 1

        

