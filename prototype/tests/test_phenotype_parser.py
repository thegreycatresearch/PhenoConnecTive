import unittest

from engine.phenotype_parser import normalize_patient_data, normalize_phenotype_entry
from models.phenotype import Phenotype


class PhenotypeParserTests(unittest.TestCase):
    def test_normalize_phenotype_entry_from_string(self):
        normalized = normalize_phenotype_entry("easy bruising")
        self.assertEqual(normalized, Phenotype(name="easy bruising"))

    def test_normalize_phenotype_entry_from_dict(self):
        normalized = normalize_phenotype_entry({"name": "joint hypermobility", "hpo": "HP:0001382"})
        self.assertEqual(normalized, Phenotype(name="joint hypermobility", hpo="HP:0001382"))

    def test_normalize_patient_data_creates_patient_model(self):
        patient_data = {
            "phenotypes": [
                "easy bruising",
                {"name": "skin hyperextensibility", "hpo": "HP:0000974"},
            ],
            "variants": [{"gene": "COL5A1", "variant": "c.1502G>A", "classification": "Pathogenic"}],
            "inheritance": "Autosomal Dominant",
        }

        patient = normalize_patient_data(patient_data)
        self.assertEqual(len(patient.phenotypes), 2)
        self.assertEqual(patient.phenotypes[0], Phenotype(name="easy bruising"))
        self.assertEqual(patient.inheritance, "Autosomal Dominant")


if __name__ == "__main__":
    unittest.main()
