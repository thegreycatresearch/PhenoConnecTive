from __future__ import annotations

from typing import Iterable

from models.variant import Variant
from models.syndrome import Syndrome


def score_variants(patient_variants: Iterable[Variant], syndrome: Syndrome) -> int:
    score = 0
    for variant in patient_variants:
        for gene in syndrome.genes:
            if not gene.name or not variant.gene:
                continue

            if variant.gene.strip().upper() == gene.name.strip().upper():
                score += gene.weight or 10
                classification = variant.classification.strip().lower()
                if classification == "pathogenic":
                    score += 5
                elif classification.startswith("likely"):
                    score += 3
    return score

