from fastapi import FastAPI, HTTPException, Request
import httpx
import uvicorn

app = FastAPI()


@app.post("/query/")
async def query_proxy(request: Request):
    # Extract data from the incoming request
    body = await request.json()
    user_prompt = body.get("prompt", "")
    if not user_prompt:
        raise HTTPException(status_code = 400, detail = "Missing 'prompt' in the request body")
    
    # Define the URL and payload for the external API
    url = "http://localhost:11434/api/generate"
    data = {
        "model": "llama3",
        "prompt": user_prompt,
    }
    
    # Send a POST request and stream the response
    async with httpx.AsyncClient() as client:
        async with client.stream("POST", url, json = data) as response:
            if response.status_code != 200:
                raise HTTPException(status_code = response.status_code,
                                    detail = "Failed to get a response from the generate API")
            
            # Stream the response back to the client
            async def stream_response():
                async for chunk in response.aiter_bytes():
                    yield chunk
            
            return stream_response()


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host = "0.0.0.0", port = 8000)
