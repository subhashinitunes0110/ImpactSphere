import pandas as pd

from backend.app.ai.embeddings import generate_embedding, cosine_similarity


CSR_FILE = "data/processed/csr_clean.csv"


def load_real_csr_categories():
    df = pd.read_csv(CSR_FILE)

    df = df.dropna(
        subset=[
            "csr_development_sector",
            "csr_sub_development_sector"
        ]
    )

    categories = (
        df[
            [
                "csr_development_sector",
                "csr_sub_development_sector"
            ]
        ]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    return categories


def build_category_text(row):
    return (
        f"CSR sector: {row['csr_development_sector']}. "
        f"Sub-sector: {row['csr_sub_development_sector']}."
    )


def search_proposal(proposal_text, top_k=5):
    categories = load_real_csr_categories()

    proposal_embedding = generate_embedding(proposal_text)

    results = []

    for _, row in categories.iterrows():
        category_text = build_category_text(row)
        category_embedding = generate_embedding(category_text)

        similarity = cosine_similarity(
            proposal_embedding,
            category_embedding
        )

        results.append(
            {
                "sector": row["csr_development_sector"],
                "sub_sector": row["csr_sub_development_sector"],
                "similarity": float(similarity)
            }
        )

    results.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return results[:top_k]


if __name__ == "__main__":

    test_proposals = [
        "Providing preventive healthcare, medical camps and sanitation facilities to underserved rural communities.",

        "Improving access to quality education and digital learning facilities for children in rural schools.",

        "Creating employment opportunities through vocational training and livelihood development for low income communities.",

        "Providing clean drinking water and improving sanitation facilities in underserved villages.",

        "Supporting women through skill development, financial independence and livelihood programmes."
    ]

    for proposal in test_proposals:

        print("\n" + "=" * 80)
        print("PROPOSAL:")
        print(proposal)

        results = search_proposal(proposal)

        print("\nTOP MATCHES:")

        for i, result in enumerate(results, 1):

            print(
                f"{i}. "
                f"{result['sector']} | "
                f"{result['sub_sector']} | "
                f"similarity={result['similarity']:.4f}"
            )