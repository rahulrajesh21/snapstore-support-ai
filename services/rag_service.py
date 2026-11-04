from agent.graph import agent
from model.query_chat import QueryChat
from services.retrieval_service import user_query
from langchain_community.retrievers import BM25Retriever
from langchain_core.messages import SystemMessage, HumanMessage
from agent.prompt import SYSTEM_PROMPT
from langchain_core.documents import Document
from services.reranker_service import rerank_document


async def reciprocal_rank_fusion(query,keyword_docs, dense_result, k=60, top_k=5):
    """
    Combines sparse keyword results (BM25) and dense semantic results (Pinecone)
    using standard Reciprocal Rank Fusion (RRF).
    """
    scores = {}
    document_map = {}

    normalized_dense = [
        item[0] if isinstance(item, tuple) else item for item in dense_result
    ]

    for results in [keyword_docs, normalized_dense]:
        for rank, doc in enumerate(results, start=1):
            doc_id = f"{doc.metadata.get('source', '')}::{doc.page_content}"

            if doc_id not in scores:
                scores[doc_id] = 0.0
                document_map[doc_id] = doc

            scores[doc_id] += 1.0 / (k + rank)

    ranked_doc_ids = sorted(
        scores.keys(),
        key=lambda doc_id: scores[doc_id],
        reverse=True
    )

    rrf_list = [document_map[doc_id] for doc_id in ranked_doc_ids]

    # Send top candidates through the cross-encoder reranker
    return await rerank_document(query=query, documents=rrf_list[:15], top_k=top_k)


async def get_hybrid_search(query: QueryChat, bm25: BM25Retriever):
    """Executes parallel BM25 keyword search and dense vector search, then fuses ranks."""
    keyword_docs = await bm25.ainvoke(query.query)
    dense_docs = await user_query(query)
    documents = await reciprocal_rank_fusion(
        query=query,
        keyword_docs=keyword_docs,
        dense_result=dense_docs,
        k=60,
        top_k=5
    )
    return documents


async def rag_chat(query: QueryChat, bm25: BM25Retriever):
    documents = await get_hybrid_search(query=query, bm25=bm25)

    if not documents:
        return {'response': "The provided policy documentation does not contain enough information to answer your question accurately."}

    # Format context with structural section breadcrumbs
    context = "\n\n".join(
        f"[{doc.metadata.get('section', 'Policy Section')}]\n{doc.page_content}"
        for doc in documents
    )

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        SystemMessage(
            content=(
                "Relevant information from the policies:\n"
                f"{context}"
            )
        ),
        HumanMessage(
            content=query.query
        )
    ]
    config = {
        "configurable": {
            "thread_id": getattr(query, "session_id", "1") or "1"
        }
    }
    response = await agent.ainvoke({"messages": messages}, config=config)
    last_message = response["messages"][-1]
    clean_text = str(last_message.text) if hasattr(last_message, "text") and last_message.text else str(last_message.content)

    return {'response': clean_text}
