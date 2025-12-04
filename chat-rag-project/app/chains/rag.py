# LangChain LCEL 层：定义 RAG 流程和逻辑
from langchain_core.documents import Document
import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama
from app.rag.setup import get_vector_store
from langchain_core.runnables import RunnableParallel,RunnablePassthrough
from langchain_core.tools import tool
from app.models.chat import RAGInput
VECTOR_STORE = get_vector_store()
RETRIEVER = VECTOR_STORE.as_retriever(search_kwargs={"k": 3}) if VECTOR_STORE else None

OLLAMA_CHAT_MODEL = os.environ.get("OLLAMA_CHAT_MODEL_NAME", "qwen2.5:1.5b")
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
OLLLAMA_TEMP = float(os.environ.get("OLLAMA_TEMPERATURE", 0.7))



strOutput = StrOutputParser()

llm = ChatOllama(
    model=OLLAMA_CHAT_MODEL,
    temperature=OLLLAMA_TEMP,
    base_url=OLLAMA_BASE_URL
)

RAG_PROMPT_TEMPLATE = """
你是一名专业的问答助手,请基于以下提供的上下文信息(Context)来回答用户的问题。

问题: {question}

上下文 (Context):
{context}

请仅根据上下文信息提供简洁、准确的回答。
"""
RAG_PROMPT = ChatPromptTemplate.from_template(RAG_PROMPT_TEMPLATE)

def format_docs(docs: list[Document]) -> str:
    """将检索到的文档列表格式化为单一字符串，用于注入到提示词中"""
    return "\n\n".join(doc.page_content for doc in docs)

RAG_CHAIN_BASE = (
    # 步骤 A: 检索文档
    RunnableParallel(
        # 'context' 键负责调用检索器并格式化结果
        context=RETRIEVER | format_docs,
        # 'question' 键负责透传原始的用户问题
        question=RunnablePassthrough()
    )
    # 步骤 B: 提示词生成
    | RAG_PROMPT
    # 步骤 C: LLM 生成答案
    | llm
    # 步骤 D: 解析为字符串
    | strOutput
)

# def get_final_rag_chain():
#     """
#     返回一个包含检索到的源文档信息的 RAG 链。
#     """
#     if not RETRIEVER:
#         raise ValueError("RAG 检索器未初始化，请检查知识库文件和 Ollama 服务。")

#     # 这是一个特殊的 LCEL 结构，用于在运行 LLM 之前，并行地获取 context 和 source_documents
#     FINAL_RAG_CHAIN = RunnableParallel(
#         # 'answer' 键运行 RAG 问答核心逻辑
#         answer=RAG_CHAIN_BASE, 
#         # 'source_documents' 键运行检索器，并获取原始文档对象
#         source_documents=RETRIEVER
#     )
    
#     return FINAL_RAG_CHAIN
# STREAM_RAG_CHAIN = (
#     RunnableParallel(
#         context = RETRIEVER | format_docs,
#         question= RunnablePassthrough(),
#     )
#     |RAG_PROMPT
#     |llm
# )
@tool(args_schema=RAGInput)
async def rag_tool(question: str) -> str:
    """
    使用内部知识库(RAG Chain)来回答关于公司政策、项目细节或自定义文档的问题。
    如果答案无法从内部知识库中找到，应返回 'NOT_FOUND'。
    """
    # 这里我们只调用 RAG_CHAIN_BASE，因为它只返回答案字符串，适合作为工具输出
    # 如果需要，你可以在这里添加逻辑来检查答案质量，例如如果答案太通用则返回特定的失败标志
    result = await RAG_CHAIN_BASE.ainvoke(question)

    # 简单地返回 LLM 生成的答案
    return result
__all__ = ["rag_tool", "STREAM_RAG_CHAIN"]
