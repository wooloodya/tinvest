from functools import partial
import requests

from .base_client import BaseClient
from .shemas import Error
from .utils import set_default_headers


class SyncClient(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._session is None:
            self._session = requests.session()

    def request(
        self,
        method: str,
        path: str,
        response_model=None,
        raise_for_status: bool = True,
        **kwargs
    ):
        url = self._api + path
        set_default_headers(kwargs, self._token)

        response = self._session.request(method, url, **kwargs)

        setattr(response, "parse_json", partial(_parse_json, response, response_model))
        setattr(response, "parse_error", partial(_parse_json, response, Error))

        if raise_for_status:
            response.raise_for_status()
        return response


def _parse_json(response, response_model=None, **kwargs):
    if response_model is None:
        return response.json(**kwargs)
    return response_model.parse_obj(response.json(**kwargs))
