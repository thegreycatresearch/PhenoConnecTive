import unittest

from engine.scoring import calculate_score
from models.patient import Patient
from models.phenotype import Phenotype
from models.syndrome import Syndrome, SyndromeGene, SyndromePhenotype


class ScoringTests(unittest.TestCase):
    def test_calculate_score_returns_weighted_sum(self):
        syndrome = Syndrome(
            id="cEDS",
            name="Classical Ehlers-Danlos Syndrome",
            genes=[SyndromeGene(name="COL5A1", weight=60)],
            phenotypes=[
                SyndromePhenotype(name="skin hyperextensibility", weight=20, cardinal=True),
                SyndromePhenotype(name="easy bruising", weight=8),
            ],
        )

        patient = Patient(
            phenotypes=[
                Phenotype(name="skin hyperextensibility"),
                Phenotype(name="easy bruising"),
                Phenotype(name="chronic pain"),
            ]
        )

        score = calculate_score(patient, syndrome)
        self.assertEqual(score, 28)


if __name__ == "__main__":
    unittest.main()
