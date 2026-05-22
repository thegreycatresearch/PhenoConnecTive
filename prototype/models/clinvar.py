from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class ClinVarRecord:
    gene: str
    variant: str
    clinical_significance: str
    review_status: Optional[str] = None
    accession: Optional[str] = None
    summary: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class VariantMatchResult:
    patient_variant: str
    gene: str
    matched_record: Optional[ClinVarRecord]
    interpretation: str
    score: int
    explanation: str
