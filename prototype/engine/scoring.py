from __future__ import annotations

import logging
from typing import Iterable

from models.patient import Patient
from models.phenotype import Phenotype
from models.syndrome import Syndrome, SyndromePhenotype

logger = logging.getLogger(__name__)


def calculate_score(patient: Patient, syndrome: Syndrome) -> int:
    score = _score_phenotypes(patient.phenotypes, syndrome.phenotypes)
    logger.debug("Calculated score %d for syndrome %s", score, syndrome.name)
    return score


def _score_phenotypes(patient_phenotypes: Iterable[Phenotype], syndrome_phenotypes: Iterable[SyndromePhenotype]) -> int:
    lookup = {phenotype.name.lower(): phenotype for phenotype in syndrome_phenotypes}
    score = 0

    for phenotype in patient_phenotypes:
        if not phenotype.name:
            continue

        syndrome_match = lookup.get(phenotype.name.lower())
        if syndrome_match is None:
            continue

        score += syndrome_match.weight if syndrome_match.weight is not None else 1

    return score
