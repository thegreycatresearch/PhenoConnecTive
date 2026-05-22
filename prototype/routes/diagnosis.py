from fastapi import APIRouter

from data import load_syndromes
from engine import calculate_score, normalize_patient_data
from schemas.diagnosis import DiagnosticRequest, DiagnosticResult

router = APIRouter()


@router.post("/rank", response_model=list[DiagnosticResult])
def rank_diagnosis(payload: DiagnosticRequest) -> list[DiagnosticResult]:
    syndromes = load_syndromes()
    patient = normalize_patient_data(payload.dict())

    results = []
    for syndrome in syndromes.values():
        score = calculate_score(patient, syndrome)
        results.append((syndrome.name, score))

    if not results:
        return []

    max_score = max(score for _, score in results)
    return [
        DiagnosticResult(
            syndrome=name,
            score=score,
            compatibility=round((score / max_score) * 100, 1) if max_score else 0.0,
        )
        for name, score in sorted(results, key=lambda item: item[1], reverse=True)
    ]
