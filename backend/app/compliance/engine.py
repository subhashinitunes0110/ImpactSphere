from .exclusions import evaluate_exclusions
from .schedule_vii import match_schedule_vii
from .schemas import (
    ComplianceResult,
    ComplianceStatus,
    ProjectComplianceInput,
)

def evaluate_project(
    data: ProjectComplianceInput
) -> ComplianceResult:

    excluded, exclusion_flags = evaluate_exclusions(data)

    schedule = match_schedule_vii(
        data.activity_description,
        data.sector
    )

    flags = list(exclusion_flags)
    reasons = []

    category = (
        data.schedule_vii_category
        or schedule["category"]
    )

    if excluded:
        reasons.append(
            "One or more CSR exclusion conditions were detected."
        )

        return ComplianceResult(
            project_id=data.project_id,
            status=ComplianceStatus.REJECT,
            eligible=False,
            eligible_for_optimization=False,
            schedule_vii_category=category,
            schedule_vii_match=bool(schedule["match"]),
            flags=flags,
            reasons=reasons,
        )

    if (
        data.schedule_vii_category
        and schedule["match"]
        and data.schedule_vii_category != schedule["category"]
    ):
        flags.append("SCHEDULE_VII_MISMATCH")

        reasons.append(
            "Provided Schedule VII category differs from the "
            "deterministic activity match; human review is required."
        )

        return ComplianceResult(
            project_id=data.project_id,
            status=ComplianceStatus.REVIEW,
            eligible=False,
            eligible_for_optimization=False,
            schedule_vii_category=data.schedule_vii_category,
            schedule_vii_match=False,
            flags=flags,
            reasons=reasons,
        )

    if not schedule["match"]:
        flags.append("SCHEDULE_VII_UNCLEAR")

        reasons.append(
            "No clear Schedule VII activity match was detected; "
            "human review is required."
        )

        return ComplianceResult(
            project_id=data.project_id,
            status=ComplianceStatus.REVIEW,
            eligible=False,
            eligible_for_optimization=False,
            schedule_vii_category=data.schedule_vii_category,
            schedule_vii_match=False,
            flags=flags,
            reasons=reasons,
        )

    reasons.append(
        "No exclusion condition was detected and the activity "
        "has a Schedule VII match."
    )

    return ComplianceResult(
        project_id=data.project_id,
        status=ComplianceStatus.PASS,
        eligible=True,
        eligible_for_optimization=True,
        schedule_vii_category=category,
        schedule_vii_match=True,
        flags=flags,
        reasons=reasons,
    )
