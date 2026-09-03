import re
from typing import Optional

from app.schemas.ai import ProjectAnalysis, Location


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def clean_text(value: Optional[str]) -> Optional[str]:
    if not value:
        return None

    value = re.sub(r"\s+", " ", value)
    value = value.strip(" .,:;-")

    return value if value else None


def extract_number(pattern: str, text: str) -> Optional[int]:
    match = re.search(pattern, text, re.IGNORECASE)

    if match:
        try:
            return int(match.group(1).replace(",", ""))
        except ValueError:
            return None

    return None


# =========================================================
# PROJECT NAME
# =========================================================

def extract_project_name(text: str) -> Optional[str]:

    patterns = [
        r"^\s*([A-Z][A-Za-z0-9 &'-]+(?:Initiative|Project|Program|Programme))\.",
        r"^\s*([A-Z][A-Za-z0-9 &'-]+(?:Initiative|Project|Program|Programme))",
    ]

    for pattern in patterns:
        match = re.search(pattern, text)

        if match:
            return clean_text(match.group(1))

    return None


# =========================================================
# LOCATION
# =========================================================

def extract_location(text: str) -> Location:

    district = None
    state = None

    # Example:
    # "in Barmer district of Rajasthan."
    match = re.search(
        r"\bin\s+([A-Za-z][A-Za-z .'-]*?)\s+district\s+of\s+([A-Za-z][A-Za-z .'-]*?)(?:[.,]|\s+The\s|\s+the\s|\s+and\s)",
        text,
        re.IGNORECASE,
    )

    if match:
        district = clean_text(match.group(1))
        state = clean_text(match.group(2))

    # Fallback district extraction
    if not district:
        match = re.search(
            r"\b([A-Za-z][A-Za-z .'-]*?)\s+district\b",
            text,
            re.IGNORECASE,
        )

        if match:
            district = clean_text(match.group(1))

    # Explicit state list
    states = [
        "Rajasthan",
        "Gujarat",
        "Maharashtra",
        "Madhya Pradesh",
        "Uttar Pradesh",
        "Bihar",
        "Jharkhand",
        "Odisha",
        "West Bengal",
        "Tamil Nadu",
        "Kerala",
        "Karnataka",
        "Telangana",
        "Andhra Pradesh",
        "Punjab",
        "Haryana",
        "Himachal Pradesh",
        "Uttarakhand",
        "Assam",
        "Chhattisgarh",
        "Delhi",
    ]

    # Always prefer an exact known state
    for item in states:
        if re.search(
            rf"\b{re.escape(item)}\b",
            text,
            re.IGNORECASE,
        ):
            state = item
            break

    return Location(
        district=district,
        state=state,
    )


# =========================================================
# DURATION
# =========================================================

def extract_duration(text: str) -> Optional[int]:

    return extract_number(
        r"(\d+)\s*(?:months?|month)",
        text,
    )


# =========================================================
# BENEFICIARIES
# =========================================================

def extract_beneficiaries(text: str) -> Optional[int]:

    patterns = [
        r"benefit\s+(?:approximately\s+)?([\d,]+)\s*(?:people|persons|beneficiaries)",
        r"beneficiaries?\s*(?:of|:)?\s*([\d,]+)",
        r"reach\s+(?:approximately\s+)?([\d,]+)\s*(?:people|persons)",
    ]

    for pattern in patterns:

        result = extract_number(
            pattern,
            text,
        )

        if result is not None:
            return result

    return None


# =========================================================
# BUDGET
# =========================================================

