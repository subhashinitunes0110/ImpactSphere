import numpy as np
from sentence_transformers import SentenceTransformer


# =========================================================
# CONFIGURATION
# =========================================================

EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# =========================================================
# MODEL LOADER
# =========================================================

_model = None


def get_embedding_model():
    """Load the Sentence Transformer model once."""

    global _model

    if _model is None:
        print(f"Loading embedding model: {EMBEDDING_MODEL}")

        _model = SentenceTransformer(
            EMBEDDING_MODEL
        )

        print("Embedding model ready.")

    return _model


# =========================================================
# GENERATE SINGLE EMBEDDING
# =========================================================

def generate_embedding(text: str):
    """Generate a normalized embedding for one piece of text."""

    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    model = get_embedding_model()

    embedding = model.encode(
        text,
        normalize_embeddings=True
    )

    return np.asarray(
        embedding,
        dtype=np.float32
    )


# =========================================================
# GENERATE MULTIPLE EMBEDDINGS
# =========================================================

def generate_embeddings(texts):
    """Generate normalized embeddings for multiple texts."""

    if not texts:
        raise ValueError("Texts list cannot be empty.")

    model = get_embedding_model()

    embeddings = model.encode(
        texts,
        normalize_embeddings=True
    )

    return np.asarray(
        embeddings,
        dtype=np.float32
    )


# =========================================================
# COSINE SIMILARITY
# =========================================================

def cosine_similarity(embedding_a, embedding_b):
    """Calculate cosine similarity between two embeddings."""

    a = np.asarray(
        embedding_a,
        dtype=np.float32
    )

    b = np.asarray(
        embedding_b,
        dtype=np.float32
    )

    denominator = (
        np.linalg.norm(a)
        *
        np.linalg.norm(b)
    )

    if denominator == 0:
        return 0.0

    similarity = np.dot(
        a,
        b
    ) / denominator

    return float(similarity)


# =========================================================
# TEXT SIMILARITY
# =========================================================

def text_similarity(text_a: str, text_b: str):
    """Calculate semantic similarity between two texts."""

    embedding_a = generate_embedding(text_a)
    embedding_b = generate_embedding(text_b)

    return cosine_similarity(
        embedding_a,
        embedding_b
    )


# =========================================================
# PROJECT → NEED MATCHING
# =========================================================

def match_project_to_needs(project_text: str, needs: list):
    """
    Match a CSR project against a list of community needs.

    Returns needs ranked from highest to lowest semantic similarity.
    """

    if not project_text:
        raise ValueError(
            "Project text cannot be empty."
        )

    if not needs:
        return []

    model = get_embedding_model()

    # Project embedding
    project_embedding = model.encode(
        project_text,
        normalize_embeddings=True
    )

    # Extract need descriptions
    need_texts = [
        need["description"]
        for need in needs
    ]

    # Generate all need embeddings
    need_embeddings = model.encode(
        need_texts,
        normalize_embeddings=True
    )

    results = []

    for index, need in enumerate(needs):

        similarity = cosine_similarity(
            project_embedding,
            need_embeddings[index]
        )

        results.append(
            {
                "need_id": need.get(
                    "id",
                    index
                ),
                "description": need[
                    "description"
                ],
                "similarity": round(
                    similarity,
                    4
                )
            }
        )

    # Highest similarity first
    results.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    return results


# =========================================================
# PIPELINE COMPATIBILITY FUNCTION
# =========================================================

def find_matching_needs(project_text: str, needs: list):
    """
    Compatibility wrapper used by the Impact Sphere pipeline.

    Internally uses the existing semantic matching engine.
    """

    return match_project_to_needs(
        project_text,
        needs
    )


# =========================================================
# QUICK TEST
# =========================================================

if __name__ == "__main__":

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
                "Remote rural communities have limited access "
                "to healthcare facilities, doctors and essential "
                "medical services."
        },
        {
            "id": 2,
            "description":
                "Students from disadvantaged communities need "
                "better access to education and digital learning."
        },
        {
            "id": 3,
            "description":
                "Rural women require livelihood opportunities "
                "and entrepreneurship training."
        }
    ]

    print("\nMatching project against regional needs...\n")

    results = find_matching_needs(
        project,
        needs
    )

    for result in results:
        print(
            f"Need {result['need_id']} "
            f"→ Similarity: {result['similarity']}"
        )
        print(
            f"   {result['description']}"
        )

    if results:
        print("\n" + "=" * 60)
        print("TOP MATCH")
        print("=" * 60)

        print(
            f"\nNeed ID: {results[0]['need_id']}"
        )

        print(
            f"Similarity: {results[0]['similarity']}"
        )

        print(
            f"Description: {results[0]['description']}"
        )