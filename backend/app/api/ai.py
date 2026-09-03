from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.ai.pipeline import analyze_proposal


router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


# =========================================================
# REQUEST SCHEMA
# =========================================================

class AnalyzeRequest(BaseModel):

    text: str

    needs: list[dict] = []


# =========================================================
# DEMO COMMUNITY NEEDS
# =========================================================

DEFAULT_NEEDS = [

    {
        "id": 1,
        "description":
            "Remote rural communities have limited access to "
            "healthcare facilities, doctors and essential medical services."
    },

    {
        "id": 2,
        "description":
            "Students from disadvantaged communities need better "
            "access to education and digital learning resources."
    },

    {
        "id": 3,
        "description":
            "Rural women require livelihood opportunities and "
            "entrepreneurship training."
    },

    {
        "id": 4,
        "description":
            "Villages lack reliable access to safe drinking water "
            "and sanitation infrastructure."
    },

    {
        "id": 5,
        "description":
            "Underserved communities need access to sports facilities "
            "and professional coaching."
    }

]


# =========================================================
# ANALYZE PROPOSAL
# =========================================================

@router.post("/analyze")
def analyze(request: AnalyzeRequest):

    if not request.text.strip():

        raise HTTPException(
            status_code=400,
            detail="Proposal text cannot be empty."
        )

    try:

        needs = (
            request.needs
            if request.needs
            else DEFAULT_NEEDS
        )

        result = analyze_proposal(
            request.text,
            needs
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )