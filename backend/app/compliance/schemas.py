from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ============================================================
# COMPLIANCE STATUS
# ============================================================

class ComplianceStatus(str, Enum):
    PASS = "PASS"
    REVIEW = "REVIEW"
    REJECT = "REJECT"


# ============================================================
# PROJECT COMPLIANCE INPUT
# ============================================================

class ProjectComplianceInput(BaseModel):

    # --------------------------------------------------------
    # Basic Project Information
    # --------------------------------------------------------

    project_id: str = Field(..., min_length=1)
    project_name: str = Field(..., min_length=1)
    activity_description: str = Field(..., min_length=1)

    # --------------------------------------------------------
    # Project Classification
    # --------------------------------------------------------

    sector: Optional[str] = None
    schedule_vii_category: Optional[str] = None
    beneficiary_group: Optional[str] = None

    # --------------------------------------------------------
    # Location
    # --------------------------------------------------------

    location: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None

    # --------------------------------------------------------
    # Implementing Agency
    # --------------------------------------------------------

    implementing_agency: Optional[str] = None
    implementing_agency_type: Optional[str] = None
    implementing_agency_csr_registration_number: Optional[str] = None

    # CSR implementing-agency eligibility checks

    implementing_agency_registered_under_12a: bool = False
    implementing_agency_registered_under_80g: bool = False
    implementing_agency_government_established: bool = False
    implementing_agency_created_by_statute: bool = False
    implementing_agency_has_3_year_track_record: bool = False

    # CSR-1

    csr1_required: bool = True
    csr1_filed: bool = False

    # --------------------------------------------------------
    # Financial Information
    # --------------------------------------------------------

    project_budget: Optional[float] = Field(
        default=None,
        ge=0
    )

    project_outlay: Optional[float] = Field(
        default=None,
        ge=0
    )

    # --------------------------------------------------------
    # Beneficiaries
    # --------------------------------------------------------

    beneficiaries: Optional[int] = Field(
        default=None,
        ge=0
    )

    # --------------------------------------------------------
    # Impact / Optimization Metrics
    # --------------------------------------------------------

    expected_impact: Optional[float] = Field(
        default=None,
        ge=0
    )

    csr_alignment: Optional[float] = Field(
        default=None,
        ge=0
    )

    feasibility: Optional[float] = Field(
        default=None,
        ge=0
    )

    sustainability: Optional[float] = Field(
        default=None,
        ge=0
    )

    # --------------------------------------------------------
    # CSR Exclusion Indicators
    # --------------------------------------------------------

    employee_benefit_indicator: bool = False

    political_contribution_indicator: bool = False

    normal_business_activity_indicator: bool = False

    statutory_obligation_indicator: bool = False

    international_activity_indicator: bool = False

    marketing_sponsorship_indicator: bool = False


# ============================================================
# COMPLIANCE RESULT
# ============================================================

class ComplianceResult(BaseModel):

    project_id: str

    status: ComplianceStatus

    eligible: bool

    eligible_for_optimization: bool

    # --------------------------------------------------------
    # Schedule VII Result
    # --------------------------------------------------------

    schedule_vii_category: Optional[str] = None

    schedule_vii_match: bool = False

    # --------------------------------------------------------
    # Compliance Flags
    # --------------------------------------------------------

    flags: List[str] = Field(
        default_factory=list
    )

    # --------------------------------------------------------
    # Human-readable Reasons
    # --------------------------------------------------------

    reasons: List[str] = Field(
        default_factory=list
    )

    # --------------------------------------------------------
    # Project Object Passed to Optimization Engine
    # --------------------------------------------------------

    project: Dict[str, Any] = Field(
        default_factory=dict
    )


# ============================================================
# CSR SECTION 135 CALCULATION INPUT
# ============================================================

class CSRCalculationInput(BaseModel):

    # --------------------------------------------------------
    # Section 135 Thresholds
    # --------------------------------------------------------

    net_worth: Optional[float] = Field(
        default=None,
        ge=0
    )

    turnover: Optional[float] = Field(
        default=None,
        ge=0
    )

    # --------------------------------------------------------
    # Net Profit History
    # --------------------------------------------------------

    net_profit_previous_3_years: List[float] = Field(
        default_factory=list
    )

    # --------------------------------------------------------
    # Company Age
    # --------------------------------------------------------

    years_since_incorporation: Optional[int] = Field(
        default=None,
        ge=0
    )


# ============================================================
# CSR SECTION 135 CALCULATION RESULT
# ============================================================

class CSRCalculationResult(BaseModel):

    applicable: bool

    average_net_profit: Optional[float] = None

    csr_requirement: float = 0.0

    triggered_by: List[str] = Field(
        default_factory=list
    )

    notes: List[str] = Field(
        default_factory=list
    )