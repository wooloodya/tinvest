import asyncio

from aiohttp import ClientSession

from .base_client import BaseClient
from .utils import set_default_headers


class AsyncClient(BaseClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._session is None:
            self._session = ClientSession(raise_for_status=True)

    def request(self, method: str, path: str, **kwargs):
        url = self._api + path

        set_default_headers(kwargs, self._token)

        return self._session.request(method, url, **kwargs)

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