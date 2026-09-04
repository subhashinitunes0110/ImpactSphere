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
# CSR KEYWORD EVIDENCE
# =========================================================

CSR_KEYWORDS = {

    "healthcare": [
        "healthcare",
        "health care",
        "medical",
        "medicine",
        "medicines",
        "doctor",
        "doctors",
        "hospital",
        "hospitals",
        "clinic",
        "clinics",
        "health services",
        "medical services",
        "health checkup",
        "health checkups",
        "preventive healthcare",
    ],

    "education": [
        "education",
        "school",
        "schools",
        "student",
        "students",
        "education facilities",
        "digital learning",
        "digital education",
        "learning resources",
        "literacy",
        "teaching",
        "classroom",
    ],

    "skill development": [
        "skill development",
        "vocational training",
        "vocational",
        "skill training",
        "job training",
        "employment training",
        "career training",
        "entrepreneurship training",
    ],

    "women empowerment": [
        "women empowerment",
        "women empowerment",
        "women",
        "girl",
        "girls",
        "gender equality",
        "women entrepreneurship",
        "women livelihood",
    ],

    "environment": [
        "environment",
        "environmental",
        "sustainability",
        "environmental sustainability",
        "tree plantation",
        "afforestation",
        "renewable energy",
        "clean energy",
        "waste management",
        "water conservation",
        "biodiversity",
    ],

    "rural development": [
        "rural development",
        "rural communities",
        "rural community",
        "village development",
        "village",
        "villages",
        "rural infrastructure",
        "rural livelihood",
    ],

    "slum development": [
        "slum development",
        "slum",
        "slums",
        "urban poor",
        "slum rehabilitation",
    ],

    "disaster management": [
        "disaster management",
        "disaster relief",
        "disaster response",
        "flood relief",
        "earthquake relief",
        "cyclone relief",
        "emergency relief",
    ],
}


def _keyword_evidence(
    text: str,
    predicted_category: str,
):
    """
    Check whether the proposal contains strong textual evidence
    supporting the ML model's predicted CSR category.

    This does NOT replace the ML classifier.

    It acts as an explainable confidence-support layer for
    obvious CSR activities.
    """

    normalized_text = text.lower()

    category = predicted_category.strip().lower()

    keywords = CSR_KEYWORDS.get(
        category,
        []
    )

    matched_keywords = [
        keyword
        for keyword in keywords
        if keyword in normalized_text
    ]

    return matched_keywords


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

    ml_confidence = 0.0

    if hasattr(classifier, "predict_proba"):

        probabilities = classifier.predict_proba(
            [text]
        )[0]

        ml_confidence = float(
            max(probabilities)
        )

    category = str(prediction)

    # =====================================================
    # EXPLAINABLE KEYWORD EVIDENCE
    # =====================================================

    matched_keywords = _keyword_evidence(
        text,
        category
    )

    # Strong keyword evidence supports the ML prediction.
    #
    # We deliberately do NOT make every keyword match
    # automatically high confidence.
    #
    # The confidence is capped at 0.95 because the final
    # decision should still remain explainable and reviewable.

    confidence = ml_confidence

    if len(matched_keywords) >= 3:

        confidence = max(
            confidence,
            0.90
        )

    elif len(matched_keywords) >= 2:

        confidence = max(
            confidence,
            0.80
        )

    elif len(matched_keywords) >= 1:

        confidence = max(
            confidence,
            0.70
        )

    confidence = min(
        confidence,
        0.95
    )

    confidence_level = get_confidence_level(
        confidence
    )

    human_review = confidence < 0.60

    return {
        "category": category,

        "confidence": round(
            confidence,
            4
        ),

        "confidence_level": confidence_level,

        "human_review_required": human_review,

        "evidence": {
            "matched_keywords": matched_keywords,
            "ml_confidence": round(
                ml_confidence,
                4
            ),
        },
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

    print(
        "ML Confidence:",
        result["evidence"]["ml_confidence"]
    )

    print(
        "Matched Keywords:",
        result["evidence"]["matched_keywords"]
    )