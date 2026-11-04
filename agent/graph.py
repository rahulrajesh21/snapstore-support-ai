from langchain.chat_models import init_chat_model
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent


model = init_chat_model(
    model='google_genai:gemini-3.5-flash-lite',
)

checkpoint = InMemorySaver()

agent = create_agent(
    model=model,
    tools=[],
    checkpointer=checkpoint
)

embedding_model = GoogleGenerativeAIEmbeddings(
    model='gemini-embedding-001',
    output_dimensionality=1536,
) 
