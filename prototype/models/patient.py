```python id="kuyoqv"
from pydantic import BaseModel, Field
from typing import List, Optional


# =====================================================
# BASIC PHENOTYPE REQUEST
# =====================================================

class PatientPhenotypeRequest(BaseModel):

    phenotypes: List[str] = Field(
        ...,
        description="List of HPO phenotype IDs",
        example=[
            "HP:0001382",
            "HP:0000974",
            "HP:0001065"
        ]
    )


# =====================================================
# FULL PATIENT ANALYSIS REQUEST
# =====================================================

class PatientAnalysisRequest(BaseModel):

    patient_id: Optional[str] = Field(
        default=None,
        description="Internal patient identifier",
        example="PATIENT_001"
    )

    phenotypes: List[str] = Field(
        ...,
        description="List of HPO phenotype terms associated with the patient",
        example=[
            "HP:0001382",
            "HP:0000974",
            "HP:0001065",
            "HP:0000978"
        ]
    )

    suspected_syndromes: Optional[List[str]] = Field(
        default=None,
        description="Optional list of clinically suspected syndromes",
        example=[
            "cEDS",
            "hEDS"
        ]
    )

    genes_identified: Optional[List[str]] = Field(
        default=None,
        description="Genes identified in sequencing or panel analysis",
        example=[
            "COL5A1",
            "COL5A2"
        ]
    )

    pathogenic_variants: Optional[List[str]] = Field(
        default=None,
        description="Known pathogenic variants identified in the patient",
        example=[
            "COL5A1:c.1502G>A",
            "COL5A2:c.3205del"
        ]
    )

    family_history: Optional[bool] = Field(
        default=None,
        description="Whether there is a positive family history",
        example=True
    )

    inheritance_pattern_observed: Optional[str] = Field(
        default=None,
        description="Observed inheritance pattern in the family",
        example="Autosomal Dominant"
    )

    vascular_complications: Optional[bool] = Field(
        default=None,
        description="Presence of vascular complications",
        example=False
    )

    cardiovascular_findings: Optional[List[str]] = Field(
        default=None,
        description="Cardiovascular manifestations identified",
        example=[
            "Mitral valve prolapse",
            "Aortic root dilation"
        ]
    )

    musculoskeletal_findings: Optional[List[str]] = Field(
        default=None,
        description="Musculoskeletal findings",
        example=[
            "Joint instability",
            "Scoliosis",
            "Chronic pain"
        ]
    )

    skin_findings: Optional[List[str]] = Field(
        default=None,
        description="Dermatological findings",
        example=[
            "Hyperextensible skin",
            "Atrophic scars"
        ]
    )

    neurological_findings: Optional[List[str]] = Field(
        default=None,
        description="Neurological or autonomic manifestations",
        example=[
            "Dysautonomia",
            "Orthostatic intolerance"
        ]
    )

    age: Optional[int] = Field(
        default=None,
        ge=0,
        le=120,
        description="Patient age",
        example=18
    )

    sex: Optional[str] = Field(
        default=None,
        description="Patient biological sex",
        example="Female"
    )

    ethnicity: Optional[str] = Field(
        default=None,
        description="Ethnicity if relevant for population genetics",
        example="Latino"
    )

    country: Optional[str] = Field(
        default=None,
        description="Country of origin",
        example="Argentina"
    )

    clinician_notes: Optional[str] = Field(
        default=None,
        description="Additional clinical notes",
        example="Patient presents generalized joint hypermobility and chronic pain since childhood."
    )


# =====================================================
# RESPONSE MODEL
# =====================================================

class PatientAnalysisSummary(BaseModel):

    patient_id: Optional[str]

    total_phenotypes: int

    total_candidate_syndromes: int

    best_match: str

    best_match_score: float

    weighted_score: int

    clinical_severity: str

    vascular_risk: str
```
