import aiohttp
import asyncio
from aiohttp import ClientWebSocketResponse, ClientResponse

async def fetch_response_headers():
    url = "https://ws2.market-qx.pro/socket.io/?EIO=3&transport=websocket"
    headers = {
        "Host": "ws2.market-qx.pro",
        "Connection": "Upgrade",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36",
        "Upgrade": "websocket",
        "Origin": "https://market-qx.pro",
        "Sec-WebSocket-Version": "13",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9,bn;q=0.8,zh-CN;q=0.7,zh;q=0.6,pt;q=0.5",
        "Sec-WebSocket-Key": "QAZ4Cew8+8LfwJc40Hzn9w==",
        "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits"
    }

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(url, headers=headers) as ws:
            print("Connected to WebSocket")

            # If connection is successful, log the request headers
            with open('response.txt', 'a') as file:
                file.write("Request Headers:\n")
                for header, value in headers.items():
                    file.write(f"{header}: {value}\n")
                file.write("\n")

            # Send a test message
            test_message = "Hello WebSocket!"
            await ws.send_str(test_message)
            with open('response.txt', 'a') as file:
                file.write(f"Sent message: {test_message}\n\n")

            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    with open('response.txt', 'a') as file:
                        file.write(f"Received message: {msg.data}\n")
                        print(f"Received message: {msg.data}")
                elif msg.type == aiohttp.WSMsgType.CLOSED:
                    print("Connection closed")
                    break
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    print("Connection error")
                    break

async def main():
    try:
        await fetch_response_headers()
    except aiohttp.ClientResponseError as e:
        with open('response.txt', 'a') as file:
            file.write(f"Connection failed with status code: {e.status}\n")
            file.write("Response Headers:\n")
            for header, value in e.headers.items():
                file.write(f"{header}: {value}\n")
            file.write("\n")
        print(f"Connection failed with status code: {e.status}")
        print("Response Headers:")
        for header, value in e.headers.items():
            print(f"{header}: {value}")

asyncio.run(main())
