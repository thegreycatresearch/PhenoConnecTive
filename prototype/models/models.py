from dataclasses import dataclass

@dataclass
class Variant:
    gene: str
    variant: str
    classification: str

@dataclass
class Phenotype:
    name: str
    hpo: str
