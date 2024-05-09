# import json
#
# import aiohttp
# import asyncio
#
# async def output_resp(url, data):
#     async with aiohttp.ClientSession() as session:
#         async with session.post(url, json=data) as response:
#             if response.status == 200:
#                 print('resp found: ')
#                 result = await response.text()
#                 # response_json = json.loads(result)  # Convert JSON string to Python dictionary
#                 print(result, end='')  # Access and print the value of 'response' key
#
# # Data and URL setup
# url = "http://localhost:11434/api/generate"
# data = {
#     "model": "phi3",
#     "prompt": "explain this code to me ```import re \nprint('Hello world')```",
# }
#
# # Running the asynchronous function
# asyncio.run(output_resp(url, data))

print()

from langchain_community.llms import Ollama

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

llm = Ollama(
    model="phi3", callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
)
llm.invoke("what is 3 + 9")