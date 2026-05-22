from fastapi import APIRouter

from engine import normalize_patient_data
from schemas.phenotypes import PatientInput, PatientResponse

router = APIRouter()


@router.post("/normalize", response_model=PatientResponse)
def normalize_phenotypes(payload: PatientInput) -> PatientResponse:
    patient = normalize_patient_data(payload.dict())
    return PatientResponse(
        phenotypes=[
            {
                "name": phenotype.name,
                "hpo": phenotype.hpo,
            }
            for phenotype in patient.phenotypes
        ],
        variants=[
            {
                "gene": variant.gene,
                "variant": variant.variant,
                "classification": variant.classification,
            }
            for variant in patient.variants
        ],
        inheritance=patient.inheritance,
    )
