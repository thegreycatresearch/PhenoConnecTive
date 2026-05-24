from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class ClinicalNoteRequest(BaseModel):
    clinical_note: str


@router.post("/parse-clinical-note")
def parse_clinical_note(request: ClinicalNoteRequest):
    return {
        "input": request.clinical_note,
        "status": "ok"
    }
