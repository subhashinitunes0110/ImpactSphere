# ImpactSphere

### ImpactSphere

> **Put every CSR rupee where it creates the greatest compliant social impact.**

ImpactSphere is an AI-assisted decision-support platform designed to help Indian companies allocate their Corporate Social Responsibility (CSR) budgets across multiple project proposals.

The platform combines **CSR compliance checking, proposal understanding, impact scoring, portfolio optimization, geographic intelligence, and explainable recommendations** into a single workflow.

Instead of relying on spreadsheets and subjective proposal-by-proposal evaluation, CSR committees can use CSRCompass to identify projects that are:

- Legally eligible under the CSR framework
- Aligned with Schedule VII
- Relevant to local-area priorities
- High-impact relative to their cost
- Feasible within the available CSR budget
- Better balanced across sectors and geographies
- Explainable and auditable before approval


---

## 🎯 Problem Statement

CSR committees at mid-to-large Indian companies often need to evaluate and prioritize dozens of project proposals during each funding cycle.

The traditional process commonly involves:

- Manual spreadsheet-based scoring
- Proposal-by-proposal compliance checking
- Subjective evaluation by different reviewers
- Manual verification of Schedule VII applicability
- Difficulty comparing impact against project cost
- Limited visibility into geographic concentration
- Manual tracking of CSR spending and utilization risks

This process becomes difficult to scale and can result in inconsistent prioritization or compliance gaps.

CSRCompass addresses this problem by turning the allocation process into a **structured, transparent and compliance-aware optimization workflow**.


---

# 💡 Our Solution

CSRCompass follows a simple pipeline:

Proposal Documents
        ↓
AI-Assisted Information Extraction
        ↓
CSR Compliance Engine
        ↓
Schedule VII Classification
        ↓
Impact & Cost-Efficiency Scoring
        ↓
Portfolio Optimization
        ↓
Geographic & Budget Analysis
        ↓
Explainable Recommendations
        ↓
Human Approval


The system does **not** replace the CSR committee.

Instead, it provides a transparent decision-support layer that helps the committee make faster and better-informed funding decisions.


---

# 🚀 Key Features

## 1. CSR Applicability & Budget Calculator

The system can determine whether a company falls under the CSR applicability thresholds based on Section 135.

CSR applicability is triggered when **any one** of the following conditions is satisfied in the immediately preceding financial year:

| Parameter | Threshold |
|-----------|-----------|
| Net Worth | ₹500 Crore or more |
| Turnover | ₹1,000 Crore or more |
| Net Profit | ₹5 Crore or more |

For an applicable company, the platform can calculate the indicative CSR obligation based on the applicable statutory formula, including the 2% requirement based on average net profits of the three immediately preceding financial years.


---

## 2. AI-Assisted Proposal Understanding

CSR proposals may arrive as:

- PDF documents
- Structured forms
- Free-text descriptions
- Project reports

The AI layer extracts relevant information such as:

- Project name
- Project objective
- CSR category
- Location
- Number of beneficiaries
- Estimated project cost
- Implementation duration
- Target population
- Expected outcomes
- Environmental/social impact indicators

AI is used primarily for **understanding unstructured proposal information**.

Statutory calculations and deterministic compliance rules remain rule-based wherever possible.


---

## 3. Schedule VII Classification

Every proposal is checked against the CSR activities specified under **Schedule VII of the Companies Act, 2013**.

The platform can classify proposals into areas such as:

- Eradicating hunger, poverty and malnutrition
- Healthcare and sanitation
- Education and vocational skills
- Gender equality and women empowerment
- Environmental sustainability
- National heritage, art and culture
- Armed forces veterans and dependants
- Sports
- Specified government relief/welfare funds
- Scientific research and technology
- Rural development
- Slum area development
- Disaster management
- Other currently applicable Schedule VII categories

The classification is explainable rather than being treated as an opaque AI decision.


---

# ⚖️ CSR Compliance Engine

Compliance is treated as a **first-class component of the system**, rather than an additional check after project ranking.

The engine can evaluate rules relating to:

### Section 135

- CSR applicability thresholds
- CSR expenditure requirement
- Local-area preference
- CSR Committee / Board responsibilities
- CSR reporting considerations

### Schedule VII

- Eligible CSR activity categories
- Category classification

### CSR Policy Rules

The engine can additionally model rules concerning:

- Eligible implementing agencies
- CSR-1 registration status
- Annual Action Plan
- Administrative overhead limits
- Unspent CSR amounts
- Ongoing projects
- Surplus arising from CSR activities
- Excess CSR expenditure / set-off
- Impact assessment applicability
- Capital asset conditions
- Website and reporting requirements

The rules are intended to be maintained in a **versioned rule database** so that regulatory changes can be incorporated without rewriting the entire application.


---

# 🧮 Impact Scoring Engine

