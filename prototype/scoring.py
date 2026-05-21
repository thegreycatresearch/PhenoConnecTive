def calculate_score(patient_data, syndrome_data):

    score = 0

    # Variant scoring
    for variant in patient_data["variants"]:

        patient_gene = variant["gene"]
        classification = variant["classification"]

        for syndrome_gene in syndrome_data["genes"]:

            if patient_gene == syndrome_gene["name"]:

                gene_weight = syndrome_gene["weight"]

                if classification == "Pathogenic":
                    score += gene_weight

                elif classification == "Likely Pathogenic":
                    score += gene_weight * 0.7

                elif classification == "VUS":
                    score += gene_weight * 0.25

    # Phenotype scoring
    for patient_pheno in patient_data["phenotypes"]:

        patient_pheno_name = patient_pheno["name"]

        for syndrome_pheno in syndrome_data["phenotypes"]:

            if patient_pheno_name == syndrome_pheno["name"]:

                score += syndrome_pheno["weight"]

                # Bonus for cardinal features
                if syndrome_pheno["cardinal"]:
                    score += 5

    # Inheritance scoring
    if patient_data["inheritance"] == syndrome_data["inheritance"]:
        score += 15

    return round(score, 2)
