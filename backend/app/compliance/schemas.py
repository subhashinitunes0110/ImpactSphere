from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class ComplianceStatus(str, Enum):
    PASS = "PASS"
    REVIEW = "REVIEW"
    REJECT = "REJECT"

class ProjectComplianceInput(BaseModel):
    project_id: str = Field(..., min_length=1)
    project_name: str = Field(..., min_length=1)
    activity_description: str = Field(..., min_length=1)
    sector: Optional[str] = None
    schedule_vii_category: Optional[str] = None
    beneficiary_group: Optional[str] = None
    location: Optional[str] = None
    implementing_agency: Optional[str] = None
    implementing_agency_type: Optional[str] = None
    implementing_agency_csr_registration_number: Optional[str] = None
    project_budget: Optional[float] = Field(default=None, ge=0)
    project_outlay: Optional[float] = Field(default=None, ge=0)
    employee_benefit_indicator: bool = False
    political_contribution_indicator: bool = False
    normal_business_activity_indicator: bool = False
    statutory_obligation_indicator: bool = False
    international_activity_indicator: bool = False

class ComplianceResult(BaseModel):
    project_id: str
    status: ComplianceStatus
    eligible: bool
    eligible_for_optimization: bool
    schedule_vii_category: Optional[str] = None
    schedule_vii_match: bool = False
    flags: List[str] = Field(default_factory=list)
    reasons: List[str] = Field(default_factory=list)

class CSRCalculationInput(BaseModel):
    net_worth: Optional[float] = Field(default=None, ge=0)
    turnover: Optional[float] = Field(default=None, ge=0)
    net_profit_previous_3_years: List[float] = Field(default_factory=list)
    years_since_incorporation: Optional[int] = Field(default=None, ge=0)

class CSRCalculationResult(BaseModel):
    applicable: bool
    average_net_profit: Optional[float] = None
    csr_requirement: float = 0.0
    triggered_by: List[str] = Field(default_factory=list)
    notes: List[str] = Field(default_factory=list)
