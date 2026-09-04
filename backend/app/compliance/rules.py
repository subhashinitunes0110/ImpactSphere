"""
Impact Sphere - CSR Compliance Rules

This module contains deterministic CSR screening rules.

Important:
These rules are intended for decision-support and screening.
They are not a substitute for legal advice or professional
CSR compliance review.
"""

from typing import Optional


# ============================================================
# SECTION 135 THRESHOLDS
# ============================================================

NET_WORTH_THRESHOLD_CRORE = 500
TURNOVER_THRESHOLD_CRORE = 1000
NET_PROFIT_THRESHOLD_CRORE = 5

CSR_PERCENTAGE = 0.02

# Administrative overhead ceiling
ADMINISTRATIVE_OVERHEAD_LIMIT_PERCENT = 5.0

# If CSR obligation is <= ₹50 lakh, CSR Committee is generally
# not required and the Board performs the relevant functions.
CSR_COMMITTEE_THRESHOLD_CRORE = 0.50


# ============================================================
# SCHEDULE VII CATEGORIES
# ============================================================

SCHEDULE_VII_CATEGORIES = {
    "healthcare": [
        "health",
        "healthcare",
        "health care",
        "hospital",
        "medical",
        "medicine",
        "malnutrition",
        "hunger",
        "poverty",
        "sanitation",
        "safe drinking water",
        "drinking water",
    ],

    "education": [
        "education",
        "school",
        "learning",
        "literacy",
        "student",
        "scholarship",
        "vocational skills",
        "skill development",
        "livelihood",
        "employment skills",
    ],

    "women_empowerment": [
        "women empowerment",
        "women",
        "gender equality",
        "gender",
        "girl child",
        "female",
    ],

    "senior_citizens": [
        "senior citizen",
        "elderly",
        "old age",
        "aged persons",
    ],

    "environment": [
        "environment",
        "environmental",
        "forest",
        "afforestation",
        "biodiversity",
        "climate",
        "renewable energy",
        "solar",
        "water conservation",
        "natural resources",
    ],

    "rural_development": [
        "rural development",
        "rural area",
        "rural",
        "village development",
        "village",
    ],

    "slum_development": [
        "slum development",
        "slum",
        "slum area",
    ],

    "sports": [
        "sports",
        "sport",
        "athlete",
        "athletics",
        "training sports",
    ],

    "heritage": [
        "heritage",
        "culture",
        "art",
        "historical",
        "monument",
    ],

    "disaster_management": [
        "disaster management",
        "disaster relief",
        "disaster",
        "relief",
        "rehabilitation",
        "emergency response",
    ],

    "science_and_technology": [
        "science",
        "technology",
        "research",
        "innovation",
        "research and development",
        "r&d",
        "incubator",
        "engineering",
    ],

    "veterans": [
        "armed forces",
        "veteran",
        "war widow",
        "ex-servicemen",
        "paramilitary",
    ],
}


# ============================================================
# EXCLUSION KEYWORDS
# ============================================================

EXCLUSION_KEYWORDS = {
    "normal_business_activity": [
        "normal business",
        "ordinary course of business",
        "core business activity",
    ],

    "political_contribution": [
        "political party",
        "political contribution",
        "election campaign",
        "political donation",
    ],

    "employee_benefit": [
        "employee benefit",
        "employee welfare",
        "employees only",
        "staff welfare",
    ],

    "marketing_sponsorship": [
        "brand promotion",
        "marketing campaign",
        "advertising",
        "commercial sponsorship",
        "product promotion",
    ],

    "statutory_obligation": [
        "statutory obligation",
        "legal obligation",
        "mandatory under law",
        "compliance requirement",
    ],
}


# ============================================================
# SECTION 135 APPLICABILITY
# ============================================================

def check_section_135_applicability(
    net_worth_crore: Optional[float],
    turnover_crore: Optional[float],
    net_profit_crore: Optional[float],
) -> tuple[bool, list[str]]:
    """
    Check whether a company crosses any Section 135 threshold.

    CSR provisions apply when ANY ONE of the following is met
    in the immediately preceding financial year:

    - Net worth >= ₹500 crore
    - Turnover >= ₹1,000 crore
    - Net profit >= ₹5 crore
    """

    reasons = []

    if net_worth_crore is not None:
        if net_worth_crore >= NET_WORTH_THRESHOLD_CRORE:
            reasons.append(
                f"Net worth is ₹{net_worth_crore:.2f} crore "
                f"(threshold: ₹{NET_WORTH_THRESHOLD_CRORE} crore)."
            )

    if turnover_crore is not None:
        if turnover_crore >= TURNOVER_THRESHOLD_CRORE:
            reasons.append(
                f"Turnover is ₹{turnover_crore:.2f} crore "
                f"(threshold: ₹{TURNOVER_THRESHOLD_CRORE} crore)."
            )

    if net_profit_crore is not None:
        if net_profit_crore >= NET_PROFIT_THRESHOLD_CRORE:
            reasons.append(
                f"Net profit is ₹{net_profit_crore:.2f} crore "
                f"(threshold: ₹{NET_PROFIT_THRESHOLD_CRORE} crore)."
            )

    return len(reasons) > 0, reasons


# ============================================================
# CSR OBLIGATION CALCULATION
# ============================================================

