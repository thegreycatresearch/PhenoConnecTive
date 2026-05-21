"""Utility functions to normalize phenotype input data."""

from typing import Any, Dict


def normalize_phenotype_entry(entry: Any) -> Dict[str, Any]:
    if isinstance(entry, str):
        return {"name": entry}

    if isinstance(entry, dict):
        return {
            "name": entry.get("name") or entry.get("label"),
            "hpo": entry.get("hpo"),
        }

    raise TypeError("Phenotype entry must be a string or a dictionary.")


def normalize_patient_data(patient_data: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(patient_data)
    normalized["phenotypes"] = [
        normalize_phenotype_entry(entry)
        for entry in patient_data.get("phenotypes", [])
    ]
    normalized["variants"] = patient_data.get("variants", [])
    normalized["inheritance"] = patient_data.get("inheritance", "")
    return normalized
