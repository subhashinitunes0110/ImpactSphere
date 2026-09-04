"""
Impact Sphere - CSR Compliance Checker

Combines deterministic CSR rules into a single compliance
screening result.

This is a decision-support system and should not be treated
as a substitute for professional legal review.
"""

from app.schemas.compliance import (
    ComplianceCheckRequest,
    ComplianceCheckResponse,
    ComplianceRuleResult,
    CSRCalculationResponse,
)

from app.compliance.rules import (
    check_section_135_applicability,
    calculate_required_csr,
    check_administrative_overhead,
    check_csr_committee_required,
    check_schedule_vii_alignment,
    check_implementing_agency,
    check_exclusions,
    check_location,
)


# ============================================================
# HELPER: ADD RULE RESULT
# ============================================================

def add_rule(
    rules: list,
    rule_id: str,
    rule_name: str,
    status: str,
    message: str,
    severity: str = "MEDIUM",
):
    rules.append(
        ComplianceRuleResult(
            rule_id=rule_id,
            rule_name=rule_name,
            status=status,
            message=message,
            severity=severity,
        )
    )


# ============================================================
# MAIN COMPLIANCE CHECKER
# ============================================================

def check_project_compliance(
    request: ComplianceCheckRequest,
) -> ComplianceCheckResponse:

    company = request.company
    project = request.project

    rules_checked = []
    flags = []
    warnings = []

    # ========================================================
    # 1. SECTION 135 APPLICABILITY
    # ========================================================

    csr_applicable, threshold_reasons = (
        check_section_135_applicability(
            net_worth_crore=company.net_worth_crore,
            turnover_crore=company.turnover_crore,
            net_profit_crore=company.net_profit_crore,
        )
    )

    if csr_applicable:

        add_rule(
            rules_checked,
            "SEC135-001",
            "Section 135 Applicability",
            "PASS",
            "Company crosses at least one Section 135 threshold.",
            "HIGH",
        )

    else:

        add_rule(
            rules_checked,
            "SEC135-001",
            "Section 135 Applicability",
            "REVIEW",
            "Company does not appear to cross the configured "
            "Section 135 thresholds based on the supplied data.",
            "HIGH",
        )

        warnings.append(
            "Section 135 applicability could not be established "
            "from the supplied financial information."
        )

    # ========================================================
    # 2. CSR OBLIGATION
    # ========================================================

    average_profit = (
        company.previous_3_year_average_net_profit_crore
    )

    required_csr = calculate_required_csr(
        average_profit
    )

    actual_csr_spend = company.csr_spent_crore

    if required_csr is not None:

        spending_gap = round(
            required_csr - actual_csr_spend,
            4,
        )

        spending_compliant = (
            actual_csr_spend >= required_csr
        )

    else:

        spending_gap = 0.0
        spending_compliant = False

    if required_csr is None:

        add_rule(
            rules_checked,
            "SEC135-002",
            "CSR Spending Calculation",
            "REVIEW",
            "Average net profit for the preceding three "
            "financial years was not supplied.",
            "HIGH",
        )

        warnings.append(
            "CSR spending obligation could not be calculated "
            "without the preceding three-year average net profit."
        )

    elif spending_compliant:

        add_rule(
            rules_checked,
            "SEC135-002",
            "CSR Spending Requirement",
            "PASS",
            (
                f"Actual CSR spending of "
                f"₹{actual_csr_spend:.4f} crore meets or exceeds "
                f"the calculated requirement of "
                f"₹{required_csr:.4f} crore."
            ),
            "HIGH",
        )

    else:

        add_rule(
            rules_checked,
            "SEC135-002",
            "CSR Spending Requirement",
            "FLAG",
            (
                f"Actual CSR spending of "
                f"₹{actual_csr_spend:.4f} crore is below the "
                f"calculated requirement of "
                f"₹{required_csr:.4f} crore."
            ),
            "HIGH",
        )

        flags.append(
            "CSR spending appears below the calculated requirement."
        )

    # ========================================================
    # 3. ADMINISTRATIVE OVERHEAD
    # ========================================================

    overhead_percentage, overhead_compliant = (
        check_administrative_overhead(
            administrative_overheads_crore=(
                company.administrative_overheads_crore
            ),
            csr_spent_crore=actual_csr_spend,
        )
    )

    if overhead_compliant:

        add_rule(
            rules_checked,
            "CSR-ADMIN-001",
            "Administrative Overhead",
            "PASS",
            (
                f"Administrative overhead is "
                f"{overhead_percentage:.2f}% of CSR expenditure."
            ),
            "MEDIUM",
        )

    else:

        add_rule(
            rules_checked,
            "CSR-ADMIN-001",
            "Administrative Overhead",
            "FLAG",
            (
                f"Administrative overhead is "
                f"{overhead_percentage:.2f}%, exceeding the "
                f"configured 5% ceiling."
            ),
            "HIGH",
        )

        flags.append(
            "Administrative overhead exceeds the configured 5% ceiling."
        )

    # ========================================================
    # 4. CSR COMMITTEE
    # ========================================================

    csr_committee_required = check_csr_committee_required(
        required_csr
    )

    if csr_committee_required:

        committee_message = (
            "CSR Committee requirement applies based on the "
            "calculated CSR obligation."
        )

    else:

        committee_message = (
            "CSR obligation is ₹50 lakh or less; the Board "
            "handles the relevant CSR functions."
        )

    add_rule(
        rules_checked,
        "SEC135-003",
        "CSR Committee Requirement",
        "PASS",
        committee_message,
        "MEDIUM",
    )

    # ========================================================
    # 5. SCHEDULE VII ALIGNMENT
    # ========================================================

    project_text = " ".join(
        filter(
            None,
            [
                project.project_name,
                project.description,
                project.intervention,
                project.category,
            ],
        )
    )

    schedule_vii_aligned, detected_category = (
        check_schedule_vii_alignment(
            text=project_text,
            ai_category=project.category,
        )
    )

    if schedule_vii_aligned:

        add_rule(
            rules_checked,
            "SCHED7-001",
            "Schedule VII Alignment",
            "PASS",
            (
                f"Project appears aligned with the Schedule VII "
                f"category: {detected_category}."
            ),
            "HIGH",
        )

    else:

        add_rule(
            rules_checked,
            "SCHED7-001",
            "Schedule VII Alignment",
            "REVIEW",
            (
                "No sufficiently clear Schedule VII category "
                "was identified."
            ),
            "HIGH",
        )

        flags.append(
            "Schedule VII alignment requires human review."
        )

    # ========================================================
    # 6. AI CLASSIFICATION CONFIDENCE
    # ========================================================

    confidence = project.classification_confidence

    if confidence is None:

        add_rule(
            rules_checked,
            "AI-001",
            "AI Classification Confidence",
            "REVIEW",
            "AI classification confidence was not supplied.",
            "MEDIUM",
        )

        warnings.append(
            "AI classification confidence is unavailable."
        )

    elif confidence >= 0.80:

        add_rule(
            rules_checked,
            "AI-001",
            "AI Classification Confidence",
            "PASS",
            (
                f"AI classification confidence is "
                f"{confidence * 100:.1f}%."
            ),
            "LOW",
        )

    elif confidence >= 0.60:

        add_rule(
            rules_checked,
            "AI-001",
            "AI Classification Confidence",
            "REVIEW",
            (
                f"AI classification confidence is "
                f"{confidence * 100:.1f}%; human verification "
                f"is recommended."
            ),
            "MEDIUM",
        )

        warnings.append(
            "AI classification has medium confidence."
        )

    else:

        add_rule(
            rules_checked,
            "AI-001",
            "AI Classification Confidence",
            "REVIEW",
            (
                f"AI classification confidence is only "
                f"{confidence * 100:.1f}%; human review is required."
            ),
            "HIGH",
        )

        warnings.append(
            "AI classification confidence is low."
        )

    # ========================================================
    # 7. IMPLEMENTING AGENCY / CSR-1
    # ========================================================

    agency_status, agency_message = (
        check_implementing_agency(
            implementing_agency=project.implementing_agency,
            csr_registration_number=(
                project.csr_registration_number
            ),
            csr1_valid=(
                project.implementing_agency_csr1_valid
            ),
        )
    )

    add_rule(
        rules_checked,
        "CSR-AGENCY-001",
        "Implementing Agency Verification",
        agency_status,
        agency_message,
        "HIGH",
    )

    if agency_status == "FLAG":
        flags.append(agency_message)

    elif agency_status == "REVIEW":
        warnings.append(agency_message)

    # ========================================================
    # 8. EXCLUSION CHECK
    # ========================================================

    exclusion_status, exclusion_flags = check_exclusions(
        normal_business_activity=(
            project.normal_business_activity
        ),
        political_contribution=(
            project.political_contribution
        ),
        employee_benefit=(
            project.employee_benefit
        ),
        marketing_sponsorship=(
            project.marketing_sponsorship
        ),
        statutory_obligation=(
            project.statutory_obligation
        ),
    )

    if exclusion_status == "PASS":

        add_rule(
            rules_checked,
            "CSR-EXCLUSION-001",
            "CSR Exclusion Screening",
            "PASS",
            "No configured CSR exclusion indicators were detected.",
            "HIGH",
        )

    else:

        add_rule(
            rules_checked,
            "CSR-EXCLUSION-001",
            "CSR Exclusion Screening",
            "FLAG",
            "One or more potential CSR exclusion indicators were detected.",
            "HIGH",
        )

        flags.extend(exclusion_flags)

    # ========================================================
    # 9. LOCATION CHECK
    # ========================================================

    location_status, location_message = check_location(
        project.outside_india
    )

    add_rule(
        rules_checked,
        "CSR-LOCATION-001",
        "Project Location",
        location_status,
        location_message,
        "HIGH",
    )

    if location_status == "REVIEW":
        warnings.append(location_message)

    # ========================================================
    # 10. ANNUAL ACTION PLAN
    # ========================================================

    if project.annual_action_plan_approved:

        add_rule(
            rules_checked,
            "CSR-GOV-001",
            "Annual Action Plan",
            "PASS",
            "Project is marked as included in the approved Annual Action Plan.",
            "MEDIUM",
        )

    else:

        add_rule(
            rules_checked,
            "CSR-GOV-001",
            "Annual Action Plan",
            "REVIEW",
            "Project is not marked as included in the approved Annual Action Plan.",
            "MEDIUM",
        )

        warnings.append(
            "Annual Action Plan inclusion requires verification."
        )

    # ========================================================
    # 11. BUILD CSR CALCULATION
    # ========================================================

    csr_calculation = CSRCalculationResponse(
        company_name=company.company_name,
        csr_applicable=csr_applicable,
        threshold_reasons=threshold_reasons,
        average_net_profit_crore=average_profit,
        required_csr_spend_crore=required_csr,
        actual_csr_spend_crore=actual_csr_spend,
        spending_gap_crore=spending_gap,
        spending_compliant=spending_compliant,
        administrative_overheads_crore=(
            company.administrative_overheads_crore
        ),
        administrative_overhead_percentage=(
            overhead_percentage
        ),
        administrative_overhead_compliant=(
            overhead_compliant
        ),
        csr_committee_required=csr_committee_required,
    )

    # ========================================================
    # 12. DETERMINE FINAL STATUS
    # ========================================================

    has_high_flags = any(
        rule.status == "FLAG"
        and rule.severity == "HIGH"
        for rule in rules_checked
    )

    has_review = any(
        rule.status == "REVIEW"
        for rule in rules_checked
    )

    if has_high_flags:

        final_status = "FLAG"

    elif has_review:

        final_status = "REVIEW"

    else:

        final_status = "PASS"

    # ========================================================
    # 13. OVERALL COMPLIANCE
    # ========================================================

    overall_compliant = (
        final_status == "PASS"
    )

    review_required = (
        final_status == "REVIEW"
        or final_status == "FLAG"
    )

    # ========================================================
    # 14. HUMAN-READABLE EXPLANATION
    # ========================================================

    if final_status == "PASS":

        explanation = (
            "The project passed the configured CSR screening rules. "
            "No blocking compliance flags were detected."
        )

    elif final_status == "FLAG":

        explanation = (
            "The project contains one or more compliance flags "
            "that require attention before approval."
        )

    else:

        explanation = (
            "The project requires human review because one or more "
            "compliance checks could not be conclusively verified."
        )

    # ========================================================
    # 15. FRONTEND-FRIENDLY CHECK SUMMARY
    # ========================================================

    checks = {
        "section_135": csr_applicable,
        "schedule_vii": schedule_vii_aligned,
        "csr_spending": spending_compliant,
        "administrative_overhead": overhead_compliant,
        "implementing_agency": agency_status,
        "exclusions": exclusion_status,
        "location": location_status,
        "annual_action_plan": (
            "PASS"
            if project.annual_action_plan_approved
            else "REVIEW"
        ),
        "ai_confidence": confidence,
    }

    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    return ComplianceCheckResponse(
        status=final_status,
        overall_compliant=overall_compliant,
        schedule_vii_alignment=schedule_vii_aligned,
        detected_schedule_vii_category=detected_category,
        implementing_agency_check=agency_status,
        exclusions_check=exclusion_status,
        csr_applicable=csr_applicable,
        csr_calculation=csr_calculation,
        rules_checked=rules_checked,
        flags=flags,
        warnings=warnings,
        review_required=review_required,
        explanation=explanation,
        checks=checks,
    )