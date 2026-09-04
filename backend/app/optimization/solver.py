from typing import Any, Dict, List, Optional, Tuple

from ortools.linear_solver import pywraplp

from backend.app.impact.scoring import compute_impact_score


def _compliance_gate(
    project: Dict[str, Any],
) -> Tuple[bool, Optional[str]]:
    """
    Decide whether a project is eligible for optimization.

    Projects with no compliance metadata are temporarily allowed so that
    existing demo projects continue to work. Once compliance metadata exists,
    only PASS + eligible=true projects can enter optimization.
    """
    compliance = project.get("compliance")

    # Legacy/demo projects do not have compliance metadata yet.
    if compliance is None:
        return True, None

    if isinstance(compliance, dict):
        status = str(
            compliance.get("status", "")
        ).upper()

        eligible = compliance.get("eligible")

        if status == "PASS" and eligible is True:
            return True, None

        if status == "REVIEW":
            return (
                False,
                "Requires human compliance review before optimization",
            )

        if status == "REJECT" or eligible is False:
            return (
                False,
                "Rejected by CSR compliance engine",
            )

    return (
        False,
        "Invalid or incomplete CSR compliance result",
    )


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

    candidates: List[Dict[str, Any]] = []
    dropped_reasons: Dict[str, str] = {}

    # =========================================================
    # COMPLIANCE → OPTIMIZATION GATE
    # =========================================================

    for project in projects:

        compliance_ok, compliance_reason = _compliance_gate(
            project
        )

        if not compliance_ok:

            dropped_reasons[
                project["id"]
            ] = (
                compliance_reason
                or "Compliance failed"
            )

            continue

        # =====================================================
        # PROJECT CAP
        # =====================================================

        if project["budget"] > project_cap:

            dropped_reasons[
                project["id"]
            ] = (
                f"Exceeds cap of ₹{project_cap:,.0f}"
            )

            continue

        # =====================================================
        # IMPACT SCORING
        # =====================================================

        project_copy = project.copy()

        score_data = compute_impact_score(
            project_copy,
            priority,
            beneficiary_group,
        )

        project_copy["score"] = (
            score_data["impact_score"]
        )

        project_copy["is_underserved"] = (
            score_data["unmet_need"] >= 60.0
        )

        candidates.append(project_copy)

    # =========================================================
    # NO ELIGIBLE CANDIDATES
    # =========================================================

    n = len(candidates)

    if n == 0:

        return {
            "funded_projects": [],
            "not_funded_projects": [
                project["id"]
                for project in projects
            ],
            "budget_allocated": 0.0,
            "remaining_budget": budget,
            "projects_funded": 0,
            "beneficiaries": 0,
            "underserved_percent": 0.0,
            "impact_score": 0.0,
            "solver": "Google OR-Tools (SCIP)",
            "reasons": dropped_reasons,
        }

    # =========================================================
    # BINARY DECISION VARIABLES
    # =========================================================

    x = [
        solver.IntVar(
            0,
            1,
            f"x_{candidates[i]['id']}",
        )
        for i in range(n)
    ]

    # =========================================================
    # CONSTRAINT 1: TOTAL BUDGET
    # =========================================================

    solver.Add(
        sum(
            candidates[i]["budget"] * x[i]
            for i in range(n)
        )
        <= budget
    )

    # =========================================================
    # CONSTRAINT 2: UNDERSERVED QUOTA
    # =========================================================

    target_underserved = (
        budget
        * (underserved_min_percent / 100.0)
    )

    solver.Add(
        sum(
            candidates[i]["budget"] * x[i]
            for i in range(n)
            if candidates[i]["is_underserved"]
        )
        >= target_underserved
    )

    # =========================================================
    # OBJECTIVE: MAXIMUM IMPACT
    # =========================================================

    solver.Maximize(
        sum(
            candidates[i]["score"] * x[i]
            for i in range(n)
        )
    )

    status = solver.Solve()

    # =========================================================
    # HANDLE INFEASIBLE SOLUTION
    # =========================================================

    if status not in (
        pywraplp.Solver.OPTIMAL,
        pywraplp.Solver.FEASIBLE,
    ):

        return {
            "funded_projects": [],
            "not_funded_projects": [
                project["id"]
                for project in projects
            ],
            "budget_allocated": 0.0,
            "remaining_budget": budget,
            "projects_funded": 0,
            "beneficiaries": 0,
            "underserved_percent": 0.0,
            "impact_score": 0.0,
            "solver": "Google OR-Tools (SCIP)",
            "reasons": {
                **dropped_reasons,
                "__solver__":
                    "No feasible optimization solution was found.",
            },
        }

    # =========================================================
    # BUILD RESULT
    # =========================================================

    funded_ids: List[str] = []

    allocated_spend = 0.0

    underserved_spend = 0.0

    reasons: Dict[str, str] = {
        **dropped_reasons
    }

    for i in range(n):

        project = candidates[i]

        if x[i].solution_value() > 0.5:

            project_id = project["id"]

            funded_ids.append(
                project_id
            )

            allocated_spend += (
                project["budget"]
            )

            if project["is_underserved"]:

                underserved_spend += (
                    project["budget"]
                )

            reasons[project_id] = (
                "Globally optimal selection: "
                f"Impact Score {project['score']}"
            )

        else:

            reasons[
                project["id"]
            ] = (
                "Not selected by linear optimizer"
            )

    # =========================================================
    # SUMMARY METRICS
    # =========================================================

    total_beneficiaries = sum(
        project["beneficiaries"]
        for project in candidates
        if project["id"] in funded_ids
    )

    avg_impact = (
        sum(
            project["score"]
            for project in candidates
            if project["id"] in funded_ids
        )
        / len(funded_ids)
        if funded_ids
        else 0.0
    )

    underserved_pct = (
        underserved_spend
        / allocated_spend
        * 100.0
        if allocated_spend > 0
        else 0.0
    )

    return {
        "funded_projects": funded_ids,

        "not_funded_projects": [
            project["id"]
            for project in projects
            if project["id"] not in funded_ids
        ],

        "budget_allocated":
            allocated_spend,

        "remaining_budget":
            budget - allocated_spend,

        "projects_funded":
            len(funded_ids),

        "beneficiaries":
            total_beneficiaries,

        "underserved_percent":
            round(underserved_pct, 1),

        "impact_score":
            round(avg_impact, 2),

        "solver":
            "Google OR-Tools (SCIP)",

        "reasons":
            reasons,
    }
