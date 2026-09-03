from typing import List
from .rules import CSR_APPLICABILITY_THRESHOLDS, CSR_SPEND_RATE
from .schemas import CSRCalculationInput, CSRCalculationResult

def calculate_average_net_profit(profits: List[float]) -> float:
    if not profits:
        return 0.0
    return sum(profits) / len(profits)

def calculate_csr_requirement(net_profit_average: float) -> float:
    return max(0.0, net_profit_average * CSR_SPEND_RATE)

def check_csr_applicability(data: CSRCalculationInput) -> CSRCalculationResult:
    triggered_by: List[str] = []
    notes: List[str] = []

    if data.net_worth is not None and data.net_worth >= CSR_APPLICABILITY_THRESHOLDS["net_worth"]:
        triggered_by.append("NET_WORTH")

    if data.turnover is not None and data.turnover >= CSR_APPLICABILITY_THRESHOLDS["turnover"]:
        triggered_by.append("TURNOVER")

    if data.net_profit_previous_3_years:
        if data.net_profit_previous_3_years[-1] >= CSR_APPLICABILITY_THRESHOLDS["net_profit"]:
            triggered_by.append("NET_PROFIT")

    applicable = bool(triggered_by)
    average_net_profit = calculate_average_net_profit(
        data.net_profit_previous_3_years
    )
    csr_requirement = (
        calculate_csr_requirement(average_net_profit)
        if applicable
        else 0.0
    )

    if not data.net_profit_previous_3_years:
        notes.append(
            "Previous-year net profit data was not provided; "
            "CSR obligation cannot be calculated from profit data."
        )
    elif len(data.net_profit_previous_3_years) < 3:
        notes.append(
            "Fewer than three preceding financial years were provided; "
            "use the applicable preceding years available under Section 135."
        )

    notes.append(
        "CSR applicability is triggered because at least one Section 135 "
        "threshold is met."
        if applicable
        else "No Section 135 applicability threshold was met from the supplied data."
    )

    return CSRCalculationResult(
        applicable=applicable,
        average_net_profit=average_net_profit,
        csr_requirement=csr_requirement,
        triggered_by=triggered_by,
        notes=notes,
    )
