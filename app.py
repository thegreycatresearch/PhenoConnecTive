from fastapi import FastAPI
from pathlib import Path
import json

app = FastAPI(
    title="PhenoConnecTive API",
    description="Phenotype-driven connective tissue disorder analysis",
    version="0.1.0"
)

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Data path
DATA_DIR = BASE_DIR / "data"

@app.get("/")
def root():

    return {
        "project": "PhenoConnecTive",
        "status": "running"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


@app.get("/syndromes")
def get_syndromes():

    syndromes_file = DATA_DIR / "syndromes.json"

    with open(
        syndromes_file,
        "r",
        encoding="utf-8"
    ) as file:

        syndromes = json.load(file)

    return syndromes
