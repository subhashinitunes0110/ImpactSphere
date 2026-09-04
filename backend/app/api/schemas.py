from pydantic import BaseModel
from typing import List, Optional

class OptimizeRequest(BaseModel):
    budget_limit: float
    min_backward_ratio: Optional[float] = 0.2
    sector_preference: Optional[str] = "All"

class OptimizeResponse(BaseModel):
    status: str
    allocated_budget: float
    unspent_budget: float
    total_impact: float
    average_impact: float
    selected_proposals: List[dict]