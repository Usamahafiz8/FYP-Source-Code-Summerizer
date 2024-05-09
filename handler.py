# from langchain_core.callbacks.base import BaseCallbackHandler
# from typing import Any, Dict, List
# from websocket import create_connection  # You might use a different WebSocket library based on your setup
#
# class WebSocketCallbackHandler(BaseCallbackHandler):
#     def __init__(self, websocket_url: str):
#         self.ws = create_connection(websocket_url)
#
#     def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
#         """Send each new token via WebSocket."""
#         self.ws.send(token)
#
#     def __del__(self):
#         self.ws.close()


from __future__ import annotations
import asyncio
from typing import TYPE_CHECKING, Any, Dict, List
from langchain_core.callbacks.base import BaseCallbackHandler

if TYPE_CHECKING:
    from langchain_core.agents import AgentAction, AgentFinish
    from langchain_core.messages import BaseMessage
    from langchain_core.outputs import LLMResult
#
# class AsyncQueueCallbackHandler(BaseCallbackHandler):
#     def __init__(self):
#         self.queue = asyncio.Queue()
#
#     async def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
#         """Place each new token into an async queue."""
#         # await self.queue.put(token)
#         print('recieved token: ', token)
#         yield token
#
#     async def get_next_token(self) -> str:
#         """Retrieve the next token from the queue."""
#         return await self.queue.get()
#
#     def is_queue_empty(self) -> bool:
#         """Check if the queue is empty."""
#         return self.queue.empty()

# ______________________________________________________________


from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.prompts import ChatPromptTemplate
# from langchain_openai import ChatOpenAI


class MyCustomHandler(BaseCallbackHandler):
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        print(f"My custom handler, token: {token}")
        
        
        
html = """<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8" />
    <title>Liqueous Assistant 🤖</title>
    <meta name="viewport" content="initial-scale=1, width=device-width" />
    <script src="https://unpkg.com/react@latest/umd/react.development.js" crossorigin="anonymous"></script>
    <script src="https://unpkg.com/react-dom@latest/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@mui/material@latest/umd/material-ui.development.js"
        crossorigin="anonymous"></script>
    <script src="https://unpkg.com/@babel/standalone@latest/babel.min.js" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link rel="stylesheet"
        href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;600;700&display=swap" />
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons" />
</head>

<body>
    <div id="root"></div>
    <script type="text/babel">
        const {
            colors,
            CssBaseline,
            ThemeProvider,
            Typography,
            TextField,
            Container,
            createTheme,
            Box,
            Skeleton,
        } = MaterialUI;

        const theme = createTheme({
            palette: {
                mode: 'dark'
            },
        });
        const WS = new WebSocket("ws://localhost:8000/chat?sid=sid");

        function App() {
            const [response, setResponse] = React.useState("");
            const [question, setQuestion] = React.useState("");
            const [loading, setLoading] = React.useState(false);

            React.useEffect(() => {
                WS.onmessage = (event,params) => {
                    setLoading(false);
                    console.log(event,"event")
                    console.log(params,"params")
                    const payload = JSON.parse(event.data);
                    setResponse(marked.parse(payload.text));
                };
            }, []);

            return (
                <Container maxWidth="lg">
                    <Box sx={{ my: 4 }}>
                        <Typography variant="h4" component="h1" gutterBottom>
                            Liqueous Chatbot 🌻
                        </Typography>
                        <TextField
                            id="outlined-basic"
                            label="Ask me Anything"
                            variant="outlined"
                            style={{ width: '100%' }}
                            value={question}
                            disabled={loading}
                            onChange={e => {
                                setQuestion(e.target.value)
                            }}
                            onKeyUp={e => {
                                setLoading(false)
                                if (e.key === "Enter") {
                                    setResponse('')
                                    setLoading(true)
                                    WS.send(question);
                                }
                            }}
                        />
                    </Box>
                    {!response && loading && (<>
                        <Skeleton />
                        <Skeleton animation="wave" />
                        <Skeleton animation={false} /></>)}
                    {response && <Typography dangerouslySetInnerHTML={{ __html: response }} />}
                </Container>
            );
        }

        ReactDOM.createRoot(document.getElementById('root')).render(
            <ThemeProvider theme={theme}>
                <CssBaseline />
                <App />
            </ThemeProvider>,
        );
    </script>
</body>

</html>
"""