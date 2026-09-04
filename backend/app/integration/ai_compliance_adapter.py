from backend.app.schemas.ai import AIAnalysisResponse
from backend.app.compliance.schemas import ProjectComplianceInput


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


def _schedule_vii_category(category: str | None) -> str | None:
    if not category:
        return None

    normalized = category.strip().lower()

    if normalized.startswith("schedule vii"):
        return category.strip()

    return SCHEDULE_VII_MAP.get(normalized)


def _description(ai: AIAnalysisResponse) -> str:
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
) -> ProjectComplianceInput:

    project = ai.project
    classification = ai.classification

    project_name = (
        project.project_name
        or "Unnamed AI-analyzed project"
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
        location=project.location.district,
        district=project.location.district,
        state=project.location.state,
        implementing_agency=project.implementing_agency,
        project_budget=project.budget,
        beneficiaries=project.beneficiaries,
    )


def ai_review_required(
    ai: AIAnalysisResponse,
) -> bool:

    return bool(
        ai.classification.human_review_required
    )
