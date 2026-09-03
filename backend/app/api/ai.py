from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.ai.pipeline import analyze_proposal


router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


class AnalyzeRequest(BaseModel):

    text: str

    needs: list[dict] = []


@router.post("/analyze")
def analyze(request: AnalyzeRequest):

    try:

        result = analyze_proposal(
            request.text,
            request.needs
        )

        return {
            "success": True,
            "data": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )