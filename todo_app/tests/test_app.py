import pytest,os,json
import todo_app.app
from dotenv import find_dotenv, load_dotenv
from unittest.mock import patch,Mock



@pytest.fixture
def client():
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)

    test_app = todo_app.app.create_app()

    with test_app.test_client() as client:
        yield client

trello_board_id = os.getenv('TRELLO_BOARD_ID')

@patch('requests.get')
def test_index_page(mock_get_requests, client):

    mock_get_requests.side_effect = mock_trello_request
    response = client.get('/')

    assert b'Coffee' in response.data
    assert b'Cake time' in response.data
    assert b'moo' in response.data

def mock_trello_request(url):
    trello_board_id = os.getenv('TRELLO_BOARD_ID')
    if url.startswith(f'https://api.trello.com/1/boards/{trello_board_id}/lists'):
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
        response.json.return_value = json_return
        return response
    elif url.startswith(f'https://api.trello.com/1/boards/{trello_board_id}/cards'):
        response = Mock()

        json_return = [
            {
                "id": "601bdd078a423353b3ade947",
                "checkItemStates": None,
                "closed": False,
                "dateLastActivity": "2021-02-11T17:06:06.953Z",
                "desc": "Having coffee to keep myself from falling asleep at the wheel",
                "descData": None,
                "dueReminder": -1,
                "idBoard": "abcd1234",
                "idList": "600ede7caeb0c67b818ec913",
                "idMembersVoted": [],
                "idShort": 22,
                "idAttachmentCover": None,
                "idLabels": [],
                "manualCoverAttachment": False,
                "name": "Coffee",
                "pos": 16384,
                "shortLink": "JlDCgB0e",
                "isTemplate": False,
                "cardRole": None,
                "badges": {
                    "attachmentsByType": {
                        "trello": {
                            "board": 0,
                            "card": 0
                        }
                    },
                    "location": False,
                    "votes": 0,
                    "viewingMemberVoted": False,
                    "subscribed": False,
                    "fogbugz": "",
                    "checkItems": 0,
                    "checkItemsChecked": 0,
                    "checkItemsEarliestDue": None,
                    "comments": 0,
                    "attachments": 0,
                    "description": True,
                    "due": None,
                    "dueComplete": False,
                    "start": None
                },
                "dueComplete": False,
                "due": None,
                "idChecklists": [],
                "idMembers": [],
                "labels": [],
                "shortUrl": "https://trello.com/c/JlDCgB0e",
                "start": None,
                "subscribed": False,
                "url": "https://trello.com/c/JlDCgB0e/22-coffee",
                "cover": {
                    "idAttachment": None,
                    "color": None,
                    "idUploadedBackground": None,
                    "size": "normal",
                    "brightness": "light",
                    "idPlugin": None
                }
            },
            {
                "id": "6037ac8cd9b8ac5fba6946d7",
                "checkItemStates": None,
                "closed": False,
                "dateLastActivity": "2021-03-02T16:08:46.455Z",
                "desc": "Time to eat some cake because why the hell not!",
                "descData": None,
                "dueReminder": None,
                "idBoard": "abcd1234",
                "idList": "600ede7caeb0c67b818ec913",
                "idMembersVoted": [],
                "idShort": 30,
                "idAttachmentCover": None,
                "idLabels": [],
                "manualCoverAttachment": False,
                "name": "Cake time",
                "pos": 65536,
                "shortLink": "IUKu6VLB",
                "isTemplate": False,
                "cardRole": None,
                "badges": {
                    "attachmentsByType": {
                        "trello": {
                            "board": 0,
                            "card": 0
                        }
                    },
                    "location": False,
                    "votes": 0,
                    "viewingMemberVoted": False,
                    "subscribed": False,
                    "fogbugz": "",
                    "checkItems": 0,
                    "checkItemsChecked": 0,
                    "checkItemsEarliestDue": None,
                    "comments": 0,
                    "attachments": 0,
                    "description": True,
                    "due": "2021-02-28T00:00:00.000Z",
                    "dueComplete": False,
                    "start": None
                },
                "dueComplete": False,
                "due": "2021-02-28T00:00:00.000Z",
                "idChecklists": [],
                "idMembers": [],
                "labels": [],
                "shortUrl": "https://trello.com/c/IUKu6VLB",
                "start": None,
                "subscribed": False,
                "url": "https://trello.com/c/IUKu6VLB/30-cake-time",
                "cover": {
                    "idAttachment": None,
                    "color": None,
                    "idUploadedBackground": None,
                    "size": "normal",
                    "brightness": "light",
                    "idPlugin": None
                }
            },
            {
                "id": "603e2d668ecdb44ae6add243",
                "checkItemStates": None,
                "closed": False,
                "dateLastActivity": "2021-03-02T12:19:51.004Z",
                "desc": "",
                "descData": None,
                "dueReminder": None,
                "idBoard": "abcd1234",
                "idList": "600ede7caeb0c67b818ec913",
                "idMembersVoted": [],
                "idShort": 31,
                "idAttachmentCover": None,
                "idLabels": [],
                "manualCoverAttachment": False,
                "name": "moo",
                "pos": 81920,
                "shortLink": "TvCH1dTC",
                "isTemplate": False,
                "cardRole": None,
                "badges": {
                    "attachmentsByType": {
                        "trello": {
                            "board": 0,
                            "card": 0
                        }
                    },
                    "location": False,
                    "votes": 0,
                    "viewingMemberVoted": False,
                    "subscribed": False,
                    "fogbugz": "",
                    "checkItems": 0,
                    "checkItemsChecked": 0,
                    "checkItemsEarliestDue": None,
                    "comments": 0,
                    "attachments": 0,
                    "description": False,
                    "due": "2021-04-01T00:00:00.000Z",
                    "dueComplete": False,
                    "start": None
                },
                "dueComplete": False,
                "due": "2021-04-01T00:00:00.000Z",
                "idChecklists": [],
                "idMembers": [],
                "labels": [],
                "shortUrl": "https://trello.com/c/TvCH1dTC",
                "start": None,
                "subscribed": False,
                "url": "https://trello.com/c/TvCH1dTC/31-moo",
                "cover": {
                    "idAttachment": None,
                    "color": None,
                    "idUploadedBackground": None,
                    "size": "normal",
                    "brightness": "light",
                    "idPlugin": None
                }
            }
        ]
        response.json.return_value = json_return
        return response
    return None