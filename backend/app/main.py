from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.api.impact import router as impact_router
from backend.app.api.optimization import router as optimization_router

app = FastAPI(title="CSRCompass - Member 3 Decision Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(impact_router)
app.include_router(optimization_router)

@app.get("/health")
def health_check():
    return {"status": "ok", "role": "Member 3 (Impact & Optimization)"}