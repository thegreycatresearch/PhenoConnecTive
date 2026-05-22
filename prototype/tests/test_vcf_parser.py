import tempfile
import unittest
from pathlib import Path

from data.vcf_parser import parse_vcf, VCFParseError


class VCFParserTests(unittest.TestCase):
    def test_parse_vcf_extracts_variants(self):
        content = """##fileformat=VCFv4.2
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO
1\t12345\t.\tA\tT\t.\tPASS\tGENE=COL5A1;CLNSIG=Pathogenic
2\t67890\t.\tG\tC,A\t.\tPASS\tGENE_NAME=TNXB;CLNSIG=VUS
"""

        with tempfile.NamedTemporaryFile("w", suffix=".vcf", delete=False) as handle:
            handle.write(content)
            path = Path(handle.name)

        try:
            variants = parse_vcf(path)
            self.assertEqual(len(variants), 3)
            self.assertEqual(variants[0].gene, "COL5A1")
            self.assertEqual(variants[0].variant, "1:12345A>T")
            self.assertEqual(variants[0].classification, "Pathogenic")
            self.assertEqual(variants[1].gene, "TNXB")
            self.assertEqual(variants[1].variant, "2:67890G>C")
            self.assertEqual(variants[2].variant, "2:67890G>A")
        finally:
            path.unlink()

    def test_parse_vcf_raises_for_missing_headers(self):
        content = """1\t12345\t.\tA\tT\t.\tPASS\tGENE=COL5A1;CLNSIG=Pathogenic
"""

        with tempfile.NamedTemporaryFile("w", suffix=".vcf", delete=False) as handle:
            handle.write(content)
            path = Path(handle.name)

        try:
            with self.assertRaises(VCFParseError):
                parse_vcf(path)
        finally:
            path.unlink()


if __name__ == "__main__":
    unittest.main()
