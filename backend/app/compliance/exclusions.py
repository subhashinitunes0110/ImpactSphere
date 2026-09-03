from typing import List, Tuple
from .schemas import ProjectComplianceInput

def evaluate_exclusions(
    data: ProjectComplianceInput
) -> Tuple[bool, List[str]]:

    flags: List[str] = []

    if data.normal_business_activity_indicator:
        flags.append("EXCL_NORMAL_BUSINESS")

    if data.international_activity_indicator:
        flags.append("EXCL_OUTSIDE_INDIA")

    if data.political_contribution_indicator:
        flags.append("EXCL_POLITICAL")

    if data.employee_benefit_indicator:
        flags.append("EXCL_EMPLOYEE_BENEFIT")

    if data.statutory_obligation_indicator:
        flags.append("EXCL_STATUTORY_OBLIGATION")

    if data.marketing_sponsorship_indicator:
        flags.append("EXCL_SPONSORSHIP_MARKETING")

    return bool(flags), flags
