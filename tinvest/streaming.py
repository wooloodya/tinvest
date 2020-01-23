import asyncio
import logging
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import aiohttp

from .constants import STREAMING
from .shemas import (
    CandleResolution,
    CandleStreamingSchema,
    ErrorStreamingSchema,
    InstrumentInfoStreamingSchema,
    OrderbookStreamingSchema,
)
from .typedefs import AnyDict
from .utils import Func

logger = logging.getLogger(__name__)


_Handler = Tuple[str, Callable]


class EventName(str, Enum):
    candle = 'candle'
    orderbook = 'orderbook'
    instrument_info = 'instrument_info'
    error = 'error'


def _retry(func):
    async def wrapper(self):
        while True:
            await func(self)

    return wrapper


class Streaming:

    schemas: Dict[EventName, Any] = {
        EventName.candle: CandleStreamingSchema,
        EventName.orderbook: OrderbookStreamingSchema,
        EventName.instrument_info: InstrumentInfoStreamingSchema,
        EventName.error: ErrorStreamingSchema,
    }

    def __init__(  # pylint: disable=R0913
        self,
        token: str,
        session=None,
        state: Optional[AnyDict] = None,
        reconnect_timeout: float = 3,
        ws_close_timeout: float = 0,
        receive_timeout: Optional[float] = 5,
        heartbeat: Optional[float] = 3,
    ) -> None:
        super().__init__()
        if not token:
            raise ValueError('Token cannot be empty')
        self._api: str = STREAMING
        self._token: str = token
        self._session: aiohttp.ClientSession = session or aiohttp.ClientSession()
        self._handlers: List[_Handler] = []
        self._state = state
        self._reconnect_timeout = reconnect_timeout
        self._ws_close_timeout = ws_close_timeout
        self._receive_timeout = receive_timeout
        self._heartbeat = heartbeat

    def add_handlers(
        self, handlers: Union[List[_Handler], 'StreamingEvents']
    ) -> 'Streaming':
        if isinstance(handlers, list):
            self._handlers.extend(handlers)
        else:
            self._handlers.extend(handlers.handlers)

        return self

    @_retry
    async def run(self) -> None:
        try:
            async with self._session.ws_connect(
                self._api,
                headers={'Authorization': f'Bearer {self._token}'},
                heartbeat=self._heartbeat,
                timeout=self._ws_close_timeout,
                receive_timeout=self._receive_timeout,
            ) as ws:
                await self._run(ws)
        except asyncio.CancelledError:
            raise
        except Exception as e:  # pylint: disable=W0703
            logger.error('Connection error: %s. Try to reconnect', e)
            await asyncio.sleep(self._reconnect_timeout)

    async def _run(self, ws):
        api = StreamingApi(ws, self._state)
        try:
            funcs = self._get_handlers('startup')
            await asyncio.gather(*[Func(func, api)() for func in funcs])

            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    data = msg.json()
                    event_name = data['event']
                    payload = data['payload']
                    funcs = self._get_handlers(event_name)
                    if event_name in self.schemas:
                        data = self.schemas[event_name].parse_obj(payload)
                    else:
                        data = payload
                    await asyncio.gather(*[Func(func, api, data)() for func in funcs])
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    break
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    break
            await self._cleanup(api)
        except asyncio.CancelledError:
            await self._cleanup(api)
            raise

    def _get_handlers(self, event_name):
        return [func for name, func in self._handlers if name == event_name]

    async def _cleanup(self, api) -> None:
        funcs = self._get_handlers('cleanup')
        await asyncio.gather(*[Func(func, api)() for func in funcs])
        await self._session.close()


class _BaseEvent:
    def __init__(self, ws):
        self.ws = ws

    async def _send(self, payload):
        await self.ws.send_json(payload)


class CandleEvent(_BaseEvent):
    INTERVALS = tuple(c.value for c in CandleResolution)

    def subscribe(
        self, figi: str, interval: CandleResolution, request_id: Optional[str] = None,
    ):
        return self._send(
            {
                'event': f'{EventName.candle}:subscribe',
                **self._get_payload(figi, interval, request_id),
            }
        )

    def unsubscribe(
        self, figi: str, interval: CandleResolution, request_id: Optional[str] = None,
    ):
        return self._send(
            {
                'event': f'{EventName.candle}:unsubscribe',
                **self._get_payload(figi, interval, request_id),
            }
        )

    def _get_payload(
        self, figi: str, interval: CandleResolution, request_id: Optional[str] = None,
    ):
        if interval not in self.INTERVALS:
            raise ValueError(f'{interval} not in {self.INTERVALS}')

        data = {'figi': figi, 'interval': interval}
        if request_id:
            data['request_id'] = request_id
        return data


class OrderbookEvent(_BaseEvent):
    def subscribe(self, figi: str, depth: int = 2, request_id: Optional[str] = None):
        return self._send(
            {
                'event': f'{EventName.orderbook}:subscribe',
                **self._get_payload(figi, depth, request_id),
            }
        )

    def unsubscribe(self, figi: str, depth: int = 2, request_id: Optional[str] = None):
        return self._send(
            {
                'event': f'{EventName.orderbook}:unsubscribe',
                **self._get_payload(figi, depth, request_id),
            }
        )

    @staticmethod
    def _get_payload(figi: str, depth: int = 2, request_id: Optional[str] = None):
        if not 0 < depth <= 20:
            raise ValueError(f'not 0 < {depth} <= 20')
        data = {'figi': figi, 'depth': depth}
        if request_id:
            data['request_id'] = request_id
        return data


class InstrumentInfoEvent(_BaseEvent):
    def subscribe(self, figi: str, request_id: Optional[str] = None):
        return self._send(
            {
                'event': f'{EventName.instrument_info}:subscribe',
                **self._get_payload(figi, request_id),
            }
        )

    def unsubscribe(self, figi: str, request_id: Optional[str] = None):
        return self._send(
            {
                'event': f'{EventName.instrument_info}:unsubscribe',
                **self._get_payload(figi, request_id),
            }
        )

    @staticmethod
    def _get_payload(figi: str, request_id: Optional[str] = None):
        data = {'figi': figi}
        if request_id:
            data['request_id'] = request_id

        return data


class StreamingEvents:
    def __init__(self) -> None:
        self.handlers: List[_Handler] = []

    def _decorator_wrapper(self, event_name: str):
        def decorator(func):
            self.handlers.append((event_name, func))
            return func

        return decorator

    def startup(self):
        return self._decorator_wrapper('startup')

    def candle(self):
        return self._decorator_wrapper(EventName.candle)

    def orderbook(self):
        return self._decorator_wrapper(EventName.orderbook)

    def instrument_info(self):
        return self._decorator_wrapper(EventName.instrument_info)

    def error(self):
        return self._decorator_wrapper(EventName.error)

    def cleanup(self):
        return self._decorator_wrapper('cleanup')


class StreamingApi:
    def __init__(self, ws, state: Optional[AnyDict] = None) -> None:
        self.candle = CandleEvent(ws)
        self.orderbook = OrderbookEvent(ws)
        self.instrument_info = InstrumentInfoEvent(ws)
        self._state = state

    def __getitem__(self, key: str) -> Any:
        if self._state and key in self._state:
            return self._state[key]
        raise IndexError
