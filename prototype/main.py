import json
from scoring import calculate_score

# Load syndrome database
with open("syndromes.json", "r") as file:
    syndromes = json.load(file)

# Example patient
patient_data = {

    "variants": [

        {
            "gene": "COL5A1",
            "variant": "c.1502G>A",
            "classification": "Pathogenic"
        }

    ],

    "phenotypes": [
        "skin hyperextensibility",
        "joint hypermobility",
        "easy bruising",
        "chronic pain"
    ],

    "inheritance": "Autosomal Dominant"
}

results = {}

# Analyze syndromes
for syndrome_id, syndrome_data in syndromes.items():

    score = calculate_score(
        patient_data,
        syndrome_data
    )

    results[syndrome_data["name"]] = score

# Sort results
sorted_results = sorted(
    results.items(),
    key=lambda x: x[1],
    reverse=True
)

# Print ranking
print("\n=== Diagnostic Ranking ===\n")

for diagnosis, score in sorted_results:
    print(f"{diagnosis}: {score}")
