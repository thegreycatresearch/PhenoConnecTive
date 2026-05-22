import unittest

from engine.phenotype_similarity import find_best_phenotype_match, load_phenotype_relationships


class PhenotypeSimilarityTests(unittest.TestCase):
    def test_equivalent_phenotype_match(self):
        relationships = load_phenotype_relationships()
        match = find_best_phenotype_match(
            "joint instability",
            ["joint hypermobility"],
            relationships,
        )

        self.assertEqual(match.target, "joint hypermobility")
        self.assertEqual(match.relation, "equivalent")
        self.assertGreaterEqual(match.similarity, 0.9)
        self.assertIn("Semantic equivalent match", match.explanation)

    def test_related_phenotype_match(self):
        relationships = load_phenotype_relationships()
        match = find_best_phenotype_match(
            "arterial fragility",
            ["vascular fragility"],
            relationships,
        )

        self.assertEqual(match.target, "vascular fragility")
        self.assertIn(match.relation, {"equivalent", "related"})
        self.assertGreater(match.similarity, 0.0)


if __name__ == "__main__":
    unittest.main()
