# RAG 基础层：负责知识库的构建和加载 (向量存储)
from fileinput import filename
import os
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


OLLAMA_EMBEDDING_MODEL = os.environ.get("OLLAMA_EMBEDDING_MODEL_NAME", "nomic-embed-text")
CHROMA_PATH = os.environ.get("CHROMA_DB_PATH", "chroma_data")
RAG_DOCS_PATH = os.environ.get("RAG_DOCS_PATH", "rag_docs")

if not os.path.exists(RAG_DOCS_PATH):
    os.makedirs(RAG_DOCS_PATH)
    with open(os.path.join(RAG_DOCS_PATH, "README.md"),
              "w",
              encoding="utf-8") as f:
        f.write("# LangChain LCEL 是一个用于构建复杂 LLM 应用程序的强大工具。它支持流式传输、并行执行和运行时检查。LangServe 是部署 LCEL 链的首选方式。本项目使用 Ollama 作为 LLM 和嵌入模型。")

def get_vector_store():
    """
    加载文档，分割，嵌入，并创建或加载向量存储。
    此函数返回一个向量存储对象。
    """
    embeddings = OllamaEmbeddings(
            model=OLLAMA_EMBEDDING_MODEL,
            base_url=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
        )
    if os.path.exists(CHROMA_PATH) and os.listdir(CHROMA_PATH):
        print("💡 知识库已存在,正在加载...")
        vector_store = Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=embeddings
        )
        return vector_store
    print("✨ 正在创建知识库...")
    # 1️⃣load
    docs = []
    for filename in os.listdir(RAG_DOCS_PATH):
        if filename.endswith(".md"):
            loader = UnstructuredMarkdownLoader(os.path.join(RAG_DOCS_PATH, filename))
            docs.extend(loader.load())
    if not docs:
        print("❌ 没有找到任何文档。")
        return None
    # 2️⃣split
    # 创建文本分割器
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
    )
    # 分割文档
    split = text_splitter.split_documents(docs)
    # 3️⃣embed
    vector_store = Chroma.from_documents(
        documents=split,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    print("✅ 知识库创建成功，共 {len(splits)} 个文档片段。")
    return vector_store
    

        
