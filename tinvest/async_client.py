import asyncio
from contextlib import asynccontextmanager
from functools import partial

from aiohttp import ClientSession

from .base_client import BaseClient
from .shemas import Error
from .utils import set_default_headers


class AsyncClient(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._session is None:
            self._session = ClientSession(raise_for_status=True)

    @asynccontextmanager
    async def request(self, method: str, path: str, response_model=None, **kwargs):
        url = self._api + path
        set_default_headers(kwargs, self._token)

        async with self._session.request(method, url, **kwargs) as response:
            setattr(
                response, "parse_json", partial(_parse_json, response, response_model)
            )
            setattr(response, "parse_error", partial(_parse_json, response, Error))
            yield response

    async def init_autoclose(self):
        loop = asyncio.get_event_loop()

        async def idle():
            try:
                while True:
                    await asyncio.sleep(60)
            except asyncio.CancelledError:
                await self._session.close()
                raise

        loop.create_task(idle())


async def _parse_json(response, response_model=None, **kwargs):
    if response_model is None:
        return await response.json(**kwargs)
    return response_model.parse_obj(await response.json(**kwargs))
