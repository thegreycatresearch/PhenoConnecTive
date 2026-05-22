from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional

from .phenotype import Phenotype
from .variant import Variant


@dataclass
class Patient:
    phenotypes: List[Phenotype] = field(default_factory=list)
    variants: List[Variant] = field(default_factory=list)
    inheritance: Optional[str] = None
