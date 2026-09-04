from ortools.linear_solver import pywraplp
from typing import List, Dict, Any, Optional, Tuple

from backend.app.impact.scoring import compute_impact_score


def _compliance_gate(
    project: Dict[str, Any],
) -> Tuple[bool, Optional[str]]:

    compliance = project.get("compliance")

    # Existing projects without compliance information
    # are allowed into the optimizer.
    if compliance is None:
        return True, None

    # Handle both dictionary and Pydantic-style compliance objects.
    if hasattr(compliance, "model_dump"):
        compliance = compliance.model_dump()

    if not isinstance(compliance, dict):
        return False, "Invalid or incomplete CSR compliance result"

    status = compliance.get("status", "")
    eligible = compliance.get("eligible")

    # Pydantic Enum → string
    if hasattr(status, "value"):
        status = status.value

    status = str(status).strip().upper()

    if status == "PASS" and eligible is True:
        return True, None

    if status == "REVIEW":
        return False, "Requires human compliance review before optimization"

    if status == "REJECT":
        return False, "Rejected by CSR compliance engine"

    if eligible is False:
        return False, "Rejected by CSR compliance engine"

    return False, "Invalid or incomplete CSR compliance result"


def solve_with_ortools(
    projects: List[Dict[str, Any]],
    budget: float,
    project_cap: float,
    underserved_min_percent: float,
    priority: str,
    beneficiary_group: str = None,
) -> Dict[str, Any]:

    solver = pywraplp.Solver.CreateSolver("SCIP")

    if not solver:
        return {
            "error": "OR-Tools solver engine not found"
        }

    candidates = []
    dropped_reasons = {}

    # --------------------------------------------------
    # BUILD CANDIDATES
    # --------------------------------------------------

    for project in projects:

        compliance_ok, compliance_reason = _compliance_gate(
            project
        )

        if not compliance_ok:
            dropped_reasons[project["id"]] = (
                compliance_reason or "Compliance failed"
            )
            continue

        if project["budget"] > project_cap:
            dropped_reasons[project["id"]] = (
                f"Exceeds cap of ₹{project_cap:,.0f}"
            )
            continue

        project_copy = project.copy()

        # --------------------------------------------------
        # IMPACT ENGINE
        # --------------------------------------------------

        score_data = compute_impact_score(
            project_copy,
            priority,
            beneficiary_group,
        )

        project_copy["score"] = score_data["impact_score"]

        project_copy["impact_metrics"] = {
            "need_score": score_data["need_score"],
            "unmet_need": score_data["unmet_need"],
            "reach_score": score_data["reach_score"],
            "cost_efficiency": score_data["cost_efficiency"],
            "impact_score": score_data["impact_score"],
            "geographic_score": score_data["geographic_score"],
        }

        project_copy["is_underserved"] = (
            score_data["unmet_need"] >= 60.0
        )

        candidates.append(project_copy)

    # --------------------------------------------------
    # NO CANDIDATES
    # --------------------------------------------------

    if not candidates:
        return {
            "funded_projects": [],
            "not_funded_projects": [
                p["id"] for p in projects
            ],
            "budget_allocated": 0.0,
            "remaining_budget": budget,
            "projects_funded": 0,
            "beneficiaries": 0,
            "underserved_percent": 0.0,
            "impact_score": 0.0,
            "solver": "Google OR-Tools (SCIP)",
            "status": "NO_CANDIDATES",
            "reasons": dropped_reasons,
        }

    n = len(candidates)

    # --------------------------------------------------
    # DECISION VARIABLES
    # --------------------------------------------------

    x = [
        solver.IntVar(
            0,
            1,
            f"x_{candidates[i]['id']}",
        )
        for i in range(n)
    ]

    # --------------------------------------------------
    # BUDGET CONSTRAINT
    # --------------------------------------------------

    solver.Add(
        sum(
            candidates[i]["budget"] * x[i]
            for i in range(n)
        )
        <= budget
    )

    # --------------------------------------------------
    # UNDERSERVED CONSTRAINT
    # --------------------------------------------------

    target_underserved = (
        budget * underserved_min_percent / 100.0
    )

    solver.Add(
        sum(
            candidates[i]["budget"] * x[i]
            for i in range(n)
            if candidates[i]["is_underserved"]
        )
        >= target_underserved
    )

    # --------------------------------------------------
    # OBJECTIVE
    # --------------------------------------------------

    solver.Maximize(
        sum(
            candidates[i]["score"] * x[i]
            for i in range(n)
        )
    )

    status = solver.Solve()

    # --------------------------------------------------
    # SOLVER FAILURE
    # --------------------------------------------------

    if status not in (
        pywraplp.Solver.OPTIMAL,
        pywraplp.Solver.FEASIBLE,
    ):
        return {
            "funded_projects": [],
            "not_funded_projects": [
                p["id"] for p in projects
            ],
            "budget_allocated": 0.0,
            "remaining_budget": budget,
            "projects_funded": 0,
            "beneficiaries": 0,
            "underserved_percent": 0.0,
            "impact_score": 0.0,
            "solver": "Google OR-Tools (SCIP)",
            "status": "INFEASIBLE",
            "reasons": {
                **dropped_reasons,
                "_solver": (
                    "No feasible allocation satisfies "
                    "the supplied constraints."
                ),
            },
        }

    # --------------------------------------------------
    # COLLECT RESULTS
    # --------------------------------------------------

    funded_ids = []
    allocated_spend = 0.0
    underserved_spend = 0.0
    total_impact = 0.0
    total_beneficiaries = 0

    funded_project_details = []

    reasons = {
        **dropped_reasons
    }

    for i in range(n):

        project = candidates[i]

        if x[i].solution_value() > 0.5:

            pid = project["id"]

            funded_ids.append(pid)

            allocated_spend += project["budget"]

            total_beneficiaries += (
                project.get("beneficiaries", 0) or 0
            )

            if project["is_underserved"]:
                underserved_spend += project["budget"]

            total_impact += project["score"]

            reasons[pid] = (
                "Globally optimal selection: "
                f"Impact Score {project['score']:.2f}"
            )

            funded_project_details.append({
                "id": pid,
                "name": project.get("name"),
                "district": project.get("district"),
                "state": project.get("state"),
                "sector": project.get("sector"),
                "budget": project.get("budget", 0.0),
                "beneficiaries": project.get(
                    "beneficiaries", 0
                ),
                "underserved": project[
                    "is_underserved"
                ],
                "impact_metrics": project[
                    "impact_metrics"
                ],
            })

        else:
            reasons[project["id"]] = (
                "Not selected by linear optimizer"
            )

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    projects_funded = len(funded_ids)

    avg_impact = (
        total_impact / projects_funded
        if projects_funded
        else 0.0
    )

    underserved_pct = (
        underserved_spend
        / allocated_spend
        * 100.0
        if allocated_spend > 0
        else 0.0
    )

    not_funded_ids = [
        p["id"]
        for p in projects
        if p["id"] not in funded_ids
    ]

    # --------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------

    return {
        "funded_projects": funded_ids,
        "not_funded_projects": not_funded_ids,
        "budget_allocated": allocated_spend,
        "remaining_budget": budget - allocated_spend,
        "projects_funded": projects_funded,
        "beneficiaries": total_beneficiaries,
        "underserved_percent": round(
            underserved_pct,
            1,
        ),
        "impact_score": round(
            avg_impact,
            2,
        ),
        "funded_project_details": funded_project_details,
        "solver": "Google OR-Tools (SCIP)",
        "status": (
            "OPTIMAL"
            if status == pywraplp.Solver.OPTIMAL
            else "FEASIBLE"
        ),
        "reasons": reasons,
    }