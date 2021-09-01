import pytest,os
import todo_app.app
import mongomock
import pymongo
from dotenv import find_dotenv, load_dotenv
from unittest.mock import patch,Mock



@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    with mongomock.patch(servers=(('fakemongo.com', 27017),)):
        test_app = todo_app.app.create_app()
        with test_app.test_client() as client:
            yield client


def test_index_page(client):

    response = client.get('/')

    assert b'To Do List' in response.data
    assert b'Items in Progress' in response.data
    assert b'Completed Items' in response.data

@mongomock.patch(servers=(('fakemongo.com', 27017),))
def test_add_item():
    db_connection = os.getenv('MONGO_DB_CONNECTION')
    db_name = os.getenv('MONGO_DB_NAME')
    connection = pymongo.MongoClient(db_connection)
    db = connection[db_name]
    item = {"moo" : "baa"}
    collection = db['test_coll']
    collection.insert_one(item)
    