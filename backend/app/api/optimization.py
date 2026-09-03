from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from backend.app.optimization.what_if import run_what_if
from backend.app.optimization.mock_data import SAMPLE_20_PROJECTS

router = APIRouter(prefix="/optimization", tags=["optimization"])

class WhatIfRequest(BaseModel):
    budget: float = 50000000.0
    priority: str = "maximum_impact"
    underserved_min_percent: float = 20.0
    beneficiary_group: Optional[str] = None
    project_cap: float = 7500000.0
    candidate_projects: Optional[List[Dict[str, Any]]] = None

@router.post("/what-if")
def simulate_what_if(req: WhatIfRequest):
    pool = req.candidate_projects if req.candidate_projects else SAMPLE_20_PROJECTS
    return run_what_if(
        projects=pool,
        budget=req.budget,
        project_cap=req.project_cap,
        underserved_min_percent=req.underserved_min_percent,
        priority=req.priority,
        beneficiary_group=req.beneficiary_group
    )

@router.post("/run")
def run_default_optimization():
    return run_what_if(
        projects=SAMPLE_20_PROJECTS,
        budget=50000000.0,
        project_cap=7500000.0,
        underserved_min_percent=20.0,
        priority="maximum_impact",
        beneficiary_group=None
    )