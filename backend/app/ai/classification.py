from pathlib import Path
import joblib


# =========================================================
# CONFIG
# =========================================================

MODEL_PATH = (
    Path(__file__).resolve().parents[3]
    / "models"
    / "classifier"
    / "csr_classifier.joblib"
)


_classifier = None


# =========================================================
# LOAD MODEL
# =========================================================

def get_classifier():

    global _classifier

    if _classifier is None:

        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Classifier model not found at:\n{MODEL_PATH}"
            )

        print("Loading CSR classifier...")

        _classifier = joblib.load(MODEL_PATH)

        print("CSR classifier ready.")

    return _classifier


# =========================================================
# CONFIDENCE
# =========================================================

def get_confidence_level(confidence):

    if confidence >= 0.80:
        return "high"

    if confidence >= 0.60:
        return "medium"

    return "low"


# =========================================================
# CLASSIFY PROJECT
# =========================================================

def classify_project(text: str):

    if not text or not text.strip():
        raise ValueError(
            "Project text cannot be empty."
        )

    classifier = get_classifier()

    # IMPORTANT:
    # TF-IDF classifier receives RAW TEXT.
    prediction = classifier.predict(
        [text]
    )[0]

    confidence = 0.0

    if hasattr(classifier, "predict_proba"):

        probabilities = classifier.predict_proba(
            [text]
        )[0]

        confidence = float(
            max(probabilities)
        )

    confidence_level = get_confidence_level(
        confidence
    )

    human_review = confidence < 0.60

    return {
        "category": str(prediction),
        "confidence": round(confidence, 4),
        "confidence_level": confidence_level,
        "human_review_required": human_review
    }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    text = """
    Mobile healthcare units will provide free
    medical checkups, medicines and preventive
    healthcare services to remote rural communities.
    """

    result = classify_project(text)

    print("\n========================================")
    print("IMPACT SPHERE - CLASSIFICATION")
    print("========================================")

    print("Category:", result["category"])
    print("Confidence:", result["confidence"])
    print("Confidence Level:", result["confidence_level"])
    print("Human Review:", result["human_review_required"])