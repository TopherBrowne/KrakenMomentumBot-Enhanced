import asyncio
import json
import websockets

async def main():
    url = "wss://ws.kraken.com/v2"
    print(f"Connecting to {url}...")
    async with websockets.connect(url) as ws:
        sub = {
            "method": "subscribe",
            "params": {
                "channel": "ticker",
                "symbol": ["BTC/USD"]
            }
        }
        await ws.send(json.dumps(sub))
        print("Sent subscribe request. Listening for 5 messages...\n")
        for i in range(5):
            msg = await ws.recv()
            print(f"[{i+1}] {msg}\n")

asyncio.run(main())
