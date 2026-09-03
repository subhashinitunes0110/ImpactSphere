"""
Impact Sphere - Regional Social Need Engine

Calculates a normalized Social Need Index for a region.
This is a decision-support prototype, not an official government index.
"""

from typing import Dict


# Prototype regional indicators.
# Later these will come from real public datasets.
REGIONAL_DATA = {
    "barmer": {
        "healthcare": 88,
        "education": 72,
        "water_sanitation": 81,
        "livelihood": 76,
        "environment": 60,
        "women_empowerment": 78,
        "rural_development": 84,
        "sports": 55,
        "disaster_management": 50,
    },
    "jaipur": {
        "healthcare": 55,
        "education": 48,
        "water_sanitation": 42,
        "livelihood": 50,
        "environment": 58,
        "women_empowerment": 45,
        "rural_development": 35,
        "sports": 40,
        "disaster_management": 30,
    },
    "jaisalmer": {
        "healthcare": 82,
        "education": 70,
        "water_sanitation": 86,
        "livelihood": 80,
        "environment": 72,
        "women_empowerment": 74,
        "rural_development": 88,
        "sports": 50,
        "disaster_management": 55,
    },
}


def normalize_region(region: str) -> str:
    """Normalize region name for lookup."""
    if not region:
        return ""

    return region.strip().lower()


def get_need_index(
    district: str,
    intervention: str
) -> float:
    """
    Return regional need score from 0-100.
    Higher score = greater social need.
    """

    district_key = normalize_region(district)
    intervention_key = normalize_region(intervention)

    district_data = REGIONAL_DATA.get(district_key)

    if not district_data:
        # Neutral fallback when real data is unavailable.
        return 50.0

    return float(district_data.get(intervention_key, 50.0))


def get_regional_profile(district: str) -> Dict[str, float]:
    """Return all available indicators for a district."""

    district_key = normalize_region(district)

    return REGIONAL_DATA.get(
        district_key,
        {}
    )