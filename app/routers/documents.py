from fastapi import APIRouter, UploadFile, File, Depends
from typing import List

from app.auth.dependencies import get_current_user
from app.schemas.document import DocumentResponse
from app.services.document_service import (
    save_document,
    get_all_documents,
    get_document_by_id,
    delete_document_by_id,
    download_document_by_id,
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.get("/", response_model=List[DocumentResponse])
async def list_documents(
    skip: int = 0,
    limit: int = 10,
    search: str = "",
    user: dict = Depends(get_current_user),
):
    return await get_all_documents(skip, limit, search, user)


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    user: dict = Depends(get_current_user),
):
    return await save_document(file, user)


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    user: dict = Depends(get_current_user),
):
    return await get_document_by_id(document_id, user)


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    user: dict = Depends(get_current_user),
):
    return await delete_document_by_id(document_id, user)


@router.get("/{document_id}/download")
async def download_document(
    document_id: str,
    user: dict = Depends(get_current_user),
):
    return await download_document_by_id(document_id, user)