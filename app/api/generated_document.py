from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.document_service import (
    get_documents_by_agent,
    get_document_by_id
)
from app.schemas.generated_document import GeneratedDocumentResponse

router = APIRouter(prefix="/documents", tags=["Generated Documents"])

# Get Documents by Agent
@router.get("/agent/{agent_id}", response_model=list[GeneratedDocumentResponse])
def read_documents_by_agent(agent_id: int, db: Session = Depends(SessionLocal)):

    documents = get_documents_by_agent(db, agent_id)

    if not documents:
        raise HTTPException(status_code=404, detail="No documents found for this agent")

    return documents

# Get Single Document
@router.get("/{document_id}", response_model=GeneratedDocumentResponse)
def read_document(document_id: int, db: Session = Depends(SessionLocal)):

    document = get_document_by_id(db, document_id)

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return document