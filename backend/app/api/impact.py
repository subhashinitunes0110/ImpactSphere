from fastapi import APIRouter
from pydantic import BaseModel, Field
from backend.app.impact.need import calculate_need_metrics
from backend.app.impact.scoring import compute_impact_score

router = APIRouter(prefix="/impact", tags=["impact"])

class ProjectScoreRequest(BaseModel):
    project_id: str
    district: str
    sector: str
    budget: float
    beneficiaries: int
    beneficiary_group: str
    expected_impact: float = Field(default=75.0, ge=0, le=100)
    csr_alignment: float = Field(default=80.0, ge=0, le=100)
    feasibility: float = Field(default=85.0, ge=0, le=100)
    sustainability: float = Field(default=80.0, ge=0, le=100)

@router.post("/need-index")
def get_need_index(district: str, sector: str = "general"):
    res = calculate_need_metrics(district, sector)
    return {
        "district": district,
        "need_score": res["need_score"],
        "unmet_need_score": res["unmet_need_score"]
    }

@router.post("/score")
def score_project(req: ProjectScoreRequest):
    scores = compute_impact_score(req.model_dump())
    return {
        "project_id": req.project_id,
        "need_score": scores["need_score"],
        "unmet_need": scores["unmet_need"],
        "reach_score": scores["reach_score"],
        "cost_efficiency": scores["cost_efficiency"],
        "impact_score": scores["impact_score"],
        "geographic_score": scores["geographic_score"]
    }