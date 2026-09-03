from pprint import pprint

from app.ai.pipeline import analyze_proposal


def main():

    proposal = """
    Rural Healthcare Initiative

    The project will establish mobile healthcare units
    to provide free medical checkups, medicines and
    preventive healthcare services to remote rural
    communities in Barmer district of Rajasthan.

    The program will operate for 24 months and is expected
    to benefit approximately 12,000 people.

    Priority beneficiaries include low-income rural families,
    elderly citizens and people who have limited access to
    healthcare facilities.
    """

    needs = [

        {
            "id": 1,

            "description":
                "Remote rural communities have limited "
                "access to healthcare facilities, doctors "
                "and essential medical services."
        },

        {
            "id": 2,

            "description":
                "Children from disadvantaged communities "
                "lack access to quality education and "
                "digital learning facilities."
        },

        {
            "id": 3,

            "description":
                "Rural women need livelihood opportunities, "
                "entrepreneurship training and financial "
                "independence."
        },

        {
            "id": 4,

            "description":
                "Villages lack reliable access to clean "
                "drinking water and sanitation facilities."
        },

        {
            "id": 5,

            "description":
                "Underserved communities require better "
                "sports infrastructure and coaching."
        }
    ]

    print()
    print("=" * 70)
    print("IMPACT SPHERE - COMPLETE AI PIPELINE")
    print("=" * 70)

    result = analyze_proposal(
        proposal,
        needs
    )

    print()
    print("=" * 70)
    print("FINAL ANALYSIS")
    print("=" * 70)

    print()

    print("PROJECT INFORMATION")
    print("-" * 70)

    pprint(
        result["project"]
    )

    print()

    print("CLASSIFICATION")
    print("-" * 70)

    print(
        "Category:",
        result[
            "classification"
        ]["category"]
    )

    print(
        "Confidence:",
        result[
            "classification"
        ]["confidence"]
    )

    print(
        "Confidence Level:",
        result[
            "classification"
        ]["confidence_level"]
    )

    print(
        "Human Review Required:",
        result[
            "classification"
        ]["human_review_required"]
    )

    print()

    print("TOP NEED MATCH")
    print("-" * 70)

    pprint(
        result[
            "need_analysis"
        ]["top_match"]
    )

    print()
    print("=" * 70)
    print("PIPELINE COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()