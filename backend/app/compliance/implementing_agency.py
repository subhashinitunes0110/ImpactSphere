from typing import List, Tuple

from .schemas import ProjectComplianceInput


def evaluate_implementing_agency(
    data: ProjectComplianceInput,
) -> Tuple[bool, List[str], List[str]]:

    flags: List[str] = []
    reasons: List[str] = []

    # ---------------------------------------------------------
    # 1. IMPLEMENTING AGENCY REQUIRED
    # ---------------------------------------------------------

    if not data.implementing_agency:
        flags.append("AGENCY_MISSING")
        reasons.append(
            "No implementing agency was provided."
        )
        return False, flags, reasons

    # ---------------------------------------------------------
    # 2. CHECK ELIGIBLE AGENCY TYPE
    # ---------------------------------------------------------

    agency_type = (
        data.implementing_agency_type or ""
    ).strip().upper()

    eligible_type = agency_type in {
        "SECTION_8",
        "PUBLIC_TRUST",
        "REGISTERED_SOCIETY",
        "GOVERNMENT_ENTITY",
        "STATUTORY_BODY",
        "ELIGIBLE_ENTITY_WITH_3_YEAR_TRACK_RECORD",
    }

    # ---------------------------------------------------------
    # 3. CHECK ELIGIBILITY ATTRIBUTES
    # ---------------------------------------------------------

    eligible_attributes = any(
        [
            data.implementing_agency_registered_under_12a,
            data.implementing_agency_registered_under_80g,
            data.implementing_agency_government_established,
            data.implementing_agency_created_by_statute,
            data.implementing_agency_has_3_year_track_record,
        ]
    )

    if not eligible_type and not eligible_attributes:
        flags.append("AGENCY_NOT_ELIGIBLE")
        reasons.append(
            "The implementing agency does not match a supported "
            "CSR implementing-agency category."
        )
        return False, flags, reasons

    # ---------------------------------------------------------
    # 4. CSR-1 CHECK
    # ---------------------------------------------------------

    if data.csr1_required and not data.csr1_filed:
        flags.append("CSR1_MISSING")
        reasons.append(
            "CSR-1 filing is required but has not been marked as filed."
        )
        return False, flags, reasons

    if data.csr1_required and data.csr1_filed:
        reasons.append(
            "CSR-1 filing requirement is satisfied."
        )

    # ---------------------------------------------------------
    # 5. SUCCESS
    # ---------------------------------------------------------

    reasons.append(
        "Implementing agency satisfies the configured CSR "
        "eligibility checks."
    )

    return True, flags, reasons
