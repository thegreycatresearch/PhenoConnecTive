from __future__ import annotations

import logging
from typing import Dict, List, Tuple

from data.loader import load_syndromes
from engine.phenotype_parser import normalize_patient_data
from engine.scoring import calculate_score
from utils.logging_config import configure_logging


def format_rankings(results: Dict[str, int]) -> List[Tuple[str, int, float]]:
    if not results:
        return []

    max_score = max(results.values())
    return [
        (diagnosis, score, round((score / max_score) * 100, 1) if max_score else 0.0)
        for diagnosis, score in sorted(results.items(), key=lambda item: item[1], reverse=True)
    ]


def display_rankings(rankings: List[Tuple[str, int, float]]) -> None:
    print("\n=== Diagnostic Ranking ===\n")
    for diagnosis, score, compatibility in rankings:
        print(diagnosis)
        print(f"Raw Score: {score}")
        print(f"Compatibility: {compatibility}%")

        if compatibility >= 80:
            print("High diagnostic compatibility")
        elif compatibility >= 50:
            print("Moderate diagnostic compatibility")
        else:
            print("Low diagnostic compatibility")

        print()


def main() -> None:
    configure_logging()
    logger = logging.getLogger(__name__)

    syndromes = load_syndromes()
    logger.info("Loaded %d syndromes", len(syndromes))

    patient_data = {
        "variants": [
            {
                "gene": "COL5A1",
                "variant": "c.1502G>A",
                "classification": "Pathogenic",
            },
            {
                "gene": "TNXB",
                "variant": "c.3001A>T",
                "classification": "VUS",
            },
        ],
        "phenotypes": [
            {"name": "skin hyperextensibility", "hpo": "HP:0000974"},
            {"name": "joint hypermobility", "hpo": "HP:0001382"},
            "easy bruising",
            "chronic pain",
        ],
        "inheritance": "Autosomal Dominant",
    }

    patient = normalize_patient_data(patient_data)
    results: Dict[str, int] = {}

    for syndrome in syndromes.values():
        score = calculate_score(patient, syndrome)
        results[syndrome.name] = score

    if not results:
        print("No syndromes loaded.")
        return

    display_rankings(format_rankings(results))


if __name__ == "__main__":
    main()
