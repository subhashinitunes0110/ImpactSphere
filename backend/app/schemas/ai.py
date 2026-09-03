from typing import List, Optional
from pydantic import BaseModel, Field


class Location(BaseModel):
    district: Optional[str] = None
    state: Optional[str] = None


class ProjectAnalysis(BaseModel):
    project_name: Optional[str] = None

    location: Location = Field(
        default_factory=Location
    )

    budget: Optional[float] = None
    duration_months: Optional[int] = None
    beneficiaries: Optional[int] = None

    beneficiary_groups: List[str] = Field(
        default_factory=list
    )

    intervention: Optional[str] = None

    objectives: List[str] = Field(
        default_factory=list
    )

    expected_outcomes: List[str] = Field(
        default_factory=list
    )

    implementing_agency: Optional[str] = None

    description: Optional[str] = None

    summary: Optional[str] = None


class ClassificationResult(BaseModel):
    category: str
    confidence: float
    confidence_level: str
    human_review_required: bool


class NeedMatch(BaseModel):
    need_id: int
    description: str
    similarity: float


class AIAnalysisResponse(BaseModel):
    success: bool
    project: ProjectAnalysis
    classification: ClassificationResult
    need_matches: List[NeedMatch] = Field(
        default_factory=list
    )