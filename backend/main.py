from fastapi import FastAPI

from app.api.ai import router as ai_router


app = FastAPI(
    title="Impact Sphere API",
    description=(
        "AI-powered CSR Need-to-Impact "
        "Allocation and Project Prioritization Platform"
    ),
    version="1.0.0"
)


# ============================================================
# ROUTERS
# ============================================================

app.include_router(
    ai_router
)


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def root():

    return {
        "project": "Impact Sphere",
        "status": "running",
        "message": "Impact Sphere API is online"
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }