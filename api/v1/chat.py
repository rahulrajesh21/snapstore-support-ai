from fastapi import APIRouter, Depends
from model.query_chat import QueryChat
from services.rag_service import rag_chat
from langchain_community.retrievers import BM25Retriever
from api.dependencies import get_bm25_retriever

router = APIRouter()

@router.post('/chat')
async def chat(query: QueryChat,bm25:BM25Retriever = Depends(get_bm25_retriever)):
    response = await rag_chat(query=query,bm25=bm25)
    return response
    


