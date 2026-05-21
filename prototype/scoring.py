def calculate_score(patient_data, syndrome_data):

    score = 0

    # Variant scoring
    for variant in patient_data["variants"]:

        gene = variant["gene"]
        classification = variant["classification"]

        if gene in syndrome_data["genes"]:

            if classification == "Pathogenic":
                score += 60

            elif classification == "Likely Pathogenic":
                score += 40

            elif classification == "VUS":
                score += 15

    # Phenotype scoring
    for phenotype in patient_data["phenotypes"]:

    phenotype_name = phenotype["name"]

    if phenotype_name in syndrome_data["phenotypes"]:
            score += 10

    # Inheritance scoring
    if patient_data["inheritance"] == syndrome_data["inheritance"]:
        score += 15

    return score
