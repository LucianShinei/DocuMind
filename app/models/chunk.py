from pydantic import BaseModel
from datetime import datetime


class DocumentChunk(BaseModel):
    document_id: str
    owner_id: str
    chunk_index: int
    text: str
    created_at: datetime