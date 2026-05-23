# PhenoConnecTive

## Phenotype-Driven Bioinformatics Platform for Connective Tissue Disorders

PhenoConnecTive is an open-source bioinformatics platform focused on phenotype-driven analysis of hereditary connective tissue disorders and related rare diseases.

The project aims to assist future clinical interpretation workflows by integrating:

- Phenotypic data (HPO terms)
- Genetic panel results
- Syndrome knowledge bases
- Variant prioritization
- Explainable diagnostic scoring

The long-term vision is to build a modern, explainable, phenotype-first diagnostic support system for disorders such as:

- Ehlers-Danlos Syndromes (EDS)
- Marfan Syndrome
- Loeys-Dietz Syndrome
- Osteogenesis Imperfecta
- Stickler Syndrome
- Other connective tissue and extracellular matrix disorders

---

# Current Features

## API

Built with FastAPI.

Current endpoints include:

| Endpoint | Description |
|---|---|
| `/` | API status |
| `/health` | Health check |
| `/genes` | Retrieve gene database |
| `/genes/{gene}` | Retrieve single gene |
| `/syndromes` | Retrieve syndrome database |
| `/syndromes/{syndrome}` | Retrieve single syndrome |
| `/search/gene/{query}` | Search genes |
| `/search/syndrome/{query}` | Search syndromes |
| `/info` | Project information |

---

# Core Technologies

- Python
- FastAPI
- JSON-based biomedical datasets
- HPO-oriented architecture
- REST API infrastructure

---

# Project Goals

## Phase 1 — Foundation
- Syndrome knowledge base
- Gene database
- Phenotype ontology structure
- API architecture
- Open-source repository

## Phase 2 — Phenotype Matching
- HPO semantic matching
- Phenotype similarity scoring
- Syndrome ranking
- Explainable results

## Phase 3 — Variant Integration
- Variant interpretation support
- ACMG evidence integration
- ClinVar compatibility
- VCF parsing

## Phase 4 — AI-Assisted Analysis
- AI-assisted phenotype prioritization
- Machine learning ranking systems
- Predictive modeling
- Clinical decision support

---

# Why This Matters

Rare disease diagnostics are often delayed for years due to fragmented phenotype interpretation and limited integration between genomic data and clinical presentation.

PhenoConnecTive aims to contribute toward more accessible, explainable, and phenotype-driven diagnostic workflows.

This project is educational, experimental, and research-oriented.

---

# Repository Structure

```txt
PhenoConnecTive/
│
├── prototype/
│   │
│   ├── app.py
│   ├── requirements.txt
│   │
│   ├── data/
│   │   ├── syndromes.json
│   │   ├── genes.json
│   │   └── phenotypes.json
│   │
│   ├── engine/
│   └── models/
