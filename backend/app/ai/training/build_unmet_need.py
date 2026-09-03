from pathlib import Path
import pandas as pd
import numpy as np


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[4]

NFHS_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "nfhs_district_need.csv"
)

CSR_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "csr_clean.csv"
)

OUTPUT_DIR = BASE_DIR / "data" / "processed"

OUTPUT_FILE = (
    OUTPUT_DIR
    / "state_unmet_need.csv"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# ============================================================
# HELPER FUNCTION
# ============================================================

def normalize_state(value):

    if pd.isna(value):
        return ""

    value = str(value).strip().upper()

    value = (
        value
        .replace("&", "AND")
        .replace(".", "")
        .replace("  ", " ")
    )

    aliases = {
        "NCT OF DELHI": "DELHI",
        "DELHI NCT": "DELHI",
        "JAMMU AND KASHMIR": "JAMMU AND KASHMIR",
        "JAMMU & KASHMIR": "JAMMU AND KASHMIR",
        "ODISHA": "ODISHA",
        "ORISSA": "ODISHA",
        "PONDICHERRY": "PUDUCHERRY",
        "UTTARANCHAL": "UTTARAKHAND"
    }

    return aliases.get(value, value)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("IMPACT SPHERE - STATE LEVEL POTENTIAL UNMET NEED")
print("=" * 70)

print("\nLoading NFHS data...")

if not NFHS_FILE.exists():
    raise FileNotFoundError(
        f"NFHS file not found:\n{NFHS_FILE}"
    )

nfhs = pd.read_csv(NFHS_FILE)

print(
    "NFHS shape:",
    nfhs.shape
)


print("\nLoading MCA CSR data...")

if not CSR_FILE.exists():
    raise FileNotFoundError(
        f"CSR file not found:\n{CSR_FILE}"
    )

csr = pd.read_csv(CSR_FILE)

print(
    "CSR shape:",
    csr.shape
)


# ============================================================
# CHECK COLUMNS
# ============================================================

required_nfhs = [
    "district",
    "state",
    "health_need_score"
]

required_csr = [
    "csr_state",
    "project_amount_spent_inr",
    "company_name"
]

missing_nfhs = [
    c for c in required_nfhs
    if c not in nfhs.columns
]

missing_csr = [
    c for c in required_csr
    if c not in csr.columns
]

if missing_nfhs:
    raise KeyError(
        f"Missing NFHS columns: {missing_nfhs}"
    )

if missing_csr:
    raise KeyError(
        f"Missing CSR columns: {missing_csr}"
    )


# ============================================================
# NORMALIZE STATE NAMES
# ============================================================

nfhs["state_normalized"] = (
    nfhs["state"]
    .apply(normalize_state)
)

csr["state_normalized"] = (
    csr["csr_state"]
    .apply(normalize_state)
)


# ============================================================
# CONVERT CSR SPENDING TO NUMERIC
# ============================================================

csr["project_amount_spent_inr"] = pd.to_numeric(
    csr["project_amount_spent_inr"],
    errors="coerce"
)

csr["project_amount_spent_inr"] = (
    csr["project_amount_spent_inr"]
    .fillna(0)
)


# ============================================================
# AGGREGATE NFHS BY STATE
# ============================================================

print("\nAggregating NFHS district need by state...")

state_need = (
    nfhs
    .groupby("state_normalized")
    .agg(
        average_health_need=(
            "health_need_score",
            "mean"
        ),

        maximum_health_need=(
            "health_need_score",
            "max"
        ),

        districts_available=(
            "district",
            "nunique"
        )
    )
    .reset_index()
)


# ============================================================
# AGGREGATE CSR BY STATE
# ============================================================

print("Aggregating historical CSR spending by state...")

state_csr = (
    csr
    .groupby("state_normalized")
    .agg(
        historical_csr_spending_inr=(
            "project_amount_spent_inr",
            "sum"
        ),

        csr_project_count=(
            "project_amount_spent_inr",
            "count"
        ),

        companies_involved=(
            "company_name",
            "nunique"
        )
    )
    .reset_index()
)


# ============================================================
# MERGE
# ============================================================

print("Matching NFHS and CSR states...")

result = pd.merge(
    state_need,
    state_csr,
    on="state_normalized",
    how="outer"
)


# ============================================================
# HANDLE MISSING VALUES
# ============================================================

result["average_health_need"] = (
    result["average_health_need"]
    .fillna(0)
)

result["maximum_health_need"] = (
    result["maximum_health_need"]
    .fillna(0)
)

result["districts_available"] = (
    result["districts_available"]
    .fillna(0)
)

result["historical_csr_spending_inr"] = (
    result["historical_csr_spending_inr"]
    .fillna(0)
)

result["csr_project_count"] = (
    result["csr_project_count"]
    .fillna(0)
)

result["companies_involved"] = (
    result["companies_involved"]
    .fillna(0)
)


# ============================================================
# NORMALIZATION FUNCTION
# ============================================================

def min_max_100(series):

    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return pd.Series(
            50.0,
            index=series.index
        )

    return (
        (series - minimum)
        / (maximum - minimum)
    ) * 100


# ============================================================
# HEALTH NEED SCORE
# ============================================================

result["health_need_score"] = min_max_100(
    result["average_health_need"]
)


# ============================================================
# CSR SUPPLY SCORE
#
# Higher historical CSR spending = higher existing
# funding supply.
# ============================================================

result["csr_supply_score"] = min_max_100(
    np.log1p(
        result["historical_csr_spending_inr"]
    )
)


# ============================================================
# FUNDING GAP SCORE
#
# Lower CSR supply relative to other states produces
# a higher funding-gap signal.
# ============================================================

result["funding_gap_score"] = (
    100
    - result["csr_supply_score"]
)


# ============================================================
# POTENTIAL UNMET NEED
#
# This is a prioritization signal, NOT a legal metric
# and NOT a causal impact estimate.
# ============================================================

result["potential_unmet_need_score"] = (
    0.70 * result["health_need_score"]
    +
    0.30 * result["funding_gap_score"]
)


# ============================================================
# ROUND VALUES
# ============================================================

numeric_columns = [
    "average_health_need",
    "maximum_health_need",
    "health_need_score",
    "csr_supply_score",
    "funding_gap_score",
    "potential_unmet_need_score"
]

for column in numeric_columns:

    result[column] = (
        result[column]
        .round(2)
    )


# ============================================================
# SORT
# ============================================================

result = result.sort_values(
    "potential_unmet_need_score",
    ascending=False
)


# ============================================================
# SAVE
# ============================================================

result.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8"
)


