from typing import Any, Dict, Optional

from backend.app.schemas.ai import AIAnalysisResponse
from backend.app.compliance.engine import evaluate_project
from backend.app.compliance.schemas import (
    ComplianceResult,
    ProjectComplianceInput,
)


SCHEDULE_VII_MAP = {
    "healthcare": "Schedule VII(i)",
    "health": "Schedule VII(i)",
    "education": "Schedule VII(ii)",
    "skill development": "Schedule VII(ii)",
    "vocational training": "Schedule VII(ii)",
    "women empowerment": "Schedule VII(iii)",
    "gender equality": "Schedule VII(iii)",
    "environment": "Schedule VII(iv)",
    "environmental sustainability": "Schedule VII(iv)",
    "rural development": "Schedule VII(x)",
    "slum development": "Schedule VII(xi)",
    "disaster management": "Schedule VII(xii)",
}


def _schedule_vii_category(
    category: Optional[str],
) -> Optional[str]:

    if not category:
        return None

    normalized = category.strip().lower()

    if normalized.startswith("schedule vii"):
        return category.strip()

    return SCHEDULE_VII_MAP.get(normalized)


def _location_value(
    ai: AIAnalysisResponse,
    field: str,
) -> Optional[str]:

    location = ai.project.location

    if hasattr(location, field):
        value = getattr(location, field, None)

        if value and str(value).strip():
            return str(value).strip()

        return None

    if isinstance(location, dict):
        value = location.get(field)

        if value and str(value).strip():
            return str(value).strip()

        return None

    return None


def _description(
    ai: AIAnalysisResponse,
) -> str:

    project = ai.project

    parts = [
        project.description,
        project.summary,
        project.intervention,
        *project.objectives,
        *project.expected_outcomes,
    ]

    text = " ".join(
        str(part).strip()
        for part in parts
        if part and str(part).strip()
    )

    return (
        text
        or project.project_name
        or "AI-analyzed CSR project"
    )


def ai_analysis_to_compliance_input(
    ai: AIAnalysisResponse,
    compliance_context: Optional[Dict[str, Any]] = None,
) -> ProjectComplianceInput:

    compliance_context = compliance_context or {}

    project = ai.project
    classification = ai.classification

    project_name = (
        project.project_name
        or "Unnamed AI-analyzed project"
    )

    district = _location_value(ai, "district")
    state = _location_value(ai, "state")

    return ProjectComplianceInput(
        project_id=(
            f"AI-{project_name.strip().lower()}"
            .replace(" ", "-")[:60]
        ),

        project_name=project_name,

        activity_description=_description(ai),

        sector=classification.category,

        schedule_vii_category=_schedule_vii_category(
            classification.category
        ),

        beneficiary_group=(
            ", ".join(project.beneficiary_groups)
            if project.beneficiary_groups
            else None
        ),

        location=district,
        district=district,
        state=state,

        implementing_agency=(
            compliance_context.get(
                "implementing_agency"
            )
            or project.implementing_agency
        ),

        implementing_agency_type=(
            compliance_context.get(
                "implementing_agency_type"
            )
        ),

        implementing_agency_csr_registration_number=(
            compliance_context.get(
                "implementing_agency_csr_registration_number"
            )
        ),

        implementing_agency_registered_under_12a=(
            compliance_context.get(
                "implementing_agency_registered_under_12a",
                False,
            )
        ),

        implementing_agency_registered_under_80g=(
            compliance_context.get(
                "implementing_agency_registered_under_80g",
                False,
            )
        ),

        implementing_agency_government_established=(
            compliance_context.get(
                "implementing_agency_government_established",
                False,
            )
        ),

        implementing_agency_created_by_statute=(
            compliance_context.get(
                "implementing_agency_created_by_statute",
                False,
            )
        ),

        implementing_agency_has_3_year_track_record=(
            compliance_context.get(
                "implementing_agency_has_3_year_track_record",
                False,
            )
        ),

        csr1_required=(
            compliance_context.get(
                "csr1_required",
                True,
            )
        ),

        csr1_filed=(
            compliance_context.get(
                "csr1_filed",
                False,
            )
        ),

        project_budget=(
            compliance_context.get(
                "project_budget"
            )
            if compliance_context.get(
                "project_budget"
            ) is not None
            else project.budget
        ),

        beneficiaries=(
            compliance_context.get(
                "project_beneficiaries"
            )
            if compliance_context.get(
                "project_beneficiaries"
            ) is not None
            else project.beneficiaries
        ),
    )


def ai_review_required(
    ai: AIAnalysisResponse,
) -> bool:

    return bool(
        ai.classification.human_review_required
    )


def evaluate_ai_compliance(
    ai: AIAnalysisResponse,
    compliance_context: Optional[Dict[str, Any]] = None,
) -> ComplianceResult:

    compliance_input = ai_analysis_to_compliance_input(
        ai,
        compliance_context,
    )

    result = evaluate_project(
        compliance_input
    )

    if ai_review_required(ai):

        result.status = "REVIEW"

        result.eligible = False

        result.eligible_for_optimization = False

        if "AI_LOW_CONFIDENCE" not in result.flags:
            result.flags.append(
                "AI_LOW_CONFIDENCE"
            )

        result.reasons.append(
            "AI classification requires human review "
            "before legal eligibility is finalized."
        )

    return result


def compliance_result_to_project(
    ai: AIAnalysisResponse,
    compliance: ComplianceResult,
) -> Dict[str, Any]:

    project = ai.project

    district = _location_value(
        ai,
        "district",
    )

    state = _location_value(
        ai,
        "state",
    )

    project_name = (
        project.project_name
        or "Unnamed AI-analyzed project"
    )

    optimization_project = {
        "id": compliance.project_id,

        "name": project_name,

        "description": _description(ai),

        "district": district,

        "state": state,

        "location": district,

        "sector": ai.classification.category,

        "beneficiary_group": (
            ", ".join(project.beneficiary_groups)
            if project.beneficiary_groups
            else ""
        ),

        "beneficiaries": (
            project.beneficiaries
            if project.beneficiaries is not None
            else 0
        ),

        "budget": (
            project.budget
            if project.budget is not None
            else 0.0
        ),

        "expected_impact": 75.0,

        "csr_alignment": 80.0,

        "feasibility": 85.0,

        "sustainability": 80.0,

        "compliance": compliance.model_dump(),

        "ai_confidence": (
            ai.classification.confidence
        ),

        "ai_confidence_level": (
            ai.classification.confidence_level
        ),

        "human_review_required": (
            ai.classification.human_review_required
        ),

        "schedule_vii_category": (
            compliance.schedule_vii_category
        ),
    }

    return optimization_project


def ai_analysis_to_optimization_project(
    ai: AIAnalysisResponse,
    compliance_context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:

    compliance = evaluate_ai_compliance(
        ai,
        compliance_context,
    )

    return compliance_result_to_project(
        ai,
        compliance,
    )