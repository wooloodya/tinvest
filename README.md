# T-Invest

```
pip install tinvest
```

```python
import asyncio

import tinvest

TOKEN = "<TOKEN>"

handlers = tinvest.StreamingHandlers()


@handlers.candle("BBG0013HGFT4", "1min")
async def candle(payload):
    print(payload)


@handlers.instrument_info("BBG0013HGFT4", "123ASD1123")
async def instrument_info(payload):
    print(payload)


@handlers.orderbook("BBG0013HGFT4", depth=5)
async def orderbook(payload):
    print(payload)


async def main():
    await tinvest.Streaming(TOKEN).add_handlers(handlers).run()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
        loop.run_forever()
    except KeyboardInterrupt:
        pass

```

```python
import tinvest

TOKEN = "<TOKEN>"

client = tinvest.SyncClient(TOKEN)
api = tinvest.PortfolioApi(client)

response = api.portfolio_get()
data = response.json()
print(tinvest.PortfolioResponse(**data))
```

```python
import asyncio
import tinvest

TOKEN = "<TOKEN>"

client = tinvest.AsyncClient(TOKEN)
api = tinvest.PortfolioApi(client)


async def request():
    await client.init_autoclose()
    async with api.portfolio_get() as response:
        data = await response.json()
        print(tinvest.PortfolioResponse(**data))


loop = asyncio.get_event_loop()
loop.run_until_complete(request())
```