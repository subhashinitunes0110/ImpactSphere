import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

SEED_PROPOSALS = [
    {
        "id": "prop-001",
        "title": "Solar Powered Community Health Centers",
        "ngo_name": "Aarogya Seva Trust",
        "csr1_registration": "CSR00012489",
        "sector": "Healthcare",
        "district": "Barwani",
        "state": "Madhya Pradesh",
        "is_aspirational": True,
        "budget": 4200000,
        "admin_overhead_pct": 4.2,
        "beneficiaries": 18000,
        "need_score": 88.5,
        "impact_score": 91.2,
        "eligible_for_optimization": True,
        "compliance_status": "Passed"
    },
    {
        "id": "prop-002",
        "title": "Digital STEM Laboratories for Girls",
        "ngo_name": "Vidyashree Foundation",
        "csr1_registration": "CSR00098231",
        "sector": "Education",
        "district": "Kiphire",
        "state": "Nagaland",
        "is_aspirational": True,
        "budget": 3500000,
        "admin_overhead_pct": 3.8,
        "beneficiaries": 6500,
        "need_score": 84.0,
        "impact_score": 87.4,
        "eligible_for_optimization": True,
        "compliance_status": "Passed"
    },
    {
        "id": "prop-003",
        "title": "High-Tech Sports Training Complex",
        "ngo_name": "Metropolitan Sports Club",
        "csr1_registration": "",
        "sector": "Sports",
        "district": "Mumbai City",
        "state": "Maharashtra",
        "is_aspirational": False,
        "budget": 12000000,
        "admin_overhead_pct": 8.5,
        "beneficiaries": 1200,
        "need_score": 22.0,
        "impact_score": 35.0,
        "eligible_for_optimization": False,
        "compliance_status": "Failed: Admin overhead exceeds 5% statutory cap; Missing MCA CSR-1"
    },
    {
        "id": "prop-004",
        "title": "Piped Potable Water Purification Grid",
        "ngo_name": "Jal Jeevan Sahayog",
        "csr1_registration": "CSR00045102",
        "sector": "Water & Sanitation",
        "district": "Bijapur",
        "state": "Chhattisgarh",
        "is_aspirational": True,
        "budget": 5800000,
        "admin_overhead_pct": 4.0,
        "beneficiaries": 24000,
        "need_score": 92.0,
        "impact_score": 94.0,
        "eligible_for_optimization": True,
        "compliance_status": "Passed"
    },
    {
        "id": "prop-005",
        "title": "Agro-Forestry & Soil Rejuvenation",
        "ngo_name": "Green Earth Network",
        "csr1_registration": "CSR00067412",
        "sector": "Environment",
        "district": "Dahod",
        "state": "Gujarat",
        "is_aspirational": True,
        "budget": 4800000,
        "admin_overhead_pct": 4.5,
        "beneficiaries": 9500,
        "need_score": 79.5,
        "impact_score": 82.0,
        "eligible_for_optimization": True,
        "compliance_status": "Passed"
    }
]

def run_seed():
    target = DATA_DIR / "proposals_store.json"
    with open(target, "w", encoding="utf-8") as f:
        json.dump(SEED_PROPOSALS, f, indent=2)
    print(f"Seed complete: {len(SEED_PROPOSALS)} records written to {target}")

if __name__ == "__main__":
    run_seed()