from __future__ import annotations

from typing import Any, Dict, List

from models.patient import (
    PatientPhenotypeRequest,
    PatientAnalysisRequest
)
from models.phenotype import Phenotype
from models.variant import Variant


def normalize_phenotype_entry(entry: Any) -> Phenotype:
    if isinstance(entry, str):
        return Phenotype(name=entry)

    if isinstance(entry, dict):
        return Phenotype(
            name=str(entry.get("name") or entry.get("label", "")),
            hpo=entry.get("hpo"),
        )

    raise TypeError("Phenotype entry must be a string or a dictionary.")


def normalize_patient_data(patient_data: Dict[str, Any]) -> Patient:
    phenotypes: List[Phenotype] = [
        normalize_phenotype_entry(entry)
        for entry in patient_data.get("phenotypes", [])
    ]

    variants: List[Variant] = []
    for variant_data in patient_data.get("variants", []):
        if isinstance(variant_data, dict):
            variants.append(
                Variant(
                    gene=str(variant_data.get("gene", "")),
                    variant=str(variant_data.get("variant", "")),
                    classification=str(variant_data.get("classification", "")),
                )
            )

    return Patient(
        phenotypes=phenotypes,
        variants=variants,
        inheritance=patient_data.get("inheritance", ""),
    )
