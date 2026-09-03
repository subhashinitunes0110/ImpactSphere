import math
from typing import Dict, Any
from backend.app.impact.need import calculate_need_metrics

def compute_impact_score(
    project: Dict[str, Any],
    priority_mode: str = "maximum_impact",
    beneficiary_preference: str = None
) -> Dict[str, float]:
    
    metrics = calculate_need_metrics(project["district"], project.get("sector", "general"))
    unmet_need = metrics["unmet_need_score"]
    
    beneficiaries = max(1, project.get("beneficiaries", 1000))
    reach_score = min((math.log10(beneficiaries) / math.log10(50000)) * 100.0, 100.0)
    
    budget = project.get("budget", 5000000.0)
    cost_in_lakhs = max(budget / 100000.0, 1.0)
    expected_impact_raw = float(project.get("expected_impact", 75.0))
    cost_efficiency = min((expected_impact_raw / cost_in_lakhs) * 20.0, 100.0)
    
    csr_align = float(project.get("csr_alignment", 80.0))
    feasibility = float(project.get("feasibility", 85.0))
    sustainability = float(project.get("sustainability", 80.0))
    
    base_impact = (
        unmet_need * 0.25 +
        expected_impact_raw * 0.25 +
        reach_score * 0.15 +
        cost_efficiency * 0.15 +
        csr_align * 0.10 +
        feasibility * 0.05 +
        sustainability * 0.05
    )
    
    final_score = base_impact
    if priority_mode == "geographic_equity":
        final_score = (base_impact * 0.70) + (metrics["geographic_score"] * 0.30)
    elif priority_mode == "csr_alignment":
        final_score = (base_impact * 0.60) + (csr_align * 0.40)
        
    if beneficiary_preference and project.get("beneficiary_group", "").strip().lower() == beneficiary_preference.strip().lower():
        final_score += 10.0
        
    return {
        "need_score": metrics["need_score"],
        "unmet_need": unmet_need,
        "reach_score": round(reach_score, 2),
        "cost_efficiency": round(cost_efficiency, 2),
        "impact_score": round(final_score, 2),
        "geographic_score": metrics["geographic_score"]
    }