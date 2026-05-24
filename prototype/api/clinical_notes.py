from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI(title="PhenoConnecTive NLP API")


# ---------- INPUT ----------
class ClinicalNote(BaseModel):
    text: str


# ---------- OUTPUT ----------
class ParsedNote(BaseModel):
    original_text: str
    symptoms: List[str]
    systems: List[str]
    tags: List[str]


# ---------- SIMPLE NLP ENGINE ----------
def extract_data(text: str):
    t = text.lower()

    symptoms = []
    systems = []
    tags = []

    # ---- SYMPTOMS ----
    if any(x in t for x in ["mareo", "vertigo", "me desmayo", "presión baja"]):
        symptoms.append("mareos / presíncope")
        systems.append("autonómico")
        tags.append("posible disautonomía")

    if any(x in t for x in ["fatiga", "cansancio extremo", "agotamiento"]):
        symptoms.append("fatiga")
        systems.append("general / sistémico")

    if any(x in t for x in ["dolor articular", "articulaciones", "me duele todo"]):
        symptoms.append("dolor musculoesquelético")
        systems.append("musculoesquelético")
        tags.append("dolor crónico")

    if any(x in t for x in ["palpitaciones", "corazón acelerado"]):
        symptoms.append("palpitaciones")
        systems.append("cardiovascular")
        tags.append("autonómico")

    if any(x in t for x in ["falta de aire", "disnea", "me cuesta respirar"]):
        symptoms.append("disnea")
        systems.append("respiratorio")

    # ---- TAGS GLOBALES ----
    if "crónico" in t or "hace años" in t:
        tags.append("condición crónica posible")

    if "empeora al pararme" in t or "al levantarme" in t:
        tags.append("ortostático")

    # limpiar duplicados
    symptoms = list(set(symptoms))
    systems = list(set(systems))
    tags = list(set(tags))

    return symptoms, systems, tags


# ---------- ENDPOINT ----------
@app.post("/parse-note", response_model=ParsedNote)
def parse_note(note: ClinicalNote):

    symptoms, systems, tags = extract_data(note.text)

    return ParsedNote(
        original_text=note.text,
        symptoms=symptoms,
        systems=systems,
        tags=tags
    )
