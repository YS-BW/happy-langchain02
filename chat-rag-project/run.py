# 项目启动文件 (加载配置, 启动 FastAPI/Uvicorn)
import os
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi import FastAPI
load_dotenv()

app = FastAPI(
    title=os.environ.get("APP_NAME", "Chat RAG API"),
)
# 跨域
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app)
