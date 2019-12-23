import pytest

from tinvest.constants import PRODUCTION
from tinvest.sync_client import Session, SyncClient


@pytest.fixture()
def session(mocker):
    _session = Session()
    mocker.patch.object(_session, 'request', autospec=True)
    return _session


@pytest.fixture()
def client(token, session):
    return SyncClient(token, session=session,)


def test_client_request(client, session, token):
    client.request('get', '/some_url')
    session.request.assert_called_once_with(
        method='get',
        url=f'{PRODUCTION}/some_url',
        headers={'Authorization': f'Bearer {token}', 'accept': 'application/json'},
    )


def test_client_response(client):
    response = client.request('get', '/some_url')
    assert 'parse_json' in dir(response)
    assert 'parse_error' in dir(response)
