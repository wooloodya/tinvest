from typing import Any, Callable, Dict, Optional, Tuple, List

import logging
import asyncio
import aiohttp

from .constants import STREAMING
from .shemas import CandleResolution
from .types import AnyDict

logger = logging.getLogger(__name__)


INTERVALS = tuple(c.value for c in CandleResolution)

_Handler = Tuple[str, Callable, Optional[AnyDict], Optional[AnyDict]]


class StreamingHandlers:
    def __init__(self):
        self.handlers: List[_Handler] = []

    def _decorator_wrapper(self, kind: str, data: Any):
        def decorator(func):
            self.handlers.append(
                (
                    kind,
                    func,
                    {"event": f"{kind}:subscribe", **data},
                    {"event": f"{kind}:unsubscribe", **data},
                )
            )
            return func

        return decorator

    def candle(self, figi: str, interval: str):
        if interval not in INTERVALS:
            raise ValueError(f"{interval} not in {INTERVALS}")

        kind = "candle"
        data = {"figi": f"{figi}", "interval": f"{interval}"}
        return self._decorator_wrapper(kind, data)

    def orderbook(self, figi: str, depth: int = 2):
        if not 0 < depth <= 20:
            raise ValueError(f"not 0 < {depth} <= 20")

        kind = "orderbook"
        data = {"figi": f"{figi}", "depth": depth}
        return self._decorator_wrapper(kind, data)

    def instrument_info(self, figi, request_id=None):
        kind = "instrument_info"
        data = {"figi": f"{figi}"}
        if request_id:
            data["request_id"] = request_id
        return self._decorator_wrapper(kind, data)

    def error(self):
        def decorator(func):
            self.handlers.append(("error", func, None, None))
            return func

        return decorator


class Streaming:
    def __init__(
        self, token: str, session=None, loop: Optional[asyncio.AbstractEventLoop] = None
    ):
        super().__init__()
        if not token:
            raise ValueError("Token cannot be empty")
        self._api: str = STREAMING
        self._token: str = token
        self._loop: asyncio.AbstractEventLoop = loop or asyncio.get_event_loop()
        self._session: aiohttp.ClientSession = session or aiohttp.ClientSession()
        self._handlers: List[_Handler] = []

    def add_handlers(self, handlers):
        if isinstance(handlers, list):
            self._handlers = handlers
        else:
            self._handlers = handlers.handlers

        return self

    async def run(self):
        async with self._session.ws_connect(
            self._api, headers={"Authorization": f"Bearer {self._token}",}
        ) as ws:
            try:
                for *_, request_data, _ in self._handlers:
                    if request_data:
                        await ws.send_json(request_data)

                async for msg in ws:
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        data = msg.json()
                        funcs = [
                            func(data["payload"])
                            for kind, func, *_ in self._handlers
                            if data["event"] == kind
                        ]
                        await asyncio.gather(*funcs)
                    elif msg.type == aiohttp.WSMsgType.CLOSED:
                        break
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        break
            except asyncio.CancelledError:
                for *_, request_data in self._handlers:
                    if request_data:
                        await ws.send_json(request_data)
                await self._session.close()
                raise
