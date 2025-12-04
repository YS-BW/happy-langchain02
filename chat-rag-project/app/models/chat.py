# Pydantic 模型层：定义请求/响应的数据结构
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """API请求体:用于接收用户提问"""
    question : str = Field(..., description="用户提问")

class ChatResponse(BaseModel):
    """API响应体:用于返回模型生成的回答"""
    answer: str = Field(..., description="模型生成的回答")
    source_documents: list[str] = Field(..., description="来源文档")
class RAGInput(BaseModel):
    question: str = Field(..., description="用户提出的，需要从内部知识库中检索信息来回答的问题")
    