from app.ai.confidence import (
    build_confidence_result
)


def main():

    test_scores = [
        0.94,
        0.76,
        0.51
    ]

    print()
    print("=" * 60)
    print("IMPACT SPHERE - CONFIDENCE ENGINE")
    print("=" * 60)

    for score in test_scores:

        result = build_confidence_result(
            score
        )

        print()
        print(
            f"Confidence: {result['percentage']}%"
        )

        print(
            f"Level: {result['level']}"
        )

        print(
            f"Human review: "
            f"{result['human_review_required']}"
        )


if __name__ == "__main__":
    main()