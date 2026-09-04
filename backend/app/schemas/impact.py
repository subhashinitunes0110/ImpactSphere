from typing import List, Optional

from pydantic import BaseModel, Field


# ============================================================
# IMPACT SCORE REQUEST
# ============================================================

class ImpactScoreRequest(BaseModel):
    """
    Input for calculating a CSR project's impact score.

    need_score is optional because the backend can automatically
    retrieve the score from the NFHS-5 district need dataset.
    """

    project_name: str

    # Project economics
    budget: float = Field(
        ...,
        gt=0,
        description="Project budget in INR"
    )

    beneficiaries: int = Field(
        ...,
        ge=0,
        description="Expected number of beneficiaries"
    )

    # --------------------------------------------------------
    # Location
    # --------------------------------------------------------

    state: Optional[str] = None

    district: Optional[str] = None

    # --------------------------------------------------------
    # Need
    # --------------------------------------------------------

    # Automatically retrieved from NFHS-5 when not provided
    need_score: Optional[float] = Field(
        default=None,
        ge=0,
        le=100,
        description="Community need score. Automatically derived from NFHS-5 if omitted."
    )

    # --------------------------------------------------------
    # Other impact dimensions
    # --------------------------------------------------------

    expected_impact_score: float = Field(
        default=0,
        ge=0,
        le=100
    )

    csr_alignment_score: float = Field(
        default=0,
        ge=0,
        le=100
    )

    feasibility_score: float = Field(
        default=0,
        ge=0,
        le=100
    )

    sustainability_score: float = Field(
        default=0,
        ge=0,
        le=100
    )

    beneficiary_priority_score: float = Field(
        default=0,
        ge=0,
        le=100
    )

    # --------------------------------------------------------
    # Beneficiary groups
    # --------------------------------------------------------

    beneficiary_groups: List[str] = Field(
        default_factory=list
    )


# ============================================================
# IMPACT SCORE COMPONENT
# ============================================================

class ImpactScoreComponent(BaseModel):

    name: str

    score: float

    weight: float

    weighted_score: float

    explanation: str


# ============================================================
# IMPACT SCORE RESPONSE
# ============================================================

class ImpactScoreResponse(BaseModel):

    project_name: str

    # Final score out of 100
    impact_score: float

    # Impact score generated per ₹1 lakh
    impact_per_lakh: float

    # Expected beneficiaries
    beneficiaries: int

    # Project budget in INR
    budget: float

    # NFHS-5 need score used
    need_score: float

    # Location used for need lookup
    state: Optional[str] = None

    district: Optional[str] = None

    # Individual scoring components
    components: List[ImpactScoreComponent]

    # Human-readable explanation
    explanation: str

    # Important disclaimer
    estimate_note: str