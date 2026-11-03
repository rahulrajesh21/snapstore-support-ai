from pydantic import BaseModel


class QueryChat(BaseModel):
    query:str
