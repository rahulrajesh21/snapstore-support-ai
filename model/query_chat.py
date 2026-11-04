from typing import Optional
from pydantic import BaseModel


class QueryChat(BaseModel):
    query: str
    session_id: Optional[str] = "1"

