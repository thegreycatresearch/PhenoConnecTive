from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Dict, Optional

from models.syndrome import Syndrome, SyndromeGene, SyndromePhenotype

logger = logging.getLogger(__name__)


def load_syndromes(file_path: Optional[Path] = None) -> Dict[str, Syndrome]:
    if file_path is None:
        file_path = Path(__file__).resolve().parent / "syndromes.json"

    logger.debug("Loading syndromes from %s", file_path)
    with file_path.open("r", encoding="utf-8") as file:
        raw_data = json.load(file)

    syndromes: Dict[str, Syndrome] = {}
    for syndrome_id, syndrome_data in raw_data.items():
        if syndrome_id == "red_flags":
            continue

        genes = []
        for gene in syndrome_data.get("genes", []):
            if isinstance(gene, dict):
                genes.append(SyndromeGene(name=gene["name"], weight=gene.get("weight")))
            else:
                genes.append(SyndromeGene(name=str(gene)))

        phenotypes = []
        for phenotype in syndrome_data.get("phenotypes", []):
            if isinstance(phenotype, dict):
                phenotypes.append(
                    SyndromePhenotype(
                        name=phenotype["name"],
                        weight=phenotype.get("weight"),
                        cardinal=bool(phenotype.get("cardinal", False)),
                    )
                )
            else:
                phenotypes.append(SyndromePhenotype(name=str(phenotype)))

        syndromes[syndrome_id] = Syndrome(
            id=syndrome_id,
            name=syndrome_data["name"],
            genes=genes,
            phenotypes=phenotypes,
            inheritance=syndrome_data.get("inheritance"),
            metadata={k: v for k, v in syndrome_data.items() if k not in {"name", "genes", "phenotypes", "inheritance"}},
        )

    logger.info("Loaded %d syndromes", len(syndromes))
    return syndromes
