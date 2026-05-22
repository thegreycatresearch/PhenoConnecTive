from __future__ import annotations

import logging
from typing import Iterable

from .phenotype_similarity import (
    find_best_phenotype_match,
    load_phenotype_relationships,
)
from models.patient import Patient
from models.phenotype import Phenotype
from models.syndrome import Syndrome, SyndromePhenotype

logger = logging.getLogger(__name__)
RELATIONSHIPS = load_phenotype_relationships()


def calculate_score(patient: Patient, syndrome: Syndrome) -> int:
    score = _score_phenotypes(patient.phenotypes, syndrome.phenotypes)
    logger.debug("Calculated score %d for syndrome %s", score, syndrome.name)
    return score


def _score_phenotypes(patient_phenotypes: Iterable[Phenotype], syndrome_phenotypes: Iterable[SyndromePhenotype]) -> int:
    score = 0
    target_lookup = {
        phenotype.name.lower(): phenotype
        for phenotype in syndrome_phenotypes
        if phenotype.name
    }
    target_names = [phenotype.name for phenotype in syndrome_phenotypes if phenotype.name]

    for phenotype in patient_phenotypes:
        if not phenotype.name:
            continue

        best_match = find_best_phenotype_match(phenotype.name, target_names, RELATIONSHIPS)
        if best_match.similarity <= 0.0 or not best_match.target:
            continue

        target = target_lookup.get(best_match.target.lower())
        if target is None:
            continue

        weight = target.weight if target.weight is not None else 1
        contribution = int(round(weight * best_match.similarity))
        score += contribution

        logger.debug(
            "Matched '%s' to '%s' (%s): weight=%s, contribution=%s",
            phenotype.name,
            best_match.target,
            best_match.relation,
            weight,
            contribution,
        )

    return score
