from typing import Any, Dict, Optional

from backend.app.compliance.engine import evaluate_project
from backend.app.compliance.schemas import (
    ComplianceResult,
    ComplianceStatus,
    ProjectComplianceInput,
)
from backend.app.schemas.ai import AIAnalysisResponse


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
    category: str | None,
) -> str | None:

    if not category:
        return None

    normalized = category.strip().lower()

    if normalized.startswith("schedule vii"):
        return category.strip()

    return SCHEDULE_VII_MAP.get(normalized)


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


def _location_value(
    ai: AIAnalysisResponse,
    field: str,
) -> Optional[str]:

    location = ai.project.location

    # Pydantic model
    if hasattr(location, field):

        value = getattr(
            location,
            field,
            None,
        )

        if value and str(value).strip():
            return str(value).strip()

        return None

    # Dictionary fallback
    if isinstance(location, dict):

        value = location.get(field)

        if value and str(value).strip():
            return str(value).strip()

        return None

    return None


def ai_analysis_to_compliance_input(
    ai: AIAnalysisResponse,
    compliance_context: Optional[Dict[str, Any]] = None,
) -> ProjectComplianceInput:

    project = ai.project

    classification = ai.classification

    context = compliance_context or {}

    project_name = (
        project.project_name
        or "Unnamed AI-analyzed project"
    )

    district = _location_value(
        ai,
        "district",
    )

    state = _location_value(
        ai,
        "state",
    )

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

        # -------------------------------------------------
        # IMPLEMENTING AGENCY
        # -------------------------------------------------

        implementing_agency=(
            project.implementing_agency
            or context.get("implementing_agency")
        ),

        implementing_agency_type=context.get(
            "implementing_agency_type"
        ),

        implementing_agency_csr_registration_number=context.get(
            "implementing_agency_csr_registration_number"
        ),

        implementing_agency_registered_under_12a=bool(
            context.get(
                "implementing_agency_registered_under_12a",
                False,
            )
        ),

        implementing_agency_registered_under_80g=bool(
            context.get(
                "implementing_agency_registered_under_80g",
                False,
            )
        ),

        implementing_agency_government_established=bool(
            context.get(
                "implementing_agency_government_established",
                False,
            )
        ),

        implementing_agency_created_by_statute=bool(
            context.get(
                "implementing_agency_created_by_statute",
                False,
            )
        ),

        implementing_agency_has_3_year_track_record=bool(
            context.get(
                "implementing_agency_has_3_year_track_record",
                False,
            )
        ),

        # -------------------------------------------------
        # CSR-1
        # -------------------------------------------------

        csr1_required=bool(
            context.get(
                "csr1_required",
                True,
            )
        ),

        csr1_filed=bool(
            context.get(
                "csr1_filed",
                False,
            )
        ),

        # -------------------------------------------------
        # PROJECT DATA
        # -------------------------------------------------

        project_budget=project.budget,

        beneficiaries=project.beneficiaries,
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

    # -------------------------------------------------
    # AI CONFIDENCE GATE
    # -------------------------------------------------

    if ai_review_required(ai):

        result.status = ComplianceStatus.REVIEW

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
    result: ComplianceResult,
) -> Dict[str, Any]:

    project = dict(
        result.project
    )

    # Always provide the keys expected by
    # downstream Impact / Optimization engines.

    project.setdefault(
        "district",
        None,
    )

    project.setdefault(
        "state",
        None,
    )

    project["compliance"] = {

        "status": result.status.value,

        "eligible": result.eligible,

        "eligible_for_optimization": (
            result.eligible_for_optimization
        ),

        "schedule_vii_category": (
            result.schedule_vii_category
        ),

        "schedule_vii_match": (
            result.schedule_vii_match
        ),

        "flags": list(
            result.flags
        ),

        "reasons": list(
            result.reasons
        ),
    }

    return project


def ai_analysis_to_optimization_project(
    ai: AIAnalysisResponse,
    compliance_context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:

    result = evaluate_ai_compliance(
        ai,
        compliance_context,
    )

    return compliance_result_to_project(
        result
    )