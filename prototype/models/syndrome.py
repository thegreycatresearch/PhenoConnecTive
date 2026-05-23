from pydantic import BaseModel, Field
from typing import List, Optional


# =====================================================
# BASE SYNDROME MODEL
# =====================================================

class SyndromeModel(BaseModel):

    name: str = Field(
        ...,
        description="Full syndrome name",
        example="Classical Ehlers-Danlos Syndrome"
    )

    abbreviation: str = Field(
        ...,
        description="Short syndrome abbreviation",
        example="cEDS"
    )

    category: str = Field(
        ...,
        description="Clinical syndrome category",
        example="Collagenopathy"
    )

    inheritance: str = Field(
        ...,
        description="Inheritance pattern",
        example="Autosomal Dominant"
    )

    primary_genes: List[str] = Field(
        default_factory=list,
        description="Primary disease-associated genes",
        example=[
            "COL5A1",
            "COL5A2"
        ]
    )

    related_genes: List[str] = Field(
        default_factory=list,
        description="Additional genes associated with phenotype overlap",
        example=[
            "COL1A1"
        ]
    )

    related_hpo_terms: List[str] = Field(
        default_factory=list,
        description="Associated Human Phenotype Ontology terms",
        example=[
            "HP:0001382",
            "HP:0000974",
            "HP:0001065"
        ]
    )

    clinical_severity: str = Field(
        ...,
        description="Overall clinical severity",
        example="Moderate"
    )

    vascular_risk: str = Field(
        ...,
        description="Associated vascular complication risk",
        example="Moderate"
    )


# =====================================================
# EXTENDED SYNDROME MODEL
# =====================================================

class ExtendedSyndromeModel(SyndromeModel):

    description: Optional[str] = Field(
        default=None,
        description="Clinical syndrome description",
        example="Connective tissue disorder associated with skin hyperextensibility and joint hypermobility."
    )

    major_features: Optional[List[str]] = Field(
        default=None,
        description="Major diagnostic clinical features",
        example=[
            "Skin hyperextensibility",
            "Atrophic scarring",
            "Joint hypermobility"
        ]
    )

    minor_features: Optional[List[str]] = Field(
        default=None,
        description="Minor clinical manifestations",
        example=[
            "Easy bruising",
            "Joint instability"
        ]
    )

    body_systems: Optional[List[str]] = Field(
        default=None,
        description="Affected organ systems",
        example=[
            "skin",
            "musculoskeletal"
        ]
    )

    diagnostic_weight: Optional[int] = Field(
        default=None,
        description="Relative diagnostic importance",
        example=10
    )

    phenotype_match_priority: Optional[str] = Field(
        default=None,
        description="Priority level during phenotype matching",
        example="Very High"
    )

    gene_confidence: Optional[str] = Field(
        default=None,
        description="Confidence of genotype-phenotype association",
        example="Critical"
    )

    orphanet: Optional[str] = Field(
        default=None,
        description="Orphanet identifier",
        example="ORPHA:287"
    )

    omim: Optional[str] = Field(
        default=None,
        description="OMIM identifier",
        example="130000"
    )

    prevalence: Optional[str] = Field(
        default=None,
        description="Estimated prevalence",
        example="Rare"
    )

    age_of_onset: Optional[str] = Field(
        default=None,
        description="Typical age of symptom onset",
        example="Childhood"
    )

    prognosis: Optional[str] = Field(
        default=None,
        description="General prognosis",
        example="Variable depending on severity and complications"
    )

    management_recommendations: Optional[List[str]] = Field(
        default=None,
        description="General clinical management recommendations",
        example=[
            "Cardiovascular monitoring",
            "Physical therapy",
            "Pain management"
        ]
    )

    differential_diagnoses: Optional[List[str]] = Field(
        default=None,
        description="Common differential diagnoses",
        example=[
            "Marfan syndrome",
            "Loeys-Dietz syndrome",
            "Hypermobility spectrum disorder"
        ]
    )

    clinical_notes: Optional[str] = Field(
        default=None,
        description="Additional syndrome notes",
        example="Phenotypic severity may vary considerably among patients."
    )


# =====================================================
# SYNDROME MATCH MODEL
# =====================================================

class SyndromeMatchModel(BaseModel):

    syndrome_key: str = Field(
        ...,
        description="Internal syndrome key",
        example="ceds"
    )

    syndrome_name: str = Field(
        ...,
        description="Full syndrome name",
        example="Classical Ehlers-Danlos Syndrome"
    )

    abbreviation: str = Field(
        ...,
        description="Syndrome abbreviation",
        example="cEDS"
    )

    score_percent: float = Field(
        ...,
        description="Phenotype overlap percentage",
        example=92.5
    )

    weighted_score: int = Field(
        ...,
        description="Weighted phenotype score",
        example=38
    )

    total_matches: int = Field(
        ...,
        description="Number of matched phenotypes",
        example=7
    )

    clinical_severity: str = Field(
        ...,
        description="Clinical severity classification",
        example="Moderate"
    )

    vascular_risk: str = Field(
        ...,
        description="Associated vascular risk level",
        example="Moderate"
    )

    inheritance: str = Field(
        ...,
        description="Inheritance pattern",
        example="Autosomal Dominant"
    )

    primary_genes: List[str] = Field(
        default_factory=list,
        description="Genes associated with the syndrome",
        example=[
            "COL5A1",
            "COL5A2"
        ]
    )


# =====================================================
# SYNDROME SEARCH REQUEST
# =====================================================

class SyndromeSearchRequest(BaseModel):

    query: str = Field(
        ...,
        description="Syndrome name or abbreviation",
        example="Ehlers-Danlos"
    )

    inheritance_filter: Optional[str] = Field(
        default=None,
        description="Filter by inheritance pattern",
        example="Autosomal Dominant"
    )

    vascular_risk_filter: Optional[str] = Field(
        default=None,
        description="Filter by vascular risk",
        example="Critical"
    )


# =====================================================
# SYNDROME SEARCH RESPONSE
# =====================================================

class SyndromeSearchResponse(BaseModel):

    total_results: int = Field(
        ...,
        description="Total number of syndromes found",
        example=3
    )

    results: List[ExtendedSyndromeModel]
