from fastapi import APIRouter, HTTPException

from app.schemas.compliance import (
    CompanyCSRInput,
    ComplianceCheckRequest,
    ComplianceCheckResponse,
    CSRCalculationResponse,
)

from app.compliance.checker import check_project_compliance

from app.compliance.rules import (
    check_section_135_applicability,
    calculate_required_csr,
    check_administrative_overhead,
    check_csr_committee_required,
)


router = APIRouter(
    prefix="/compliance",
    tags=["Compliance"],
)


# ============================================================
# FULL PROJECT COMPLIANCE CHECK
# ============================================================

@router.post(
    "/check",
    response_model=ComplianceCheckResponse,
)
async def check_compliance(
    request: ComplianceCheckRequest,
):
    """
    Run the complete CSR compliance screening pipeline.

    Input:
        Company financial information
        +
        AI-analyzed project information

    Output:
        PASS / FLAG / REVIEW
        +
        individual rule results
        +
        CSR calculation
        +
        human-readable explanation
    """

    try:

        result = check_project_compliance(request)

        return result

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Compliance check failed: {str(e)}",
        )


# ============================================================
# CSR CALCULATION
# ============================================================

@router.post(
    "/calculate-csr",
    response_model=CSRCalculationResponse,
)
async def calculate_csr(
    company: CompanyCSRInput,
):
    """
    Calculate the company's basic CSR obligation
    and related CSR compliance indicators.
    """

    try:

        # ----------------------------------------------------
        # Section 135 applicability
        # ----------------------------------------------------

        csr_applicable, threshold_reasons = (
            check_section_135_applicability(
                net_worth_crore=company.net_worth_crore,
                turnover_crore=company.turnover_crore,
                net_profit_crore=company.net_profit_crore,
            )
        )

        # ----------------------------------------------------
        # Average profit
        # ----------------------------------------------------

        average_profit = (
            company.previous_3_year_average_net_profit_crore
        )

        # ----------------------------------------------------
        # Required CSR expenditure
        # ----------------------------------------------------

        required_csr = calculate_required_csr(
            average_profit
        )

        # ----------------------------------------------------
        # Actual CSR expenditure
        # ----------------------------------------------------

        actual_spend = company.csr_spent_crore

        if required_csr is not None:

            spending_gap = round(
                required_csr - actual_spend,
                4,
            )

            spending_compliant = (
                actual_spend >= required_csr
            )

        else:

            spending_gap = 0.0
            spending_compliant = False

        # ----------------------------------------------------
        # Administrative overhead
        # ----------------------------------------------------

        overhead_percentage, overhead_compliant = (
            check_administrative_overhead(
                administrative_overheads_crore=(
                    company.administrative_overheads_crore
                ),
                csr_spent_crore=actual_spend,
            )
        )

        # ----------------------------------------------------
        # CSR Committee
        # ----------------------------------------------------

        csr_committee_required = (
            check_csr_committee_required(
                required_csr
            )
        )

        # ----------------------------------------------------
        # Response
        # ----------------------------------------------------

        return CSRCalculationResponse(
            company_name=company.company_name,
            csr_applicable=csr_applicable,
            threshold_reasons=threshold_reasons,
            average_net_profit_crore=average_profit,
            required_csr_spend_crore=required_csr,
            actual_csr_spend_crore=actual_spend,
            spending_gap_crore=spending_gap,
            spending_compliant=spending_compliant,
            administrative_overheads_crore=(
                company.administrative_overheads_crore
            ),
            administrative_overhead_percentage=(
                overhead_percentage
            ),
            administrative_overhead_compliant=(
                overhead_compliant
            ),
            csr_committee_required=(
                csr_committee_required
            ),
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"CSR calculation failed: {str(e)}",
        )


# ============================================================
# CSR RULE INFORMATION
# ============================================================

@router.get("/rules")
async def get_compliance_rules():
    """
    Return the main configured CSR screening thresholds.

    Useful for the frontend to display the rules used by
    Impact Sphere.
    """

    return {
        "section_135": {
            "net_worth_threshold_crore": 500,
            "turnover_threshold_crore": 1000,
            "net_profit_threshold_crore": 5,
            "csr_percentage": 2,
        },

        "administrative_overhead": {
            "maximum_percentage": 5,
        },

        "csr_committee": {
            "obligation_threshold_crore": 0.50,
            "obligation_threshold_lakh": 50,
        },

        "note": (
            "These are configured decision-support screening "
            "rules and should be verified against the applicable "
            "Companies Act, CSR Rules and amendments."
        ),
    }