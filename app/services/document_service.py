from pathlib import Path
from fastapi import UploadFile

from datetime import datetime, timezone
from app.models.document import Document

from app.database.mongodb import get_documents_collection
from bson import ObjectId
from fastapi import HTTPException
from fastapi.responses import FileResponse

from app.schemas.mappers import document_to_response

from datetime import datetime

from app.auth.auth import create_access_token
from app.auth.security import hash_password, verify_password
from app.database.mongodb import get_database
from app.models.user import User

from app.services.pdf_service import extract_text

from app.services.chunk_service import create_chunks


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


async def save_document(file: UploadFile, user: dict):
    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:

        contents = await file.read()

        buffer.write(contents)
        text = ""
    if file.content_type == "application/pdf":
        text = await extract_text(str(file_path))
    

    document = Document(
    filename=file.filename,
    stored_path=str(file_path),
    content_type=file.content_type,
    size=file.size,
    owner_id=user["sub"],
    text=text,
    uploaded_at=datetime.now(timezone.utc),
)
    collection = get_documents_collection()

    result = await collection.insert_one(
    document.model_dump()
)
    await create_chunks(
    str(result.inserted_id),
    user["sub"],
    text,
)

    return document

from app.database.mongodb import get_documents_collection


from app.schemas.mappers import document_to_response


async def get_all_documents(
    skip=0,
    limit=10,
    search="",
    user=None,
):
    collection = get_documents_collection()

    query = {
    "owner_id": user["sub"]
}

    if search:
        query["filename"] = {
            "$regex": search,
            "$options": "i",
        }

    documents = (
        await collection.find(query)
        .skip(skip)
        .limit(limit)
        .to_list(length=limit)
    )

    return [document_to_response(doc) for doc in documents]

async def get_document_by_id(
    document_id: str,
    user: dict,
):
    collection = get_documents_collection()

    document = await collection.find_one({"_id": ObjectId(document_id), "owner_id": user["sub"]})

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return document_to_response(document)


async def delete_document_by_id(
    document_id: str,
    user: dict,
):
    collection = get_documents_collection()

    document = await collection.find_one(
        {
            "_id": ObjectId(document_id),
            "owner_id": user["sub"],
        }
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    Path(document["stored_path"]).unlink(missing_ok=True)

    await collection.delete_one(
        {
            "_id": ObjectId(document_id),
            "owner_id": user["sub"],
        }
    )

    return {"message": "Document deleted successfully"}

async def download_document_by_id(
    document_id: str,
    user: dict,
):
    collection = get_documents_collection()

    document = await collection.find_one(
        {
            "_id": ObjectId(document_id),
            "owner_id": user["sub"],
        }
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    return FileResponse(
        path=document["stored_path"],
        filename=document["filename"],
        media_type=document["content_type"],
    )