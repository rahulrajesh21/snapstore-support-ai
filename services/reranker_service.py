import os
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from model.query_chat import QueryChat
from langchain_core.documents import Document

_tokenizer = None
_model = None
_device = None


def get_reranker():
    """
    Lazy-loads the cross-encoder reranker model and tokenizer on the first call,
    caching them in memory and leveraging Apple Silicon (MPS) if available.
    """
    global _tokenizer, _model, _device

    if _model is None:
        if torch.backends.mps.is_available():
            _device = torch.device("mps")
        elif torch.cuda.is_available():
            _device = torch.device("cuda")
        else:
            _device = torch.device("cpu")

        model_name = os.getenv("RERANKER_MODEL", "BAAI/bge-reranker-v2-m3")
        print(f"Loading reranker model '{model_name}' on device '{_device}'...")

        _tokenizer = AutoTokenizer.from_pretrained(model_name)
        _model = AutoModelForSequenceClassification.from_pretrained(model_name).to(_device)
        _model.eval()
        print(f"Reranker '{model_name}' loaded successfully.")

    return _tokenizer, _model, _device


async def rerank_document(
    query: QueryChat,
    documents: list[Document],
    top_k: int = 5
) -> list[Document]:
    """
    Scores and re-ranks retrieved candidate documents using a cross-encoder model.
    """
    if not documents:
        return []

    tokenizer, model, device = get_reranker()
    query_text = query.query if hasattr(query, "query") else str(query)

    pairs = [[query_text, doc.page_content] for doc in documents]

    inputs = tokenizer(
        pairs,
        padding=True,
        truncation=True,
        return_tensors="pt",
        max_length=1024
    )

    # Move tensors to active device (MPS/CUDA/CPU)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.inference_mode():
        outputs = model(**inputs)
        scores = outputs.logits.view(-1).float().cpu()

    ranked_documents = sorted(
        zip(documents, scores.tolist()),
        key=lambda item: item[1],
        reverse=True
    )

    return [doc for doc, score in ranked_documents[:top_k]]
