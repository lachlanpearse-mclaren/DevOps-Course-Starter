import os,pytest
from threading import Thread
from todo_app.data.todo import create_test_db,delete_test_db
from todo_app import app
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from dotenv import find_dotenv,load_dotenv

@pytest.fixture(scope='module')
def app_with_temp_board():
    
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    
    db_name = create_test_db('test_todo_app')
    os.environ['MONGO_DB_NAME'] = db_name

    application = app.create_app()
    application.config['LOGIN_DISABLED'] = True

    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application

    thread.join(1)
    delete_test_db(db_name)

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
    
    select = Select(driver.find_element_by_xpath("//*[starts-with(@id, 'new_list_id_')]"))
    select.select_by_index(2)
    driver.find_element_by_xpath("//*[starts-with(@id, 'toggle_item_button')]").click()
    
    assert driver.find_element_by_xpath("//*[starts-with(@id, 'Doing')]")

    select = Select(driver.find_element_by_xpath("//*[starts-with(@id, 'new_list_id_')]"))
    select.select_by_index(3)
    driver.find_element_by_xpath("//*[starts-with(@id, 'toggle_item_button')]").click()
    
    assert driver.find_element_by_xpath("//*[starts-with(@id, 'Done')]")





