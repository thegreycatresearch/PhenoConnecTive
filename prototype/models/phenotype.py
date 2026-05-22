from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Phenotype:
    name: str
    hpo: Optional[str] = None
