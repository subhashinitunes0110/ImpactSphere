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

    implementing_agency: str | None = None
    implementing_agency_type: str | None = None
    implementing_agency_csr_registration_number: str | None = None

    implementing_agency_registered_under_12a: bool = False
    implementing_agency_registered_under_80g: bool = False
    implementing_agency_government_established: bool = False
    implementing_agency_created_by_statute: bool = False
    implementing_agency_has_3_year_track_record: bool = False

    csr1_required: bool = True
    csr1_filed: bool = False

    budget: float = Field(default=50000000.0, ge=0)
    project_budget: float | None = Field(default=None, ge=0)
    project_beneficiaries: int | None = Field(default=None, ge=0)

    project_cap: float = Field(default=7500000.0, ge=0)
    underserved_min_percent: float = Field(default=20.0, ge=0)

    priority: str = "maximum_impact"
    beneficiary_group: str | None = None


def _compliance_context(
    payload: IntegratedOptimizationRequest,
) -> Dict[str, Any]:
    return {
        "implementing_agency": payload.implementing_agency,
        "implementing_agency_type": payload.implementing_agency_type,
        "implementing_agency_csr_registration_number":
            payload.implementing_agency_csr_registration_number,
        "implementing_agency_registered_under_12a":
            payload.implementing_agency_registered_under_12a,
        "implementing_agency_registered_under_80g":
            payload.implementing_agency_registered_under_80g,
        "implementing_agency_government_established":
            payload.implementing_agency_government_established,
        "implementing_agency_created_by_statute":
            payload.implementing_agency_created_by_statute,
        "implementing_agency_has_3_year_track_record":
            payload.implementing_agency_has_3_year_track_record,
        "csr1_required": payload.csr1_required,
        "csr1_filed": payload.csr1_filed,
    }


@router.post("/ai-compliance")
def check_ai_analysis(
    analysis: AIAnalysisResponse,
) -> ComplianceResult:
    return evaluate_ai_compliance(analysis)


@router.post("/analyze-and-check")
def analyze_and_check(
    payload: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Full AI → Compliance pipeline.

    Returns both:
    1. AI analysis
    2. Deterministic CSR compliance result
    """

    text = str(payload.get("text", "")).strip()
    needs = payload.get("needs") or []

    if not text:
        raise HTTPException(
            status_code=400,
            detail="Proposal text cannot be empty.",
        )

    try:
        # STEP 1:
        # AI extracts project information, classifies the project,
        # and matches community needs.
        ai_result = analyze_proposal(text, needs)

        analysis = AIAnalysisResponse.model_validate(ai_result)

        # STEP 2:
        # Deterministic compliance engine validates the AI result.
        compliance = evaluate_ai_compliance(
            analysis,
            payload,
        )

        # IMPORTANT:
        # Frontend expects BOTH ai_analysis and compliance.
        return {
            "success": True,
            "ai_analysis": analysis.model_dump(),
            "compliance": compliance.model_dump(),
        }

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

        project = ai_analysis_to_optimization_project(
            analysis,
            payload,
        )

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
        # ---------------------------------------------------------
        # STEP 1 — AI ANALYSIS
        # ---------------------------------------------------------
        ai_result = analyze_proposal(
            text,
            payload.needs,
        )

        analysis = AIAnalysisResponse.model_validate(
            ai_result
        )

        # ---------------------------------------------------------
        # STEP 2 — COMPLIANCE
        # ---------------------------------------------------------
        context = _compliance_context(payload)

        compliance = evaluate_ai_compliance(
            analysis,
            context,
        )

        # ---------------------------------------------------------
        # STEP 3 — COMPLIANCE GATE
        # ---------------------------------------------------------
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

        # ---------------------------------------------------------
        # STEP 4 — CONVERT TO OPTIMIZATION PROJECT
        # ---------------------------------------------------------
        project = ai_analysis_to_optimization_project(
            analysis,
            context,
        )

        if payload.project_budget is not None:
            project["budget"] = payload.project_budget

        if payload.project_beneficiaries is not None:
            project["beneficiaries"] = (
                payload.project_beneficiaries
            )

        project["budget"] = project.get(
            "budget",
            0.0,
        ) or 0.0

        project["beneficiaries"] = project.get(
            "beneficiaries",
            0,
        ) or 0

        # ---------------------------------------------------------
        # STEP 5 — OR-TOOLS OPTIMIZATION
        # ---------------------------------------------------------
        optimization = solve_with_ortools(
            projects=[project],
            budget=payload.budget,
            project_cap=payload.project_cap,
            underserved_min_percent=0.0,
            priority=payload.priority,
            beneficiary_group=payload.beneficiary_group,
        )

        # ---------------------------------------------------------
        # STEP 6 — COMPLETE RESPONSE
        # ---------------------------------------------------------
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