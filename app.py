from fastapi import FastAPI
import json

app = FastAPI(
    title="PhenoConnecTive API",
    description="Phenotype-driven connective tissue disorder analysis",
    version="0.1.0"
)

@app.get("/")
def root():

    return {
        "project": "PhenoConnecTive",
        "status": "running",
        "message": "API online"
    }


@app.get("/syndromes")
def get_syndromes():

    with open(
        "data/syndromes.json",
        "r"
    ) as file:

        syndromes = json.load(file)

    return syndromes


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }
