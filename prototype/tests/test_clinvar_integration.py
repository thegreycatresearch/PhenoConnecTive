import unittest
from pathlib import Path

from data.clinvar_loader import load_clinvar_records
from data.variant_database import VariantDatabase
from engine.variant_matcher import interpret_pathogenicity, match_patient_variants
from models.patient import Patient
from models.variant import Variant


class ClinVarIntegrationTests(unittest.TestCase):
    def test_load_clinvar_records_validates_data(self):
        records = load_clinvar_records(Path(__file__).resolve().parent.parent / "data" / "clinvar.json")
        self.assertEqual(len(records), 4)
        self.assertEqual(records[0].gene, "COL5A1")
        self.assertEqual(records[0].clinical_significance, "Pathogenic")

    def test_variant_database_lookup_returns_record(self):
        records = load_clinvar_records(Path(__file__).resolve().parent.parent / "data" / "clinvar.json")
        database = VariantDatabase(records)
        matches = database.lookup("COL5A1", "c.1502G>A")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].accession, "RCV000000001")

    def test_match_patient_variants_interprets_pathogenicity(self):
        records = load_clinvar_records(Path(__file__).resolve().parent.parent / "data" / "clinvar.json")
        database = VariantDatabase(records)
        patient = Patient(
            variants=[
                Variant(gene="COL5A1", variant="c.1502G>A", classification="Pathogenic"),
                Variant(gene="TNXB", variant="c.3001A>T", classification="VUS"),
            ]
        )

        matches = match_patient_variants(patient, database)
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0].interpretation, "pathogenic")
        self.assertEqual(matches[0].score, 100)
        self.assertEqual(matches[1].interpretation, "vus")

    def test_interpret_pathogenicity_normalizes_labels(self):
        record = load_clinvar_records(Path(__file__).resolve().parent.parent / "data" / "clinvar.json")[2]
        self.assertEqual(interpret_pathogenicity(record), "likely pathogenic")


if __name__ == "__main__":
    unittest.main()
