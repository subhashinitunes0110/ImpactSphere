import re
from typing import Optional

from app.schemas.ai import ProjectAnalysis, Location


# ============================================================
# IMPACT SPHERE
# LOCAL PROJECT INFORMATION EXTRACTION
# ============================================================
#
# This extractor does NOT use OpenAI or any paid API.
#
# It extracts useful project information using:
#   - regular expressions
#   - keyword detection
#   - simple NLP rules
#
# Missing information is returned as None.
# ============================================================


def find_first_number(patterns, text):
    """
    Try multiple regex patterns and return the first number found.
    """

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            try:
                return float(
                    match.group(1).replace(",", "")
                )
            except ValueError:
                pass

    return None


def extract_budget(text: str) -> Optional[float]:
    """
    Extract project budget.

    Examples:
        Budget: ₹80 lakh
        Budget: Rs. 50,00,000
        Cost: 2 crore
        Project cost is 5000000
    """

    # Crores
    crore_patterns = [
        r"(?:budget|cost|allocation|funding)[^\d₹]{0,30}"
        r"₹?\s*([\d,.]+)\s*crore",

        r"₹?\s*([\d,.]+)\s*crore"
    ]

    value = find_first_number(
        crore_patterns,
        text
    )

    if value is not None:
        return value * 10_000_000

    # Lakhs
    lakh_patterns = [
        r"(?:budget|cost|allocation|funding)[^\d₹]{0,30}"
        r"₹?\s*([\d,.]+)\s*lakh",

        r"₹?\s*([\d,.]+)\s*lakh"
    ]

    value = find_first_number(
        lakh_patterns,
        text
    )

    if value is not None:
        return value * 100_000

    # Direct rupee amount
    rupee_patterns = [
        r"(?:budget|cost|allocation|funding)[^\d]{0,30}"
        r"₹\s*([\d,]+)",

        r"(?:budget|cost|allocation|funding)[^\d]{0,30}"
        r"Rs\.?\s*([\d,]+)"
    ]

    value = find_first_number(
        rupee_patterns,
        text
    )

    if value is not None:
        return value

    return None


def extract_duration(text: str) -> Optional[int]:
    """
    Extract project duration in months.
    """

    match = re.search(
        r"(\d+)\s*(?:month|months)",
        text,
        re.IGNORECASE
    )

    if match:
        return int(match.group(1))

    # Convert years to months
    match = re.search(
        r"(\d+)\s*(?:year|years)",
        text,
        re.IGNORECASE
    )

    if match:
        return int(match.group(1)) * 12

    return None


