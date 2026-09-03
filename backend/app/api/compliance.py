from fastapi import APIRouter

from app.compliance.calculator import check_csr_applicability
from app.compliance.engine import evaluate_project
from app.compliance.schemas import (
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
    "/evaluate-project",
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