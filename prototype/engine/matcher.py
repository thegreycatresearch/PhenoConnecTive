from prototype.engine.scoring import analyze_patient


# =====================================================
# PHENOTYPE MATCHER
# =====================================================

class PhenotypeMatcher:

    def __init__(self):

        self.analysis_result = None


    # =================================================
    # RUN ANALYSIS
    # =================================================

    def match(self, phenotypes):

        self.analysis_result = analyze_patient(
            phenotypes
        )

        return self.analysis_result


    # =================================================
    # GET BEST MATCH
    # =================================================

    def get_best_match(self):

        if not self.analysis_result:

            return None

        results = self.analysis_result.get(
            "results",
            []
        )

        if len(results) == 0:

            return None

        return results[0]


    # =================================================
    # GET TOP MATCHES
    # =================================================

    def get_top_matches(
        self,
        limit=5
    ):

        if not self.analysis_result:

            return []

        results = self.analysis_result.get(
            "results",
            []
        )

        return results[:limit]


    # =================================================
    # FILTER BY SCORE
    # =================================================

    def filter_by_score(
        self,
        minimum_score=50
    ):

        if not self.analysis_result:

            return []

        results = self.analysis_result.get(
            "results",
            []
        )

        filtered = []

        for result in results:

            if result["score_percent"] >= minimum_score:

                filtered.append(result)

        return filtered


    # =================================================
    # FILTER BY WEIGHTED SCORE
    # =================================================

    def filter_by_weighted_score(
        self,
        minimum_weighted_score=15
    ):

        if not self.analysis_result:

            return []

        results = self.analysis_result.get(
            "results",
            []
        )

        filtered = []

        for result in results:

            if result["weighted_score"] >= minimum_weighted_score:

                filtered.append(result)

        return filtered


    # =================================================
    # GET MATCH SUMMARY
    # =================================================

    def summary(self):

        if not self.analysis_result:

            return {

                "status": "No analysis performed"
            }

        best_match = self.get_best_match()

        return {

            "status": "Analysis complete",

            "total_syndromes_analyzed": len(
                self.analysis_result.get(
                    "results",
                    []
                )
            ),

            "valid_phenotypes": len(
                self.analysis_result.get(
                    "valid_phenotypes",
                    []
                )
            ),

            "invalid_phenotypes": len(
                self.analysis_result.get(
                    "invalid_phenotypes",
                    []
                )
            ),

            "best_match": {

                "syndrome": best_match.get(
                    "syndrome_name"
                ),

                "abbreviation": best_match.get(
                    "abbreviation"
                ),

                "score_percent": best_match.get(
                    "score_percent"
                ),

                "weighted_score": best_match.get(
                    "weighted_score"
                )
            }
        }


# =====================================================
# TEST MODE
# =====================================================

if __name__ == "__main__":

    matcher = PhenotypeMatcher()

    patient_data = [

        "HP:0001382",
        "HP:0000974",
        "HP:0001065",
        "HP:0000978"
    ]

    matcher.match(patient_data)

    print("\n=== SUMMARY ===\n")

    print(
        matcher.summary()
    )

    print("\n=== BEST MATCH ===\n")

    print(
        matcher.get_best_match()
    )

    print("\n=== TOP MATCHES ===\n")

    print(
        matcher.get_top_matches()
    )
