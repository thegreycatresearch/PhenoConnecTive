from __future__ import annotations

import logging
from typing import List

from data.variant_database import VariantDatabase
from models.clinvar import ClinVarRecord, VariantMatchResult
from models.patient import Patient
from models.variant import Variant

logger = logging.getLogger(__name__)

CLASSIFICATION_WEIGHTS = {
    "pathogenic": 100,
    "likely pathogenic": 75,
    "vus": 25,
    "benign": 0,
}

CLASSIFICATION_FALLBACK = "uncertain significance"


def interpret_pathogenicity(record: ClinVarRecord) -> str:
    classification = record.clinical_significance.strip().lower()
    normalized = classification.replace("clinvar:", "")
    if normalized in CLASSIFICATION_WEIGHTS:
        return normalized
    if "pathogenic" in normalized:
        return "likely pathogenic" if "likely" in normalized else "pathogenic"
    if "benign" in normalized:
        return "benign"
    if "uncertain" in normalized or "vus" in normalized:
        return "vus"
    return CLASSIFICATION_FALLBACK


def _score_classification(interpretation: str) -> int:
    return CLASSIFICATION_WEIGHTS.get(interpretation, 10)


def _select_best_record(records: List[ClinVarRecord]) -> ClinVarRecord:
    def ranking(record: ClinVarRecord) -> int:
        interpretation = interpret_pathogenicity(record)
        return CLASSIFICATION_WEIGHTS.get(interpretation, 10)

    best = max(records, key=ranking)
    logger.debug(
        "Selected best ClinVar record %s with classification %s",
        best.accession,
        best.clinical_significance,
    )
    return best


def match_patient_variants(patient: Patient, database: VariantDatabase) -> List[VariantMatchResult]:
    results: List[VariantMatchResult] = []

    for variant in patient.variants:
        if not variant.gene or not variant.variant:
            explanation = "Variant entry is incomplete and cannot be matched."
            results.append(
                VariantMatchResult(
                    patient_variant=str(variant.variant),
                    gene=str(variant.gene),
                    matched_record=None,
                    interpretation=CLASSIFICATION_FALLBACK,
                    score=0,
                    explanation=explanation,
                )
            )
            continue

        matched_records = database.lookup(variant.gene, variant.variant)
        if not matched_records:
            explanation = (
                f"No ClinVar record found for gene {variant.gene} and variant {variant.variant}."
            )
            results.append(
                VariantMatchResult(
                    patient_variant=variant.variant,
                    gene=variant.gene,
                    matched_record=None,
                    interpretation=CLASSIFICATION_FALLBACK,
                    score=0,
                    explanation=explanation,
                )
            )
            continue

        best_record = _select_best_record(matched_records)
        interpretation = interpret_pathogenicity(best_record)
        score = _score_classification(interpretation)
        explanation = (
            f"Matched {variant.variant} in {variant.gene} to ClinVar record {best_record.accession} "
            f"with interpretation '{interpretation}'."
        )

        results.append(
            VariantMatchResult(
                patient_variant=variant.variant,
                gene=variant.gene,
                matched_record=best_record,
                interpretation=interpretation,
                score=score,
                explanation=explanation,
            )
        )

    return results
