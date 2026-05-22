from fastapi import FastAPI
import json

app = FastAPI(
    title="PhenoConnecTive API"
)

@app.get("/")
def root():

    return {
        "message": "PhenoConnecTive is running"
    }


@app.get("/syndromes")
def get_syndromes():

    with open(
        "data/syndromes.json",
        "r"
    ) as file:

        syndromes = json.load(file)

    return syndromes
