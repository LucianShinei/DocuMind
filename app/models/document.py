from pydantic import BaseModel
from datetime import datetime


class Document(BaseModel):
    filename: str
    stored_path: str
    content_type: str
    size: int
    uploaded_at: datetime