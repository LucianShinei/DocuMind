from datetime import datetime, timezone

from app.database.mongodb import get_chunks_collection
from app.models.chunk import DocumentChunk


CHUNK_SIZE = 800


async def create_chunks(
    document_id: str,
    owner_id: str,
    text: str,
):
    collection = get_chunks_collection()

    chunks = []

    for i in range(0, len(text), CHUNK_SIZE):

        chunk_text = text[i:i + CHUNK_SIZE]

        chunk = DocumentChunk(
            document_id=document_id,
            owner_id=owner_id,
            chunk_index=len(chunks),
            text=chunk_text,
            created_at=datetime.now(timezone.utc),
        )

        chunks.append(chunk.model_dump())

    if chunks:
        await collection.insert_many(chunks)