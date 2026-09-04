import re
from typing import Optional

from backend.app.schemas.ai import ProjectAnalysis, Location


# =========================================================
# TEXT CLEANING
# =========================================================

def clean_text(text: str) -> str:
    """
    Normalize extracted proposal text.
    """
    if not text:
        return ""

    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)

    return text.strip()


def first_match(patterns, text, flags=re.IGNORECASE):
    """
    Try multiple regex patterns and return the first capture group.
    """
    for pattern in patterns:
        match = re.search(pattern, text, flags)
        if match:
            return match.group(1).strip()

    return None


def clean_sentence(value: Optional[str]) -> Optional[str]:
    """
    Clean a short extracted field without allowing it to consume
    the rest of the proposal.
    """
    if not value:
        return None

    value = value.strip()

    # Stop at the first sentence boundary.
    value = re.split(r"[.!?]\s+", value, maxsplit=1)[0]

    return value.strip(" .,:;-")


# =========================================================
# PROJECT NAME
# =========================================================

def extract_project_name(text: str) -> Optional[str]:

    # Explicit "Project Name:" / "Project Title:"
    value = first_match(
        [
            r"(?:project\s*name|project\s*title)\s*[:\-]\s*([^\n.!?]+)",
            r"(?:initiative\s*name|program\s*name)\s*[:\-]\s*([^\n.!?]+)",
        ],
        text,
    )

    if value:
        return value.strip(" .:-")


    # Example:
    # "Rural Healthcare Initiative will provide..."
    match = re.search(
        r"\b([A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+){1,6})\s+"
        r"(?:will|aims|seeks|plans|proposes)\b",
        text,
    )

    if match:
        return match.group(1).strip()


    # If the first sentence begins with a likely project title,
    # use only the first sentence.
    sentences = re.split(r"(?<=[.!?])\s+", text)

    if sentences:
        first_sentence = sentences[0].strip()

        ignored = {
            "project proposal",
            "proposal",
            "csr proposal",
            "project description",
            "executive summary",
        }

        if first_sentence.lower() not in ignored:
            candidate = first_sentence

            # Remove common leading labels.
            candidate = re.sub(
                r"^(?:project\s*name|project\s*title)\s*[:\-]\s*",
                "",
                candidate,
                flags=re.IGNORECASE,
            )

            # If sentence contains a descriptive phrase, keep the
            # first short title-like portion.
            candidate = re.split(
                r"\b(?:this project|the project|a project)\b",
                candidate,
                maxsplit=1,
                flags=re.IGNORECASE,
            )[0]

            candidate = candidate.strip(" .:-")

            if candidate:
                return candidate[:150]

    return None


# =========================================================
# LOCATION
# =========================================================

INDIAN_STATES = [
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Assam",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal",
]


