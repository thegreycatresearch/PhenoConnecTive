def calculate_score(patient_data, syndrome_data):

    score = 0

    # Gene scoring
    for gene in patient_data["genes"]:
        if gene in syndrome_data["genes"]:
            score += 50

    # Phenotype scoring
    for phenotype in patient_data["phenotypes"]:
        if phenotype in syndrome_data["phenotypes"]:
            score += 10

    # Inheritance scoring
    if patient_data["inheritance"] == syndrome_data["inheritance"]:
        score += 15

    return score
