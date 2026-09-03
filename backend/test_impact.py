from app.impact.need_index import get_need_index
from app.impact.unmet_need import (
    calculate_unmet_need,
    get_need_level
)
from app.impact.scoring import (
    calculate_impact_score,
    calculate_impact_per_lakh
)


print("=" * 60)
print("IMPACT SPHERE - IMPACT ENGINE")
print("=" * 60)


# ---------------------------------------------------------
# 1. REGIONAL NEED
# ---------------------------------------------------------

district = "Barmer"
intervention = "healthcare"

need = get_need_index(
    district,
    intervention
)

print("\nREGIONAL NEED")
print("-" * 60)
print(f"District: {district}")
print(f"Intervention: {intervention}")
print(f"Need Index: {need}/100")


# ---------------------------------------------------------
# 2. UNMET NEED
# ---------------------------------------------------------

existing_coverage = 20

unmet_need = calculate_unmet_need(
    need,
    existing_coverage
)

print("\nUNMET NEED")
print("-" * 60)
print(f"Need Severity: {need}")
print(f"Existing Coverage: {existing_coverage}%")
print(f"Unmet Need: {unmet_need}/100")
print(f"Need Level: {get_need_level(unmet_need)}")


# ---------------------------------------------------------
# 3. IMPACT SCORE
# ---------------------------------------------------------

result = calculate_impact_score(
    need_vulnerability=unmet_need,
    expected_social_impact=90,
    beneficiary_reach=85,
    cost_efficiency=78,
    csr_alignment=95,
    feasibility=90,
    sustainability=80,
)

print("\nIMPACT SCORE")
print("-" * 60)

print(
    f"Need / Vulnerability: "
    f"{result['component_scores']['need_vulnerability']}"
)

print(
    f"Expected Social Impact: "
    f"{result['component_scores']['expected_social_impact']}"
)

print(
    f"Beneficiary Reach: "
    f"{result['component_scores']['beneficiary_reach']}"
)

print(
    f"Cost Efficiency: "
    f"{result['component_scores']['cost_efficiency']}"
)

print(
    f"CSR Alignment: "
    f"{result['component_scores']['csr_alignment']}"
)

print(
    f"Feasibility: "
    f"{result['component_scores']['feasibility']}"
)

print(
    f"Sustainability: "
    f"{result['component_scores']['sustainability']}"
)

print("\n----------------------------------------")

print(
    f"TOTAL IMPACT SCORE: "
    f"{result['total_score']}/100"
)

print(
    f"PRIORITY: "
    f"{result['priority'].upper()}"
)


# ---------------------------------------------------------
# 4. IMPACT PER ₹1 LAKH
# ---------------------------------------------------------

project_cost = 8000000  # ₹80 lakh

impact_per_lakh = calculate_impact_per_lakh(
    result["total_score"],
    project_cost
)

print("\nCOST EFFICIENCY")
print("-" * 60)

print(f"Project Cost: ₹{project_cost:,.0f}")

print(
    f"Impact / ₹1 Lakh: "
    f"{impact_per_lakh}"
)

print("\n" + "=" * 60)
print("IMPACT ENGINE TEST COMPLETE")
print("=" * 60)