def extract_location(text: str) -> Location:

    district = None
    state = None

    # -----------------------------------------------------
    # Pattern 1:
    # "Dharwad district of Karnataka"
    # -----------------------------------------------------
    match = re.search(
        r"\bin\s+([A-Za-z][A-Za-z'-]*(?:\s+[A-Za-z][A-Za-z'-]*){0,5})"
        r"\s+district\s+of\s+("
        + "|".join(re.escape(s) for s in sorted(INDIAN_STATES, key=len, reverse=True))
        + r")\b",
        text,
        re.IGNORECASE,
    )

    if match:
        district = match.group(1).strip()
        state = match.group(2).strip()

    # -----------------------------------------------------
    # Pattern 2:
    # "Dharwad district, Karnataka"
    # -----------------------------------------------------
    if not district:
        match = re.search(
            r"\b([A-Za-z][A-Za-z'-]*(?:\s+[A-Za-z][A-Za-z'-]*){0,5})"
            r"\s+district\s*(?:,|-)\s*("
            + "|".join(re.escape(s) for s in sorted(INDIAN_STATES, key=len, reverse=True))
            + r")\b",
            text,
            re.IGNORECASE,
        )

        if match:
            district = match.group(1).strip()
            state = match.group(2).strip()

    # -----------------------------------------------------
    # Pattern 3:
    # "district: Dharwad"
    # -----------------------------------------------------
    if not district:
        district = first_match(
            [
                r"\bdistrict\s*[:\-]\s*([A-Za-z][A-Za-z'-]*(?:\s+[A-Za-z][A-Za-z'-]*){0,5})",
            ],
            text,
        )

    # -----------------------------------------------------
    # Pattern 4:
    # "in Dharwad district"
    # IMPORTANT: stop at "district", do NOT consume the next
    # sentence.
    # -----------------------------------------------------
    if not district:
        match = re.search(
            r"\bin\s+([A-Za-z][A-Za-z'-]*(?:\s+[A-Za-z][A-Za-z'-]*){0,5})"
            r"\s+district\b",
            text,
            re.IGNORECASE,
        )

        if match:
            district = match.group(1).strip()

    # -----------------------------------------------------
    # Explicit state patterns
    # -----------------------------------------------------
    if not state:
        state = first_match(
            [
                r"\bstate\s*[:\-]\s*([A-Za-z][A-Za-z .'-]*?)(?=[.!?,;\n]|$)",
                r"\bstate\s+of\s+([A-Za-z][A-Za-z .'-]*?)(?=[.!?,;\n]|$)",
            ],
            text,
        )

    # -----------------------------------------------------
    # Detect known Indian state anywhere in text.
    # This is much safer than greedy "district of ..."
    # -----------------------------------------------------
    if not state:
        for candidate in sorted(INDIAN_STATES, key=len, reverse=True):
            if re.search(
                rf"\b{re.escape(candidate)}\b",
                text,
                re.IGNORECASE,
            ):
                state = candidate
                break

    # -----------------------------------------------------
    # Cleanup
    # -----------------------------------------------------
    if district:
        district = district.split("\n")[0]
        district = district.strip(" .,:;-")

    if state:
        state = state.split("\n")[0]
        state = state.strip(" .,:;-")

    return Location(
        district=district,
        state=state,
    )


# =========================================================
# BUDGET
# =========================================================

def extract_budget(text: str) -> Optional[float]:

    # -----------------------------------------------------
    # First handle values with explicit Indian units.
    # Examples:
    # ₹50 lakh
    # ₹5 crore
    # Rs. 50 lakh
    # INR 5 crore
    # -----------------------------------------------------

    unit_patterns = [
        r"(?:budget|project\s+cost|total\s+cost|estimated\s+cost)"
        r"\s*(?:is|of|:|-)?\s*"
        r"(?:₹|rs\.?|inr)\s*"
        r"([\d,.]+)\s*(crore|cr|lakh|lakhs)\b",

        r"(?:₹|rs\.?|inr)\s*"
        r"([\d,.]+)\s*(crore|cr|lakh|lakhs)\b",
    ]

    for pattern in unit_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if not match:
            continue

        number = float(
            match.group(1).replace(",", "")
        )

        unit = match.group(2).lower()

        if unit in {"crore", "cr"}:
            number *= 10_000_000

        elif unit in {"lakh", "lakhs"}:
            number *= 100_000

        return number

    # -----------------------------------------------------
    # Then handle plain numeric budgets.
    # Examples:
    # budget: ₹5,000,000
    # budget is 5000000
    # -----------------------------------------------------

    plain_patterns = [
        r"(?:budget|project\s+cost|total\s+cost|estimated\s+cost)"
        r"\s*(?:is|of|:|-)?\s*₹\s*([\d,]+(?:\.\d+)?)",

        r"(?:budget|project\s+cost|total\s+cost|estimated\s+cost)"
        r"\s*(?:is|of|:|-)?\s*(?:rs\.?|inr)\s*"
        r"([\d,]+(?:\.\d+)?)",

        r"(?:budget|project\s+cost|total\s+cost|estimated\s+cost)"
        r"\s*(?:is|of|:|-)?\s*"
        r"([\d,]+(?:\.\d+)?)",
    ]

    for pattern in plain_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE,
        )

        if match:
            return float(
                match.group(1).replace(",", "")
            )

    return None


