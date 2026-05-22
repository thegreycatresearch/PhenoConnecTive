from __future__ import annotations

import logging
from typing import Dict, Iterable, List

from models.clinvar import ClinVarRecord

logger = logging.getLogger(__name__)


def normalize_gene(gene: str) -> str:
    return gene.strip().upper()


def normalize_variant(variant: str) -> str:
    return variant.strip().upper()


class VariantDatabase:
    def __init__(self, records: Iterable[ClinVarRecord] = ()) -> None:
        self.records: List[ClinVarRecord] = []
        self._index: Dict[tuple[str, str], List[ClinVarRecord]] = {}
        for record in records:
            self.add_record(record)

    def add_record(self, record: ClinVarRecord) -> None:
        self.records.append(record)
        key = (normalize_gene(record.gene), normalize_variant(record.variant))
        self._index.setdefault(key, []).append(record)
        logger.debug("Indexed ClinVar record %s for gene %s", record.accession, record.gene)

    def lookup(self, gene: str, variant: str) -> List[ClinVarRecord]:
        key = (normalize_gene(gene), normalize_variant(variant))
        return self._index.get(key, [])

    def lookup_by_gene(self, gene: str) -> List[ClinVarRecord]:
        normalized_gene = normalize_gene(gene)
        return [record for record in self.records if normalize_gene(record.gene) == normalized_gene]
