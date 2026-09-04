from fastapi import APIRouter
from app.api.schemas import OptimizeRequest, OptimizeResponse
from app.optimization.solver import optimize_portfolio

router = APIRouter()

MOCK_PROPOSALS = [
    {"id": "1", "name": "Rural Primary Healthcare", "sector": "Healthcare", "district": "District X", "budget": 5000000, "impactScore": 88, "isBackwardDistrict": True},
    {"id": "2", "name": "Digital STEM Lab", "sector": "Education", "district": "District C", "budget": 3500000, "impactScore": 85, "isBackwardDistrict": False},
    {"id": "3", "name": "Clean Drinking Water Unit", "sector": "Water & Sanitation", "district": "District Y", "budget": 4500000, "impactScore": 82, "isBackwardDistrict": True},
    {"id": "4", "name": "Solar Micro-Grids", "sector": "Renewable Energy", "district": "District Z", "budget": 6000000, "impactScore": 80, "isBackwardDistrict": False},
    {"id": "5", "name": "Women Vocational Center", "sector": "Skill Development", "district": "District W", "budget": 3000000, "impactScore": 79, "isBackwardDistrict": True},
]

@router.post("/optimize", response_model=OptimizeResponse)
def run_optimization(payload: OptimizeRequest):
    return optimize_portfolio(
        proposals=MOCK_PROPOSALS,
        budget_limit=payload.budget_limit,
        min_backward_ratio=payload.min_backward_ratio or 0.2
    )