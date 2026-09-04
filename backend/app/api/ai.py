from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.app.ai.pipeline import analyze_proposal


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


class AnalyzeRequest(BaseModel):
    text: str
    needs: list[dict] = []


DEFAULT_NEEDS = [
    {
        "id": 1,
        "description": "Healthcare access for underserved communities",
    },
    {
        "id": 2,
        "description": "Education and learning opportunities",
    },
    {
        "id": 3,
        "description": "Skill development and employment",
    },
    {
        "id": 4,
        "description": "Environmental sustainability",
    },
    {
        "id": 5,
        "description": "Rural development",
    },
    {
        "id": 6,
        "description": "Women empowerment",
    },
    {
        "id": 7,
        "description": "Disaster management and relief",
    },
]


@router.post("/analyze")
def analyze(request: AnalyzeRequest):

    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Proposal text cannot be empty.",
        )

    try:
        needs = request.needs if request.needs else DEFAULT_NEEDS

        result = analyze_proposal(
            request.text,
            needs,
        )

        return result

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )
