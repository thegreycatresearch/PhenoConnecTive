from pydantic import BaseModel, Field
from typing import List, Optional


# =====================================================
# BASE PHENOTYPE MODEL
# =====================================================

class PhenotypeModel(BaseModel):

    hpo_id: str = Field(
        ...,
        description="Human Phenotype Ontology identifier",
        example="HP:0001382"
    )

    name: str = Field(
        ...,
        description="Phenotype name",
        example="Joint hypermobility"
    )

    category: str = Field(
        ...,
        description="Clinical phenotype category",
        example="musculoskeletal"
    )

    weight_default: int = Field(
        ...,
        description="Default importance weight for phenotype scoring",
        example=10
    )

    severity: str = Field(
        ...,
        description="Clinical severity classification",
        example="core"
    )

    related_disorders: List[str] = Field(
        default_factory=list,
        description="Associated syndromes or disorders",
        example=[
            "hEDS",
            "cEDS",
            "Marfan syndrome"
        ]
    )

    synonyms: List[str] = Field(
        default_factory=list,
        description="Alternative phenotype names",
        example=[
            "generalized hypermobility",
            "hypermobile joints"
        ]
    )


# =====================================================
# EXTENDED PHENOTYPE MODEL
# =====================================================

class ExtendedPhenotypeModel(PhenotypeModel):

    body_systems: Optional[List[str]] = Field(
        default=None,
        description="Affected body systems",
        example=[
            "musculoskeletal",
            "connective tissue"
        ]
    )

    associated_genes: Optional[List[str]] = Field(
        default=None,
        description="Genes commonly associated with this phenotype",
        example=[
            "COL5A1",
            "TNXB",
            "FBN1"
        ]
    )

    inheritance_patterns: Optional[List[str]] = Field(
        default=None,
        description="Inheritance patterns associated with phenotype",
        example=[
            "Autosomal Dominant",
            "Autosomal Recessive"
        ]
    )

    onset_age_group: Optional[str] = Field(
        default=None,
        description="Typical onset age group",
        example="Childhood"
    )

    frequency: Optional[str] = Field(
        default=None,
        description="Phenotype frequency among affected individuals",
        example="Common"
    )

    diagnostic_relevance: Optional[str] = Field(
        default=None,
        description="Importance in diagnostic interpretation",
        example="Highly specific"
    )

    clinical_notes: Optional[str] = Field(
        default=None,
        description="Additional phenotype interpretation notes",
        example="Often associated with recurrent subluxations and chronic pain."
    )


# =====================================================
# PHENOTYPE MATCH MODEL
# =====================================================

class PhenotypeMatchModel(BaseModel):

    hpo_id: str = Field(
        ...,
        description="Matched HPO identifier",
        example="HP:0001382"
    )

    phenotype_name: str = Field(
        ...,
        description="Matched phenotype name",
        example="Joint hypermobility"
    )

    weight: int = Field(
        ...,
        description="Phenotype contribution score",
        example=10
    )

    category: str = Field(
        ...,
        description="Phenotype category",
        example="musculoskeletal"
    )

    matched: bool = Field(
        ...,
        description="Whether the phenotype matched the syndrome",
        example=True
    )


# =====================================================
# PHENOTYPE SEARCH REQUEST
# =====================================================

class PhenotypeSearchRequest(BaseModel):

    query: str = Field(
        ...,
        description="Phenotype name, synonym, or HPO ID",
        example="joint hypermobility"
    )

    category_filter: Optional[str] = Field(
        default=None,
        description="Optional category filter",
        example="musculoskeletal"
    )

    severity_filter: Optional[str] = Field(
        default=None,
        description="Optional severity filter",
        example="core"
    )


# =====================================================
# PHENOTYPE SEARCH RESPONSE
# =====================================================

class PhenotypeSearchResponse(BaseModel):

    total_results: int = Field(
        ...,
        description="Number of phenotypes found",
        example=4
    )

    results: List[PhenotypeModel]
