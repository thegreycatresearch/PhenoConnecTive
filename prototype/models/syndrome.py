from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SyndromeGene:
    name: str
    weight: Optional[int] = None


@dataclass
class SyndromePhenotype:
    name: str
    weight: Optional[int] = None
    cardinal: bool = False


@dataclass
class Syndrome:
    id: str
    name: str
    genes: List[SyndromeGene] = field(default_factory=list)
    phenotypes: List[SyndromePhenotype] = field(default_factory=list)
    inheritance: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
