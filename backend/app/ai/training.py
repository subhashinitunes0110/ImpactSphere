from pathlib import Path
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

import joblib


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[3]

DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "csr_clean.csv"
)

MODEL_DIR = (
    BASE_DIR
    / "models"
    / "classifier"
)

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

MODEL_FILE = (
    MODEL_DIR
    / "csr_sector_classifier.joblib"
)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("IMPACT SPHERE - CSR PROJECT CLASSIFIER")
print("=" * 70)

print("\nLoading real MCA CSR data...")

if not DATA_FILE.exists():

    raise FileNotFoundError(
        f"Dataset not found:\n{DATA_FILE}"
    )

df = pd.read_csv(DATA_FILE)

print(
    "\nDataset shape:",
    df.shape
)


# ============================================================
# CHECK COLUMNS
# ============================================================

required_columns = [
    "csr_development_sector",
    "csr_sub_development_sector"
]

missing = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing:

    raise KeyError(
        f"Missing columns: {missing}"
    )


# ============================================================
# CREATE TEXT FEATURE
# ============================================================

df["csr_development_sector"] = (
    df["csr_development_sector"]
    .fillna("")
    .astype(str)
    .str.strip()
)

df["csr_sub_development_sector"] = (
    df["csr_sub_development_sector"]
    .fillna("")
    .astype(str)
    .str.strip()
)


# We use the sub-sector as the textual description available
# in this MCA export and predict the broader CSR sector.

df["text"] = (
    df["csr_sub_development_sector"]
    + " "
    + df["csr_development_sector"]
)


# ============================================================
# REMOVE INVALID ROWS
# ============================================================

df = df[
    (df["text"].str.strip() != "")
    &
    (df["csr_development_sector"].str.strip() != "")
].copy()


# ============================================================
# REMOVE VERY RARE LABELS
#
# Logistic Regression needs enough examples per class.
# ============================================================

label_counts = (
    df["csr_development_sector"]
    .value_counts()
)

valid_labels = label_counts[
    label_counts >= 10
].index

df = df[
    df["csr_development_sector"]
    .isin(valid_labels)
].copy()


print(
    "\nRows used for training:",
    len(df)
)

print(
    "Number of sectors:",
    df["csr_development_sector"].nunique()
)


# ============================================================
# SHOW LABEL DISTRIBUTION
# ============================================================

print("\n" + "-" * 70)
print("SECTOR DISTRIBUTION")
print("-" * 70)

print(
    df["csr_development_sector"]
    .value_counts()
    .head(20)
    .to_string()
)


# ============================================================
# FEATURES + TARGET
# ============================================================

X = df["text"]

y = df["csr_development_sector"]


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)


print("\nTraining rows:", len(X_train))
print("Testing rows:", len(X_test))


# ============================================================
# MODEL
# ============================================================

model = Pipeline(
    [
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                ngram_range=(1, 2),
                min_df=2,
                max_features=50000,
                sublinear_tf=True
            )
        ),

        (
            "classifier",
            LogisticRegression(
                max_iter=1000,
                class_weight="balanced"
            )
        )
    ]
)


# ============================================================
# TRAIN
# ============================================================

print("\nTraining model...")

model.fit(
    X_train,
    y_train
)


# ============================================================
# EVALUATE
# ============================================================

print("\nEvaluating model...")

predictions = model.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(
    f"\nAccuracy: {accuracy:.4f}"
)


print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)


# ============================================================
# SAVE MODEL
# ============================================================

joblib.dump(
    model,
    MODEL_FILE
)

print("\n" + "=" * 70)
print("MODEL SAVED")
print("=" * 70)

print(
    "\nModel:",
    MODEL_FILE
)

print(
    "\nAccuracy:",
    round(accuracy, 4)
)

print("\nTraining complete.")