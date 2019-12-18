import requests

from .base_client import BaseClient


class Client(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._session is None:
            self._session = requests.session()

    def portfolio(self):
        response = self._session.get(f"{self._api}/portfolio", headers=self.headers)
        data = response.json()
        return data["payload"]["positions"]

    def portfolio_currencies(self):
        response = self._session.get(
            f"{self._api}/portfolio/currencies", headers=self.headers
        )
        data = response.json()
        return data["payload"]["currencies"]

    def operations(self, from_, to, figi=None):
        # response = self._session.get(f'{self._api}/operations?from=&to=', headers=self.headers)
        # data = response.json()
        # return data['payload']['operations']
        raise NotImplementedError()