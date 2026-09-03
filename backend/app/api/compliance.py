from fastapi import APIRouter

from backend.app.compliance.calculator import check_csr_applicability
from backend.app.compliance.engine import evaluate_project
from backend.app.compliance.schemas import (
    CSRCalculationInput,
    CSRCalculationResult,
    ComplianceResult,
    ProjectComplianceInput,
)


router = APIRouter(
    prefix="/compliance",
    tags=["CSR Compliance"],
)


@router.post(
    "/check",
    response_model=ComplianceResult,
)
def evaluate_project_compliance(
    data: ProjectComplianceInput,
) -> ComplianceResult:
    return evaluate_project(data)


@router.post(
    "/calculate",
    response_model=CSRCalculationResult,
)
def calculate_csr(
    data: CSRCalculationInput,
) -> CSRCalculationResult:
    return check_csr_applicability(data)