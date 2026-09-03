from app.ai.pipeline import analyze_proposal


def main():

    # =========================================================
    # SAMPLE CSR PROPOSAL
    # =========================================================

    proposal = """
    Rural Healthcare Initiative

    The project will establish mobile healthcare units to provide
    free medical checkups, medicines and preventive healthcare
    services to remote rural communities in Barmer district of
    Rajasthan.

    The program will operate for 24 months and is expected to
    benefit approximately 12,000 people.

    Priority beneficiaries include rural families, elderly
    citizens and people who have limited access to healthcare
    facilities.
    """

    # =========================================================
    # COMMUNITY NEEDS
    # =========================================================

    needs = [

        {
            "id": 1,
            "description":
                "Remote rural communities have limited access to "
                "healthcare facilities, doctors and essential "
                "medical services."
        },

        {
            "id": 2,
            "description":
                "Students from disadvantaged communities need "
                "better access to education and digital learning "
                "resources."
        },

        {
            "id": 3,
            "description":
                "Rural women require livelihood opportunities "
                "and entrepreneurship training."
        },

        {
            "id": 4,
            "description":
                "Villages lack reliable access to safe drinking "
                "water and sanitation infrastructure."
        },

        {
            "id": 5,
            "description":
                "Underserved communities need access to sports "
                "facilities and professional coaching."
        }

    ]

    # =========================================================
    # RUN AI PIPELINE
    # =========================================================

    result = analyze_proposal(
        proposal,
        needs
    )

    # =========================================================
    # FINAL ANALYSIS
    # =========================================================

    print("\n" + "=" * 60)
    print("FINAL ANALYSIS")
    print("=" * 60)

    # =========================================================
    # PROJECT INFORMATION
    # =========================================================

    print("\nPROJECT INFORMATION")
    print("-" * 60)

    print(result["project"])

    # =========================================================
    # CLASSIFICATION
    # =========================================================

    print("\nCLASSIFICATION")
    print("-" * 60)

    classification = result["classification"]

    print(
        "Category:",
        classification.get("category")
    )

    print(
        "Confidence:",
        classification.get("confidence")
    )

    print(
        "Confidence Level:",
        classification.get("confidence_level")
    )

    print(
        "Human Review Required:",
        classification.get("human_review_required")
    )

    # =========================================================
    # NEED MATCHING
    # =========================================================

    print("\nTOP NEED MATCH")
    print("-" * 60)

    need_matches = result.get(
        "need_matches",
        []
    )

    if need_matches:

        print(
            need_matches[0]
        )

    else:

        print(
            "No matching community need found."
        )

    # =========================================================
    # ALL NEED MATCHES
    # =========================================================

    print("\nALL NEED MATCHES")
    print("-" * 60)

    if need_matches:

        for index, match in enumerate(
            need_matches,
            start=1
        ):

            print(
                f"{index}. "
                f"{match['description']}"
            )

            print(
                f"   Similarity: "
                f"{match['similarity']}"
            )

    else:

        print("No matches found.")

    # =========================================================
    # COMPLETE
    # =========================================================

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()