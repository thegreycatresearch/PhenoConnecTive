from __future__ import annotations

from pydantic import BaseModel
from typing import List, Optional


class VariantInput(BaseModel):
    gene: str
    variant: str
    classification: Optional[str] = None


class VariantAnalysisRequest(BaseModel):
    variants: List[VariantInput] = []


class VariantMatchResponse(BaseModel):
    gene: str
    patient_variant: str
    interpretation: str
    score: int
    explanation: str
    accession: Optional[str] = None
    clinical_significance: Optional[str] = None
    review_status: Optional[str] = None
    summary: Optional[str] = None
