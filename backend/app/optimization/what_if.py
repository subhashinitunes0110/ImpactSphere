from typing import List, Dict, Any
from backend.app.impact.scoring import compute_impact_score

def run_what_if(
    projects: List[Dict[str, Any]],
    budget: float,
    project_cap: float,
    underserved_min_percent: float,
    priority: str,
    beneficiary_group: str = None
) -> Dict[str, Any]:
    
    valid_candidates = []
    dropped_projects = {}
    
    for p in projects:
        if p["budget"] > project_cap:
            dropped_projects[p["id"]] = f"Exceeds individual cap of ₹{project_cap:,.0f}"
        else:
            valid_candidates.append(p.copy())
            
    for p in valid_candidates:
        score_data = compute_impact_score(p, priority, beneficiary_group)
        p["final_score"] = score_data["impact_score"]
        p["unmet_need"] = score_data["unmet_need"]
        p["is_underserved"] = score_data["unmet_need"] >= 60.0

    valid_candidates.sort(key=lambda x: x["final_score"], reverse=True)
    
    funded = []
    not_funded_ids = list(dropped_projects.keys())
    allocated_spend = 0.0
    underserved_spend = 0.0
    target_underserved = budget * (underserved_min_percent / 100.0)
    reasons = {**dropped_projects}
    
    # Pass 1: Underserved minimum allocation
    remaining_candidates = []
    for p in valid_candidates:
        if p["is_underserved"] and underserved_spend < target_underserved:
            if allocated_spend + p["budget"] <= budget:
                funded.append(p)
                allocated_spend += p["budget"]
                underserved_spend += p["budget"]
                reasons[p["id"]] = f"Funded: Underserved quota priority (Score: {p['final_score']})"
                continue
        remaining_candidates.append(p)
        
    # Pass 2: Greedy fill with remaining budget
    for p in remaining_candidates:
        if allocated_spend + p["budget"] <= budget:
            funded.append(p)
            allocated_spend += p["budget"]
            if p["is_underserved"]:
                underserved_spend += p["budget"]
            reasons[p["id"]] = f"Funded: High marginal score ({p['final_score']})"
        else:
            not_funded_ids.append(p["id"])
            reasons[p["id"]] = "Not Funded: Budget ceiling reached"
            
    total_beneficiaries = sum(p.get("beneficiaries", 0) for p in funded)
    avg_impact = (sum(p["final_score"] for p in funded) / len(funded)) if funded else 0.0
    underserved_ratio = (underserved_spend / allocated_spend * 100.0) if allocated_spend > 0 else 0.0
    
    return {
        "funded_projects": [p["id"] for p in funded],
        "not_funded_projects": not_funded_ids,
        "budget_allocated": allocated_spend,
        "remaining_budget": budget - allocated_spend,
        "projects_funded": len(funded),
        "beneficiaries": total_beneficiaries,
        "underserved_percent": round(underserved_ratio, 1),
        "impact_score": round(avg_impact, 2),
        "reasons": reasons
    }