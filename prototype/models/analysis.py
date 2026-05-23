```python id="t0u8mr"
from pydantic import BaseModel, Field
from typing import List, Optional


# =====================================================
# MATCHED PHENOTYPE MODEL
# =====================================================

class MatchedPhenotypeModel(BaseModel):

    hpo_id: str = Field(
        ...,
        description="Matched Human Phenotype Ontology ID",
        example="HP:0001382"
    )

    name: str = Field(
        ...,
        description="Phenotype name",
        example="Joint hypermobility"
    )

    category: str = Field(
        ...,
        description="Phenotype category",
        example="musculoskeletal"
    )

    weight: int = Field(
        ...,
        description="Phenotype scoring weight",
        example=10
    )


# =====================================================
# ANALYSIS RESULT MODEL
# =====================================================

class AnalysisResultModel(BaseModel):

    syndrome_key: str = Field(
        ...,
        description="Internal syndrome identifier",
        example="heds"
    )

    syndrome_name: str = Field(
        ...,
        description="Full syndrome name",
        example="Hypermobile Ehlers-Danlos Syndrome"
    )

    abbreviation: str = Field(
        ...,
        description="Syndrome abbreviation",
        example="hEDS"
    )

    score_percent: float = Field(
        ...,
        description="Phenotype overlap percentage",
        example=87.5
    )

    weighted_score: int = Field(
        ...,
        description="Weighted phenotype score",
        example=42
    )

    total_matches: int = Field(
        ...,
        description="Total matched phenotypes",
        example=8
    )

    inheritance: str = Field(
        ...,
        description="Inheritance pattern",
        example="Autosomal Dominant"
    )

    clinical_severity: str = Field(
        ...,
        description="Clinical severity level",
        example="Moderate to Severe"
    )

    vascular_risk: str = Field(
        ...,
        description="Associated vascular complication risk",
        example="Low"
    )

    primary_genes: List[str] = Field(
        default_factory=list,
        description="Main associated genes",
        example=[
            "TNXB",
            "COL5A1"
        ]
    )

    matched_phenotypes: List[
        MatchedPhenotypeModel
    ] = Field(
        default_factory=list,
        description="Matched phenotype list"
    )


# =====================================================
# COMPLETE ANALYSIS RESPONSE
# =====================================================

class FullAnalysisResponse(BaseModel):

    patient_id: Optional[str] = Field(
        default=None,
        description="Patient identifier",
        example="PATIENT_001"
    )

    input_phenotypes: List[str] = Field(
        ...,
        description="Submitted phenotype list",
        example=[
            "HP:0001382",
            "HP:0000974"
        ]
    )

    valid_phenotypes: List[str] = Field(
        default_factory=list,
        description="Validated HPO terms"
    )

    invalid_phenotypes: List[str] = Field(
        default_factory=list,
        description="Invalid or unknown HPO terms"
    )

    total_valid_phenotypes: int = Field(
        ...,
        description="Total number of valid phenotypes",
        example=4
    )

    total_invalid_phenotypes: int = Field(
        ...,
        description="Total number of invalid phenotypes",
        example=1
    )

    analysis_version: str = Field(
        ...,
        description="Analysis engine version",
        example="1.0.0"
    )

    generated_at: str = Field(
        ...,
        description="ISO timestamp of analysis generation",
        example="2026-05-23T18:22:00Z"
    )

    results: List[
        AnalysisResultModel
    ] = Field(
        default_factory=list,
        description="Ranked syndrome matches"
    )


# =====================================================
# BEST MATCH RESPONSE
# =====================================================

class BestMatchResponse(BaseModel):

    syndrome_name: str = Field(
        ...,
        description="Best matched syndrome",
        example="Classical Ehlers-Danlos Syndrome"
    )

    abbreviation: str = Field(
        ...,
        description="Short syndrome abbreviation",
        example="cEDS"
    )

    score_percent: float = Field(
        ...,
        description="Overall phenotype overlap score",
        example=94.2
    )

    weighted_score: int = Field(
        ...,
        description="Weighted phenotype score",
        example=51
    )

    confidence_level: str = Field(
        ...,
        description="Interpretive confidence level",
        example="High"
    )

    matched_phenotype_count: int = Field(
        ...,
        description="Total matched phenotypes",
        example=9
    )

    vascular_risk: str = Field(
        ...,
        description="Clinical vascular risk",
        example="Moderate"
    )

    primary_genes: List[str] = Field(
        default_factory=list,
        description="Most relevant associated genes"
    )


# =====================================================
# ANALYSIS SUMMARY MODEL
# =====================================================

class AnalysisSummaryModel(BaseModel):

    total_syndromes_analyzed: int = Field(
        ...,
        description="Total syndromes analyzed",
        example=12
    )

    top_match: str = Field(
        ...,
        description="Top ranked syndrome",
        example="hEDS"
    )

    top_match_score: float = Field(
        ...,
        description="Highest match score",
        example=89.4
    )

    total_patient_phenotypes: int = Field(
        ...,
        description="Phenotypes submitted",
        example=7
    )

    total_matches_found: int = Field(
        ...,
        description="Syndromes with meaningful overlap",
        example=5
    )

    engine_name: str = Field(
        ...,
        description="Analysis engine name",
        example="PhenoConnecTive Scoring Engine"
    )

    engine_version: str = Field(
        ...,
        description="Current engine version",
        example="1.0.0"
    )
```