# ============================================================
# DISPLAY
# ============================================================

print("\n" + "=" * 70)
print("TOP STATES BY POTENTIAL UNMET NEED")
print("=" * 70)

display_columns = [
    "state_normalized",
    "health_need_score",
    "historical_csr_spending_inr",
    "csr_project_count",
    "funding_gap_score",
    "potential_unmet_need_score"
]

print(
    result[
        display_columns
    ]
    .head(15)
    .to_string(index=False)
)


# ============================================================
# MATCHING SUMMARY
# ============================================================

nfhs_states = set(
    nfhs["state_normalized"].unique()
)

csr_states = set(
    csr["state_normalized"].unique()
)

matched_states = (
    nfhs_states
    & csr_states
)

print("\n" + "-" * 70)
print("STATE MATCHING")
print("-" * 70)

print(
    "NFHS states:",
    len(nfhs_states)
)

print(
    "CSR states:",
    len(csr_states)
)

print(
    "Matched states:",
    len(matched_states)
)


# ============================================================
# SUCCESS
# ============================================================

print("\n" + "=" * 70)
print("SUCCESS")
print("=" * 70)

print("\nSaved to:")

print(OUTPUT_FILE)

print(
    "\nNOTE:"
)

print(
    "potential_unmet_need_score is a "
    "prioritization signal based on "
    "health need and historical CSR supply."
)

print(
    "It is not a statutory CSR metric "
    "and does not represent causal impact."
)