from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()
from contextlib import asynccontextmanager
from api.v1.chat import router
from services.retrieval_service import load_keyword

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Initializing BM25 keyword index...")
    app.state.bm25_retriever = load_keyword()
    print("BM25Retriever loaded successfully.")

    yield
    print("Shutting down the application...")




app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=['*'],
    allow_headers=['*']
)
app.include_router(
    router=router,
    prefix='/api/v1'
)

@app.get('/')
def root():
    return {
        "status": "online",
        "service": "SnapStore Support AI API",
        "chat_endpoint": "/api/v1/chat",
        "docs": "/docs"
    }