def calculate_required_csr(
    average_net_profit_crore: Optional[float],
) -> Optional[float]:
    """
    Calculate the basic CSR obligation as 2% of the average
    net profits of the immediately preceding three financial years.
    """

    if average_net_profit_crore is None:
        return None

    if average_net_profit_crore < 0:
        return 0.0

    return round(
        average_net_profit_crore * CSR_PERCENTAGE,
        4,
    )


# ============================================================
# ADMINISTRATIVE OVERHEAD CHECK
# ============================================================

def check_administrative_overhead(
    administrative_overheads_crore: float,
    csr_spent_crore: float,
) -> tuple[float, bool]:
    """
    Calculate administrative overhead percentage and check
    against the configured 5% ceiling.

    Returns:
        (percentage, compliant)
    """

    if csr_spent_crore <= 0:
        return 0.0, True

    percentage = (
        administrative_overheads_crore
        / csr_spent_crore
    ) * 100

    compliant = percentage <= ADMINISTRATIVE_OVERHEAD_LIMIT_PERCENT

    return round(percentage, 2), compliant


# ============================================================
# CSR COMMITTEE REQUIREMENT
# ============================================================

def check_csr_committee_required(
    csr_obligation_crore: Optional[float],
) -> bool:
    """
    For a CSR obligation of ₹50 lakh or less, the CSR Committee
    requirement does not apply and the Board performs the relevant
    functions.

    ₹50 lakh = ₹0.50 crore.
    """

    if csr_obligation_crore is None:
        return True

    return csr_obligation_crore > CSR_COMMITTEE_THRESHOLD_CRORE


# ============================================================
# SCHEDULE VII CATEGORY DETECTION
# ============================================================

def detect_schedule_vii_category(
    text: str,
) -> Optional[str]:
    """
    Deterministic keyword-based fallback for Schedule VII
    category detection.

    The AI classification model should normally provide the
    category. This function acts as a transparent fallback.
    """

    if not text:
        return None

    text_lower = text.lower()

    category_scores = {}

    for category, keywords in SCHEDULE_VII_CATEGORIES.items():

        score = 0

        for keyword in keywords:
            if keyword.lower() in text_lower:
                score += 1

        if score > 0:
            category_scores[category] = score

    if not category_scores:
        return None

    return max(
        category_scores,
        key=category_scores.get,
    )


# ============================================================
# SCHEDULE VII ALIGNMENT
# ============================================================

def check_schedule_vii_alignment(
    text: str,
    ai_category: Optional[str] = None,
) -> tuple[bool, Optional[str]]:
    """
    Determine whether a project appears aligned with a
    Schedule VII category.

    AI category is preferred when supplied.
    Otherwise the deterministic keyword classifier is used.
    """

    detected_category = ai_category

    if not detected_category:
        detected_category = detect_schedule_vii_category(text)

    if not detected_category:
        return False, None

    return True, detected_category


# ============================================================
# IMPLEMENTING AGENCY CHECK
# ============================================================

def check_implementing_agency(
    implementing_agency: Optional[str],
    csr_registration_number: Optional[str],
    csr1_valid: Optional[bool],
) -> tuple[str, str]:
    """
    Check whether implementing-agency information is available.

    We intentionally do NOT assume that an agency is CSR-1
    compliant merely because a name or registration number
    has been entered.
    """

    if not implementing_agency:
        return (
            "REVIEW",
            "Implementing agency information is missing."
        )

    if csr1_valid is True:
        return (
            "PASS",
            "Implementing agency CSR-1 status has been verified."
        )

    if csr1_valid is False:
        return (
            "FLAG",
            "Implementing agency CSR-1 status could not be validated."
        )

    if not csr_registration_number:
        return (
            "REVIEW",
            "Implementing agency is provided, but CSR-1 "
            "registration details are missing."
        )

    return (
        "REVIEW",
        "CSR-1 registration number is provided, but "
        "verification is still required."
    )


# ============================================================
# EXCLUSION CHECK
# ============================================================

def check_exclusions(
    normal_business_activity: bool,
    political_contribution: bool,
    employee_benefit: bool,
    marketing_sponsorship: bool,
    statutory_obligation: bool,
) -> tuple[str, list[str]]:
    """
    Check activities that may fall outside permissible CSR
    expenditure categories.
    """

    flags = []

    if normal_business_activity:
        flags.append(
            "Project may constitute normal business activity."
        )

    if political_contribution:
        flags.append(
            "Project may involve a political contribution."
        )

    if employee_benefit:
        flags.append(
            "Project appears to primarily provide employee benefits."
        )

    if marketing_sponsorship:
        flags.append(
            "Project may be primarily a marketing or sponsorship activity."
        )

    if statutory_obligation:
        flags.append(
            "Project may be an expenditure required under another law."
        )

    if flags:
        return "FLAG", flags

    return "PASS", []


# ============================================================
# OUTSIDE INDIA CHECK
# ============================================================

def check_location(
    outside_india: bool,
) -> tuple[str, str]:
    """
    Flag projects outside India for review.

    Certain statutory exceptions may exist, so this is a
    screening flag rather than an automatic legal conclusion.
    """

    if outside_india:
        return (
            "REVIEW",
            "Project is outside India and requires verification "
            "against applicable CSR exceptions."
        )

    return (
        "PASS",
        "Project location is within India."
    )