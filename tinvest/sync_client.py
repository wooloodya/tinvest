import requests

from .base_client import BaseClient
from .utils import set_default_headers


class SyncClient(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._session is None:
            self._session = requests.session()

    def request(self, method: str, path: str, raise_for_status: bool = True, **kwargs):
        url = self._api + path

        set_default_headers(kwargs, self._token)

        response = self._session.request(method, url, **kwargs)

        if raise_for_status:
            response.raise_for_status()
        return response
