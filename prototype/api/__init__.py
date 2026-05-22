from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.phenotypes import router as phenotype_router
from routes.variants import router as variant_router
from utils.logging_config import configure_logging


def create_application() -> FastAPI:
    configure_logging("INFO")
    app = FastAPI(
        title="PhenoConnecTive API",
        version="0.1.0",
        description="API backend for phenotype matching, variant analysis, and diagnostic ranking.",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(phenotype_router, prefix="/phenotypes", tags=["phenotypes"])
    app.include_router(variant_router, prefix="/variants", tags=["variants"])
    app.include_router(diagnosis_router, prefix="/diagnosis", tags=["diagnosis"])

    @app.get("/")
    def health_check() -> dict[str, str]:
        return {"message": "PhenoConnecTive API is running"}

    return app


app = create_application()
