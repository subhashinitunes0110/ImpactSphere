from app.ai.extraction import extract_project_info
from app.ai.classification import classify_project
from app.ai.confidence import assess_confidence
from app.ai.need_matching import match_project_to_health_need


# =========================================================
# CONFIDENCE LEVEL
# =========================================================

def get_confidence_level(confidence: float) -> str:
    """
    Convert numeric confidence into a readable level.

    These thresholds are system thresholds,
    NOT legal requirements.
    """

    if confidence >= 0.80:
        return "high"

    elif confidence >= 0.60:
        return "medium"

    return "low"


# =========================================================
# MAIN AI PIPELINE
# =========================================================

def analyze_proposal(proposal: str):
    """
    Complete Impact Sphere AI proposal analysis pipeline.

    Flow:

    PDF text
        ↓
    Project Information Extraction
        ↓
    CSR Classification
        ↓
    Confidence Assessment
        ↓
    NFHS Need Analysis
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

    # Convert Pydantic model to dictionary
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

    # Support dictionary/object return formats
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
    # STEP 4 — NFHS NEED ANALYSIS
    # -----------------------------------------------------

    print("\n" + "=" * 60)
    print("STEP 4/4 - Analysing community need...")
    print("=" * 60)

    need_analysis = match_project_to_health_need(
        proposal,
        top_k=10
    )

    print(
        f"Detected intervention: "
        f"{need_analysis.get('intervention_type')}"
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

        "need_analysis": {

            "intervention_type":
                need_analysis.get(
                    "intervention_type"
                ),

            "priority_districts":
                need_analysis.get(
                    "districts",
                    []
                ),

            "data_source":
                "NFHS-5"
        }
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

    print("\n")
    print("=" * 60)
    print("IMPACT SPHERE — AI ANALYSIS")
    print("=" * 60)

    result = analyze_proposal(proposal)

    print("\n")
    print("=" * 60)
    print("FINAL ANALYSIS")
    print("=" * 60)

    print("\nPROJECT INFORMATION")
    print("-" * 60)
    print(result["project"])

    print("\nCLASSIFICATION")
    print("-" * 60)

    print(
        "Category:",
        result["classification"]["category"]
    )

    print(
        "Confidence:",
        result["classification"]["confidence"]
    )

    print(
        "Confidence Level:",
        result["classification"]["confidence_level"]
    )

    print(
        "Human Review Required:",
        result["classification"]["human_review_required"]
    )

    print("\nNFHS NEED ANALYSIS")
    print("-" * 60)

    print(
        "Intervention:",
        result["need_analysis"]["intervention_type"]
    )

    for index, district in enumerate(
        result["need_analysis"]["priority_districts"],
        1
    ):

        print(
            f"{index}. "
            f"{district['district']}, "
            f"{district['state']} "
            f"→ Need: "
            f"{district['health_need_score']}"
        )

    print("\n")
    print("=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)