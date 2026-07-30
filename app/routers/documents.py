from fastapi import APIRouter, UploadFile, File
from app.models import document
from typing import List
from app.schemas.document import DocumentResponse
from app.services.document_service import (
    save_document,
    get_all_documents,
    get_document_by_id,
    delete_document,
    download_document,
)


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.get("/", response_model=List[DocumentResponse])
async def list_documents():
    return await get_all_documents()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    document = await save_document(file)
    return document

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str):
    return await get_document_by_id(document_id)


@router.delete("/{document_id}")
async def remove_document(document_id: str):
    return await delete_document(document_id)


@router.get("/{document_id}/download")
async def download(document_id: str):
    return await download_document(document_id)