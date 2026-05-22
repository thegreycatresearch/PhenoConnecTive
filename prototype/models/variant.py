from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Variant:
    gene: str
    variant: str
    classification: str
