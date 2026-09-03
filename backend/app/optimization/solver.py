from ortools.linear_solver import pywraplp
from typing import List, Dict, Any
from backend.app.impact.scoring import compute_impact_score

def solve_with_ortools(
    projects: List[Dict[str, Any]],
    budget: float,
    project_cap: float,
    underserved_min_percent: float,
    priority: str,
    beneficiary_group: str = None
) -> Dict[str, Any]:
    # Initialize the SCIP Mixed-Integer Programming solver
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        return {"error": "OR-Tools solver engine not found"}

    candidates = []
    dropped_reasons = {}

    for p in projects:
        if p["budget"] > project_cap:
            dropped_reasons[p["id"]] = f"Exceeds cap of ₹{project_cap:,.0f}"
        else:
            p_copy = p.copy()
            score_data = compute_impact_score(p_copy, priority, beneficiary_group)
            p_copy["score"] = score_data["impact_score"]
            p_copy["is_underserved"] = score_data["unmet_need"] >= 60.0
            candidates.append(p_copy)

    n = len(candidates)
    if n == 0:
        return {"funded_projects": [], "budget_allocated": 0}

    # Binary Decision Variables: x[i] = 1 if selected, 0 if skipped
    x = [solver.IntVar(0, 1, f"x_{candidates[i]['id']}") for i in range(n)]

    # Constraint 1: Total cost <= Budget
    solver.Add(sum(candidates[i]["budget"] * x[i] for i in range(n)) <= budget)

    # Constraint 2: Underserved expenditure >= Quota percentage of budget
    target_underserved = budget * (underserved_min_percent / 100.0)
    solver.Add(
        sum(candidates[i]["budget"] * x[i] for i in range(n) if candidates[i]["is_underserved"]) >= target_underserved
    )

    # Objective: Maximize total combined impact score
    solver.Maximize(sum(candidates[i]["score"] * x[i] for i in range(n)))

    solver.Solve()

    funded_ids = []
    allocated_spend = 0.0
    underserved_spend = 0.0
    reasons = {**dropped_reasons}

    for i in range(n):
        if x[i].solution_value() > 0.5:
            pid = candidates[i]["id"]
            funded_ids.append(pid)
            allocated_spend += candidates[i]["budget"]
            if candidates[i]["is_underserved"]:
                underserved_spend += candidates[i]["budget"]
            reasons[pid] = f"Globally optimal selection: Impact Score {candidates[i]['score']}"
        else:
            reasons[candidates[i]["id"]] = "Not selected by linear optimizer"

    total_beneficiaries = sum(p["beneficiaries"] for p in candidates if p["id"] in funded_ids)
    avg_impact = (sum(p["score"] for p in candidates if p["id"] in funded_ids) / len(funded_ids)) if funded_ids else 0.0
    underserved_pct = (underserved_spend / allocated_spend * 100.0) if allocated_spend > 0 else 0.0

    return {
        "funded_projects": funded_ids,
        "not_funded_projects": [p["id"] for p in projects if p["id"] not in funded_ids],
        "budget_allocated": allocated_spend,
        "remaining_budget": budget - allocated_spend,
        "projects_funded": len(funded_ids),
        "beneficiaries": total_beneficiaries,
        "underserved_percent": round(underserved_pct, 1),
        "impact_score": round(avg_impact, 2),
        "solver": "Google OR-Tools (SCIP)",
        "reasons": reasons
    }