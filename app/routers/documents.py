from fastapi import APIRouter, UploadFile, File
from app.models import document
from app.services.document_service import get_all_documents, save_document
from typing import List
from app.schemas.document import DocumentResponse


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.get("/", response_model=List[DocumentResponse])
async def list_documents():
    return await get_all_documents()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    saved_path = await save_document(file)

    document = await save_document(file)

    return document