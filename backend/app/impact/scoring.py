"""
Impact Sphere - Project Impact Scoring Engine

Total Impact Score = 0-100

Weights:
    Need / Vulnerability       25%
    Expected Social Impact     25%
    Beneficiary Reach          15%
    Cost Efficiency            15%
    CSR Alignment              10%
    Feasibility                 5%
    Sustainability              5%
"""

from typing import Dict


WEIGHTS = {
    "need_vulnerability": 0.25,
    "expected_social_impact": 0.25,
    "beneficiary_reach": 0.15,
    "cost_efficiency": 0.15,
    "csr_alignment": 0.10,
    "feasibility": 0.05,
    "sustainability": 0.05,
}


def calculate_impact_score(
    need_vulnerability: float,
    expected_social_impact: float,
    beneficiary_reach: float,
    cost_efficiency: float,
    csr_alignment: float,
    feasibility: float,
    sustainability: float,
) -> Dict:

    scores = {
        "need_vulnerability": need_vulnerability,
        "expected_social_impact": expected_social_impact,
        "beneficiary_reach": beneficiary_reach,
        "cost_efficiency": cost_efficiency,
        "csr_alignment": csr_alignment,
        "feasibility": feasibility,
        "sustainability": sustainability,
    }

    # Keep every component between 0 and 100.
    scores = {
        key: max(0.0, min(100.0, float(value)))
        for key, value in scores.items()
    }

    weighted_scores = {
        key: round(
            scores[key] * WEIGHTS[key],
            2
        )
        for key in scores
    }

    total_score = round(
        sum(weighted_scores.values()),
        2
    )

    return {
        "total_score": total_score,
        "component_scores": scores,
        "weighted_scores": weighted_scores,
        "weights": WEIGHTS,
        "priority": get_priority_level(total_score),
    }


def get_priority_level(score: float) -> str:

    if score >= 80:
        return "very_high"

    if score >= 65:
        return "high"

    if score >= 50:
        return "medium"

    return "low"


def calculate_impact_per_lakh(
    impact_score: float,
    project_cost: float
) -> float:
    """
    Calculate impact score generated per ₹1 lakh.

    Example:

        Impact = 80
        Cost = ₹40 lakh

        80 / 40 = 2.0 impact points per ₹1 lakh
    """

    if project_cost <= 0:
        return 0.0

    cost_in_lakh = project_cost / 100000

    return round(
        impact_score / cost_in_lakh,
        2
    )