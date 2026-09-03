import pytest
from backend.app.optimization.what_if import run_what_if
from backend.app.optimization.mock_data import SAMPLE_20_PROJECTS

def test_budget_never_exceeded():
    test_budget = 25000000.0  # ₹2.5 Cr limit
    result = run_what_if(
        projects=SAMPLE_20_PROJECTS,
        budget=test_budget,
        project_cap=7500000.0,
        underserved_min_percent=20.0,
        priority="maximum_impact"
    )
    # The allocator must never spend more than the available budget
    assert result["budget_allocated"] <= test_budget
    assert result["remaining_budget"] >= 0
    assert result["projects_funded"] == len(result["funded_projects"])

def test_project_cap_enforced():
    cap = 4000000.0  # ₹40 Lakh cap
    result = run_what_if(
        projects=SAMPLE_20_PROJECTS,
        budget=50000000.0,
        project_cap=cap,
        underserved_min_percent=0.0,
        priority="maximum_impact"
    )
    # No funded project can exceed the maximum individual project cap
    funded_items = [p for p in SAMPLE_20_PROJECTS if p["id"] in result["funded_projects"]]
    for item in funded_items:
        assert item["budget"] <= cap

def test_beneficiary_bonus_nudge():
    # Run with preference for children
    result_children = run_what_if(
        projects=SAMPLE_20_PROJECTS,
        budget=30000000.0,
        project_cap=7500000.0,
        underserved_min_percent=0.0,
        priority="maximum_impact",
        beneficiary_group="children"
    )
    # P002 targets children; verify preference boosts it into funded selection
    assert "P002" in result_children["funded_projects"]