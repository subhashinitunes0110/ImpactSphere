from pathlib import Path
import pandas as pd
import numpy as np


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[4]

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "raw"
    / "NFHS_5_India_Districts_Factsheet_Data.xls"
)

OUTPUT_DIR = BASE_DIR / "data" / "processed"

OUTPUT_FILE = OUTPUT_DIR / "nfhs_district_need.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("IMPACT SPHERE - NFHS-5 DISTRICT NEED PREPARATION")
print("=" * 70)

print("\nLoading:")
print(INPUT_FILE)

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"NFHS file not found:\n{INPUT_FILE}"
    )

df = pd.read_excel(INPUT_FILE)

print("\nOriginal shape:", df.shape)


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .astype(str)
    .str.strip()
)

print("\nDistrict column check:")

if "District Names" not in df.columns:
    raise KeyError(
        "Column 'District Names' was not found."
    )

if "State/UT" not in df.columns:
    raise KeyError(
        "Column 'State/UT' was not found."
    )


# ============================================================
# BASIC DISTRICT INFORMATION
# ============================================================

result = pd.DataFrame()

result["district"] = (
    df["District Names"]
    .astype(str)
    .str.strip()
)

result["state"] = (
    df["State/UT"]
    .astype(str)
    .str.strip()
)


# ============================================================
# REMOVE INVALID DISTRICTS
# ============================================================

invalid_values = [
    "",
    "nan",
    "NaN",
    "None",
    "Total",
    "TOTAL"
]

result = result[
    ~result["district"].isin(invalid_values)
].copy()


# ============================================================
# NFHS HEALTH / NUTRITION NEED INDICATORS
#
# These are indicators where HIGHER values generally
# represent greater deprivation / health burden.
# ============================================================

need_keywords = [
    "stunted",
    "wasted",
    "underweight",
    "anaemia",
    "anemia",
    "not fully immunized",
    "diarrhoea",
    "fever",
    "acute respiratory",
    "low birth weight",
    "unmet need",
    "no facility",
    "no toilet",
    "open defecation",
    "tobacco",
    "alcohol",
    "elevated blood pressure",
    "high blood sugar",
    "hypertension",
    "blood pressure"
]


# ============================================================
# FIND MATCHING NFHS COLUMNS
# ============================================================

selected_columns = []

for column in df.columns:

    column_lower = column.lower()

    for keyword in need_keywords:

        if keyword in column_lower:

            # Ignore district/state identifiers
            if column not in [
                "District Names",
                "State/UT"
            ]:
                selected_columns.append(column)

            break


# Remove duplicates while preserving order

selected_columns = list(
    dict.fromkeys(selected_columns)
)


# ============================================================
# SHOW SELECTED INDICATORS
# ============================================================

print("\n" + "-" * 70)
print("SELECTED NEED INDICATORS")
print("-" * 70)

for i, column in enumerate(selected_columns):
    print(f"{i + 1}. {column}")

print(
    f"\nTotal indicators selected: "
    f"{len(selected_columns)}"
)


# ============================================================
# CHECK
# ============================================================

if len(selected_columns) == 0:

    raise ValueError(
        "No NFHS need indicators were detected. "
        "Check the column names."
    )


# ============================================================
# NORMALIZATION
#
# Convert each indicator to a 0-100 deprivation score.
#
# 0   = relatively lower burden
# 100 = relatively higher burden
# ============================================================

need_scores = []

for column in selected_columns:

    values = pd.to_numeric(
        df[column],
        errors="coerce"
    )

    # If almost everything is missing, skip it
    if values.notna().sum() < 10:
        continue

    minimum = values.min()
    maximum = values.max()

    if pd.isna(minimum) or pd.isna(maximum):
        continue

    # Avoid division by zero
    if maximum == minimum:

        normalized = pd.Series(
            0.0,
            index=df.index
        )

    else:

        normalized = (
            (values - minimum)
            / (maximum - minimum)
        ) * 100

    need_scores.append(normalized)


# ============================================================
# BUILD OVERALL HEALTH NEED SCORE
# ============================================================

need_matrix = pd.concat(
    need_scores,
    axis=1
)

overall_need = need_matrix.mean(
    axis=1,
    skipna=True
)


# ============================================================
# ADD SCORE TO RESULT
# ============================================================

result["health_need_score"] = (
    overall_need
    .round(2)
)


# ============================================================
# ADD NUMBER OF INDICATORS AVAILABLE
# ============================================================

result["need_indicators_available"] = (
    need_matrix.notna().sum(axis=1)
)


# ============================================================
# REMOVE DUPLICATE DISTRICTS
# ============================================================

result = (
    result
    .drop_duplicates(
        subset=["district", "state"]
    )
)


# ============================================================
# SORT
# ============================================================

result = result.sort_values(
    "health_need_score",
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
# SUMMARY
# ============================================================

print("\n" + "=" * 70)
print("NFHS NEED DATA CREATED")
print("=" * 70)

print("\nDistricts:", len(result))

print(
    "States:",
    result["state"].nunique()
)

print(
    "Average health need score:",
    round(
        result["health_need_score"].mean(),
        2
    )
)

print(
    "Highest health need score:",
    round(
        result["health_need_score"].max(),
        2
    )
)

print(
    "Lowest health need score:",
    round(
        result["health_need_score"].min(),
        2
    )
)


# ============================================================
# TOP 10 HIGH-NEED DISTRICTS
# ============================================================

print("\n" + "-" * 70)
print("TOP 10 HIGH-NEED DISTRICTS")
print("-" * 70)

print(
    result[
        [
            "district",
            "state",
            "health_need_score",
            "need_indicators_available"
        ]
    ]
    .head(10)
    .to_string(index=False)
)


# ============================================================
# SUCCESS
# ============================================================

print("\n" + "=" * 70)
print("SUCCESS")
print("=" * 70)

print("\nSaved to:")
print(OUTPUT_FILE)