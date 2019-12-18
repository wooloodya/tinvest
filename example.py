import asyncio

import tinvest

TOKEN = "<TOKEN>"

# client = tinvest.Client(TOKEN)

handlers = tinvest.StreamingHandlers()


@handlers.candle("BBG005DXJS36", "1min")
async def candle(payload):
    print(payload)


@handlers.instrument_info("BBG005DXJS36", "123ASD1123")
async def instrument_info(payload):
    print(payload)


@handlers.orderbook("BBG005DXJS36", depth=5)
async def orderbook(payload):
    print(payload["bids"])
    print(payload["asks"])


async def main():
    await tinvest.Streaming(TOKEN).add_handlers(handlers).run()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
        loop.run_forever()
    except KeyboardInterrupt:
        pass
