import os
from langchain_core.prompts import ChatPromptTemplate
# 修正导入路径：AgentExecutor 和 create_react_agent

from langchain.agents import create_agent
from langchain_community.tools.tavily_search import TavilySearchResults 
from langchain_deepseek import ChatDeepSeek
from sympy import im
from app.chains.rag import rag_tool
from dotenv import load_dotenv
from app.models.chat import ChatResponse
from langchain.agents.structured_output import ToolStrategy
load_dotenv()

# --- 1. 定义工具集 ---
# 确保 rag_tool 已正确定义并导入
tools = [
    rag_tool,
]

# --- 2. 定义 Agent 提示词模板 ---
AGENT_PROMPT = "你是一个万能助理。你的主要目标是准确回答用户的问题。你应该首先尝试使用 rag_tool来回答关于你内部知识或项目细节的问题。如果问题是关于实时或外部世界的，请使用其他可用的工具。请严格遵循 Thought/Action/Action Input/Observation 格式进行思考。"

# --- 3. 初始化 LLM ---
# 使用 DeepSeek Chat 模型，它具有较好的指令遵循能力
LLM =  ChatDeepSeek(
    model="deepseek-chat",
)


def get_agent():
    """创建并返回 Agent 的执行器 (AgentExecutor)"""
    
    # 步骤 A: 使用 create_react_agent 创建 Agent Chain
    agent = create_agent(
        model=LLM, 
        tools=tools, 
        system_prompt=AGENT_PROMPT,
        response_format=ToolStrategy(ChatResponse)
    )
    return agent