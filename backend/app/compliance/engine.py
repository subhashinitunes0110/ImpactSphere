from typing import Any, Dict

from .exclusions import evaluate_exclusions
from .implementing_agency import evaluate_implementing_agency
from .schedule_vii import match_schedule_vii
from .schemas import (
    ComplianceResult,
    ComplianceStatus,
    ProjectComplianceInput,
)


def _project_payload(
    data: ProjectComplianceInput,
    category: str | None,
) -> Dict[str, Any]:

    project = {
        "id": data.project_id,
        "name": data.project_name,
        "description": data.activity_description,
        "budget": data.project_budget,
        "outlay": data.project_outlay,
        "location": data.location,
        "district": data.district or data.location,
        "state": data.state,
        "sector": data.sector,
        "beneficiary_group": data.beneficiary_group,
        "beneficiaries": data.beneficiaries,
        "expected_impact": data.expected_impact,
        "csr_alignment": data.csr_alignment,
        "feasibility": data.feasibility,
        "sustainability": data.sustainability,
        "schedule_vii_category": category,
    }

    return {
        key: value
        for key, value in project.items()
        if value is not None
    }


def _result(
    data: ProjectComplianceInput,
    status: ComplianceStatus,
    eligible: bool,
    schedule_vii_category: str | None,
    schedule_vii_match: bool,
    flags: list[str],
    reasons: list[str],
) -> ComplianceResult:

    return ComplianceResult(
        project_id=data.project_id,
        status=status,
        eligible=eligible,
        eligible_for_optimization=(
            status == ComplianceStatus.PASS
        ),
        schedule_vii_category=schedule_vii_category,
        schedule_vii_match=schedule_vii_match,
        flags=flags,
        reasons=reasons,
        project=_project_payload(
            data,
            schedule_vii_category,
        ),
    )


def evaluate_project(
    data: ProjectComplianceInput,
) -> ComplianceResult:

    # ---------------------------------------------------------
    # 1. CSR EXCLUSIONS
    # ---------------------------------------------------------

    excluded, exclusion_flags = evaluate_exclusions(data)

    # ---------------------------------------------------------
    # 2. SCHEDULE VII VALIDATION
    # ---------------------------------------------------------

    schedule = match_schedule_vii(
        data.activity_description,
        data.sector,
    )

    # ---------------------------------------------------------
    # 3. IMPLEMENTING AGENCY + CSR-1 VALIDATION
    # ---------------------------------------------------------

    agency_ok, agency_flags, agency_reasons = (
        evaluate_implementing_agency(data)
    )

    flags = list(exclusion_flags)
    flags.extend(agency_flags)

    reasons: list[str] = list(agency_reasons)

    category = (
        data.schedule_vii_category
        or schedule["category"]
    )

    # ---------------------------------------------------------
    # 4. EXCLUSION → REJECT
    # ---------------------------------------------------------

    if excluded:
        reasons.append(
            "One or more CSR exclusion conditions were detected."
        )

        return _result(
            data,
            ComplianceStatus.REJECT,
            False,
            category,
            bool(schedule["match"]),
            flags,
            reasons,
        )

    # ---------------------------------------------------------
    # 5. IMPLEMENTING AGENCY / CSR-1 → REVIEW
    # ---------------------------------------------------------

    if not agency_ok:
        reasons.append(
            "Implementing-agency compliance requires "
            "correction or human review."
        )

        return _result(
            data,
            ComplianceStatus.REVIEW,
            False,
            category,
            bool(schedule["match"]),
            flags,
            reasons,
        )

    # ---------------------------------------------------------
    # 6. SCHEDULE VII CATEGORY MISMATCH → REVIEW
    # ---------------------------------------------------------

    if (
        data.schedule_vii_category
        and schedule["match"]
        and data.schedule_vii_category
        != schedule["category"]
    ):
        flags.append("SCHEDULE_VII_MISMATCH")

        reasons.append(
            "Provided Schedule VII category differs from "
            "the deterministic activity match; human review "
            "is required."
        )

        return _result(
            data,
            ComplianceStatus.REVIEW,
            False,
            data.schedule_vii_category,
            False,
            flags,
            reasons,
        )

    # ---------------------------------------------------------
    # 7. SCHEDULE VII UNCLEAR → REVIEW
    # ---------------------------------------------------------

    if not schedule["match"]:
        flags.append("SCHEDULE_VII_UNCLEAR")

        reasons.append(
            "No clear Schedule VII activity match was detected; "
            "human review is required."
        )

        return _result(
            data,
            ComplianceStatus.REVIEW,
            False,
            data.schedule_vii_category,
            False,
            flags,
            reasons,
        )

    # ---------------------------------------------------------
    # 8. FULL COMPLIANCE → PASS
    # ---------------------------------------------------------

    reasons.append(
        "No exclusion condition was detected and the activity "
        "has a Schedule VII match."
    )

    return _result(
        data,
        ComplianceStatus.PASS,
        True,
        category,
        True,
        flags,
        reasons,
    )
