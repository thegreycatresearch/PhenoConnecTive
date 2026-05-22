from __future__ import annotations

from pydantic import BaseModel
from typing import List, Optional


class PhenotypeInput(BaseModel):
    name: str
    hpo: Optional[str] = None


class VariantInput(BaseModel):
    gene: str
    variant: str
    classification: Optional[str] = None


class PatientInput(BaseModel):
    phenotypes: List[PhenotypeInput] = []
    variants: List[VariantInput] = []
    inheritance: Optional[str] = None


class PatientResponse(BaseModel):
    phenotypes: List[PhenotypeInput]
    variants: List[VariantInput]
    inheritance: Optional[str] = None
