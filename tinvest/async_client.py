from contextlib import asynccontextmanager
from functools import partial
from typing import Any

from aiohttp import ClientResponse, ClientSession

from .base_client import BaseClient
from .shemas import Error
from .utils import set_default_headers


class AsyncClient(BaseClient[ClientSession]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._session is None:
            self._session = ClientSession()

    @asynccontextmanager
    async def request(self, method: str, path: str, response_model=None, **kwargs):
        url = self._base_url + path
        set_default_headers(kwargs, self._token)

        async with self.session.request(method, url, **kwargs) as response:
            setattr(
                response, 'parse_json', partial(_parse_json, response, response_model),
            )
            setattr(response, 'parse_error', partial(_parse_json, response, Error))
            yield response

    async def close(self) -> None:
        await self.session.close()


async def _parse_json(
    response: ClientResponse, response_model: Any = None, **kwargs: Any
) -> Any:
    if response_model is None:
        return await response.json(**kwargs)
    return response_model.parse_obj(await response.json(**kwargs))
