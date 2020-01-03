from typing import Any

from requests import Response, Session, session

from .base_client import BaseClient
from .shemas import Error
from .utils import set_default_headers


class ResponseWrapper:
    def __init__(self, response: Response, response_model: Any):
        self._response = response
        self._response_model = response_model

    def __getattr__(self, name):
        return getattr(self._response, name)

    def parse_json(self, **kwargs: Any) -> Any:
        return self._parse_json(self._response_model, **kwargs)

    def parse_error(self, **kwargs: Any) -> Any:
        return self._parse_json(Error, **kwargs)

    def _parse_json(self, response_model: Any, **kwargs: Any) -> Any:
        if response_model is None:
            return self._response.json(**kwargs)
        return response_model.parse_obj(self._response.json(**kwargs))


class SyncClient(BaseClient[Session]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._session is None:
            self._session = session()

    def request(
        self,
        method: str,
        path: str,
        response_model: Any = None,
        raise_for_status: bool = False,
        **kwargs: Any,
    ) -> ResponseWrapper:
        url = self._base_url + path
        set_default_headers(kwargs, self._token)

        response = ResponseWrapper(
            self.session.request(method, url, **kwargs), response_model
        )

        if raise_for_status:
            response.raise_for_status()

        return response


__all__ = ('SyncClient', 'ResponseWrapper')
