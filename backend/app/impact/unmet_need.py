"""
Impact Sphere - Unmet Need Engine

Need and unmet need are different.

Need:
    How severe is the problem?

Unmet Need:
    How much of that need remains insufficiently addressed?
"""


def calculate_unmet_need(
    need_score: float,
    existing_coverage: float
) -> float:
    """
    Calculate unmet need on a 0-100 scale.

    need_score:
        Severity of the problem, 0-100.

    existing_coverage:
        Existing service/intervention coverage, 0-100.

    Formula:

        Unmet Need =
            Need Severity × (1 - Existing Coverage / 100)

    Example:

        Need = 90
        Coverage = 20

        Unmet Need = 90 × (1 - 0.20)
                   = 72
    """

    need_score = max(0.0, min(100.0, need_score))
    existing_coverage = max(
        0.0,
        min(100.0, existing_coverage)
    )

    unmet_need = need_score * (
        1 - existing_coverage / 100
    )

    return round(unmet_need, 2)


def get_need_level(score: float) -> str:
    """Convert numeric unmet need into an understandable level."""

    if score >= 75:
        return "very_high"

    if score >= 60:
        return "high"

    if score >= 40:
        return "moderate"

    return "low"