from typing import Any, Dict, List, Optional

from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.app.optimization.mock_data import SAMPLE_20_PROJECTS
from backend.app.optimization.solver import solve_with_ortools
from backend.app.optimization.what_if import run_what_if


router = APIRouter(
    prefix="/optimization",
    tags=["optimization"],
)


class WhatIfRequest(BaseModel):
    budget: float = Field(
        default=50000000.0,
        ge=0,
    )

    priority: str = "maximum_impact"

    underserved_min_percent: float = Field(
        default=20.0,
        ge=0,
        le=100,
    )

    beneficiary_group: Optional[str] = None

    project_cap: float = Field(
        default=7500000.0,
        ge=0,
    )

    candidate_projects: Optional[
        List[Dict[str, Any]]
    ] = None


def _get_project_pool(
    candidate_projects: Optional[
        List[Dict[str, Any]]
    ],
) -> List[Dict[str, Any]]:

    if candidate_projects:
        return candidate_projects

    return SAMPLE_20_PROJECTS


@router.post("/what-if")
def simulate_what_if(
    req: WhatIfRequest,
) -> Dict[str, Any]:

    pool = _get_project_pool(
        req.candidate_projects
    )

    return run_what_if(
        projects=pool,
        budget=req.budget,
        project_cap=req.project_cap,
        underserved_min_percent=(
            req.underserved_min_percent
        ),
        priority=req.priority,
        beneficiary_group=req.beneficiary_group,
    )


@router.post("/run")
def run_default_optimization() -> Dict[str, Any]:

    return run_what_if(
        projects=SAMPLE_20_PROJECTS,
        budget=50000000.0,
        project_cap=7500000.0,
        underserved_min_percent=20.0,
        priority="maximum_impact",
        beneficiary_group=None,
    )


@router.post("/solve-optimal")
def solve_globally_optimal(
    req: WhatIfRequest,
) -> Dict[str, Any]:

    pool = _get_project_pool(
        req.candidate_projects
    )

    return solve_with_ortools(
        projects=pool,
        budget=req.budget,
        project_cap=req.project_cap,
        underserved_min_percent=(
            req.underserved_min_percent
        ),
        priority=req.priority,
        beneficiary_group=req.beneficiary_group,
    )