def extract_budget(text: str) -> Optional[float]:

    patterns = [
        r"(?:budget|cost|project cost|estimated cost)"
        r"\s*(?:is|of|:)?\s*₹?\s*([\d,]+(?:\.\d+)?)\s*(?:crore|cr)?",

        r"₹\s*([\d,]+(?:\.\d+)?)\s*(?:crore|cr|lakh)?",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if match:

            try:

                value = float(
                    match.group(1).replace(",", "")
                )

                full_match = match.group(0).lower()

                if "crore" in full_match or "cr" in full_match:
                    value *= 10_000_000

                elif "lakh" in full_match:
                    value *= 100_000

                return value

            except ValueError:
                pass

    return None


# =========================================================
# BENEFICIARY GROUPS
# =========================================================

def extract_beneficiary_groups(text: str):

    groups = []

    keywords = {
        "senior citizens": [
            "senior citizens",
            "elderly",
            "older people",
        ],
        "children": [
            "children",
            "students",
            "kids",
        ],
        "women": [
            "women",
            "girls",
        ],
        "rural communities": [
            "rural communities",
            "rural families",
            "villages",
        ],
        "low-income communities": [
            "low-income",
            "low income",
            "poor communities",
        ],
        "persons with disabilities": [
            "persons with disabilities",
            "people with disabilities",
            "disabled",
        ],
    }

    text_lower = text.lower()

    for group, terms in keywords.items():

        if any(term in text_lower for term in terms):
            groups.append(group)

    return groups


# =========================================================
# INTERVENTION
# =========================================================

def extract_intervention(text: str) -> Optional[str]:

    categories = [
        "healthcare",
        "education",
        "livelihood",
        "women empowerment",
        "water and sanitation",
        "environment",
        "sports",
        "rural development",
        "skill development",
        "disaster management",
    ]

    text_lower = text.lower()

    for category in categories:

        if category in text_lower:
            return category

    # Additional healthcare detection
    if any(
        word in text_lower
        for word in [
            "medical",
            "doctor",
            "medicines",
            "healthcare",
            "health services",
        ]
    ):
        return "healthcare"

    return None


# =========================================================
# OBJECTIVES
# =========================================================

def extract_objectives(text: str):

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text.strip(),
    )

    objectives = []

    objective_words = [
        "provide",
        "establish",
        "improve",
        "increase",
        "support",
        "enable",
        "create",
        "develop",
        "reduce",
        "promote",
    ]

    for sentence in sentences:

        sentence = clean_text(sentence)

        if not sentence:
            continue

        lower = sentence.lower()

        if any(
            word in lower
            for word in objective_words
        ):
            objectives.append(sentence)

    return objectives[:5]


# =========================================================
# EXPECTED OUTCOMES
# =========================================================

def extract_expected_outcomes(text: str):

    outcomes = []

    # Explicit outcome statements
    patterns = [
        r"expected to benefit approximately\s+([\d,]+)\s+(?:people|persons|beneficiaries)",
        r"expected to\s+([^.]*)",
        r"outcomes?\s*(?:are|include|:)\s*([^.]*)",
    ]

    for pattern in patterns:

        matches = re.findall(
            pattern,
            text,
            re.IGNORECASE,
        )

        for match in matches:

            value = clean_text(match)

            if not value:
                continue

            # Reconstruct numeric beneficiary outcome
            if value.replace(",", "").isdigit():
                value = f"benefit approximately {value} people"

            if len(value) > 5:
                outcomes.append(value)

    # Remove duplicates
    unique = []

    for outcome in outcomes:
        if outcome not in unique:
            unique.append(outcome)

    return unique[:5]


# =========================================================
# SUMMARY
# =========================================================

def generate_summary(
    text: str,
    project_name: Optional[str],
    intervention: Optional[str],
    beneficiaries: Optional[int],
    location: Location,
):

    parts = []

    if project_name:
        parts.append(project_name)

    if intervention:
        parts.append(
            f"focuses on {intervention}"
        )

    if location.district and location.state:
        parts.append(
            f"in {location.district}, {location.state}"
        )

    if beneficiaries:
        parts.append(
            f"targeting approximately {beneficiaries:,} beneficiaries"
        )

    if parts:
        return "The project " + " ".join(parts) + "."

    return clean_text(text[:500])


# =========================================================
# MAIN EXTRACTION FUNCTION
# =========================================================

def extract_project_info(text: str) -> ProjectAnalysis:

    if not text or not text.strip():
        raise ValueError(
            "Project text cannot be empty."
        )

    text = text.strip()

    project_name = extract_project_name(text)

    location = extract_location(text)

    budget = extract_budget(text)

    duration = extract_duration(text)

    beneficiaries = extract_beneficiaries(text)

    beneficiary_groups = extract_beneficiary_groups(
        text
    )

    intervention = extract_intervention(
        text
    )

    objectives = extract_objectives(
        text
    )

    expected_outcomes = extract_expected_outcomes(
        text
    )

    summary = generate_summary(
        text=text,
        project_name=project_name,
        intervention=intervention,
        beneficiaries=beneficiaries,
        location=location,
    )

    return ProjectAnalysis(
        project_name=project_name,
        location=location,
        budget=budget,
        duration_months=duration,
        beneficiaries=beneficiaries,
        beneficiary_groups=beneficiary_groups,
        intervention=intervention,
        objectives=objectives,
        expected_outcomes=expected_outcomes,
        implementing_agency=None,
        description=text,
        summary=summary,
    )