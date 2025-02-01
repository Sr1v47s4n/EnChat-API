import asyncio
import websockets
import json

TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzM4Mzc5MTAxLCJpYXQiOjE3MzgzNzg4MDEsImp0aSI6Ijc1NDIxZGUxMmZlMjRkNzE4YjFmMmI0ZjVjNWM1ZDJlIiwidXNlcl9pZCI6MX0.e7WZgwnHRYa2spXROoLCo_hZCWiqDOkpkc-allqLf3s"  # Replace with a valid JWT token
ROOM_ID = "2"  # Adjust this based on your WebSocket route


async def connect():
    url = f"ws://127.0.0.1:8000/ws/chat/{ROOM_ID}/?token={TOKEN}"

    try:
        async with websockets.connect(url) as ws:
            print("Connected to WebSocket!")

            # Send a test message
            message = json.dumps({"message": "Hello, WebSocket!"})
            await ws.send(message)

            # Receive a response
            response = await ws.recv()
            print("Received:", response)

    except Exception as e:
        print("Error:", e)


asyncio.run(connect())
