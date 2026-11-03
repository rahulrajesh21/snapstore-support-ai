from agent.graph import agent
from model.query_chat import QueryChat
from services.retrieval_service import user_query
from langchain_core.messages import SystemMessage, HumanMessage
from agent.prompt import SYSTEM_PROMPT


async def rag_chat(query:QueryChat):
    documents = await user_query(query)

    context = "\n\n".join(
        doc.page_content for doc in documents
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
    config = {"configurable":{
        "thread_id":"1"
    }}
    response = await agent.ainvoke({"messages":messages},config=config)
    last_message = response["messages"][-1]
    clean_text = str(last_message.text) if hasattr(last_message, "text") and last_message.text else str(last_message.content)

    return {'response':clean_text}
