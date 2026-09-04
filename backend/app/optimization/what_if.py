from typing import List, Dict, Any, Optional, Tuple

from backend.app.impact.scoring import compute_impact_score


def _compliance_gate(
    project: Dict[str, Any],
) -> Tuple[bool, Optional[str]]:
    """
    Allow legacy/demo projects without compliance metadata.

    If compliance metadata exists, only PASS + eligible=True
    projects can enter the What-If simulation.
    """

    compliance = project.get("compliance")

    # Existing mock/demo projects may not yet have
    # compliance metadata.
    if compliance is None:
        return True, None

    if hasattr(compliance, "model_dump"):
        compliance = compliance.model_dump()

    if not isinstance(compliance, dict):
        return False, "Invalid or incomplete CSR compliance result"

    status = compliance.get("status", "")
    eligible = compliance.get("eligible")

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


def run_what_if(
    projects: List[Dict[str, Any]],
    budget: float,
    project_cap: float,
    underserved_min_percent: float,
    priority: str,
    beneficiary_group: str = None,
) -> Dict[str, Any]:

    valid_candidates = []
    dropped_projects = {}

    # --------------------------------------------------
    # BUILD VALID CANDIDATES
    # --------------------------------------------------

    for project in projects:

        compliance_ok, compliance_reason = _compliance_gate(project)

        if not compliance_ok:
            dropped_projects[project["id"]] = compliance_reason
            continue

        project_budget = float(project.get("budget", 0.0))

        if project_budget > project_cap:
            dropped_projects[project["id"]] = (
                f"Exceeds individual cap of ₹{project_cap:,.0f}"
            )
            continue

        project_copy = project.copy()
        valid_candidates.append(project_copy)

    # --------------------------------------------------
    # CALCULATE IMPACT SCORES
    # --------------------------------------------------

    for project in valid_candidates:

        score_data = compute_impact_score(
            project,
            priority,
            beneficiary_group,
        )

        project["final_score"] = score_data["impact_score"]

        project["impact_metrics"] = {
            "need_score": score_data["need_score"],
            "unmet_need": score_data["unmet_need"],
            "reach_score": score_data["reach_score"],
            "cost_efficiency": score_data["cost_efficiency"],
            "impact_score": score_data["impact_score"],
            "geographic_score": score_data["geographic_score"],
        }

        project["unmet_need"] = score_data["unmet_need"]

        project["is_underserved"] = (
            score_data["unmet_need"] >= 60.0
        )

    # Highest-impact projects first
    valid_candidates.sort(
        key=lambda project: project["final_score"],
        reverse=True,
    )

    # --------------------------------------------------
    # ALLOCATION
    # --------------------------------------------------

    funded = []

    not_funded_ids = list(dropped_projects.keys())

    allocated_spend = 0.0
    underserved_spend = 0.0

    target_underserved = (
        budget * underserved_min_percent / 100.0
    )

    reasons = {
        **dropped_projects
    }

    # --------------------------------------------------
    # PASS 1
    # Satisfy underserved allocation requirement
    # --------------------------------------------------

    remaining_candidates = []

    for project in valid_candidates:

        if (
            project["is_underserved"]
            and underserved_spend < target_underserved
        ):

            if (
                allocated_spend + project["budget"]
                <= budget
            ):

                funded.append(project)

                allocated_spend += project["budget"]

                underserved_spend += project["budget"]

                reasons[project["id"]] = (
                    "Funded: Underserved quota priority "
                    f"(Impact Score: {project['final_score']:.2f})"
                )

                continue

        remaining_candidates.append(project)

    # --------------------------------------------------
    # PASS 2
    # Fill remaining budget using impact score
    # --------------------------------------------------

    for project in remaining_candidates:

        if (
            allocated_spend + project["budget"]
            <= budget
        ):

            funded.append(project)

            allocated_spend += project["budget"]

            if project["is_underserved"]:
                underserved_spend += project["budget"]

            reasons[project["id"]] = (
                "Funded: High impact score "
                f"({project['final_score']:.2f})"
            )

        else:

            not_funded_ids.append(project["id"])

            reasons[project["id"]] = (
                "Not funded: Budget ceiling reached"
            )

    # --------------------------------------------------
    # SUMMARY METRICS
    # --------------------------------------------------

    total_beneficiaries = sum(
        project.get("beneficiaries", 0) or 0
        for project in funded
    )

    avg_impact = (
        sum(
            project["final_score"]
            for project in funded
        )
        / len(funded)
        if funded
        else 0.0
    )

    underserved_ratio = (
        underserved_spend
        / allocated_spend
        * 100.0
        if allocated_spend > 0
        else 0.0
    )

    # --------------------------------------------------
    # FUNDED PROJECT DETAILS
    # --------------------------------------------------

    funded_project_details = []

    for project in funded:

        funded_project_details.append({
            "id": project["id"],
            "name": project.get("name"),
            "district": project.get("district"),
            "state": project.get("state"),
            "sector": project.get("sector"),
            "budget": project.get("budget", 0.0),
            "beneficiaries": project.get(
                "beneficiaries",
                0,
            ),
            "beneficiary_group": project.get(
                "beneficiary_group"
            ),
            "underserved": project["is_underserved"],
            "impact_score": project["final_score"],
            "impact_metrics": project["impact_metrics"],
        })

    # --------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------

    return {
        "funded_projects": [
            project["id"]
            for project in funded
        ],

        "not_funded_projects": not_funded_ids,

        "budget_allocated": allocated_spend,

        "remaining_budget": budget - allocated_spend,

        "projects_funded": len(funded),

        "beneficiaries": total_beneficiaries,

        "underserved_percent": round(
            underserved_ratio,
            1,
        ),

        "impact_score": round(
            avg_impact,
            2,
        ),

        "funded_project_details": funded_project_details,

        "solver": "What-If Greedy Simulation",

        "status": "SIMULATED",

        "constraints": {
            "total_budget": budget,
            "project_cap": project_cap,
            "underserved_min_percent": underserved_min_percent,
            "priority": priority,
            "beneficiary_group": beneficiary_group,
        },

        "reasons": reasons,
    }
