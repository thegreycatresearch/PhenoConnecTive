from fastapi import FastAPI, HTTPException
from pathlib import Path
import json

app = FastAPI(

    title="PhenoConnecTive API",

    description="""
# PhenoConnecTive

Phenotype-driven bioinformatics platform focused on hereditary connective tissue disorders and rare diseases.

## Main Goals

- Phenotype-first analysis
- Connective tissue disorder interpretation
- Gene + phenotype integration
- Explainable diagnostic support
- Future AI-assisted prioritization

## Current Supported Areas

- Ehlers-Danlos Syndromes
- Marfan Syndrome
- Loeys-Dietz Syndrome
- Osteogenesis Imperfecta
- Stickler Syndrome

## Planned Features

- HPO semantic matching
- Variant prioritization
- ACMG support
- ClinVar integration
- VCF parsing
- AI-assisted phenotype scoring

## Important Disclaimer

This project is experimental and research-oriented.
It is NOT intended for clinical diagnosis or medical decision-making.
""",

    version="0.2.0",

    contact={
        "name": "Kris Stazzone",
        "url": "https://github.com/thegreycatresearch",
    },

    license_info={
        "name": "Research Use Only"
    },

    openapi_tags=[

        {
            "name": "System",
            "description": "General API system endpoints."
        },

        {
            "name": "Genes",
            "description": "Gene database endpoints."
        },

        {
            "name": "Syndromes",
            "description": "Syndrome database endpoints."
        },

        {
            "name": "Search",
            "description": "Search endpoints for genes and syndromes."
        },

        {
            "name": "Project",
            "description": "Project metadata and information."
        }
    ]
)

# =====================================================
# PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

SYNDROMES_FILE = DATA_DIR / "syndromes.json"

GENES_FILE = DATA_DIR / "genes.json"


# =====================================================
# JSON LOADER
# =====================================================

def load_json(file_path):

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except FileNotFoundError:

        raise HTTPException(
            status_code=404,
            detail=f"File not found: {file_path.name}"
        )

    except json.JSONDecodeError:

        raise HTTPException(
            status_code=500,
            detail=f"Invalid JSON format in {file_path.name}"
        )


# =====================================================
# ROOT
# =====================================================

@app.get(

    "/",

    tags=["System"],

    summary="API Root",

    description="""
Returns the API status and basic project information.
""",

    response_description="Basic API status information"
)
def root():

    return {

        "project": "PhenoConnecTive",

        "status": "running",

        "version": "0.2.0",

        "description": "Phenotype-driven connective tissue disorder analysis platform"
    }


# =====================================================
# HEALTH CHECK
# =====================================================

@app.get(

    "/health",

    tags=["System"],

    summary="Health Check",

    description="""
Checks whether the API is online and functioning properly.
""",

    response_description="Health status"
)
def health():

    return {

        "status": "healthy",

        "api": "online"
    }


# =====================================================
# GET ALL SYNDROMES
# =====================================================

@app.get(

    "/syndromes",

    tags=["Syndromes"],

    summary="Retrieve all syndromes",

    description="""
Returns all syndrome entries currently stored in the database.

Includes:
- syndrome names
- inheritance
- associated genes
- phenotype data
- weighted phenotype information
""",

    response_description="Complete syndrome database"
)
def get_syndromes():

    data = load_json(SYNDROMES_FILE)

    return {

        "total_syndromes": len(data),

        "syndromes": data
    }


# =====================================================
# GET SINGLE SYNDROME
# =====================================================

@app.get(

    "/syndromes/{syndrome_name}",

    tags=["Syndromes"],

    summary="Retrieve a specific syndrome",

    description="""
Returns detailed information for a single syndrome.

Examples:
- cEDS
- vEDS
- marfan
- lds
""",

    response_description="Detailed syndrome information"
)
def get_syndrome(syndrome_name: str):

    syndromes = load_json(SYNDROMES_FILE)

    syndrome_name = syndrome_name.lower()

    if syndrome_name not in syndromes:

        raise HTTPException(
            status_code=404,
            detail=f"Syndrome '{syndrome_name}' not found"
        )

    return syndromes[syndrome_name]


# =====================================================
# GET ALL GENES
# =====================================================

@app.get(

    "/genes",

    tags=["Genes"],

    summary="Retrieve all genes",

    description="""
Returns the complete gene database.

Includes:
- gene names
- associated disorders
- inheritance
- pathways
- protein functions
- phenotype associations
""",

    response_description="Complete gene database"
)
def get_genes():

    data = load_json(GENES_FILE)

    return {

        "total_genes": len(data),

        "genes": data
    }


# =====================================================
# GET SINGLE GENE
# =====================================================

@app.get(

    "/genes/{gene_name}",

    tags=["Genes"],

    summary="Retrieve a specific gene",

    description="""
Returns detailed information about a single gene.

Examples:
- COL5A1
- COL3A1
- FBN1
- TGFBR2
""",

    response_description="Detailed gene information"
)
def get_gene(gene_name: str):

    genes = load_json(GENES_FILE)

    gene_name = gene_name.upper()

    if gene_name not in genes:

        raise HTTPException(
            status_code=404,
            detail=f"Gene '{gene_name}' not found"
        )

    return genes[gene_name]


# =====================================================
# SEARCH GENE
# =====================================================

@app.get(

    "/search/gene/{gene_name}",

    tags=["Search"],

    summary="Search genes",

    description="""
Searches for genes by partial name matching.

Useful for:
- autocomplete
- exploratory analysis
- quick gene lookup
""",

    response_description="Matching genes"
)
def search_gene(gene_name: str):

    genes = load_json(GENES_FILE)

    gene_name = gene_name.upper()

    matches = {}

    for gene, info in genes.items():

        if gene_name in gene:

            matches[gene] = info

    return {

        "query": gene_name,

        "matches_found": len(matches),

        "results": matches
    }


# =====================================================
# SEARCH SYNDROME
# =====================================================

@app.get(

    "/search/syndrome/{query}",

    tags=["Search"],

    summary="Search syndromes",

    description="""
Searches syndromes by:
- abbreviation
- syndrome key
- syndrome full name
""",

    response_description="Matching syndromes"
)
def search_syndrome(query: str):

    syndromes = load_json(SYNDROMES_FILE)

    query = query.lower()

    matches = {}

    for syndrome, info in syndromes.items():

        syndrome_name = info.get("name", "").lower()

        if query in syndrome.lower() or query in syndrome_name:

            matches[syndrome] = info

    return {

        "query": query,

        "matches_found": len(matches),

        "results": matches
    }


# =====================================================
# PROJECT INFO
# =====================================================

@app.get(

    "/info",

    tags=["Project"],

    summary="Project information",

    description="""
Returns general information about the PhenoConnecTive project.

Includes:
- focus areas
- supported disorders
- planned features
- roadmap concepts
""",

    response_description="Project metadata"
)
def info():

    return {

        "project": "PhenoConnecTive",

        "focus": [

            "Bioinformatics",

            "Rare Diseases",

            "Connective Tissue Disorders",

            "Phenotype Matching",

            "Genetic Analysis"
        ],

        "supported_disorders": [

            "Ehlers-Danlos Syndromes",

            "Marfan Syndrome",

            "Loeys-Dietz Syndrome",

            "Osteogenesis Imperfecta",

            "Stickler Syndrome"
        ],

        "planned_features": [

            "Variant scoring",

            "Phenotype matching",

            "HPO integration",

            "VCF parsing",

            "ClinVar integration",

            "AI-assisted prioritization",

            "Explainable diagnostics"
        ]
    }
