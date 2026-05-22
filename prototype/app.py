from fastapi import FastAPI, HTTPException
from pathlib import Path
import json

app = FastAPI(
    title="PhenoConnecTive API",
    description="Phenotype-driven connective tissue disorder analysis platform",
    version="0.1.0"
)

# =========================
# PATHS
# =========================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

SYNDROMES_FILE = DATA_DIR / "syndromes.json"
GENES_FILE = DATA_DIR / "genes.json"


# =========================
# LOADERS
# =========================

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


# =========================
# ROOT
# =========================

@app.get("/")
def root():

    return {
        "project": "PhenoConnecTive",
        "status": "running",
        "version": "0.1.0",
        "description": "Phenotype-driven connective tissue disorder analysis"
    }


# =========================
# HEALTH CHECK
# =========================

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "api": "online"
    }


# =========================
# SYNDROMES
# =========================

@app.get("/syndromes")
def get_syndromes():

    data = load_json(SYNDROMES_FILE)

    return {
        "total_syndromes": len(data),
        "syndromes": data
    }


# =========================
# GENES
# =========================

@app.get("/genes")
def get_genes():

    data = load_json(GENES_FILE)

    return {
        "total_genes": len(data),
        "genes": data
    }


# =========================
# SINGLE GENE
# =========================

@app.get("/genes/{gene_name}")
def get_gene(gene_name: str):

    genes = load_json(GENES_FILE)

    gene_name = gene_name.upper()

    if gene_name not in genes:

        raise HTTPException(
            status_code=404,
            detail=f"Gene '{gene_name}' not found"
        )

    return genes[gene_name]


# =========================
# SINGLE SYNDROME
# =========================

@app.get("/syndromes/{syndrome_name}")
def get_syndrome(syndrome_name: str):

    syndromes = load_json(SYNDROMES_FILE)

    syndrome_name = syndrome_name.lower()

    if syndrome_name not in syndromes:

        raise HTTPException(
            status_code=404,
            detail=f"Syndrome '{syndrome_name}' not found"
        )

    return syndromes[syndrome_name]


# =========================
# SEARCH GENE
# =========================

@app.get("/search/gene/{gene_name}")
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


# =========================
# SEARCH SYNDROME
# =========================

@app.get("/search/syndrome/{query}")
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


# =========================
# API INFO
# =========================

@app.get("/info")
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
```
