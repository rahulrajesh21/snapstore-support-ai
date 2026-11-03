from fastapi import APIRouter
from model.query_chat import QueryChat
from services.rag_service import rag_chat

router = APIRouter()

@router.post('/chat')
async def chat(query: QueryChat):
    response = await rag_chat(query=query)
    return response
    


