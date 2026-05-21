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
    },

    {
        "gene": "TNXB",
        "variant": "c.3001A>T",
        "classification": "VUS"
    }

],
           

    ],

"phenotypes": [

    {
        "name": "skin hyperextensibility",
        "hpo": "HP:0000974"
    },

    {
        "name": "joint hypermobility",
        "hpo": "HP:0001382"
    }

],
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
max_score = max(results.values())
print("\n=== Diagnostic Ranking ===\n")

for diagnosis, score in sorted_results:

    compatibility = round((score / max_score) * 100, 1)

    print(f"{diagnosis}")
    print(f"Raw Score: {score}")
    print(f"Compatibility: {compatibility}%")

    if compatibility >= 80:
        print("High diagnostic compatibility")

    elif compatibility >= 50:
        print("Moderate diagnostic compatibility")

    else:
        print("Low diagnostic compatibility")

    print()
