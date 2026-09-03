from dataclasses import dataclass
from enum import Enum
from typing import Tuple

RULE_VERSION = "2026-09"


class RuleType(str, Enum):
    ELIGIBILITY = "ELIGIBILITY"
    EXCLUSION = "EXCLUSION"
    IMPLEMENTATION = "IMPLEMENTATION"
    GOVERNANCE = "GOVERNANCE"


@dataclass(frozen=True)
class CSRRule:
    rule_id: str
    source: str
    section: str
    rule_name: str
    rule_type: RuleType
    description: str
    version: str = RULE_VERSION


CSR_APPLICABILITY_THRESHOLDS = {
    "net_worth": 500_00_00_000,
    "turnover": 1000_00_00_000,
    "net_profit": 5_00_00_000,
}

CSR_SPEND_RATE = 0.02
ADMINISTRATIVE_OVERHEAD_CAP = 0.05


SCHEDULE_VII_RULES: Tuple[CSRRule, ...] = (
    CSRRule("SCH7_01", "Schedule VII", "Schedule VII(i)", "Hunger, Poverty, Health, Sanitation and Safe Drinking Water", RuleType.ELIGIBILITY, "Health, poverty, nutrition, sanitation and safe drinking water."),
    CSRRule("SCH7_02", "Schedule VII", "Schedule VII(ii)", "Education, Vocational Skills and Livelihood", RuleType.ELIGIBILITY, "Education, special education, vocation skills and livelihood enhancement."),
    CSRRule("SCH7_03", "Schedule VII", "Schedule VII(iii)", "Gender Equality, Women Empowerment and Senior Citizens", RuleType.ELIGIBILITY, "Gender equality, women empowerment, senior citizens and reduction of inequalities."),
    CSRRule("SCH7_04", "Schedule VII", "Schedule VII(iv)", "Environmental Sustainability", RuleType.ELIGIBILITY, "Environmental sustainability, ecological balance, animal welfare and natural resources."),
    CSRRule("SCH7_05", "Schedule VII", "Schedule VII(v)", "National Heritage, Art and Culture", RuleType.ELIGIBILITY, "National heritage, art, culture, libraries, traditional arts and handicrafts."),
    CSRRule("SCH7_06", "Schedule VII", "Schedule VII(vi)", "Armed Forces Veterans and Dependents", RuleType.ELIGIBILITY, "Benefits for armed forces veterans, war widows and dependents."),
    CSRRule("SCH7_07", "Schedule VII", "Schedule VII(vii)", "Rural and Nationally Recognised Sports", RuleType.ELIGIBILITY, "Rural, nationally recognised, paralympic and Olympic sports."),
    CSRRule("SCH7_08", "Schedule VII", "Schedule VII(viii)", "Specified Relief and Welfare Funds", RuleType.ELIGIBILITY, "Specified government relief and welfare funds including PM National Relief Fund and PM CARES."),
    CSRRule("SCH7_09", "Schedule VII", "Schedule VII(ix)", "Science Technology Engineering and Medicine Research", RuleType.ELIGIBILITY, "Qualifying incubators and R&D in science, technology, engineering and medicine."),
    CSRRule("SCH7_10", "Schedule VII", "Schedule VII(x)", "Rural Development", RuleType.ELIGIBILITY, "Rural development projects."),
    CSRRule("SCH7_11", "Schedule VII", "Schedule VII(xi)", "Slum Area Development", RuleType.ELIGIBILITY, "Slum area development."),
    CSRRule("SCH7_12", "Schedule VII", "Schedule VII(xii)", "Disaster Management", RuleType.ELIGIBILITY, "Disaster management including relief, rehabilitation and reconstruction."),
)


EXCLUSION_RULES: Tuple[CSRRule, ...] = (
    CSRRule("EXCL_NORMAL_BUSINESS", "CSR Policy Rules", "Rule 2(1)(d)(i)", "Normal Course of Business", RuleType.EXCLUSION, "Normal course of business activities are excluded."),
    CSRRule("EXCL_OUTSIDE_INDIA", "CSR Policy Rules", "Rule 2(1)(d)(ii)", "Activities Outside India", RuleType.EXCLUSION, "Activities outside India are excluded except permitted Indian sports training."),
    CSRRule("EXCL_POLITICAL", "CSR Policy Rules", "Rule 2(1)(d)(iii)", "Political Contributions", RuleType.EXCLUSION, "Political contributions under section 182 are excluded."),
    CSRRule("EXCL_EMPLOYEE_BENEFIT", "CSR Policy Rules", "Rule 2(1)(d)(iv)", "Employee Benefit", RuleType.EXCLUSION, "Activities benefiting company employees are excluded."),
    CSRRule("EXCL_SPONSORSHIP_MARKETING", "CSR Policy Rules", "Rule 2(1)(d)(v)", "Marketing Sponsorship", RuleType.EXCLUSION, "Sponsorship for marketing benefits is excluded."),
    CSRRule("EXCL_STATUTORY_OBLIGATION", "CSR Policy Rules", "Rule 2(1)(d)(vi)", "Statutory Obligation", RuleType.EXCLUSION, "Activities fulfilling statutory obligations are excluded."),
)


IMPLEMENTING_AGENCY_RULES: Tuple[CSRRule, ...] = (
    CSRRule("IMPL_RULE_4", "CSR Policy Rules", "Rule 4(1)", "Eligible Implementing Agency", RuleType.IMPLEMENTATION, "Qualifying Section 8 companies, registered public trusts or societies, government entities, statutory entities and other permitted entities."),
    CSRRule("IMPL_CSR1", "CSR Policy Rules", "Rule 4(2)", "CSR-1 Registration", RuleType.IMPLEMENTATION, "Covered implementing agencies generally require CSR-1 registration."),
)


GOVERNANCE_RULES: Tuple[CSRRule, ...] = (
    CSRRule("GOV_ADMIN_OVERHEAD", "CSR Policy Rules", "Rule 7(1)", "Administrative Overhead Cap", RuleType.GOVERNANCE, "Administrative overheads must not exceed 5% of total CSR expenditure."),
    CSRRule("GOV_IMPACT_ASSESSMENT", "CSR Policy Rules", "Rule 8(3)", "Impact Assessment", RuleType.GOVERNANCE, "Qualifying companies and projects are subject to applicable impact-assessment requirements."),
)


ALL_RULES: Tuple[CSRRule, ...] = (
    *SCHEDULE_VII_RULES,
    *EXCLUSION_RULES,
    *IMPLEMENTING_AGENCY_RULES,
    *GOVERNANCE_RULES,
)