import json
from pathlib import Path

from scoring import calculate_score
from phenotype_parser import normalize_patient_data


def load_syndromes():
    syndromes_path = Path(__file__).resolve().parent / "syndromes.json"
    with syndromes_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def main():
    syndromes = load_syndromes()

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

    patient_data = normalize_patient_data(patient_data)
    results = {}

    for syndrome_id, syndrome_data in syndromes.items():
        if syndrome_id == "red_flags":
            continue

        score = calculate_score(patient_data, syndrome_data)
        results[syndrome_data["name"]] = score

    if not results:
        print("No syndromes loaded.")
        return

    sorted_results = sorted(results.items(), key=lambda item: item[1], reverse=True)
    max_score = max(results.values())

    print("\n=== Diagnostic Ranking ===\n")

    for diagnosis, score in sorted_results:
        compatibility = round((score / max_score) * 100, 1) if max_score else 0.0

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


if __name__ == "__main__":
    main()
