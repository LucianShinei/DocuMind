from pathlib import Path
from fastapi import UploadFile

from datetime import datetime
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


async def get_all_documents(
    skip: int = 0,
    limit: int = 10,
    search: str = "",
):
    collection = get_documents_collection()

    query = {}

    if search:
        query = {"filename": {"$regex": search, "$options": "i"}}

    documents = (
        await collection.find(query)
        .skip(skip)
        .limit(limit)
        .to_list(length=limit)
    )

    return [document_to_response(doc) for doc in documents]

async def get_document_by_id(document_id: str):
    collection = get_documents_collection()

    document = await collection.find_one({"_id": ObjectId(document_id)})

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return document_to_response(document)


async def delete_document(document_id: str):
    collection = get_documents_collection()

    document = await collection.find_one({"_id": ObjectId(document_id)})

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    Path(document["stored_path"]).unlink(missing_ok=True)

    await collection.delete_one({"_id": ObjectId(document_id)})

    return {"message": "Document deleted successfully"}


async def download_document(document_id: str):
    collection = get_documents_collection()

    document = await collection.find_one({"_id": ObjectId(document_id)})

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return FileResponse(
        path=document["stored_path"],
        filename=document["filename"],
        media_type=document["content_type"],
    )


async def register_user(user):
    db = get_database()

    existing = await db.users.find_one({"email": user.email})

    if existing:
        raise ValueError("Email already registered")

    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        created_at=datetime.utcnow(),
    )

    result = await db.users.insert_one(new_user.model_dump())

    return {
        "id": str(result.inserted_id),
        "username": user.username,
        "email": user.email,
    }


async def login_user(user):
    db = get_database()

    existing = await db.users.find_one({"email": user.email})

    if not existing or not verify_password(
        user.password,
        existing["hashed_password"],
    ):
        raise ValueError("Invalid credentials")

    token = create_access_token(
        {
            "sub": str(existing["_id"]),
            "email": existing["email"],
        }
    )

    return {"access_token": token, "token_type": "bearer"}