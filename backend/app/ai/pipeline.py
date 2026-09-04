from backend.app.ai.extraction import extract_project_info
from backend.app.ai.classification import classify_project
from backend.app.ai.confidence import assess_confidence
from backend.app.ai.embeddings import match_project_to_needs


# =========================================================
# CONFIDENCE LEVEL
# =========================================================

def get_confidence_level(confidence: float) -> str:
    """
    Convert numeric confidence into a readable level.

    These are system thresholds, NOT legal requirements.
    """

    if confidence >= 0.80:
        return "high"

    elif confidence >= 0.60:
        return "medium"

    return "low"


# =========================================================
# MAIN AI PIPELINE
# =========================================================

def analyze_proposal(proposal: str, needs: list):
    """
    Complete Impact Sphere AI pipeline.

    Flow:

    Proposal Text
        ↓
    Project Information Extraction
        ↓
    Classification
        ↓
    Confidence Assessment
        ↓
    Community Need Matching
        ↓
    Final Structured Result
    """

    if not proposal or not proposal.strip():
        raise ValueError("Proposal text cannot be empty.")

    # -----------------------------------------------------
    # STEP 1 — EXTRACT PROJECT INFORMATION
    # -----------------------------------------------------

    print("\n" + "=" * 60)
    print("STEP 1/4 - Extracting project information...")
    print("=" * 60)

    project = extract_project_info(proposal)

    if hasattr(project, "model_dump"):
        project_dict = project.model_dump()
    elif hasattr(project, "dict"):
        project_dict = project.dict()
    else:
        project_dict = project

    # -----------------------------------------------------
    # STEP 2 — CLASSIFICATION
    # -----------------------------------------------------

    print("\n" + "=" * 60)
    print("STEP 2/4 - Classifying project...")
    print("=" * 60)

    classification_result = classify_project(proposal)

    if isinstance(classification_result, dict):

        category = classification_result.get(
            "category",
            classification_result.get(
                "label",
                "unknown"
            )
        )

        confidence = float(
            classification_result.get(
                "confidence",
                0.0
            )
        )

    else:

        category = getattr(
            classification_result,
            "category",
            "unknown"
        )

        confidence = float(
            getattr(
                classification_result,
                "confidence",
                0.0
            )
        )

    print(f"Category: {category}")
    print(f"Confidence: {confidence:.4f}")

    # -----------------------------------------------------
    # STEP 3 — CONFIDENCE ASSESSMENT
    # -----------------------------------------------------

    print("\n" + "=" * 60)
    print("STEP 3/4 - Assessing confidence...")
    print("=" * 60)

    try:

        confidence_result = assess_confidence(
            confidence
        )

    except TypeError:

        confidence_result = assess_confidence(
            classification_result
        )

    # -----------------------------------------------------
    # NORMALIZE CONFIDENCE RESULT
    # -----------------------------------------------------

    confidence_level = None
    human_review_required = None

    if isinstance(confidence_result, dict):

        confidence_level = confidence_result.get(
            "confidence_level"
        )

        if confidence_level is None:
            confidence_level = confidence_result.get(
                "level"
            )

        human_review_required = confidence_result.get(
            "human_review_required"
        )

        if human_review_required is None:
            human_review_required = confidence_result.get(
                "requires_review"
            )

    else:

        confidence_level = getattr(
            confidence_result,
            "confidence_level",
            None
        )

        if confidence_level is None:
            confidence_level = getattr(
                confidence_result,
                "level",
                None
            )

        human_review_required = getattr(
            confidence_result,
            "human_review_required",
            None
        )

    # -----------------------------------------------------
    # FALLBACK
    # -----------------------------------------------------

    if confidence_level is None:

        confidence_level = get_confidence_level(
            confidence
        )

    if human_review_required is None:

        human_review_required = (
            confidence < 0.60
        )

    print(
        f"Confidence Level: {confidence_level}"
    )

    print(
        f"Human Review Required: "
        f"{human_review_required}"
    )

    # -----------------------------------------------------
    # STEP 4 — COMMUNITY NEED MATCHING
    # -----------------------------------------------------

    print("\n" + "=" * 60)
    print("STEP 4/4 - Matching against community needs...")
    print("=" * 60)

    need_matches = match_project_to_needs(
        proposal,
        needs
    )

    # -----------------------------------------------------
    # FINAL RESULT
    # -----------------------------------------------------

    result = {

        "success": True,

        "project": project_dict,

        "classification": {

            "category": category,

            "confidence": round(
                confidence,
                4
            ),

            "confidence_level":
                confidence_level,

            "human_review_required":
                bool(human_review_required)
        },

        "need_matches": need_matches
    }

    return result


# =========================================================
# SIMPLE TEST
# =========================================================

if __name__ == "__main__":

    proposal = """
    Rural Healthcare Initiative

    The project will establish mobile healthcare units
    to provide free medical checkups, medicines and
    preventive healthcare services to remote rural
    communities in Barmer district of Rajasthan.

    The program will operate for 24 months and is
    expected to benefit approximately 12,000 people.

    Priority beneficiaries include rural families,
    elderly citizens and people who have limited access
    to healthcare facilities.
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
                "Students from disadvantaged communities "
                "need better access to education and "
                "digital learning resources."
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
                "Villages lack reliable access to safe "
                "drinking water and sanitation infrastructure."
        },
        {
            "id": 5,
            "description":
                "Underserved communities need access to "
                "sports facilities and professional coaching."
        }
    ]

    result = analyze_proposal(
        proposal,
        needs
    )

    print("\n")
    print("=" * 60)
    print("FINAL AI RESULT")
    print("=" * 60)
    print(result)
