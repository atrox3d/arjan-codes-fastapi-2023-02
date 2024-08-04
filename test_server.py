import re
import requests
import pytest

@pytest.fixture
def address() -> str:
    return '127.0.0.1'

@pytest.fixture
def port() -> int:
    return 8000

@pytest.fixture
def server(address: str, port: int) -> str:
    return f'http://{address}:{port}'

@pytest.fixture
def hammer() -> dict:
    return {'name': 'Hammer', 'price': 9.99, 'count': 20, 'id': 0, 'category': 'tools'}

@pytest.fixture
def pliers() -> dict:
    return {'name': 'Pliers', 'price': 5.99, 'count': 20, 'id': 1, 'category': 'tools'}

@pytest.fixture
def nails() -> dict:
    return {'name': 'Nails', 'price': 1.99, 'count': 20, 'id': 2, 'category': 'consumables'}

@pytest.fixture
def items(hammer: dict, pliers: dict, nails: dict) -> dict:
    return {'0': hammer, '1': pliers, '2': nails}

@pytest.fixture
def not_found() -> dict:
    return {'detail': 'Not Found'}

@pytest.fixture
def query() -> dict:
    return {'name': None, 'price': None, 'count': None, 'category': None}

def test_reachable(server):
    try:
        response = requests.get(server)
        assert response.status_code == 200
    except requests.exceptions.ConnectionError:
        pytest.exit('cannot reach server')

def test_index(server, items):
    response = requests.get(server)
    assert response.status_code == 200
    assert response.json() == {'items': items}

def test_item_0_hammer(server, hammer):
    response = requests.get(f'{server}/items/0')
    assert response.status_code == 200
    assert response.json() == hammer

def test_item_55_notfound(server, not_found):
    response = requests.get(f'{server}/items/55')
    assert response.status_code == 404
    assert response.json() == not_found

def test_query_parameters(server, query, nails):
    response = requests.get(f'{server}/items?name=Nails')
    assert response.status_code == 200
    query['name'] = 'Nails'
    assert response.json()['selection'] == [nails]
    assert response.json() == {'query': query, 'selection': [nails]}

def test_reset_items(server, items):
    response = requests.get(f'{server}/reset')
    assert response.status_code == 200
    assert response.json() == {'reset': items}

def test_add_item(server, hammer):
    payload = hammer.copy()
    payload['id'] = 99
    response = requests.post(f'{server}', json=payload)
    assert response.status_code == 200
    assert response.json() == {'added': payload}
