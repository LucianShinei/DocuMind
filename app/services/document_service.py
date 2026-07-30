from pathlib import Path
from fastapi import UploadFile

from datetime import datetime
from app.models.document import Document

from app.database.mongodb import get_documents_collection


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


async def save_document(file: UploadFile):

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:

        contents = await file.read()

        buffer.write(contents)

    document = Document(
        filename=file.filename,
        stored_path=str(file_path),
        content_type=file.content_type,
        size=file.size,
        uploaded_at=datetime.utcnow(),
    )
    collection = get_documents_collection()

    await collection.insert_one(document.model_dump())

    return document

from app.database.mongodb import get_documents_collection


from app.schemas.mappers import document_to_response


async def get_all_documents():

    collection = get_documents_collection()

    documents = await collection.find().to_list(length=None)

    return [document_to_response(doc) for doc in documents]