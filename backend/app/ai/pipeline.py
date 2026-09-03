from app.ai.extraction import extract_project_information
from app.ai.classification import classify_project
from app.ai.confidence import assess_confidence
from app.ai.embeddings import match_project_to_needs


def analyze_proposal(
    proposal_text: str,
    needs: list
):

    # =====================================================
    # STEP 1 — EXTRACT PROJECT INFORMATION
    # =====================================================

    project = extract_project_information(
        proposal_text
    )

    # =====================================================
    # STEP 2 — CLASSIFY PROJECT
    # =====================================================

    classification = classify_project(
        proposal_text
    )

    # =====================================================
    # STEP 3 — CONFIDENCE
    # =====================================================

    confidence = classification.get(
        "confidence",
        0.0
    )

    confidence_result = assess_confidence(
        confidence
    )

    # =====================================================
    # STEP 4 — BUILD PROJECT TEXT FOR MATCHING
    # =====================================================

    project_text_parts = []

    if project.project_name:
        project_text_parts.append(
            project.project_name
        )

    if project.intervention:
        project_text_parts.append(
            project.intervention
        )

    if project.description:
        project_text_parts.append(
            project.description
        )

    if project.objectives:
        project_text_parts.extend(
            project.objectives
        )

    if project.expected_outcomes:
        project_text_parts.extend(
            project.expected_outcomes
        )

    project_text = " ".join(
        project_text_parts
    )

    # =====================================================
    # STEP 5 — SEMANTIC NEED MATCHING
    # =====================================================

    need_matches = match_project_to_needs(
        project_text,
        needs
    )

    # =====================================================
    # STEP 6 — FINAL RESPONSE
    # =====================================================

    return {
        "success": True,

        "project": project,

        "classification": {
            "category": classification.get(
                "category",
                "unknown"
            ),

            "confidence": round(
                float(confidence),
                4
            ),

            "confidence_level":
                confidence_result[
                    "confidence_level"
                ],

            "human_review_required":
                confidence_result[
                    "human_review_required"
                ]
        },

        "need_matches": need_matches
    }