from datetime import datetime
from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: str
    filename: str
    stored_path: str
    content_type: str
    size: int
    uploaded_at: datetime