from __future__ import annotations

from pathlib import Path

from typing import List, Dict

import json
import re


# =====================================================
# PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"


# =====================================================
# LOAD PHENOTYPES DATABASE
# =====================================================

with open(
    DATA_DIR / "phenotypes.json",
    "r",
    encoding="utf-8"
) as file:

    PHENOTYPES_DB = json.load(file)


# =====================================================
# PHENOTYPE PARSER
# =====================================================

class PhenotypeParser:

    """
    NLP-assisted phenotype extraction system.

    Current features:
    - phenotype keyword detection
    - synonym matching
    - HPO normalization
    - simple clinical NLP

    Future:
    - negation detection
    - AI embeddings
    - transformer models
    - multilingual phenotype parsing
    - clinical note interpretation
    """

    def __init__(self):

        self.phenotypes = PHENOTYPES_DB

    # =================================================
    # CLEAN TEXT
    # =================================================

    def clean_text(
        self,
        text: str
    ) -> str:

        text = text.lower()

        text = re.sub(
            r"[^a-zA-Z0-9\s\-]",
            "",
            text
        )

        return text

    # =================================================
    # EXTRACT HPO TERMS
    # =================================================

    def extract_hpo_terms(
        self,
        clinical_text: str
    ) -> List[Dict]:

        cleaned_text = self.clean_text(
            clinical_text
        )

        detected = []

        for hpo_id, phenotype in self.phenotypes.items():

            phenotype_name = phenotype.get(
                "name",
                ""
            ).lower()

            synonyms = phenotype.get(
                "synonyms",
                []
            )

            category = phenotype.get(
                "category",
                "unknown"
            )

            weight = phenotype.get(
                "weight_default",
                1
            )

            # =========================================
            # MATCH MAIN NAME
            # =========================================

            if phenotype_name in cleaned_text:

                detected.append({

                    "hpo_id": hpo_id,

                    "name": phenotype.get(
                        "name"
                    ),

                    "category": category,

                    "weight": weight,

                    "match_type": "primary_name"
                })

                continue

            # =========================================
            # MATCH SYNONYMS
            # =========================================

            synonym_found = False

            for synonym in synonyms:

                synonym_clean = synonym.lower()

                if synonym_clean in cleaned_text:

                    detected.append({

                        "hpo_id": hpo_id,

                        "name": phenotype.get(
                            "name"
                        ),

                        "category": category,

                        "weight": weight,

                        "match_type": "synonym"
                    })

                    synonym_found = True

                    break

            if synonym_found:

                continue

        return detected

    # =================================================
    # EXTRACT ONLY HPO IDS
    # =================================================

    def extract_hpo_ids(
        self,
        clinical_text: str
    ) -> List[str]:

        detected = self.extract_hpo_terms(
            clinical_text
        )

        return [

            item["hpo_id"]

            for item in detected
        ]

    # =================================================
    # SUMMARY
    # =================================================

    def summarize_detection(
        self,
        clinical_text: str
    ):

        matches = self.extract_hpo_terms(
            clinical_text
        )

        categories = {}

        for item in matches:

            category = item[
                "category"
            ]

            categories[category] = (
                categories.get(category, 0) + 1
            )

        return {

            "input_text": clinical_text,

            "total_matches": len(matches),

            "matched_hpo_terms": matches,

            "category_distribution": categories
        }
