from typing import Any, Dict

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from backend.app.ai.pipeline import analyze_proposal
from backend.app.compliance.schemas import ComplianceResult
from backend.app.integration.ai_compliance_adapter import (
    ai_analysis_to_optimization_project,
    evaluate_ai_compliance,
)
from backend.app.schemas.ai import AIAnalysisResponse
from backend.app.optimization.solver import solve_with_ortools

router = APIRouter(
    prefix="/integration",
    tags=["AI → Compliance → Optimization"],
)


class IntegratedOptimizationRequest(BaseModel):
    text: str
    needs: list[dict] = Field(default_factory=list)

    # Implementing agency
    implementing_agency: str | None = None
    implementing_agency_type: str | None = None
    implementing_agency_csr_registration_number: str | None = None

    implementing_agency_registered_under_12a: bool = False
    implementing_agency_registered_under_80g: bool = False
    implementing_agency_government_established: bool = False
    implementing_agency_created_by_statute: bool = False
    implementing_agency_has_3_year_track_record: bool = False

    # CSR-1
    csr1_required: bool = True
    csr1_filed: bool = False

    # Company-level optimization budget
    budget: float = Field(default=50000000.0, ge=0)

    # Proposed project budget
    project_budget: float | None = Field(default=None, ge=0)

    # Proposed project beneficiaries
    project_beneficiaries: int | None = Field(default=None, ge=0)

    # Optimization configuration
    project_cap: float = Field(default=7500000.0, ge=0)
    underserved_min_percent: float = Field(default=20.0, ge=0, le=100)
    priority: str = "maximum_impact"
    beneficiary_group: str | None = None


def _compliance_context(
    payload: IntegratedOptimizationRequest,
) -> Dict[str, Any]:

    return {
        "implementing_agency": payload.implementing_agency,
        "implementing_agency_type": payload.implementing_agency_type,
        "implementing_agency_csr_registration_number": (
            payload.implementing_agency_csr_registration_number
        ),
        "implementing_agency_registered_under_12a": (
            payload.implementing_agency_registered_under_12a
        ),
        "implementing_agency_registered_under_80g": (
            payload.implementing_agency_registered_under_80g
        ),
        "implementing_agency_government_established": (
            payload.implementing_agency_government_established
        ),
        "implementing_agency_created_by_statute": (
            payload.implementing_agency_created_by_statute
        ),
        "implementing_agency_has_3_year_track_record": (
            payload.implementing_agency_has_3_year_track_record
        ),
        "csr1_required": payload.csr1_required,
        "csr1_filed": payload.csr1_filed,
    }


@router.post(
    "/ai-compliance",
    response_model=ComplianceResult,
)
def check_ai_analysis(
    analysis: AIAnalysisResponse,
) -> ComplianceResult:

    return evaluate_ai_compliance(analysis)


@router.post("/analyze-and-check")
def analyze_and_check(
    payload: Dict[str, Any],
) -> ComplianceResult:

    text = str(payload.get("text", "")).strip()
    needs = payload.get("needs") or []

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Proposal text cannot be empty.",
        )

    try:
        ai_result = analyze_proposal(text, needs)

        analysis = AIAnalysisResponse.model_validate(
            ai_result
        )

        return evaluate_ai_compliance(
            analysis,
            payload,
        )

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@router.post("/analyze-for-optimization")
def analyze_for_optimization(
    payload: Dict[str, Any],
) -> Dict[str, Any]:

    text = str(payload.get("text") or payload.get("proposal_text") or "").strip()
    needs = payload.get("needs") or []

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Proposal text cannot be empty.",
        )

    try:
        ai_result = analyze_proposal(text, needs)

        analysis = AIAnalysisResponse.model_validate(
            ai_result
        )

        project = ai_analysis_to_optimization_project(
            analysis,
            payload,
        )

        # Explicit request values override AI extraction
        if payload.get("project_budget") is not None:
            project["budget"] = payload["project_budget"]

        if payload.get("project_beneficiaries") is not None:
            project["beneficiaries"] = payload[
                "project_beneficiaries"
            ]

        return {
            "success": True,
            "project": project,
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )


@router.post("/optimize-proposal")
def optimize_proposal(
    payload: IntegratedOptimizationRequest,
) -> Dict[str, Any]:

    text = payload.text.strip()

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Proposal text cannot be empty.",
        )

    try:

        # =========================================================
        # 1. AI ANALYSIS
        # =========================================================

        ai_result = analyze_proposal(
            text,
            payload.needs,
        )

        analysis = AIAnalysisResponse.model_validate(
            ai_result
        )

        # =========================================================
        # 2. CSR COMPLIANCE
        # =========================================================

        context = _compliance_context(payload)

        compliance = evaluate_ai_compliance(
            analysis,
            context,
        )

        # Compliance must pass before optimization
        if not compliance.eligible_for_optimization:

            return {
                "success": True,
                "stage": "COMPLIANCE_REVIEW",
                "message": (
                    "Project cannot enter optimization "
                    "until CSR compliance is passed."
                ),
                "ai_analysis": analysis.model_dump(),
                "compliance": compliance.model_dump(),
                "optimization": None,
            }

        # =========================================================
        # 3. CONVERT AI PROJECT → OPTIMIZATION PROJECT
        # =========================================================

        project = ai_analysis_to_optimization_project(
            analysis,
            context,
        )

        # Explicit request values take priority over AI extraction
        if payload.project_budget is not None:
            project["budget"] = payload.project_budget

        if payload.project_beneficiaries is not None:
            project["beneficiaries"] = (
                payload.project_beneficiaries
            )

        # Safe defaults
        project["budget"] = project.get("budget") or 0.0

        project["beneficiaries"] = (
            project.get("beneficiaries") or 0
        )

        # =========================================================
        # 4. PROJECT-LEVEL OPTIMIZATION
        # =========================================================
        #
        # This endpoint evaluates ONE proposal.
        #
        # The portfolio-level underserved constraint is disabled
        # here because a single project cannot satisfy a percentage
        # requirement over an entire CSR portfolio.
        #
        # The full portfolio optimizer continues to enforce that
        # constraint through /optimization/solve-optimal.
        #
        # =========================================================

        optimization = solve_with_ortools(
            projects=[project],
            budget=payload.budget,
            project_cap=payload.project_cap,
            underserved_min_percent=0.0,
            priority=payload.priority,
            beneficiary_group=payload.beneficiary_group,
        )

        # =========================================================
        # 5. FINAL RESPONSE
        # =========================================================

        return {
            "success": True,
            "stage": "OPTIMIZED",
            "ai_analysis": analysis.model_dump(),
            "compliance": compliance.model_dump(),
            "optimization": optimization,
            "project": project,
        }

    except HTTPException:
        raise

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        )