from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sentence_transformers import SentenceTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parents[3]

DATA_PATH = BASE_DIR / "data" / "train.csv"

MODEL_DIR = BASE_DIR / "models" / "semantic_classifier"

CLASSIFIER_PATH = MODEL_DIR / "classifier.joblib"

EMBEDDING_MODEL_PATH = MODEL_DIR / "embedding_model_name.txt"


# =========================================================
# CONFIGURATION
# =========================================================

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# =========================================================
# LOAD DATA
# =========================================================

def load_dataset():

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH)

    required_columns = {"text", "label"}

    if not required_columns.issubset(df.columns):

        raise ValueError(
            "CSV must contain 'text' and 'label' columns."
        )

    df = df.dropna(
        subset=["text", "label"]
    )

    df["text"] = df["text"].astype(str)
    df["label"] = df["label"].astype(str)

    return df


# =========================================================
# LOAD SENTENCE TRANSFORMER
# =========================================================

def load_embedding_model():

    print()
    print("Loading Sentence Transformer...")
    print(f"Model: {EMBEDDING_MODEL}")

    model = SentenceTransformer(
        EMBEDDING_MODEL
    )

    print("Embedding model loaded.")

    return model


# =========================================================
# GENERATE EMBEDDINGS
# =========================================================

def generate_embeddings(
    model,
    texts
):

    print()
    print("Generating semantic embeddings...")

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        normalize_embeddings=True,
    )

    return np.asarray(embeddings)


# =========================================================
# TRAIN MODEL
# =========================================================

def train_model():

    print()
    print("=" * 60)
    print("IMPACT SPHERE SEMANTIC CLASSIFIER")
    print("=" * 60)

    # Load dataset
    df = load_dataset()

    print()
    print(f"Dataset size: {len(df)}")
    print(f"Categories: {df['label'].nunique()}")

    # Split BEFORE generating embeddings
    X_train_text, X_test_text, y_train, y_test = train_test_split(
        df["text"].tolist(),
        df["label"].tolist(),
        test_size=0.20,
        random_state=42,
        stratify=df["label"],
    )

    print()
    print(f"Training samples: {len(X_train_text)}")
    print(f"Testing samples: {len(X_test_text)}")

    # Load embedding model
    embedding_model = load_embedding_model()

    # Generate embeddings
    X_train = generate_embeddings(
        embedding_model,
        X_train_text
    )

    X_test = generate_embeddings(
        embedding_model,
        X_test_text
    )

    print()
    print(f"Embedding dimensions: {X_train.shape[1]}")

    # =====================================================
    # TRAIN CLASSIFIER
    # =====================================================

    print()
    print("Training Logistic Regression classifier...")

    classifier = LogisticRegression(
        max_iter=2000
    )

    classifier.fit(
        X_train,
        y_train
    )

    # =====================================================
    # EVALUATION
    # =====================================================

    predictions = classifier.predict(
        X_test
    )

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    print()
    print("=" * 60)
    print("MODEL EVALUATION")
    print("=" * 60)

    print()
    print(f"Accuracy: {accuracy:.4f}")

    print()
    print("Classification Report:")
    print()

    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )

    # =====================================================
    # SAVE MODEL
    # =====================================================

    MODEL_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    joblib.dump(
        classifier,
        CLASSIFIER_PATH
    )

    EMBEDDING_MODEL_PATH.write_text(
        EMBEDDING_MODEL,
        encoding="utf-8"
    )

    print()
    print("=" * 60)
    print("MODEL SAVED")
    print("=" * 60)

    print()
    print(
        f"Classifier:\n{CLASSIFIER_PATH}"
    )

    print()
    print(
        f"Embedding model:\n{EMBEDDING_MODEL}"
    )

    return embedding_model, classifier


# =========================================================
# PREDICT
# =========================================================

def predict_category(
    embedding_model,
    classifier,
    text
):

    embedding = embedding_model.encode(
        [text],
        normalize_embeddings=True
    )

    probabilities = classifier.predict_proba(
        embedding
    )[0]

    classes = classifier.classes_

    best_index = probabilities.argmax()

    category = classes[best_index]

    confidence = probabilities[best_index]

    # Sort all categories by probability
    ranked = sorted(
        zip(classes, probabilities),
        key=lambda x: x[1],
        reverse=True
    )

    return {
        "category": category,
        "confidence": float(confidence),
        "ranked_predictions": [
            {
                "category": label,
                "confidence": float(probability)
            }
            for label, probability in ranked
        ]
    }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    embedding_model, classifier = train_model()

    print()
    print("=" * 60)
    print("IMPACT SPHERE TEST PREDICTIONS")
    print("=" * 60)

    test_proposals = [

        """
        A mobile medical unit will travel to remote villages
        and provide free health screening, medicines and
        preventive healthcare services.
        """,

        """
        The project will provide scholarships, digital
        classrooms and additional learning support to
        students from disadvantaged communities.
        """,

        """
        Rural women will receive entrepreneurship training,
        financial literacy education and support for starting
        small businesses.
        """,

        """
        The initiative will install clean drinking water
        systems and sanitation facilities in villages that
        lack reliable access to safe water.
        """,

        """
        The program will establish community sports centres
        and provide professional coaching to talented
        children from underserved areas.
        """,
    ]

    for index, proposal in enumerate(
        test_proposals,
        start=1
    ):

        result = predict_category(
            embedding_model,
            classifier,
            proposal
        )

        print()
        print(f"TEST PROPOSAL {index}")
        print("-" * 60)

        print(
            f"Prediction: {result['category']}"
        )

        print(
            f"Confidence: {result['confidence']:.2%}"
        )

        print()
        print("Top predictions:")

        for item in result["ranked_predictions"][:3]:

            print(
                f"  {item['category']}: "
                f"{item['confidence']:.2%}"
            )