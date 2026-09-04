from fastapi import APIRouter, HTTPException

from backend.app.ai.pipeline import analyze_proposal
from backend.app.compliance.engine import evaluate_project
from backend.app.compliance.schemas import ComplianceResult
from backend.app.integration.ai_compliance_adapter import (
    ai_analysis_to_compliance_input,
    ai_review_required,
)
from backend.app.schemas.ai import AIAnalysisResponse


router = APIRouter(
    prefix="/integration",
    tags=["AI → Compliance"],
)


@router.post(
    "/ai-compliance",
    response_model=ComplianceResult,
)
def check_ai_analysis(
    analysis: AIAnalysisResponse,
) -> ComplianceResult:

    compliance_input = ai_analysis_to_compliance_input(
        analysis
    )

    result = evaluate_project(
        compliance_input
    )

    if ai_review_required(analysis):
        result.status = "REVIEW"
        result.eligible = False
        result.eligible_for_optimization = False

        if "AI_LOW_CONFIDENCE" not in result.flags:
            result.flags.append("AI_LOW_CONFIDENCE")

        result.reasons.append(
            "AI classification requires human review "
            "before legal eligibility is finalized."
        )

    return result


@router.post(
    "/analyze-and-check",
    response_model=ComplianceResult,
)
def analyze_and_check(
    payload: dict,
) -> ComplianceResult:

    text = str(
        payload.get("text", "")
    ).strip()

    needs = payload.get("needs") or []

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Proposal text cannot be empty.",
        )

    try:
        ai_result = analyze_proposal(
            text,
            needs,
        )

        analysis = AIAnalysisResponse.model_validate(
            ai_result
        )

        return check_ai_analysis(
            analysis
        )

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )
