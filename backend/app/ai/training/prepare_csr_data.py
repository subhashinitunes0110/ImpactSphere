from pathlib import Path
import pandas as pd


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[4]

RAW_FILE = BASE_DIR / "data" / "raw" / "CSR_Report_2026-09-03.csv"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "csr_clean.csv"


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 60)
print("IMPACT SPHERE - CSR DATA PREPROCESSING")
print("=" * 60)

print(f"\nLoading dataset:")
print(RAW_FILE)

if not RAW_FILE.exists():
    raise FileNotFoundError(
        f"\nDataset not found:\n{RAW_FILE}"
    )

df = pd.read_csv(RAW_FILE)

print(f"\nOriginal shape: {df.shape}")


# ============================================================
# STANDARDIZE COLUMN NAMES
# ============================================================

df.columns = [
    column.strip()
    .lower()
    .replace(" ", "_")
    .replace("(", "")
    .replace(")", "")
    .replace(".", "")
    .replace("-", "_")
    for column in df.columns
]

print("\nColumns:")
for column in df.columns:
    print(" -", column)


# ============================================================
# REMOVE EMPTY ROWS
# ============================================================

before = len(df)

df = df.dropna(how="all")

print(f"\nRemoved empty rows: {before - len(df)}")


# ============================================================
# CLEAN TEXT COLUMNS
# ============================================================

text_columns = [
    "company_name",
    "financial_year",
    "psu_non_psu",
    "csr_state",
    "csr_development_sector",
    "csr_sub_development_sector",
]

for column in text_columns:
    if column in df.columns:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
        )


# ============================================================
# CLEAN SPENDING COLUMN
# ============================================================

amount_column = "project_amount_spent_in_inr_cr"

if amount_column not in df.columns:
    raise KeyError(
        f"Financial column not found: {amount_column}"
    )

df[amount_column] = (
    df[amount_column]
    .astype(str)
    .str.replace(",", "", regex=False)
    .str.replace("₹", "", regex=False)
    .str.strip()
)

df[amount_column] = pd.to_numeric(
    df[amount_column],
    errors="coerce"
)


# ============================================================
# REMOVE INVALID SPENDING VALUES
# ============================================================

before = len(df)

df = df[
    df[amount_column].notna()
    & (df[amount_column] >= 0)
]

print(
    f"Removed invalid spending rows: "
    f"{before - len(df)}"
)


# ============================================================
# REMOVE DUPLICATES
# ============================================================

before = len(df)

df = df.drop_duplicates()

print(f"Removed duplicate rows: {before - len(df)}")


# ============================================================
# CREATE INR FEATURES
# ============================================================

df["project_amount_spent_inr"] = (
    df[amount_column] * 10_000_000
)

df["project_amount_spent_inr_lakh"] = (
    df[amount_column] * 100
)


# ============================================================
# DATA QUALITY REPORT
# ============================================================

print("\n" + "=" * 60)
print("DATA QUALITY REPORT")
print("=" * 60)

print(f"\nFinal rows: {len(df)}")
print(f"Final columns: {len(df.columns)}")

print("\nMissing values:")
print(df.isna().sum().to_string())


# ============================================================
# BASIC STATISTICS
# ============================================================

print("\n" + "=" * 60)
print("DATASET STATISTICS")
print("=" * 60)

print(
    f"\nNumber of states: "
    f"{df['csr_state'].nunique()}"
)

print(
    f"Number of main sectors: "
    f"{df['csr_development_sector'].nunique()}"
)

print(
    f"Number of sub-sectors: "
    f"{df['csr_sub_development_sector'].nunique()}"
)

print(
    f"Number of companies: "
    f"{df['company_name'].nunique()}"
)

print("\nFinancial years:")
print(
    df["financial_year"]
    .value_counts()
    .sort_index()
    .to_string()
)

print(
    f"\nTotal CSR spending: "
    f"{df[amount_column].sum():,.2f} Cr"
)


# ============================================================
# SAVE CLEAN DATA
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8"
)

print("\n" + "=" * 60)
print("SUCCESS")
print("=" * 60)

print(f"\nClean dataset saved to:")
print(OUTPUT_FILE)

print("\nPreview:")
print(df.head(5).to_string(index=False))