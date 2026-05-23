```python
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from pathlib import Path

from datetime import datetime

from typing import Optional

import json


# =====================================================
# IMPORT ENGINE
# =====================================================

from engine.matcher import PhenotypeMatcher


# =====================================================
# IMPORT MODELS
# =====================================================

from models.patient import (
    PatientPhenotypeRequest,
    PatientAnalysisRequest,
    PatientAnalysisSummary
)

from models.analysis import (
    FullAnalysisResponse,
    BestMatchResponse
)

from models.phenotype import (
    PhenotypeSearchResponse
)

from models.syndrome import (
    SyndromeSearchResponse
)


# =====================================================
# FASTAPI CONFIG
# =====================================================

app = FastAPI(

    title="PhenoConnecTive API",

    description="""
AI-assisted bioinformatics platform for:

- phenotype analysis
- connective tissue disorders
- rare disease prioritization
- syndrome matching
- genotype-phenotype interpretation
- HPO ontology analysis
- Ehlers-Danlos syndrome research
- Marfan / Loeys-Dietz differential analysis

Built for:
- clinicians
- researchers
- bioinformatics projects
- rare disease startups
- AI-assisted diagnostics
""",

    version="1.0.0",

    contact={

        "name": "PhenoConnecTive Research",

        "url": "https://github.com/thegreycatresearch/PhenoConnecTive"
    },

    license_info={

        "name": "MIT License"
    }
)


# =====================================================
# CORS
# =====================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =====================================================
# PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"


# =====================================================
# JSON LOADER
# =====================================================

def load_json(filename):

    file_path = DATA_DIR / filename

    if not file_path.exists():

        raise HTTPException(

            status_code=404,

            detail=f"{filename} not found"
        )

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# =====================================================
# ROOT
# =====================================================

@app.get(
    "/",
    tags=["System"]
)

def root():

    return {

        "project": "PhenoConnecTive",

        "description": "AI-assisted phenotype-genotype analysis platform",

        "version": "1.0.0",

        "status": "online",

        "documentation": "/docs",

        "timestamp": datetime.utcnow().isoformat()
    }


# =====================================================
# HEALTH
# =====================================================

@app.get(
    "/health",
    tags=["System"]
)

def health():

    return {

        "status": "healthy",

        "api": "PhenoConnecTive",

        "engine": "Phenotype Scoring Engine",

        "version": "1.0.0",

        "timestamp": datetime.utcnow().isoformat()
    }


# =====================================================
# API INFO
# =====================================================

@app.get(
    "/info",
    tags=["System"]
)

def api_info():

    return {

        "name": "PhenoConnecTive",

        "version": "1.0.0",

        "modules": [

            "Phenotype Matching",
            "Syndrome Prioritization",
            "Gene Association",
            "Rare Disease Analysis",
            "Connective Tissue Disorders"
        ],

        "supported_disorders": [

            "Ehlers-Danlos Syndrome",
            "Marfan Syndrome",
            "Loeys-Dietz Syndrome",
            "Osteogenesis Imperfecta",
            "Stickler Syndrome"
        ]
    }


# =====================================================
# GET ALL SYNDROMES
# =====================================================

@app.get(
    "/syndromes",
    tags=["Syndromes"]
)

def get_syndromes():

    return load_json(
        "syndromes.json"
    )


# =====================================================
# GET SINGLE SYNDROME
# =====================================================

@app.get(
    "/syndromes/{syndrome_key}",
    tags=["Syndromes"]
)

def get_single_syndrome(
    syndrome_key: str
):

    syndromes = load_json(
        "syndromes.json"
    )

    syndrome = syndromes.get(
        syndrome_key.lower()
    )

    if not syndrome:

        raise HTTPException(

            status_code=404,

            detail="Syndrome not found"
        )

    return syndrome


# =====================================================
# SEARCH SYNDROMES
# =====================================================

@app.get(
    "/search/syndromes",
    response_model=SyndromeSearchResponse,
    tags=["Search"]
)

def search_syndromes(

    query: str = Query(...)

):

    syndromes = load_json(
        "syndromes.json"
    )

    results = []

    for key, syndrome in syndromes.items():

        name = syndrome.get(
            "name",
            ""
        )

        abbreviation = syndrome.get(
            "abbreviation",
            ""
        )

        if (

            query.lower() in name.lower()

            or

            query.lower() in abbreviation.lower()
        ):

            results.append(
                syndrome
            )

    return {

        "total_results": len(results),

        "results": results
    }


# =====================================================
# GET ALL GENES
# =====================================================

@app.get(
    "/genes",
    tags=["Genes"]
)

def get_genes():

    return load_json(
        "genes.json"
    )


# =====================================================
# GET SINGLE GENE
# =====================================================

@app.get(
    "/genes/{gene_name}",
    tags=["Genes"]
)

def get_single_gene(
    gene_name: str
):

    genes = load_json(
        "genes.json"
    )

    gene = genes.get(
        gene_name.upper()
    )

    if not gene:

        raise HTTPException(

            status_code=404,

            detail="Gene not found"
        )

    return gene


# =====================================================
# GET ALL PHENOTYPES
# =====================================================

@app.get(
    "/phenotypes",
    tags=["Phenotypes"]
)

def get_phenotypes():

    return load_json(
        "phenotypes.json"
    )


# =====================================================
# GET SINGLE PHENOTYPE
# =====================================================

@app.get(
    "/phenotypes/{hpo_id}",
    tags=["Phenotypes"]
)

def get_single_phenotype(
    hpo_id: str
):

    phenotypes = load_json(
        "phenotypes.json"
    )

    phenotype = phenotypes.get(
        hpo_id
    )

    if not phenotype:

        raise HTTPException(

            status_code=404,

            detail="Phenotype not found"
        )

    return phenotype


# =====================================================
# SEARCH PHENOTYPES
# =====================================================

@app.get(
    "/search/phenotypes",
    response_model=PhenotypeSearchResponse,
    tags=["Search"]
)

def search_phenotypes(

    query: str = Query(...)

):

    phenotypes = load_json(
        "phenotypes.json"
    )

    results = []

    for hpo_id, phenotype in phenotypes.items():

        phenotype_name = phenotype.get(
            "name",
            ""
        )

        synonyms = phenotype.get(
            "synonyms",
            []
        )

        if query.lower() in phenotype_name.lower():

            phenotype["hpo_id"] = hpo_id

            results.append(
                phenotype
            )

            continue

        for synonym in synonyms:

            if query.lower() in synonym.lower():

                phenotype["hpo_id"] = hpo_id

                results.append(
                    phenotype
                )

                break

    return {

        "total_results": len(results),

        "results": results
    }


# =====================================================
# ANALYZE PATIENT
# =====================================================

@app.post(
    "/analyze_patient",
    response_model=FullAnalysisResponse,
    tags=["Analysis"]
)

def analyze_patient(

    request: PatientAnalysisRequest
):

    matcher = PhenotypeMatcher()

    analysis = matcher.match(
        request.phenotypes
    )

    return {

        "patient_id": request.patient_id,

        "input_phenotypes": request.phenotypes,

        "valid_phenotypes": analysis[
            "valid_phenotypes"
        ],

        "invalid_phenotypes": analysis[
            "invalid_phenotypes"
        ],

        "total_valid_phenotypes": len(
            analysis["valid_phenotypes"]
        ),

        "total_invalid_phenotypes": len(
            analysis["invalid_phenotypes"]
        ),

        "analysis_version": "1.0.0",

        "generated_at": datetime.utcnow().isoformat(),

        "results": analysis["results"]
    }


# =====================================================
# BEST MATCH
# =====================================================

@app.post(
    "/best_match",
    response_model=BestMatchResponse,
    tags=["Analysis"]
)

def best_match(

    request: PatientPhenotypeRequest
):

    matcher = PhenotypeMatcher()

    matcher.match(
        request.phenotypes
    )

    best = matcher.get_best_match()

    if not best:

        raise HTTPException(

            status_code=404,

            detail="No matches found"
        )

    confidence = "Low"

    if best["score_percent"] >= 80:

        confidence = "Very High"

    elif best["score_percent"] >= 60:

        confidence = "High"

    elif best["score_percent"] >= 40:

        confidence = "Moderate"

    return {

        "syndrome_name": best[
            "syndrome_name"
        ],

        "abbreviation": best[
            "abbreviation"
        ],

        "score_percent": best[
            "score_percent"
        ],

        "weighted_score": best[
            "weighted_score"
        ],

        "confidence_level": confidence,

        "matched_phenotype_count": best[
            "total_matches"
        ],

        "vascular_risk": best[
            "vascular_risk"
        ],

        "primary_genes": best[
            "primary_genes"
        ]
    }


# =====================================================
# ANALYSIS SUMMARY
# =====================================================

@app.post(
    "/analysis_summary",
    response_model=PatientAnalysisSummary,
    tags=["Analysis"]
)

def analysis_summary(

    request: PatientAnalysisRequest
):

    matcher = PhenotypeMatcher()

    matcher.match(
        request.phenotypes
    )

    best = matcher.get_best_match()

    return {

        "patient_id": request.patient_id,

        "total_phenotypes": len(
            request.phenotypes
        ),

        "total_candidate_syndromes": len(
            matcher.analysis_result["results"]
        ),

        "best_match": best[
            "syndrome_name"
        ],

        "best_match_score": best[
            "score_percent"
        ],

        "weighted_score": best[
            "weighted_score"
        ],

        "clinical_severity": best[
            "clinical_severity"
        ],

        "vascular_risk": best[
            "vascular_risk"
        ]
    }
```
