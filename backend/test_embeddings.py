from app.ai.embeddings import (
    text_similarity,
    match_project_to_needs
)


def main():

    print()
    print("=" * 60)
    print("IMPACT SPHERE - SEMANTIC NEED MATCHING")
    print("=" * 60)

    project = """
    Mobile healthcare units will provide free medical
    checkups, medicines and preventive healthcare services
    to remote rural communities.
    """

    needs = [

        {
            "id": 1,
            "description":
                "Limited access to healthcare facilities "
                "and medical services in remote rural areas."
        },

        {
            "id": 2,
            "description":
                "Students from disadvantaged communities "
                "need better access to education and digital "
                "learning resources."
        },

        {
            "id": 3,
            "description":
                "Rural women require employment opportunities "
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

    print()
    print("Project:")
    print(project.strip())

    print()
    print("Matching project against regional needs...")
    print()

    results = match_project_to_needs(
        project,
        needs
    )

    for result in results:

        print(
            f"Need {result['need_id']} "
            f"→ Similarity: "
            f"{result['similarity']:.4f}"
        )

        print(
            f"   {result['description']}"
        )

    print()
    print("=" * 60)
    print("TOP MATCH")
    print("=" * 60)

    top = results[0]

    print()
    print(
        f"Need ID: {top['need_id']}"
    )

    print(
        f"Similarity: {top['similarity']:.4f}"
    )

    print(
        f"Description: {top['description']}"
    )


if __name__ == "__main__":

    main()