"""
Impact Sphere - Confidence Engine

Determines how confident the AI system is in its classification.
Low-confidence predictions are sent for human review.
"""


def assess_confidence(confidence: float) -> dict:
    """
    Convert a numerical confidence score into a human-readable
    confidence level and determine whether human review is required.

    Thresholds:
        >= 0.80  -> high
        >= 0.60  -> medium
        <  0.60  -> low + human review
    """

    # Keep confidence within valid range
    confidence = max(0.0, min(1.0, float(confidence)))

    if confidence >= 0.80:
        level = "high"
        human_review = False

    elif confidence >= 0.60:
        level = "medium"
        human_review = False

    else:
        level = "low"
        human_review = True

    return {
        "confidence": round(confidence, 4),
        "confidence_percent": round(confidence * 100, 2),
        "level": level,
        "human_review_required": human_review,
    }


# Simple standalone test
if __name__ == "__main__":
    print("=" * 55)
    print("IMPACT SPHERE - CONFIDENCE ENGINE")
    print("=" * 55)

    test_values = [0.94, 0.76, 0.51]

    for value in test_values:
        result = assess_confidence(value)

        print()
        print(f"Confidence: {result['confidence_percent']}%")
        print(f"Level: {result['level']}")
        print(f"Human review: {result['human_review_required']}")