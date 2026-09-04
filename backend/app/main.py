from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.ai import router as ai_router
from backend.app.api.integration import router as integration_router
from backend.app.api.compliance import router as compliance_router
from backend.app.api.impact import router as impact_router
from backend.app.api.optimization import router as optimization_router


app = FastAPI(title="CSRCompass - Integrated Decision Engine")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# CSR Compliance Engine
app.include_router(compliance_router)

# Impact / Need Engine
app.include_router(impact_router)

# AI Proposal Analysis
app.include_router(ai_router)

# AI → Compliance Integration
app.include_router(integration_router)

# Optimization / What-If Engine
app.include_router(optimization_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "role": "CSRCompass Integrated Decision Engine"
    }
