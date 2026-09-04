import math

from app.schemas.impact import (
    ImpactScoreRequest,
    ImpactScoreResponse,
    ImpactScoreComponent,
)

from app.impact.need_index import get_district_need


# ============================================================
# IMPACT SCORE WEIGHTS
# ============================================================

WEIGHTS = {
    "need": 0.25,
    "expected_impact": 0.25,
    "beneficiary_reach": 0.15,
    "cost_efficiency": 0.15,
    "csr_alignment": 0.10,
    "feasibility": 0.05,
    "sustainability": 0.05,
}


# ============================================================
# BENEFICIARY REACH SCORE
# ============================================================

def calculate_beneficiary_reach(
    beneficiaries: int,
) -> float:

    if beneficiaries <= 0:
        return 0.0

    score = (
        math.log10(beneficiaries + 1)
        / math.log10(10001)
    ) * 100

    return round(
        min(score, 100),
        2,
    )


# ============================================================
# COST EFFICIENCY SCORE
# ============================================================

def calculate_cost_efficiency(
    budget: float,
    beneficiaries: int,
) -> float:

    if budget <= 0 or beneficiaries <= 0:
        return 0.0

    cost_per_beneficiary = (
        budget / beneficiaries
    )

    score = (
        10000 / max(cost_per_beneficiary, 1)
    ) * 50

    return round(
        min(score, 100),
        2,
    )


# ============================================================
# MAIN IMPACT SCORE
# ============================================================

def calculate_impact_score(
    request: ImpactScoreRequest,
) -> ImpactScoreResponse:

    # ========================================================
    # 1. GET NEED SCORE
    # ========================================================

    need_score = request.need_score

    # If need_score was not manually provided,
    # automatically retrieve it from NFHS-5.
    if need_score is None:

        if not request.district:
            raise ValueError(
                "District is required to automatically "
                "calculate the NFHS-5 need score."
            )

        need_data = get_district_need(
            district=request.district,
            state=request.state,
        )

        if not need_data["found"]:
            raise ValueError(
                f"No NFHS-5 need data found for "
                f"{request.district}, {request.state}."
            )

        need_score = need_data["health_need_score"]

    # ========================================================
    # 2. CALCULATE OTHER DIMENSIONS
    # ========================================================

    expected_impact = request.expected_impact_score

    beneficiary_reach = calculate_beneficiary_reach(
        request.beneficiaries
    )

    cost_efficiency = calculate_cost_efficiency(
        request.budget,
        request.beneficiaries
    )

    csr_alignment = request.csr_alignment_score

    feasibility = request.feasibility_score

    sustainability = request.sustainability_score

    # ========================================================
    # 3. BUILD COMPONENTS
    # ========================================================

    components_data = [

        (
            "Need / Vulnerability",
            need_score,
            WEIGHTS["need"],
            "Higher scores indicate greater community need."
        ),

        (
            "Expected Social Impact",
            expected_impact,
            WEIGHTS["expected_impact"],
            "Estimated potential social impact of the intervention."
        ),

        (
            "Beneficiary Reach",
            beneficiary_reach,
            WEIGHTS["beneficiary_reach"],
            "Measures the scale of the expected beneficiary population."
        ),

        (
            "Cost Efficiency",
            cost_efficiency,
            WEIGHTS["cost_efficiency"],
            "Rewards projects that can reach beneficiaries efficiently."
        ),

        (
            "CSR Alignment",
            csr_alignment,
            WEIGHTS["csr_alignment"],
            "Measures alignment with the company's CSR objectives."
        ),

        (
            "Feasibility",
            feasibility,
            WEIGHTS["feasibility"],
            "Measures implementation readiness and practicality."
        ),

        (
            "Sustainability",
            sustainability,
            WEIGHTS["sustainability"],
            "Measures the likelihood of benefits continuing over time."
        ),
    ]

    components = []

    total_score = 0.0

    # ========================================================
    # 4. CALCULATE WEIGHTED SCORE
    # ========================================================

    for (
        name,
        score,
        weight,
        explanation,
    ) in components_data:

        weighted_score = (
            score * weight
        )

        total_score += weighted_score

        components.append(
            ImpactScoreComponent(
                name=name,
                score=round(score, 2),
                weight=weight,
                weighted_score=round(
                    weighted_score,
                    2,
                ),
                explanation=explanation,
            )
        )

    total_score = round(
        min(max(total_score, 0), 100),
        2,
    )

    # ========================================================
    # 5. IMPACT PER ₹1 LAKH
    # ========================================================

    if request.budget > 0:

        budget_in_lakh = (
            request.budget / 100000
        )

        impact_per_lakh = (
            total_score / budget_in_lakh
        )

    else:

        impact_per_lakh = 0.0

    impact_per_lakh = round(
        impact_per_lakh,
        2,
    )

    # ========================================================
    # 6. EXPLANATION
    # ========================================================

    location_text = request.district or "Unknown district"

    if request.state:
        location_text += f", {request.state}"

    explanation = (
        f"{request.project_name} received an impact score "
        f"of {total_score}/100. "
        f"The project is located in {location_text}. "
        f"The NFHS-5 derived community need score is "
        f"{need_score}/100. "
        f"The project has an estimated social impact score "
        f"of {expected_impact}/100 and is expected to reach "
        f"{request.beneficiaries:,} beneficiaries."
    )

    # ========================================================
    # 7. RESPONSE
    # ========================================================

    return ImpactScoreResponse(

        project_name=request.project_name,

        impact_score=total_score,

        impact_per_lakh=impact_per_lakh,

        beneficiaries=request.beneficiaries,

        budget=request.budget,

        need_score=round(
            need_score,
            2,
        ),

        state=request.state,

        district=request.district,

        components=components,

        explanation=explanation,

        estimate_note=(
            "Impact scores are decision-support estimates "
            "based on configured scoring criteria and "
            "NFHS-5-derived need data. They do not represent "
            "guaranteed or causally attributable social outcomes."
        ),
    )