After compliance screening, eligible proposals receive a transparent impact score.

A proposed scoring model is:

| Criterion | Weight |
|-----------|-------:|
| Expected Social Impact | 30% |
| Beneficiary Reach | 20% |
| Cost Efficiency | 15% |
| CSR Objective Alignment | 15% |
| Geographic Need | 10% |
| Feasibility | 5% |
| Sustainability | 5% |
| **Total** | **100%** |

### Example

A project costing ₹50 lakh that benefits 10,000 people may receive a stronger cost-efficiency score than a ₹50 lakh project benefiting only 1,000 people, assuming other factors are comparable.

The scoring weights are configurable and represent the organization's **decision preferences**, not statutory requirements.


---

# 💰 Portfolio Optimization

Simply ranking projects is not enough.

A CSR committee may have:

- ₹5 Crore available
- 20 eligible proposals
- Different project costs
- Different impact scores
- Sectoral priorities
- Geographic priorities
- Funding constraints

CSRCompass therefore treats allocation as a **portfolio optimization problem**.

### Objective

Maximize total expected impact while remaining within the available CSR budget.

Conceptually:

Maximize:

    Σ ImpactScoreᵢ × xᵢ

Subject to:

    Σ Costᵢ × xᵢ ≤ AvailableBudget

where:

    xᵢ = 1 → project selected
    xᵢ = 0 → project not selected


Optional constraints can include:

- Minimum education allocation
- Minimum healthcare allocation
- Rural allocation targets
- Maximum allocation to one project
- Geographic concentration limits
- Sector diversification
- Company-specific CSR priorities


---

# 🔄 What-If Simulator

CSR managers can experiment with different funding scenarios before making a decision.

For example:

### Scenario A

CSR Budget:

    ₹5 Crore

Result:

    7 projects selected
    32,000 estimated beneficiaries


### Scenario B

CSR Budget:

    ₹3 Crore

Result:

    5 projects selected
    21,000 estimated beneficiaries


The system can show how changing:

- Budget
- Project weights
- Sector priorities
- Geographic constraints
- Minimum/maximum allocations

changes the recommended portfolio.

This allows CSR committees to answer:

> "What happens to our impact if our budget changes?"

rather than manually rebuilding spreadsheets.


---

# 🗺️ Geographic Intelligence

CSRCompass can visualize proposed and selected projects geographically.

This helps identify:

- Geographic concentration
- Underserved regions
- Rural vs urban distribution
- Local-area preference
- Regional beneficiary distribution

A map-based view allows the committee to understand not just **which projects were selected**, but **where CSR money is going**.


---

# 🔍 Explainable Recommendations

The system does not simply return:

> "Project A is recommended."

Instead, it explains the recommendation.

Example:

### Why Project A?

- Schedule VII aligned: Healthcare
- Expected beneficiaries: 8,500
- Cost: ₹40 lakh
- High impact-per-rupee
- Located in a high-need region
- Fits current geographic constraints
- Does not exceed project-level funding limit
- Strong implementation feasibility

The committee can therefore understand **why a project was prioritized**.


---

# 👨‍⚖️ Human-in-the-Loop

CSRCompass is a **decision-support system**, not an autonomous legal decision maker.

Human reviewers can:

- Override an AI classification
- Adjust scoring weights
- Modify constraints
- Review compliance flags
- Reject recommendations
- Approve final allocations

This is especially important because proposal language can be ambiguous and real-world CSR eligibility may require professional/legal interpretation.


---

# 🧠 Why AI + Rules Instead of AI Alone?

A major design principle of ImpactSphere is:

> **Use AI for understanding; use deterministic logic for compliance and calculations.**

### AI is useful for:

- Extracting information from PDFs
- Understanding proposal descriptions
- Classifying project themes
- Summarizing proposals
- Identifying potential compliance issues

### Deterministic systems are used for:

- CSR threshold calculations
- Budget calculations
- Statutory rule checks
- Scoring
- Optimization
- Constraint enforcement

This makes the system more **auditable, explainable and reliable** than using an LLM as the sole decision-maker.


---

# 🏗️ System Architecture

```text
                    ┌──────────────────────┐
                    │     CSR Manager      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   React / Next.js    │
                    │      Frontend        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       FastAPI        │
                    │       Backend        │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
       │ AI / PDF    │  │ Compliance  │  │   Impact     │
       │ Processing  │  │   Engine    │  │   Scoring    │
       └─────────────┘  └─────────────┘  └──────┬──────┘
                                                 │
                                                 ▼
                                         ┌──────────────┐
                                         │ OR-Tools     │
                                         │ Optimization │
                                         └──────┬───────┘
                                                │
                                                ▼
                                         ┌──────────────┐
                                         │ PostgreSQL   │
                                         │ + pgvector   │
                                         └──────────────┘
