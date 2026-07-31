from datetime import datetime
from pydantic import BaseModel, Field


class DocumentChunk(BaseModel):
    document_id: str
    owner_id: str
    chunk_index: int
    text: str
    embedding: list[float] = Field(default_factory=list)
    created_at: datetime