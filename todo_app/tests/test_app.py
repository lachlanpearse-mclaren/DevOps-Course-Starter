import pytest,os,json
import todo_app.app
from dotenv import find_dotenv, load_dotenv
from unittest.mock import patch,Mock

trello_board_id = os.getenv('TRELLO_BOARD_ID')

@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    test_app = todo_app.app.create_app()

    with test_app.test_client() as client:
        yield client

@patch('requests.get')
def test_index_page(mock_get_requests, client):

    mock_get_requests.side_effect = mock_get_lists(f'https://api.trello.com/1/boards/{trello_board_id}/lists', None)
    response = client.get('/')

def mock_get_lists(url, params):
    if url == f'https://api.trello.com/1/boards/{trello_board_id}/lists':
        response = Mock()

        json_return = [
            {
                "id": "600ede7caeb0c67b818ec913",
                "name": "To Do",
                "closed": False,
                "pos": 16384,
                "softLimit": None,
                "idBoard": trello_board_id,
                "subscribed": False
            },
            {
                "id": "600ede7caeb0c67b818ec914",
                "name": "Doing",
                "closed": False,
                "pos": 32768,
                "softLimit": None,
                "idBoard": trello_board_id,
                "subscribed": False
            },
            {
                "id": "600ede7caeb0c67b818ec915",
                "name": "Done",
                "closed": False,
                "pos": 49152,
                "softLimit": None,
                "idBoard": trello_board_id,
                "subscribed": False
            }
        ]
        response.json.return_value = json.dumps(json_return)
        return response
    return None