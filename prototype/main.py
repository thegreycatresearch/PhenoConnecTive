import json

# Load syndrome database
with open("syndromes.json", "r") as file:
    syndromes = json.load(file)

# Example patient data
patient_genes = ["COL5A1"]
patient_phenotypes = [
    "skin hyperextensibility",
    "joint hypermobility"
]

results = {}

# Scoring system
for syndrome_id, syndrome_data in syndromes.items():

    score = 0

    # Gene scoring
    for gene in patient_genes:
        if gene in syndrome_data["genes"]:
            score += 50

    # Phenotype scoring
    for phenotype in patient_phenotypes:
        if phenotype in syndrome_data["phenotypes"]:
            score += 10

    results[syndrome_data["name"]] = score

# Sort results
sorted_results = sorted(
    results.items(),
    key=lambda x: x[1],
    reverse=True
)

# Print ranking
print("\nDiagnostic Ranking:\n")

for diagnosis, score in sorted_results:
    print(f"{diagnosis}: {score}")
