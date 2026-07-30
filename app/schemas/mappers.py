from app.schemas.document import DocumentResponse


def document_to_response(document: dict) -> DocumentResponse:
    return DocumentResponse(
        id=str(document["_id"]),
        filename=document["filename"],
        stored_path=document["stored_path"],
        content_type=document["content_type"],
        size=document["size"],
        uploaded_at=document["uploaded_at"],
    )