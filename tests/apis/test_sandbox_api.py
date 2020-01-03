import pytest

from tinvest import (
    Empty,
    SandboxApi,
    SandboxSetCurrencyBalanceRequest,
    SandboxSetPositionBalanceRequest,
)


@pytest.fixture()
def http_client(mocker):
    return mocker.Mock()


@pytest.fixture()
def api_client(http_client):
    return SandboxApi(http_client)


def test_sandbox_register(api_client, http_client):
    api_client.sandbox_register_post()
    http_client.request.assert_called_once_with(
        'POST', '/sandbox/sandbox/register', response_model=Empty
    )


def test_sandbox_currencies_balance(api_client, http_client):
    body = SandboxSetCurrencyBalanceRequest.parse_obj(
        {'balance': 1000.0, 'currency': 'USD'}
    )
    api_client.sandbox_currencies_balance_post(body)
    http_client.request.assert_called_once_with(
        'POST',
        '/sandbox/sandbox/currencies/balance',
        response_model=Empty,
        data=body.json(by_alias=True),
    )


def test_sandbox_positions_balance(api_client, http_client):
    body = SandboxSetPositionBalanceRequest.parse_obj(
        {'balance': 1000.0, 'figi': '<FIGI>'}
    )
    api_client.sandbox_positions_balance_post(body)
    http_client.request.assert_called_once_with(
        'POST',
        '/sandbox/sandbox/positions/balance',
        response_model=Empty,
        data=body.json(by_alias=True),
    )


def test_sandbox_clear(api_client, http_client):
    api_client.sandbox_clear_post()
    http_client.request.assert_called_once_with(
        'POST', '/sandbox/sandbox/clear', response_model=Empty
    )
