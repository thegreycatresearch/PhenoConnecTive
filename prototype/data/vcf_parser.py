from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from models.variant import Variant

logger = logging.getLogger(__name__)


class VCFParseError(ValueError):
    pass


def _parse_info_field(info_value: str) -> Dict[str, str]:
    values: Dict[str, str] = {}
    for item in info_value.split(";"):
        if not item:
            continue

        if "=" in item:
            key, value = item.split("=", 1)
            values[key] = value
        else:
            values[item] = ""

    return values


def _detect_gene(info: Dict[str, str]) -> Optional[str]:
    for key in ("GENE", "GENE_NAME", "GENEID", "SYMBOL"):
        if key in info and info[key]:
            return info[key]

    ann_value = info.get("ANN") or info.get("CSQ")
    if ann_value:
        first_annotation = ann_value.split(",", 1)[0]
        parts = first_annotation.split("|")
        if len(parts) > 3 and parts[3]:
            return parts[3]

    return None


def _build_variant_string(chrom: str, pos: str, ref: str, alt: str) -> str:
    if not chrom or not pos or not ref or not alt:
        raise VCFParseError("Incomplete variant coordinates")

    return f"{chrom}:{pos}{ref}>{alt}"


def parse_vcf(file_path: Path | str) -> List[Variant]:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"VCF file not found: {path}")

    variants: List[Variant] = []
    header_columns: Optional[List[str]] = None

    with path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            if line.startswith("##"):
                continue

            if line.startswith("#CHROM"):
                header_columns = line.lstrip("#").strip().split("\t")
                continue

            if line.startswith("#"):
                continue

            if header_columns is None:
                raise VCFParseError("Missing VCF header line (#CHROM)")

            fields = line.strip().split("\t")
            if len(fields) < 8:
                logger.warning("Skipping malformed VCF line %s: not enough fields", line_number)
                continue

            chrom, pos, _id, ref, alt_field, _qual, _filter, info_value = fields[:8]
            info = _parse_info_field(info_value)
            gene = _detect_gene(info) or ""
            classification = info.get("CLNSIG", info.get("CLNSIG2", ""))

            for alt in alt_field.split(","):
                alt = alt.strip()
                if not alt or alt == ".":
                    logger.debug("Skipping invalid ALT allele on line %s", line_number)
                    continue

                try:
                    variant_string = _build_variant_string(chrom, pos, ref, alt)
                except VCFParseError as error:
                    logger.warning("Skipping variant on line %s: %s", line_number, error)
                    continue

                variants.append(
                    Variant(
                        gene=gene,
                        variant=variant_string,
                        classification=classification,
                    )
                )

    logger.info("Parsed %d variants from VCF file %s", len(variants), path.name)
    return variants
