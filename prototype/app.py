from fastapi import FastAPI
from pathlib import Path
import json

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

@app.get("/")
def root():

    return {
        "message": "PhenoConnecTive API running"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.get("/syndromes")
def syndromes():

    file_path = DATA_DIR / "syndromes.json"

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        data = json.load(file)

    return data
