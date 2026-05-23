import json
from pathlib import Path


# =====================================================
# PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"

SYNDROMES_FILE = DATA_DIR / "syndromes.json"

PHENOTYPES_FILE = DATA_DIR / "phenotypes.json"


# =====================================================
# LOADERS
# =====================================================

def load_json(file_path):

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def load_syndromes():

    return load_json(SYNDROMES_FILE)


def load_phenotypes():

    return load_json(PHENOTYPES_FILE)


# =====================================================
# PHENOTYPE VALIDATION
# =====================================================

def validate_phenotypes(patient_phenotypes):

    phenotype_db = load_phenotypes()

    valid = []

    invalid = []

    for phenotype in patient_phenotypes:

        if phenotype in phenotype_db:

            valid.append(phenotype)

        else:

            invalid.append(phenotype)

    return {

        "valid": valid,

        "invalid": invalid
    }


# =====================================================
# WEIGHTED SCORE ENGINE
# =====================================================

def calculate_match_score(
    patient_phenotypes,
    syndrome_phenotypes,
    phenotype_database
):

    patient_set = set(patient_phenotypes)

    syndrome_set = set(syndrome_phenotypes)

    matched = patient_set.intersection(syndrome_set)

    if len(syndrome_set) == 0:

        return {

            "score": 0,
            "matched": [],
            "weighted_score": 0
        }

    raw_score = (
        len(matched) / len(syndrome_set)
    ) * 100

    weighted_score = 0

    matched_details = []

    for phenotype in matched:

        phenotype_info = phenotype_database.get(
            phenotype,
            {}
        )

        weight = phenotype_info.get(
            "weight_default",
            1
        )

        weighted_score += weight

        matched_details.append({

            "hpo_id": phenotype,

            "name": phenotype_info.get(
                "name",
                "Unknown phenotype"
            ),

            "weight": weight,

            "category": phenotype_info.get(
                "category",
                "unknown"
            )
        })

    return {

        "score": round(raw_score, 2),

        "weighted_score": weighted_score,

        "matched": matched_details
    }


# =====================================================
# MAIN ANALYSIS ENGINE
# =====================================================

def analyze_patient(patient_phenotypes):

    syndromes = load_syndromes()

    phenotype_database = load_phenotypes()

    validation = validate_phenotypes(
        patient_phenotypes
    )

    valid_phenotypes = validation["valid"]

    results = []

    for syndrome_key, syndrome_data in syndromes.items():

        syndrome_hpo = syndrome_data.get(
            "related_hpo_terms",
            []
        )

        match_result = calculate_match_score(

            valid_phenotypes,

            syndrome_hpo,

            phenotype_database
        )

        results.append({

            "syndrome_key": syndrome_key,

            "syndrome_name": syndrome_data.get(
                "name"
            ),

            "abbreviation": syndrome_data.get(
                "abbreviation"
            ),

            "score_percent": match_result["score"],

            "weighted_score": match_result[
                "weighted_score"
            ],

            "matched_phenotypes": match_result[
                "matched"
            ],

            "total_matches": len(
                match_result["matched"]
            ),

            "inheritance": syndrome_data.get(
                "inheritance"
            ),

            "primary_genes": syndrome_data.get(
                "primary_genes",
                []
            ),

            "clinical_severity": syndrome_data.get(
                "clinical_severity"
            ),

            "vascular_risk": syndrome_data.get(
                "vascular_risk"
            )
        })

    results.sort(

        key=lambda x: (
            x["weighted_score"],
            x["score_percent"]
        ),

        reverse=True
    )

    return {

        "input_phenotypes": patient_phenotypes,

        "valid_phenotypes": validation["valid"],

        "invalid_phenotypes": validation["invalid"],

        "results": results
    }


# =====================================================
# TEST MODE
# =====================================================

if __name__ == "__main__":

    sample_patient = [

        "HP:0001382",
        "HP:0000974",
        "HP:0001065",
        "HP:0000978"
    ]

    analysis = analyze_patient(
        sample_patient
    )

    print(

        json.dumps(
            analysis,
            indent=2
        )
    )
