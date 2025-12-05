# 项目启动文件 (加载配置, 启动 FastAPI/Uvicorn)
import os
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi import FastAPI
from app.api.endpoints import router
# 加载 .env 文件中的环境变量
load_dotenv()

app = FastAPI(
    # 从环境变量中获取应用名称，如果不存在则使用默认值
    title=os.environ.get("APP_NAME", "Chat RAG API"),
)
# 包含 API 路由
app.include_router(router)

# --------------------------
# 关键: CORS 跨域配置
# --------------------------
# 定义允许跨域访问的来源列表
origins = [
    # 允许所有常见的本地开发地址和端口，确保前端访问不受阻碍
    "http://localhost",         # 允许 localhost 根域名
    "http://127.0.0.1",         # 允许 127.0.0.1 根域名
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    # 开发过程中，如果前端运行在其他端口，可以添加在这里
     "*" # 在开发环境中，也可以使用 "*" 允许所有来源，但生产环境应限制
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,              # 允许的来源列表
    allow_credentials=True,             # 允许跨域请求携带凭证
    allow_methods=["*"],                # 允许所有HTTP方法 (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],                # 允许所有请求头，以确保 Content-Type, Authorization 等通过
    expose_headers=[],                  # 通常不需要暴露自定义头
    max_age=600,                        # 缓存 CORS 预检请求的结果 10 分钟
)

if __name__ == "__main__":
    # 使用 Uvicorn 启动应用
    # host="0.0.0.0" 允许外部网络访问 (如果需要)
    # port=8000 是默认的 FastAPI 端口
    uvicorn.run(app, host="0.0.0.0", port=8000)