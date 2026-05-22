from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from models.clinvar import ClinVarRecord

logger = logging.getLogger(__name__)


def _validate_record(raw_record: Dict[str, Any]) -> None:
    required_fields = ["gene", "variant", "clinical_significance"]
    missing_fields = [field for field in required_fields if field not in raw_record or not raw_record[field]]
    if missing_fields:
        raise ValueError(f"ClinVar record is missing required fields: {', '.join(missing_fields)}")


def load_clinvar_records(file_path: Optional[Path] = None) -> List[ClinVarRecord]:
    if file_path is None:
        file_path = Path(__file__).resolve().parent / "clinvar.json"

    logger.debug("Loading ClinVar records from %s", file_path)
    with file_path.open("r", encoding="utf-8") as file:
        raw_records = json.load(file)

    records: List[ClinVarRecord] = []
    for raw_record in raw_records:
        _validate_record(raw_record)
        metadata = {
            key: str(value)
            for key, value in raw_record.items()
            if key not in {"gene", "variant", "clinical_significance", "review_status", "accession", "summary"}
        }
        records.append(
            ClinVarRecord(
                gene=str(raw_record["gene"]).strip(),
                variant=str(raw_record["variant"]).strip(),
                clinical_significance=str(raw_record["clinical_significance"]).strip(),
                review_status=str(raw_record.get("review_status", "")).strip() or None,
                accession=str(raw_record.get("accession", "")).strip() or None,
                summary=str(raw_record.get("summary", "")).strip() or None,
                metadata=metadata,
            )
        )

    logger.info("Loaded %d ClinVar records", len(records))
    return records
