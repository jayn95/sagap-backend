from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.db.session import SessionLocal
from app.schemas.report import FATRItem, DesktopAssignmentItem
from app.services import report_service
from fastapi.responses import StreamingResponse
from app.utils import excel, pdf
from io import BytesIO

router = APIRouter(prefix="/reports", tags=["Reports"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -----------------------------
# API Endpoints
# -----------------------------

@router.get("/fatr", response_model=List[FATRItem])
def get_fatr_report(db: Session = Depends(get_db)):
    """
    Retrieves FATR report data.
    Delegates logic to report_service.
    """
    return report_service.generate_fatr_report(db)


@router.get("/desktop-assignment", response_model=List[DesktopAssignmentItem])
def get_desktop_assignment_report(db: Session = Depends(get_db)):
    """
    Retrieves Desktop Assignment Form data.
    Delegates logic to report_service.
    """
    return report_service.generate_desktop_assignment_form(db)

@router.get("/fatr/excel")
def get_fatr_excel(db: Session = Depends(get_db)):
    data = report_service.generate_fatr_report(db)
    file_bytes = excel.generate_excel(data, sheet_name="FATR Report")
    return StreamingResponse(BytesIO(file_bytes), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=fatr_report.xlsx"})

@router.get("/fatr/pdf")
def get_fatr_pdf(db: Session = Depends(get_db)):
    data = report_service.generate_fatr_report(db)
    file_bytes = pdf.generate_pdf(data, title="FATR Report")
    return StreamingResponse(BytesIO(file_bytes), media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=fatr_report.pdf"})