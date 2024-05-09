# # from flask import Flask
# # from flask_socketio import SocketIO, emit
# # from flask_socketio import send, emit
# #
# #
# # app = Flask(__name__)
# # socketio = SocketIO(app, cors_allowed_origins="*")
# #
# # @socketio.on('connect')
# # def handle_connect():
# #     emit('status', {'data': 'Connected'})
# #
# #
# # # Dummy example of emitting a new token
# # @socketio.on('some_event')
# # def handle_message(message):
# #     # Assuming `token` is being generated here
# #     token = "Example token"
# #     emit('new_token', token)
# #
# #
# # if __name__ == '__main__':
# #     socketio.run(app, host='0.0.0.0', port=5000)
# print()
#
# from langchain_community.llms import Ollama
# from langchain.callbacks.manager import CallbackManager
# from handler import MyCustomHandler
#
#
# async def invoke_model(query):
#     callback_handler = MyCustomHandler()
#     llm = Ollama(
#         model = "phi3",
#         callback_manager = CallbackManager([callback_handler])
#     )
#
#     # Start the model invocation
#     asyncio.create_task(llm.invoke(query))  # This needs to be implemented if not already available
#
#     # Process tokens as they arrive
#     while True:
#         token = await callback_handler.get_next_token()
#         # Here, you would send the token to your frontend via WebSocket
#         print(token, end = '-', flush = True)  # Replace this line with WebSocket send
#         if callback_handler.is_queue_empty():
#             break
#
#
# import asyncio
#
# # Example of how to run the async function
# asyncio.run(invoke_model("what is 3 + 9"))
print()

import os
import uvicorn
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi import FastAPI, Request, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict
# from agent import invoke_agent
# from database import insert_or_update_chat_history, retrieve_chat_history
from handler import html

from dotenv import load_dotenv

from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title = "Chatbot Streaming using FastAPI")

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

# HTML content here for simplicity; typically, you might load this from a file or another module.
html = """<!DOCTYPE html>..."""


@app.get("/{sid}", response_class = HTMLResponse)
async def web_app(request: Request, sid: str):
    """
    Serve the HTML interface for the chatbot.
    """
    listen_port = int(os.getenv('LISTEN_PORT', '8000'))
    customized_html = html.replace('8000', str(listen_port)).replace('sid=sid', f'sid={sid}')
    return HTMLResponse(content = customized_html)

from langchain_core.callbacks import BaseCallbackHandler
from langchain_community.llms import Ollama

from langchain.callbacks.manager import CallbackManager
class MyCustomHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        print(f"My custom handler, token: {token}")


@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket, sid: str):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # Process the data through the LLM (logic to be implemented)
            response = f"Processed: {data}"  # Placeholder for actual LLM processing
            llm = Ollama(
                model = "phi3", callback_manager = CallbackManager([MyCustomHandler()])
            )
            llm.invoke(data)
            
            
            await websocket.send_text(response)
    except WebSocketDisconnect:
        print("Client disconnected")
