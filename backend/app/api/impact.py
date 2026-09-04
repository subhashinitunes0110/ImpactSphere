from fastapi import APIRouter, HTTPException

from app.schemas.impact import (
    ImpactScoreRequest,
    ImpactScoreResponse,
)

from app.impact.scorer import calculate_impact_score


router = APIRouter(
    prefix="/impact",
    tags=["Impact"],
)


@router.post(
    "/score",
    response_model=ImpactScoreResponse,
)
async def calculate_project_impact(
    request: ImpactScoreRequest,
):
    """
    Calculate the Impact Sphere score for a CSR project.
    """

    try:
        result = calculate_impact_score(request)
        return result

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Impact scoring failed: {str(e)}",
        )