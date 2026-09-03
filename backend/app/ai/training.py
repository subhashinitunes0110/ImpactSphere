import os
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    classification_report,
    confusion_matrix
)
import joblib


# ============================================================
# CONFIG
# ============================================================

DATA_PATH = "data/processed/csr_clean.csv"

MODEL_DIR = "models/classifier"
MODEL_PATH = os.path.join(
    MODEL_DIR,
    "csr_sector_classifier.joblib"
)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 70)
print("IMPACT SPHERE - CSR SECTOR CLASSIFIER TRAINING")
print("=" * 70)

print("\nLoading real MCA CSR dataset...")

df = pd.read_csv(DATA_PATH)

print(f"Total records: {len(df):,}")


# ============================================================
# CLEAN DATA
# ============================================================

required_columns = [
    "csr_sub_development_sector",
    "csr_development_sector"
]

df = df.dropna(subset=required_columns)

df["csr_sub_development_sector"] = (
    df["csr_sub_development_sector"]
    .astype(str)
    .str.strip()
)

df["csr_development_sector"] = (
    df["csr_development_sector"]
    .astype(str)
    .str.strip()
)

df = df[
    (df["csr_sub_development_sector"] != "") &
    (df["csr_development_sector"] != "")
]

print(f"Usable records: {len(df):,}")

print(
    f"Unique development sectors: "
    f"{df['csr_development_sector'].nunique()}"
)

print(
    f"Unique sub-development sectors: "
    f"{df['csr_sub_development_sector'].nunique()}"
)


# ============================================================
# FEATURES AND TARGET
# ============================================================

X = df["csr_sub_development_sector"]
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

print("\nDataset split:")
print(f"Training samples: {len(X_train):,}")
print(f"Testing samples:  {len(X_test):,}")


# ============================================================
# MODEL
# ============================================================

model = Pipeline([
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
])


# ============================================================
# TRAIN
# ============================================================

print("\nTraining model...")

model.fit(X_train, y_train)

print("Training complete.")


# ============================================================
# PREDICTION
# ============================================================

y_pred = model.predict(X_test)


# ============================================================
# METRICS
# ============================================================

accuracy = accuracy_score(y_test, y_pred)

precision, recall, f1, _ = precision_recall_fscore_support(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0
)

print("\n" + "=" * 70)
print("MODEL PERFORMANCE")
print("=" * 70)

print(f"\nAccuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")


# ============================================================
# DETAILED REPORT
# ============================================================

print("\n" + "=" * 70)
print("CLASSIFICATION REPORT")
print("=" * 70)

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

labels = sorted(y_test.unique())

cm = confusion_matrix(
    y_test,
    y_pred,
    labels=labels
)

print("\n" + "=" * 70)
print("CONFUSION MATRIX")
print("=" * 70)

print("\nClasses:")

for i, label in enumerate(labels):
    print(f"{i}: {label}")

print("\nMatrix:")
print(cm)


# ============================================================
# SAVE MODEL
# ============================================================

os.makedirs(MODEL_DIR, exist_ok=True)

joblib.dump(
    model,
    MODEL_PATH
)

print("\n" + "=" * 70)
print("MODEL SAVED")
print("=" * 70)

print(f"\nSaved to:")
print(MODEL_PATH)

print("\nTraining pipeline completed successfully.")