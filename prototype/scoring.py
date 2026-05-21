from typing import Any, Dict, List


def _normalize_gene_entry(gene_entry: Any) -> Dict[str, Any]:
    if isinstance(gene_entry, str):
        return {"name": gene_entry, "weight": 10}

    if isinstance(gene_entry, dict):
        return {
            "name": gene_entry.get("name"),
            "weight": gene_entry.get("weight", 10),
        }

    raise TypeError("Gene entry must be a string or a dictionary.")


def _normalize_phenotype_entry(phenotype_entry: Any) -> Dict[str, Any]:
    if isinstance(phenotype_entry, str):
        return {"name": phenotype_entry, "weight": 5, "cardinal": False}

    if isinstance(phenotype_entry, dict):
        return {
            "name": phenotype_entry.get("name"),
            "weight": phenotype_entry.get("weight", 5),
            "cardinal": bool(phenotype_entry.get("cardinal", False)),
        }

    raise TypeError("Phenotype entry must be a string or a dictionary.")


def calculate_score(patient_data: Dict[str, Any], syndrome_data: Dict[str, Any]) -> float:
    score = 0.0

    syndrome_genes: List[Dict[str, Any]] = [
        _normalize_gene_entry(entry) for entry in syndrome_data.get("genes", [])
    ]
    syndrome_phenotypes: List[Dict[str, Any]] = [
        _normalize_phenotype_entry(entry)
        for entry in syndrome_data.get("phenotypes", [])
    ]

    for variant in patient_data.get("variants", []):
        patient_gene = variant.get("gene")
        classification = variant.get("classification", "")
        if not patient_gene:
            continue

        for syndrome_gene in syndrome_genes:
            if patient_gene == syndrome_gene["name"]:
                if classification == "Pathogenic":
                    score += syndrome_gene["weight"]
                elif classification == "Likely Pathogenic":
                    score += syndrome_gene["weight"] * 0.7
                elif classification == "VUS":
                    score += syndrome_gene["weight"] * 0.25

    for patient_pheno in patient_data.get("phenotypes", []):
        patient_pheno_name = patient_pheno.get("name")
        if not patient_pheno_name:
            continue

        for syndrome_pheno in syndrome_phenotypes:
            if patient_pheno_name == syndrome_pheno["name"]:
                score += syndrome_pheno["weight"]
                if syndrome_pheno["cardinal"]:
                    score += 5

    if (
        patient_data.get("inheritance")
        and patient_data.get("inheritance") == syndrome_data.get("inheritance")
    ):
        score += 15

    return round(score, 2)
