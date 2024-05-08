import asyncio
import websockets
import aiohttp
import json


#
#
async def send_post_request(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json = data) as response:
            return await response.json()


#
#
async def handle_websocket_connection(websocket, path):
    async for message in websocket:
        # Assuming message from the client is the 'prompt' to send to the API
        data = {
            "model": "llama3",
            "prompt": message
        }
        url = "http://localhost:11434/api/generate"
        print('url: ', url)
        # Sending POST request to your API server
        response = await send_post_request(url, data)
        print('resp: ', response)
        # Sending response back to client through WebSocket
        if response:
            await websocket.send(json.dumps(response))
        else:
            await websocket.send(json.dumps({"error": "No response from API"}))


#
#
start_server = websockets.serve(handle_websocket_connection, 'localhost', 6789)
#
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
print('done...')
print(start_server)
# import asyncio
# import websockets
# import aiohttp
# import json
#
#
# async def send_post_request(url, data):
#     async with aiohttp.ClientSession() as session:
#         async with session.post(url, json = data) as response:
#             return await response.json()
#
#
# async def handle_websocket_connection(websocket, path):
#     async for message in websocket:
#         # Assuming the message from the client is the 'prompt' to send to the API
#         data = {
#             "model": "llama3",
#             "prompt": message
#         }
#         url = "http://localhost:11434/api/generate"
#
#         # Sending POST request to your API server
#         response = await send_post_request(url, data)
#
#         # Printing the API response to the console
#         print("Received response from API:", response)
#
#
# start_server = websockets.serve(handle_websocket_connection, 'localhost', 6789)
#
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio
