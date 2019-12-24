from tinvest.utils import set_default_headers


def test_set_default_headers(token):
    data = {}
    set_default_headers(data, token)
    assert data == {
        'headers': {'accept': 'application/json', 'Authorization': f'Bearer {token}'}
    }


def test_set_default_headers_with_headers(token):
    data = {
        'headers': {'Authorization': 'Bearer <OTHER_TOKEN>', 'X-Custom-Header': 'value'}
    }
    set_default_headers(data, token)
    assert data == {
        'headers': {
            'accept': 'application/json',
            'Authorization': 'Bearer <OTHER_TOKEN>',
            'X-Custom-Header': 'value',
        }
    }
