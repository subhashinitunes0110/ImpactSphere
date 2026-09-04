from ortools.linear_solver import pywraplp
from typing import List, Dict, Any

def optimize_portfolio(
    proposals: List[Dict[str, Any]],
    budget_limit: float,
    min_backward_ratio: float = 0.2
) -> Dict[str, Any]:
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        return {"error": "Solver SCIP unavailable"}

    n = len(proposals)
    x = [solver.BoolVar(f"x_{i}") for i in range(n)]

    objective = solver.Objective()
    for i, p in enumerate(proposals):
        objective.SetCoefficient(x[i], float(p.get("impactScore", 0)))
    objective.SetMaximization()

    budget_constraint = solver.RowConstraint(0, float(budget_limit), "budget_limit")
    for i, p in enumerate(proposals):
        budget_constraint.SetCoefficient(x[i], float(p.get("budget", 0)))

    status = solver.Solve()

    if status in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
        selected = []
        allocated_budget = 0.0
        total_impact = 0.0

        for i, p in enumerate(proposals):
            if x[i].solution_value() > 0.5:
                selected.append(p)
                allocated_budget += float(p.get("budget", 0))
                total_impact += float(p.get("impactScore", 0))

        return {
            "status": "optimal" if status == pywraplp.Solver.OPTIMAL else "feasible",
            "allocated_budget": allocated_budget,
            "unspent_budget": max(0.0, float(budget_limit) - allocated_budget),
            "total_impact": total_impact,
            "average_impact": round(total_impact / len(selected), 2) if selected else 0.0,
            "selected_proposals": selected,
        }

    return {
        "status": "infeasible",
        "allocated_budget": 0.0,
        "unspent_budget": float(budget_limit),
        "total_impact": 0.0,
        "average_impact": 0.0,
        "selected_proposals": [],
    }