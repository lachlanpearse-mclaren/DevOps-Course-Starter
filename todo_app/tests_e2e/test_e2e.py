import os,pytest
from threading import Thread
from todo_app.data.trello_api import create_trello_board,delete_trello_board
from todo_app import app
from selenium import webdriver
from dotenv import find_dotenv,load_dotenv

@pytest.fixture(scope='module')
def app_with_temp_board():
    board_id = create_trello_board('TestBoard')
    file_path = find_dotenv('.env')
    load_dotenv(file_path)
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

    driver.find_element_by_id('new_item_title').send_keys('Test Item Name')
    driver.find_element_by_id('new_item_desc').send_keys('This is a description for the test item to see if it creates ok')
    driver.find_element_by_id('new_item_submit').click()

    

    assert 'Test Item Name' in driver.page_source



