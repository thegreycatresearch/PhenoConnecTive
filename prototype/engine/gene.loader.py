import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def load_genes():

    file_path = DATA_DIR / "genes.json"

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        genes = json.load(file)

    return genes
