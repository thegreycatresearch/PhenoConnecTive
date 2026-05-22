from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

logger = logging.getLogger(__name__)

RelationshipEntry = Dict[str, List[str]]
RelationshipMap = Dict[str, RelationshipEntry]
NormalizedMap = Dict[str, str]
ClusterMap = Dict[str, set[str]]


@dataclass
class PhenotypeMatch:
    query: str
    target: str
    similarity: float
    relation: str
    explanation: str


def normalize_term(term: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", " ", term.strip().lower())
    return normalized.strip()


def load_phenotype_relationships(file_path: Optional[Path] = None) -> RelationshipMap:
    if file_path is None:
        file_path = Path(__file__).resolve().parent.parent / "data" / "phenotype_relationships.json"

    logger.debug("Loading phenotype relationships from %s", file_path)
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _build_relationship_index(relationships: RelationshipMap) -> Tuple[NormalizedMap, ClusterMap, Dict[str, set[str]]]:
    canonical_by_name: NormalizedMap = {}
    equivalent_clusters: ClusterMap = {}
    related_map: Dict[str, set[str]] = {}

    for canonical_name, relationship in relationships.items():
        normalized_canonical = normalize_term(canonical_name)
        equivalents = {normalized_canonical}

        for alias in relationship.get("equivalent", []):
            equivalents.add(normalize_term(alias))

        for entry in equivalents:
            canonical_by_name[entry] = normalized_canonical
            equivalent_clusters[entry] = equivalents

        for related_term in relationship.get("related", []):
            normalized_related = normalize_term(related_term)
            related_map.setdefault(normalized_canonical, set()).add(normalized_related)
            related_map.setdefault(normalized_related, set()).add(normalized_canonical)

    return canonical_by_name, equivalent_clusters, related_map


def _compare_terms(
    source: str,
    target: str,
    canonical_by_name: NormalizedMap,
    equivalent_clusters: ClusterMap,
    related_map: Dict[str, set[str]],
) -> Tuple[float, str]:
    if source == target:
        return 1.0, "exact"

    if source in equivalent_clusters and target in equivalent_clusters[source]:
        return 0.9, "equivalent"

    source_canonical = canonical_by_name.get(source, source)
    target_canonical = canonical_by_name.get(target, target)

    if source_canonical == target_canonical:
        return 0.9, "equivalent"

    if target_canonical in related_map.get(source_canonical, set()):
        return 0.7, "related"

    return 0.0, "none"


def find_best_phenotype_match(
    query: str,
    targets: Iterable[str],
    relationships: Optional[RelationshipMap] = None,
) -> PhenotypeMatch:
    if relationships is None:
        relationships = load_phenotype_relationships()

    canonical_by_name, equivalent_clusters, related_map = _build_relationship_index(relationships)
    normalized_query = normalize_term(query)

    best_match = PhenotypeMatch(
        query=query,
        target="",
        similarity=0.0,
        relation="none",
        explanation="No semantic phenotype match was found.",
    )

    for target in targets:
        normalized_target = normalize_term(target)
        similarity, relation = _compare_terms(
            normalized_query,
            normalized_target,
            canonical_by_name,
            equivalent_clusters,
            related_map,
        )

        if similarity <= best_match.similarity:
            continue

        explanation = _build_explanation(query, target, relation, similarity)
        best_match = PhenotypeMatch(
            query=query,
            target=target,
            similarity=similarity,
            relation=relation,
            explanation=explanation,
        )

    logger.debug(
        "Best phenotype match for %s is %s with similarity %.2f (%s)",
        query,
        best_match.target,
        best_match.similarity,
        best_match.relation,
    )

    return best_match


def _build_explanation(query: str, target: str, relation: str, similarity: float) -> str:
    if relation == "exact":
        return f"Exact match between '{query}' and '{target}'."

    if relation == "equivalent":
        return f"Semantic equivalent match between '{query}' and '{target}'."

    if relation == "related":
        return f"Related phenotype match between '{query}' and '{target}'."

    return f"No semantic match found between '{query}' and '{target}'."
