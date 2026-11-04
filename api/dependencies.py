from fastapi import Request
from langchain_community.retrievers import BM25Retriever


def get_bm25_retriever(request: Request) -> BM25Retriever:
    return request.app.state.bm25_retriever