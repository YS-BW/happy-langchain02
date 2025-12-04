# FastAPI 路由层：处理 HTTP 请求和响应
from fastapi import APIRouter
from app.models.chat import ChatRequest, ChatResponse
from app.chains.agent import get_agent
router = APIRouter()
AGENT = get_agent()


@router.post("/chat",response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    接收用户问题,Agent 决定使用 RAG Tool 或其他工具来回答。
    """

    
    result = await AGENT.ainvoke({"messages": [{"role": "user", "content": request.question}]})
    
   
    return result['structured_response']


   


    