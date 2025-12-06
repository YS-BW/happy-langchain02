# FastAPI 路由层：处理 HTTP 请求和响应
import re
from fastapi import APIRouter
from app.models.chat import ChatRequest, ChatResponse
from app.chains.agent import get_agent
from fastapi.responses import StreamingResponse
import json
from langchain_core.messages import AIMessage,ToolMessage
import asyncio
router = APIRouter()
AGENT = get_agent()


@router.post("/chat-stream")
async def chat_stream_endpoint(request: ChatRequest):

    async_gen = AGENT.astream({"messages": [{"role": "user", "content": request.question}]}, stream_mode="values")

    async def event_generator():

        async for chunk in async_gen:
            # 遍历 chunk 中的所有消息
                msg = chunk["messages"][-1]
            
                if msg.__class__.__name__ == "AIMessage":
                    if msg.content:  # 避免空消息
                        yield msg.content
                        await asyncio.sleep(0.05)
            

    return StreamingResponse(event_generator(), media_type="text/plain")