from fastapi import APIRouter, HTTPException

from data import VariantDatabase, load_clinvar_records
from engine import match_patient_variants
from models.patient import Patient
from models.variant import Variant
from schemas.variants import VariantAnalysisRequest, VariantMatchResponse

router = APIRouter()


@router.post("/analyze", response_model=list[VariantMatchResponse])
def analyze_variants(payload: VariantAnalysisRequest) -> list[VariantMatchResponse]:
    try:
        records = load_clinvar_records()
    except FileNotFoundError as error:
        raise HTTPException(status_code=503, detail=str(error))

    database = VariantDatabase(records)
    patient = Patient(
        variants=[
            Variant(gene=variant.gene, variant=variant.variant, classification=variant.classification or "")
            for variant in payload.variants
        ]
    )

    results = match_patient_variants(patient, database)
    return [
        VariantMatchResponse(
            gene=result.gene,
            patient_variant=result.patient_variant,
            interpretation=result.interpretation,
            score=result.score,
            explanation=result.explanation,
            accession=result.matched_record.accession if result.matched_record else None,
            clinical_significance=result.matched_record.clinical_significance if result.matched_record else None,
            review_status=result.matched_record.review_status if result.matched_record else None,
            summary=result.matched_record.summary if result.matched_record else None,
        )
        for result in results
    ]
