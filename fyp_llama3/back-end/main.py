# from fastapi import FastAPI, HTTPException, Request
# import httpx
# import uvicorn
#
# app = FastAPI()
#
#
# @app.post("/query/")
# async def query_proxy(request: Request):
#     # Extract data from the incoming request
#     body = await request.json()
#     user_prompt = body.get("prompt", "")
#     if not user_prompt:
#         raise HTTPException(status_code = 400, detail = "Missing 'prompt' in the request body")
#
#     # Define the URL and payload for the external API
#     url = "http://localhost:11434/api/generate"
#     data = {
#         "model": "llama3",
#         "prompt": user_prompt,
#     }
#
#     # Send a POST request and stream the response
#     async with httpx.AsyncClient() as client:
#         async with client.stream("POST", url, json = data) as response:
#             if response.status_code != 200:
#                 raise HTTPException(status_code = response.status_code,
#                                     detail = "Failed to get a response from the generate API")
#
#             # Stream the response back to the client
#             async def stream_response():
#                 async for chunk in response.aiter_bytes():
#                     yield chunk
#
#             return stream_response()
#
#
# if __name__ == "__main__":
#     import uvicorn
#
#     uvicorn.run(app, host = "0.0.0.0", port = 8000)
import json

print()
from handler import create_specified_query
from fastapi import FastAPI, WebSocket, Request, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import markdown
from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.callbacks import BaseCallbackHandler



load_dotenv()

app = FastAPI(title = "Chatbot Streaming using FastAPI")


class MyCustomHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs) -> str:
        print(token, end = '')
        # return token


app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)
llm = Ollama(
    model = "llama3", callback_manager = CallbackManager([MyCustomHandler()])
)


@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # print(data)
            data = json.loads(data)  # Parse the JSON data received
            tab_id = data['tabId']
            message = data['message']
            prompt = create_specified_query(data)
            print('*'*50)
            print(f"Received from {tab_id}: {message}")
            await websocket.send_json({'text': 'Processing...', 'overwrite': True})
            # websocket.send_text(data)
            # Process the data through the LLM
            llm_resp = ''
            
            async for event in llm.astream_events(
                    prompt,
                    # include_names=["ChatOpenAI"],
                    version = 'v1'
            ):
                # print('---', event)
                kind = event["event"]
                if kind == "on_llm_stream":
                    content = event["data"]["chunk"]
                    # print("\nContent type: ",content, type(content))
                    if content:
                        llm_resp += content
                        html_content = markdown.markdown(llm_resp)
                        # print(event, content)
                        custom_html = html_content.replace('<h1>', '<h5>').replace('</h1>', '</h5>')
                        
                        # print('sent . . .', html_content)
                        await websocket.send_json({'text': custom_html, 'overwrite': True})
    except WebSocketDisconnect:
        print("Client disconnected")




if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host = "localhost", port = 8005)