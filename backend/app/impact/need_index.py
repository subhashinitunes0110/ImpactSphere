from pathlib import Path

import pandas as pd


# ============================================================
# DATASET LOCATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[3]

DATA_PATH = (
    BASE_DIR
    / "data"
    / "processed"
    / "nfhs_district_need.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

def load_nfhs_data() -> pd.DataFrame:

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"NFHS dataset not found: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    required_columns = {
        "district",
        "state",
        "health_need_score",
        "need_indicators_available",
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(
            f"NFHS dataset missing columns: {sorted(missing)}"
        )

    return df


# ============================================================
# FIND DISTRICT
# ============================================================

def get_district_need(
    district: str,
    state: str | None = None,
) -> dict:

    if not district or not district.strip():
        raise ValueError(
            "District is required."
        )

    df = load_nfhs_data()

    district_clean = (
        district.strip()
        .lower()
    )

    df["_district_clean"] = (
        df["district"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    matches = df[
        df["_district_clean"] == district_clean
    ]

    # --------------------------------------------------------
    # Optional state filtering
    # --------------------------------------------------------

    if state and not matches.empty:

        state_clean = (
            state.strip()
            .lower()
        )

        matches = matches[
            matches["state"]
            .astype(str)
            .str.strip()
            .str.lower()
            == state_clean
        ]

    # --------------------------------------------------------
    # No match
    # --------------------------------------------------------

    if matches.empty:

        return {
            "found": False,
            "district": district,
            "state": state,
            "health_need_score": None,
            "need_indicators_available": 0,
            "message": (
                "No matching NFHS-5 district record found."
            ),
        }

    row = matches.iloc[0]

    return {
        "found": True,
        "district": str(row["district"]),
        "state": str(row["state"]),
        "health_need_score": round(
            float(row["health_need_score"]),
            2,
        ),
        "need_indicators_available": int(
            row["need_indicators_available"]
        ),
        "data_source": "NFHS-5",
        "message": (
            "District need score retrieved from "
            "NFHS-5 derived need index."
        ),
    }


# ============================================================
# TOP NEED DISTRICTS
# ============================================================

def get_top_need_districts(
    top_k: int = 10,
) -> list:

    df = load_nfhs_data()

    df = df.sort_values(
        "health_need_score",
        ascending=False,
    )

    results = []

    for _, row in df.head(top_k).iterrows():

        results.append(
            {
                "district": str(row["district"]),
                "state": str(row["state"]),
                "health_need_score": round(
                    float(row["health_need_score"]),
                    2,
                ),
                "need_indicators_available": int(
                    row["need_indicators_available"]
                ),
            }
        )

    return results