# =========================================================
# DURATION
# =========================================================

def extract_duration(text: str) -> Optional[int]:

    value = first_match(
        [
            r"(\d+)\s*(?:months?|month)\b",
        ],
        text,
    )

    if value:
        return int(value)

    years = first_match(
        [
            r"(\d+)\s*(?:years?|year)\b",
        ],
        text,
    )

    if years:
        return int(years) * 12

    return None


# =========================================================
# BENEFICIARIES
# =========================================================

def extract_beneficiaries(text: str) -> Optional[int]:

    patterns = [

        r"(?:benefit|benefits|beneficiaries|beneficiary)"
        r".{0,80}?"
        r"(\d[\d,]*)\s*(?:people|persons|beneficiaries|families|students)?",

        r"(\d[\d,]*)\s*(?:people|persons|beneficiaries)"
        r".{0,50}?(?:benefit|serve|target)",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE | re.DOTALL,
        )

        if match:

            try:
                return int(
                    match.group(1).replace(",", "")
                )

            except ValueError:
                pass

    return None


# =========================================================
# BENEFICIARY GROUPS
# =========================================================

def extract_beneficiary_groups(text: str):

    groups = []

    group_patterns = {
        "children": [
            r"\bchildren\b",
            r"\bstudents\b",
        ],

        "women": [
            r"\bwomen\b",
            r"\bgirls\b",
        ],

        "senior citizens": [
            r"\bsenior citizens\b",
            r"\bthe elderly\b",
            r"\belderly\b",
        ],

        "rural communities": [
            r"\brural communities\b",
            r"\brural population\b",
            r"\brural families\b",
        ],

        "low-income communities": [
            r"\blow-income communities\b",
            r"\blow income communities\b",
            r"\bpoor communities\b",
            r"\bunderprivileged communities\b",
        ],

        "persons with disabilities": [
            r"\bpersons with disabilities\b",
            r"\bpeople with disabilities\b",
            r"\bdisabled persons\b",
        ],

        "farmers": [
            r"\bfarmers\b",
            r"\bfarming communities\b",
        ],
    }

    for group, patterns in group_patterns.items():

        for pattern in patterns:

            if re.search(
                pattern,
                text,
                re.IGNORECASE,
            ):

                if group not in groups:
                    groups.append(group)

                break

    return groups


# =========================================================
# INTERVENTION
# =========================================================

def extract_intervention(text: str) -> Optional[str]:

    intervention_keywords = [
        "healthcare",
        "education",
        "digital learning",
        "water and sanitation",
        "sanitation",
        "drinking water",
        "livelihood",
        "skill development",
        "women empowerment",
        "environment",
        "rural development",
        "slum development",
        "sports",
        "disaster management",
        "agriculture",
        "infrastructure",
    ]

    text_lower = text.lower()

    for keyword in intervention_keywords:

        if keyword in text_lower:
            return keyword

    return None


# =========================================================
# OBJECTIVES
# =========================================================

def extract_objectives(text: str):

    objectives = []

    match = re.search(
        r"(?:objectives?|aims?|goals?)\s*[:\-]?\s*"
        r"(.*?)(?:\n\s*\n|expected outcomes?|$)",
        text,
        re.IGNORECASE | re.DOTALL,
    )

    if match:

        section = match.group(1).strip()

        sentences = re.split(
            r"[.!?]\s+|\n+",
            section,
        )

        for sentence in sentences:

            sentence = sentence.strip(" -•\t")

            if len(sentence) > 15:
                objectives.append(sentence[:500])

    # Fallback
    if not objectives:

        sentences = re.split(
            r"(?<=[.!?])\s+",
            text,
        )

        for sentence in sentences:

            sentence = sentence.strip()

            if any(
                word in sentence.lower()
                for word in [
                    "provide",
                    "establish",
                    "improve",
                    "support",
                    "develop",
                    "increase",
                    "reduce",
                    "deliver",
                ]
            ):

                if len(sentence) > 20:

                    objectives.append(sentence[:500])

                    if len(objectives) >= 2:
                        break

    return objectives


