from pathlib import Path
import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[4]

INPUT_FILE = BASE_DIR / "data" / "processed" / "csr_clean.csv"
OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "csr_state_sector_year.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("IMPACT SPHERE - CSR FUNDING PATTERN ANALYSIS")
print("=" * 70)

print("\nLoading:")
print(INPUT_FILE)

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Could not find:\n{INPUT_FILE}\n\n"
        "Run prepare_csr_data.py first."
    )

df = pd.read_csv(INPUT_FILE)

print(f"\nInput shape: {df.shape}")


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

required_columns = [
    "financial_year",
    "csr_state",
    "csr_development_sector",
    "project_amount_spent_inr"
]

missing = [
    column for column in required_columns
    if column not in df.columns
]

if missing:
    print("\nAvailable columns:")
    print(df.columns.tolist())

    raise KeyError(
        f"\nMissing required columns: {missing}"
    )


# ============================================================
# CLEAN GROUPING COLUMNS
# ============================================================

for column in [
    "financial_year",
    "csr_state",
    "csr_development_sector"
]:
    df[column] = (
        df[column]
        .astype("string")
        .str.strip()
    )


# Remove rows without required information

df = df.dropna(
    subset=[
        "financial_year",
        "csr_state",
        "csr_development_sector"
    ]
)


# ============================================================
# AGGREGATE STATE × SECTOR × YEAR
# ============================================================

grouped = (
    df.groupby(
        [
            "financial_year",
            "csr_state",
            "csr_development_sector"
        ],
        dropna=False
    )
    .agg(
        total_csr_spent_inr=(
            "project_amount_spent_inr",
            "sum"
        ),

        total_projects=(
            "project_amount_spent_inr",
            "count"
        ),

        average_project_spend_inr=(
            "project_amount_spent_inr",
            "mean"
        ),

        median_project_spend_inr=(
            "project_amount_spent_inr",
            "median"
        ),

        maximum_project_spend_inr=(
            "project_amount_spent_inr",
            "max"
        ),

        minimum_project_spend_inr=(
            "project_amount_spent_inr",
            "min"
        )
    )
    .reset_index()
)


# ============================================================
# CONVERT TO CRORES
# ============================================================

grouped["total_csr_spent_cr"] = (
    grouped["total_csr_spent_inr"] / 10_000_000
)

grouped["average_project_spend_cr"] = (
    grouped["average_project_spend_inr"] / 10_000_000
)


# ============================================================
# PROJECT SHARE WITHIN STATE + YEAR
# ============================================================

state_year_projects = (
    grouped
    .groupby(
        ["financial_year", "csr_state"]
    )["total_projects"]
    .transform("sum")
)

grouped["sector_project_share"] = (
    grouped["total_projects"]
    / state_year_projects
)


# ============================================================
# SPENDING SHARE WITHIN STATE + YEAR
# ============================================================

state_year_spending = (
    grouped
    .groupby(
        ["financial_year", "csr_state"]
    )["total_csr_spent_inr"]
    .transform("sum")
)

grouped["sector_spending_share"] = (
    grouped["total_csr_spent_inr"]
    / state_year_spending
)


# ============================================================
# SORT
# ============================================================

grouped = grouped.sort_values(
    [
        "financial_year",
        "csr_state",
        "total_csr_spent_inr"
    ],
    ascending=[True, True, False]
)


# ============================================================
# SAVE
# ============================================================

grouped.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8"
)


# ============================================================
# REPORT
# ============================================================

print("\n" + "=" * 70)
print("FUNDING PATTERN SUMMARY")
print("=" * 70)

print(f"\nAggregated rows: {len(grouped)}")

print(
    f"States represented: "
    f"{grouped['csr_state'].nunique()}"
)

print(
    f"Sectors represented: "
    f"{grouped['csr_development_sector'].nunique()}"
)

print(
    f"Financial years represented: "
    f"{grouped['financial_year'].nunique()}"
)


# ============================================================
# TOP STATES
# ============================================================

print("\n" + "-" * 70)
print("TOP STATES BY CSR SPENDING")
print("-" * 70)

top_states = (
    grouped
    .groupby("csr_state")["total_csr_spent_cr"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(top_states.to_string())


# ============================================================
# TOP SECTORS
# ============================================================

print("\n" + "-" * 70)
print("TOP CSR SECTORS")
print("-" * 70)

top_sectors = (
    grouped
    .groupby("csr_development_sector")[
        "total_csr_spent_cr"
    ]
    .sum()
    .sort_values(ascending=False)
    .head(15)
)

print(top_sectors.to_string())


# ============================================================
# TOP STATE × SECTOR COMBINATIONS
# ============================================================

print("\n" + "-" * 70)
print("TOP STATE × SECTOR COMBINATIONS")
print("-" * 70)

top_combinations = grouped.nlargest(
    15,
    "total_csr_spent_cr"
)[
    [
        "financial_year",
        "csr_state",
        "csr_development_sector",
        "total_csr_spent_cr",
        "total_projects"
    ]
]

print(
    top_combinations.to_string(index=False)
)


# ============================================================
# SUCCESS
# ============================================================

print("\n" + "=" * 70)
print("SUCCESS")
print("=" * 70)

print("\nSaved to:")
print(OUTPUT_FILE)