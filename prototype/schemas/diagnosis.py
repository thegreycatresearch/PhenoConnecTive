from __future__ import annotations

from pydantic import BaseModel
from typing import List, Optional


class DiagnosticRequest(BaseModel):
    phenotypes: List[dict] = []
    variants: List[dict] = []
    inheritance: Optional[str] = None


class DiagnosticResult(BaseModel):
    syndrome: str
    score: int
    compatibility: float