# =========================================================
# EXPECTED OUTCOMES
# =========================================================

def extract_expected_outcomes(text: str):

    outcomes = []

    match = re.search(
        r"(?:expected outcomes?|outcomes?|expected results?)"
        r"\s*[:\-]?\s*(.*?)(?:\n\s*\n|$)",
        text,
        re.IGNORECASE | re.DOTALL,
    )

    if match:

        section = match.group(1).strip()

        sentences = re.split(
            r"[.!?]\s+|\n+",
            section,
        )

        for sentence in sentences:

            sentence = sentence.strip(" -•\t")

            if len(sentence) > 10:
                outcomes.append(sentence[:500])

    return outcomes


# =========================================================
# IMPLEMENTING AGENCY
# =========================================================

def extract_implementing_agency(text: str) -> Optional[str]:

    return first_match(
        [
            r"(?:implementing\s+agency|implementation\s+partner)"
            r"\s*[:\-]\s*([^\n.!?]+)",

            r"(?:implemented\s+by|implemented\s+through)"
            r"\s+([A-Za-z0-9&.,'()\- ]+?)(?=[.!?,;\n]|$)",
        ],
        text,
    )


# =========================================================
# DESCRIPTION
# =========================================================

def extract_description(text: str) -> Optional[str]:

    if not text:
        return None

    cleaned = clean_text(text)

    if len(cleaned) <= 1000:
        return cleaned

    return cleaned[:1000] + "..."


# =========================================================
# SUMMARY
# =========================================================

def generate_summary(
    project_name,
    intervention,
    location,
    beneficiaries,
):

    parts = []

    if project_name:
        parts.append(project_name)

    if intervention:
        parts.append(
            f"focuses on {intervention}"
        )

    if location.state:

        location_text = location.state

        if location.district:
            location_text = (
                f"{location.district}, "
                f"{location.state}"
            )

        parts.append(
            f"in {location_text}"
        )

    if beneficiaries:

        parts.append(
            f"targeting approximately "
            f"{beneficiaries:,} beneficiaries"
        )

    if not parts:
        return None

    return " ".join(parts) + "."


# =========================================================
# MAIN EXTRACTION FUNCTION
# =========================================================

def extract_project_information(
    text: str,
) -> ProjectAnalysis:

    if not text or not text.strip():

        raise ValueError(
            "Proposal text cannot be empty."
        )

    text = clean_text(text)

    project_name = extract_project_name(text)

    location = extract_location(text)

    budget = extract_budget(text)

    duration_months = extract_duration(text)

    beneficiaries = extract_beneficiaries(text)

    beneficiary_groups = extract_beneficiary_groups(text)

    intervention = extract_intervention(text)

    objectives = extract_objectives(text)

    expected_outcomes = extract_expected_outcomes(text)

    implementing_agency = extract_implementing_agency(text)

    description = extract_description(text)

    summary = generate_summary(
        project_name=project_name,
        intervention=intervention,
        location=location,
        beneficiaries=beneficiaries,
    )

    return ProjectAnalysis(
        project_name=project_name,
        location=location,
        budget=budget,
        duration_months=duration_months,
        beneficiaries=beneficiaries,
        beneficiary_groups=beneficiary_groups,
        intervention=intervention,
        objectives=objectives,
        expected_outcomes=expected_outcomes,
        implementing_agency=implementing_agency,
        description=description,
        summary=summary,
    )


# Backward-compatible aliases used by the AI pipeline
extract_project_info = extract_project_information
extract_project_data = extract_project_information