def extract_beneficiaries(text: str) -> Optional[int]:
    """
    Extract approximate number of beneficiaries.

    Examples:
        benefit 12,000 people
        reach 5000 beneficiaries
        beneficiaries: 3000
    """

    patterns = [
        r"(?:benefit|benefits|reach|serve|serving|"
        r"beneficiaries)[^\d]{0,30}([\d,]+)",

        r"([\d,]+)\s*(?:people|persons|beneficiaries|families)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            try:
                return int(
                    match.group(1).replace(",", "")
                )
            except ValueError:
                pass

    return None


def extract_location(text: str) -> Location:
    """
    Extract location using common Indian district/state patterns.

    This is intentionally conservative.
    """

    states = [
        "Rajasthan",
        "Maharashtra",
        "Gujarat",
        "Madhya Pradesh",
        "Uttar Pradesh",
        "Bihar",
        "West Bengal",
        "Tamil Nadu",
        "Kerala",
        "Karnataka",
        "Telangana",
        "Andhra Pradesh",
        "Odisha",
        "Jharkhand",
        "Chhattisgarh",
        "Punjab",
        "Haryana",
        "Himachal Pradesh",
        "Uttarakhand",
        "Assam",
        "Meghalaya",
        "Manipur",
        "Mizoram",
        "Nagaland",
        "Tripura",
        "Sikkim",
        "Goa",
        "Delhi"
    ]

    state = None

    for candidate in states:

        if re.search(
            rf"\b{re.escape(candidate)}\b",
            text,
            re.IGNORECASE
        ):
            state = candidate
            break

    district = None

    district_match = re.search(
        r"(?:district|dist\.?)\s*[:\-]?\s*"
        r"([A-Za-z][A-Za-z\s]{2,40})",
        text,
        re.IGNORECASE
    )

    if district_match:
        district = (
            district_match
            .group(1)
            .strip()
        )

        # Remove trailing words
        district = re.split(
            r"\b(?:of|in|for|and|the)\b",
            district,
            flags=re.IGNORECASE
        )[0].strip()

    return Location(
        district=district,
        state=state
    )


def extract_project_name(text: str) -> Optional[str]:
    """
    Try to identify project title.
    """

    patterns = [
        r"(?:project name|project title)\s*[:\-]\s*(.+)",

        r"^([A-Z][A-Za-z\s\-]{5,80})\s*$"
    ]

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    for line in lines[:10]:

        match = re.match(
            patterns[0],
            line,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

    # If the first meaningful line looks like a title
    if lines:

        first = lines[0]

        if (
            len(first) <= 100
            and len(first.split()) <= 12
        ):
            return first

    return None


def extract_beneficiary_groups(text: str):
    """
    Identify common beneficiary groups.
    """

    groups = []

    keywords = {
        "children": [
            "children",
            "students",
            "school children"
        ],

        "women": [
            "women",
            "girls",
            "female"
        ],

        "senior citizens": [
            "elderly",
            "senior citizens",
            "older people"
        ],

        "rural communities": [
            "rural communities",
            "rural population",
            "villages",
            "rural families"
        ],

        "persons with disabilities": [
            "persons with disabilities",
            "disabled persons",
            "people with disabilities"
        ],

        "low-income communities": [
            "low-income",
            "low income",
            "poor families",
            "economically weaker"
        ]
    }

    lower_text = text.lower()

    for group, words in keywords.items():

        if any(word in lower_text for word in words):
            groups.append(group)

    return groups


def extract_intervention(text: str) -> Optional[str]:
    """
    Identify the primary intervention using keywords.
    """

    interventions = {

        "healthcare": [
            "healthcare",
            "health care",
            "medical",
            "hospital",
            "clinic",
            "doctor",
            "medicine",
            "screening"
        ],

        "education": [
            "education",
            "school",
            "students",
            "learning",
            "classroom",
            "digital learning"
        ],

        "water_sanitation": [
            "drinking water",
            "sanitation",
            "toilet",
            "water supply",
            "clean water"
        ],

        "livelihood": [
            "livelihood",
            "employment",
            "entrepreneurship",
            "skill training",
            "vocational"
        ],

        "environment": [
            "environment",
            "tree plantation",
            "renewable energy",
            "solar",
            "waste management",
            "climate"
        ],

        "women_empowerment": [
            "women empowerment",
            "women's empowerment",
            "female empowerment"
        ],

        "sports": [
            "sports",
            "athletics",
            "coaching",
            "playground"
        ],

        "disaster_management": [
            "disaster",
            "flood relief",
            "earthquake",
            "emergency response"
        ]
    }

    lower_text = text.lower()

    scores = {}

    for category, words in interventions.items():

        score = 0

        for word in words:

            if word in lower_text:
                score += 1

        scores[category] = score

    if not scores:
        return None

    best_category = max(
        scores,
        key=scores.get
    )

    if scores[best_category] == 0:
        return None

    return best_category


def extract_objectives(text: str):
    """
    Extract sentences that appear to describe objectives.
    """

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    objectives = []

    keywords = [
        "aim",
        "objective",
        "goal",
        "provide",
        "establish",
        "improve",
        "increase",
        "reduce",
        "support",
        "enable"
    ]

    for sentence in sentences:

        lower = sentence.lower()

        if any(
            keyword in lower
            for keyword in keywords
        ):

            sentence = sentence.strip()

            if sentence and len(sentence) > 20:
                objectives.append(sentence)

    return objectives[:5]


def extract_expected_outcomes(text: str):
    """
    Extract sentences describing expected outcomes.
    """

    sentences = re.split(
        r"(?<=[.!?])\s+",
        text
    )

    outcomes = []

    keywords = [
        "expected",
        "outcome",
        "impact",
        "benefit",
        "will improve",
        "will increase",
        "will reduce",
        "will provide"
    ]

    for sentence in sentences:

        lower = sentence.lower()

        if any(
            keyword in lower
            for keyword in keywords
        ):

            sentence = sentence.strip()

            if sentence and len(sentence) > 20:
                outcomes.append(sentence)

    return outcomes[:5]


def extract_implementing_agency(text: str):
    """
    Extract implementing agency when explicitly mentioned.
    """

    patterns = [
        r"(?:implementing agency|implementation partner)"
        r"\s*[:\-]\s*(.+)",

        r"(?:implemented by|to be implemented by)"
        r"\s*(.+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            value = match.group(1).strip()

            value = value.split(".")[0]

            return value

    return None


# ============================================================
# MAIN EXTRACTION FUNCTION
# ============================================================

def extract_project_information(
    text: str
) -> ProjectAnalysis:

    if not text or not text.strip():
        raise ValueError(
            "Proposal text cannot be empty."
        )

    project_name = extract_project_name(text)

    location = extract_location(text)

    budget = extract_budget(text)

    duration = extract_duration(text)

    beneficiaries = extract_beneficiaries(text)

    beneficiary_groups = (
        extract_beneficiary_groups(text)
    )

    intervention = extract_intervention(text)

    objectives = extract_objectives(text)

    expected_outcomes = (
        extract_expected_outcomes(text)
    )

    implementing_agency = (
        extract_implementing_agency(text)
    )

    summary = text.strip()

    if len(summary) > 500:
        summary = summary[:500] + "..."

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

        implementing_agency=implementing_agency,

        schedule_vii_category=None,

        classification_confidence=0.0,

        summary=summary
    )