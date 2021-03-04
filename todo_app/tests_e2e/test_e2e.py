import os,pytest
from threading import Thread
from todo_app.data.trello_api import create_trello_board,delete_trello_board
from todo_app import app
from selenium import webdriver

@pytest.fixture(scope='module')
def app_with_temp_board():
    board_id = create_trello_board('TestBoard')
    os.environ['TRELLO_BOARD_ID'] = board_id

    application = app.create_app()

    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application

    thread.join(1)
    delete_trello_board(board_id)


@pytest.fixture(scope="module")
def driver():
    with webdriver.Firefox() as driver:
        yield driver

def test_task_journey(driver,app_with_temp_board):
    driver.get('http://127.0.0.1:5000')

    assert driver.title == 'To-Do App'