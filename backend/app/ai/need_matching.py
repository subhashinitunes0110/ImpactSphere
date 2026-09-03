import pandas as pd
from pathlib import Path


# =========================================================
# CONFIGURATION
# =========================================================

NFHS_FILE = Path(
    "data/processed/nfhs_district_need.csv"
)


# =========================================================
# LOAD NFHS DATA
# =========================================================

def load_nfhs_needs():

    if not NFHS_FILE.exists():
        raise FileNotFoundError(
            f"NFHS file not found: {NFHS_FILE}"
        )

    df = pd.read_csv(NFHS_FILE)

    required_columns = [
        "district",
        "state",
        "health_need_score",
        "need_indicators_available"
    ]

    missing = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns in NFHS file: {missing}"
        )

    return df


# =========================================================
# RANK DISTRICTS BY HEALTH NEED
# =========================================================

def rank_health_need_districts(
    top_k: int = 10
):

    df = load_nfhs_needs()

    df = df.dropna(
        subset=["health_need_score"]
    )

    df = df.sort_values(
        by="health_need_score",
        ascending=False
    )

    results = []

    for _, row in df.head(top_k).iterrows():

        results.append(
            {
                "district": row["district"],
                "state": row["state"],
                "health_need_score": round(
                    float(row["health_need_score"]),
                    2
                ),
                "need_indicators_available": int(
                    row["need_indicators_available"]
                )
            }
        )

    return results


# =========================================================
# PROJECT → HEALTH NEED PRIORITY
# =========================================================

def match_project_to_health_need(
    project_text: str,
    top_k: int = 10
):
    """
    Prototype routing function.

    The proposal text is used to establish that the
    intervention concerns healthcare.

    District ranking itself is driven by the real
    NFHS health-need score.
    """

    if not project_text or not project_text.strip():
        raise ValueError(
            "Project text cannot be empty."
        )

    project_lower = project_text.lower()

    healthcare_keywords = [
        "health",
        "healthcare",
        "medical",
        "medicine",
        "hospital",
        "doctor",
        "clinic",
        "sanitation",
        "nutrition",
        "immunization",
        "maternal",
        "child health"
    ]

    is_health_project = any(
        keyword in project_lower
        for keyword in healthcare_keywords
    )

    if not is_health_project:
        return {
            "intervention_type": "non_health",
            "districts": []
        }

    districts = rank_health_need_districts(
        top_k=top_k
    )

    return {
        "intervention_type": "healthcare",
        "districts": districts
    }


# =========================================================
# QUICK TEST
# =========================================================

if __name__ == "__main__":

    print("=" * 70)
    print("IMPACT SPHERE - NFHS HEALTH NEED PRIORITIZATION")
    print("=" * 70)

    proposal = (
        "Providing preventive healthcare, medical camps "
        "and essential medical services to underserved "
        "rural communities."
    )

    print("\nProposal:")
    print(proposal)

    result = match_project_to_health_need(
        proposal,
        top_k=10
    )

    print(
        f"\nDetected intervention: "
        f"{result['intervention_type']}"
    )

    print("\nTOP HEALTH-NEED DISTRICTS:")
    print("-" * 70)

    for index, district in enumerate(
        result["districts"],
        1
    ):

        print(
            f"{index}. "
            f"{district['district']}, "
            f"{district['state']}"
        )

        print(
            f"   Health Need Score: "
            f"{district['health_need_score']}"
        )

        print(
            f"   Indicators Available: "
            f"{district['need_indicators_available']}"
        )