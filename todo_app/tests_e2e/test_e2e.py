import os,pytest
from threading import Thread
from todo_app.data.trello_api import create_trello_board,delete_trello_board
from todo_app import app
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from dotenv import find_dotenv,load_dotenv

@pytest.fixture(scope='module')
def app_with_temp_board():
    
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    
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
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome(options=opts) as driver:
        yield driver

def test_task_journey(driver,app_with_temp_board):
    driver.get('http://127.0.0.1:5000')

    assert driver.title == 'To-Do App'
    
    driver.find_element_by_id('new_item_title').send_keys('Test Item Name')
    driver.find_element_by_id('new_item_desc').send_keys('This is a description for the test item to see if it creates ok')
    driver.find_element_by_id('new_item_submit').click()

    assert driver.find_element_by_xpath("//*[starts-with(@id, 'Todo')]")
    
    select = Select(driver.find_element_by_xpath("//*[starts-with(@id, 'new_trello_list_id_')]"))
    select.select_by_index(2)
    driver.find_element_by_xpath("//*[starts-with(@id, 'toggle_item_button')]").click()
    
    assert driver.find_element_by_xpath("//*[starts-with(@id, 'Doing')]")

    select = Select(driver.find_element_by_xpath("//*[starts-with(@id, 'new_trello_list_id_')]"))
    select.select_by_index(3)
    driver.find_element_by_xpath("//*[starts-with(@id, 'toggle_item_button')]").click()
    
    assert driver.find_element_by_xpath("//*[starts-with(@id, 'Done')]")





