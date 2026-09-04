from typing import List, Optional, Literal
from pydantic import BaseModel, Field


# ============================================================
# COMPANY CSR INPUT
# ============================================================

class CompanyCSRInput(BaseModel):
    company_name: str

    financial_year: Optional[str] = None

    # Section 135 applicability thresholds
    net_worth_crore: Optional[float] = Field(
        default=None,
        ge=0
    )

    turnover_crore: Optional[float] = Field(
        default=None,
        ge=0
    )

    net_profit_crore: Optional[float] = Field(
        default=None,
        ge=0
    )

    # Average net profit of immediately preceding
    # three financial years
    previous_3_year_average_net_profit_crore: Optional[float] = Field(
        default=None,
        ge=0
    )

    # Company's CSR budget
    csr_budget_crore: Optional[float] = Field(
        default=None,
        ge=0
    )

    # Actual CSR expenditure
    csr_spent_crore: float = Field(
        default=0,
        ge=0
    )

    # Administrative overhead expenditure
    administrative_overheads_crore: float = Field(
        default=0,
        ge=0
    )


# ============================================================
# PROJECT COMPLIANCE INPUT
# ============================================================

class ProjectComplianceInput(BaseModel):

    project_name: str

    description: str = ""

    intervention: Optional[str] = None

    # Schedule VII category predicted by AI
    category: Optional[str] = None

    # AI classification confidence
    # Example: 0.92 = 92%
    classification_confidence: Optional[float] = Field(
        default=None,
        ge=0,
        le=1
    )

    # Location information
    location: Optional[dict] = None

    location_state: Optional[str] = None

    location_district: Optional[str] = None

    # Project budget
    budget: Optional[float] = Field(
        default=None,
        ge=0
    )

    # Expected beneficiaries
    beneficiaries: Optional[int] = Field(
        default=None,
        ge=0
    )

    beneficiary_groups: List[str] = Field(
        default_factory=list
    )

    # ========================================================
    # IMPLEMENTING AGENCY
    # ========================================================

    implementing_agency: Optional[str] = None

    # CSR-1 registration number
    csr_registration_number: Optional[str] = None

    # Whether CSR-1 validity has been verified
    implementing_agency_csr1_valid: Optional[bool] = None

    # ========================================================
    # POTENTIAL CSR EXCLUSIONS
    # ========================================================

    # Activity is part of company's normal business
    normal_business_activity: bool = False

    # Political contribution
    political_contribution: bool = False

    # Employee benefit
    employee_benefit: bool = False

    # Marketing / sponsorship activity
    marketing_sponsorship: bool = False

    # Activity already required under another law
    statutory_obligation: bool = False

    # Project is outside India
    outside_india: bool = False

    # ========================================================
    # CSR GOVERNANCE
    # ========================================================

    # Whether project is included in approved Annual Action Plan
    annual_action_plan_approved: bool = False

    # ========================================================
    # ADMINISTRATIVE OVERHEAD
    # ========================================================

    administrative_overhead_percent: Optional[float] = Field(
        default=None,
        ge=0
    )


# ============================================================
# COMPLETE COMPLIANCE REQUEST
# ============================================================

class ComplianceCheckRequest(BaseModel):

    company: CompanyCSRInput

    project: ProjectComplianceInput


# ============================================================
# INDIVIDUAL COMPLIANCE RULE RESULT
# ============================================================

class ComplianceRuleResult(BaseModel):

    rule_id: str

    rule_name: str

    status: Literal[
        "PASS",
        "FLAG",
        "REVIEW"
    ]

    message: str

    severity: Literal[
        "LOW",
        "MEDIUM",
        "HIGH"
    ] = "MEDIUM"


# ============================================================
# CSR CALCULATION RESPONSE
# ============================================================

class CSRCalculationResponse(BaseModel):

    company_name: str

    # Whether Section 135 CSR provisions apply
    csr_applicable: bool

    # Why CSR applicability was triggered
    threshold_reasons: List[str] = Field(
        default_factory=list
    )

    # Average profit used for calculation
    average_net_profit_crore: Optional[float] = None

    # 2% CSR obligation
    required_csr_spend_crore: Optional[float] = None

    # Actual CSR spending
    actual_csr_spend_crore: float = 0

    # Difference between required and actual spending
    spending_gap_crore: float = 0

    spending_compliant: bool

    # Administrative overhead
    administrative_overheads_crore: float = 0

    administrative_overhead_percentage: float = 0

    administrative_overhead_compliant: bool

    # Whether CSR Committee is required
    csr_committee_required: bool


# ============================================================
# FINAL COMPLIANCE RESPONSE
# ============================================================

class ComplianceCheckResponse(BaseModel):

    # Overall result
    status: Literal[
        "PASS",
        "FLAG",
        "REVIEW"
    ]

    overall_compliant: bool

    # Schedule VII alignment
    schedule_vii_alignment: bool

    # Category detected by the compliance engine
    detected_schedule_vii_category: Optional[str] = None

    # Implementing agency result
    implementing_agency_check: str

    # Exclusion checks
    exclusions_check: str

    # CSR applicability
    csr_applicable: bool

    # CSR calculation details
    csr_calculation: CSRCalculationResponse

    # Every individual rule checked
    rules_checked: List[ComplianceRuleResult] = Field(
        default_factory=list
    )

    # Important flags
    flags: List[str] = Field(
        default_factory=list
    )

    # Non-blocking warnings
    warnings: List[str] = Field(
        default_factory=list
    )

    # Whether human verification is needed
    review_required: bool

    # Human-readable explanation
    explanation: str

    # Machine-readable summary for frontend
    checks: dict = Field(
        default_factory=dict
    )