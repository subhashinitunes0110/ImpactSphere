"use client";

import { useState } from "react";
import Sidebar from "@/components/Sidebar";
import { postToAPI } from "@/lib/api";

interface AIProject {
  project_name?: string;
  location?: {
    district?: string;
    state?: string;
  };
  budget?: number;
  beneficiaries?: number;
  beneficiary_groups?: string[];
  intervention?: string;
  objectives?: string[];
  expected_outcomes?: string[];
  implementing_agency?: string;
  description?: string;
  summary?: string;
}

interface Classification {
  category: string;
  confidence: number;
  confidence_level: string;
  human_review_required: boolean;
}

interface Compliance {
  status: string;
  eligible: boolean;
  eligible_for_optimization: boolean;
  schedule_vii_category?: string;
  schedule_vii_match: boolean;
  flags: string[];
  reasons: string[];
}

interface AnalysisResponse {
  success: boolean;
  project: AIProject;
  classification: Classification;
  need_matches?: unknown[];
}

const DEMO_PROPOSAL = `Rural Healthcare Initiative

This project will provide healthcare services to rural communities
in Dharwad district of Karnataka.

The project has a budget of ₹50 lakh and will benefit approximately
10000 people.

The objective is to improve access to healthcare through medical
services for underserved rural communities.`;

function formatLakhs(value?: number) {
  if (value === undefined || value === null) return "—";
  return `₹${(value / 100000).toFixed(1)} L`;
}

export default function ProposalsPage() {
  const [proposalText, setProposalText] =
    useState<string>(DEMO_PROPOSAL);

  const [analysis, setAnalysis] =
    useState<AnalysisResponse | null>(null);

  const [compliance, setCompliance] =
    useState<Compliance | null>(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function analyzeProposal() {
    const text = proposalText.trim();

    if (!text) {
      setError("Please enter a project proposal.");
      return;
    }

    setLoading(true);
    setError(null);
    setAnalysis(null);
    setCompliance(null);

    try {
      const response = await postToAPI<
        {
          text: string;
          needs: unknown[];
          implementing_agency: string;
          implementing_agency_type: string;
          implementing_agency_registered_under_12a: boolean;
          implementing_agency_registered_under_80g: boolean;
          implementing_agency_has_3_year_track_record: boolean;
          csr1_required: boolean;
          csr1_filed: boolean;
        },
        {
          success: boolean;
          ai_analysis: AnalysisResponse;
          compliance: Compliance;
        }
      >("/integration/analyze-and-check", {
        text,
        needs: [],
        implementing_agency: "Eligible Section 8 NGO",
        implementing_agency_type: "SECTION_8",
        implementing_agency_registered_under_12a: true,
        implementing_agency_registered_under_80g: true,
        implementing_agency_has_3_year_track_record: true,
        csr1_required: true,
        csr1_filed: true,
      });

      if (response.ai_analysis) {
        setAnalysis(response.ai_analysis);
        setCompliance(response.compliance);
      } else {
        throw new Error("Invalid response from backend.");
      }
    } catch (err) {
      console.error(err);

      setError(
        err instanceof Error
          ? err.message
          : "Unable to analyze proposal."
      );
    } finally {
      setLoading(false);
    }
  }

  const project = analysis?.project;

  return (
    <div className="flex min-h-screen bg-slate-50 text-slate-900">
      <Sidebar />

      <main className="flex-1 p-8 space-y-6">

        {/* HEADER */}
        <header>
          <h1 className="text-2xl font-bold">
            CSR Proposal Intelligence
          </h1>

          <p className="text-sm text-slate-500 mt-1">
            AI-powered proposal extraction, Schedule VII classification
            and CSR compliance screening
          </p>
        </header>

        {/* PROPOSAL INPUT */}
        <section className="bg-white rounded-2xl border border-slate-100 shadow-sm p-7">

          <div className="flex justify-between items-start gap-4">
            <div>
              <h2 className="text-lg font-bold">
                Project Proposal
              </h2>

              <p className="text-sm text-slate-400 mt-1">
                Paste the proposal text to begin AI analysis
              </p>
            </div>

            <button
              onClick={() => setProposalText(DEMO_PROPOSAL)}
              className="px-4 py-2 rounded-xl border border-slate-200 text-sm font-medium text-slate-600 hover:bg-slate-50 transition"
            >
              Load Demo Proposal
            </button>
          </div>

          <textarea
            value={proposalText}
            onChange={(e) => setProposalText(e.target.value)}
            className="mt-5 w-full min-h-[250px] resize-y rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm leading-6 text-slate-800 outline-none focus:border-blue-400 focus:bg-white transition"
            placeholder="Paste your CSR project proposal here..."
          />

          <div className="flex justify-end mt-5">
            <button
              onClick={analyzeProposal}
              disabled={loading}
              className="px-7 py-3 rounded-xl bg-blue-600 text-white font-semibold hover:bg-blue-700 transition disabled:opacity-50"
            >
              {loading
                ? "Analyzing Proposal..."
                : "Analyze & Check Compliance"}
            </button>
          </div>

          {error && (
            <div className="mt-4 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
              <span className="font-semibold">
                Analysis Error:
              </span>{" "}
              {error}
            </div>
          )}
        </section>

        {/* DECISION PIPELINE */}
        <section className="bg-white rounded-2xl border border-slate-100 shadow-sm p-7">

          <h2 className="text-lg font-bold">
            Decision Pipeline
          </h2>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-3 mt-5">

            <div className="rounded-xl border border-blue-100 bg-blue-50 p-4">
              <p className="text-xs font-bold text-blue-600">
                STEP 1
              </p>

              <h3 className="font-bold mt-2">
                AI Extraction
              </h3>

              <p className="text-xs text-slate-500 mt-2">
                Project information extracted from proposal
              </p>
            </div>

            <div className="rounded-xl border border-indigo-100 bg-indigo-50 p-4">
              <p className="text-xs font-bold text-indigo-600">
                STEP 2
              </p>

              <h3 className="font-bold mt-2">
                Schedule VII
              </h3>

              <p className="text-xs text-slate-500 mt-2">
                Activity matched against permitted CSR areas
              </p>
            </div>

            <div className="rounded-xl border border-purple-100 bg-purple-50 p-4">
              <p className="text-xs font-bold text-purple-600">
                STEP 3
              </p>

              <h3 className="font-bold mt-2">
                Compliance
              </h3>

              <p className="text-xs text-slate-500 mt-2">
                Exclusions and implementing agency checks
              </p>
            </div>

            <div className="rounded-xl border border-emerald-100 bg-emerald-50 p-4">
              <p className="text-xs font-bold text-emerald-600">
                STEP 4
              </p>

              <h3 className="font-bold mt-2">
                Optimization
              </h3>

              <p className="text-xs text-slate-500 mt-2">
                Eligible projects enter the allocation engine
              </p>
            </div>

          </div>
        </section>

        {/* RESULT */}
        {analysis && compliance && (
          <>
            {/* COMPLIANCE GATE */}
            <section
              className={`rounded-2xl border p-7 ${
                compliance.status === "PASS"
                  ? "border-emerald-200 bg-emerald-50"
                  : compliance.status === "REJECT"
                  ? "border-red-200 bg-red-50"
                  : "border-amber-200 bg-amber-50"
              }`}
            >
              <div className="flex justify-between items-center gap-6">

                <div>
                  <span
                    className={`inline-flex px-3 py-1 rounded-full text-xs font-bold ${
                      compliance.status === "PASS"
                        ? "bg-emerald-100 text-emerald-700"
                        : compliance.status === "REJECT"
                        ? "bg-red-100 text-red-700"
                        : "bg-amber-100 text-amber-700"
                    }`}
                  >
                    {compliance.status}
                  </span>

                  <h2 className="text-xl font-bold mt-3">
                    {compliance.status === "PASS"
                      ? "CSR Eligible"
                      : compliance.status === "REJECT"
                      ? "CSR Not Eligible"
                      : "Human Review Required"}
                  </h2>

                  <p className="text-sm text-slate-600 mt-1">
                    {compliance.status === "PASS"
                      ? "The project passed the configured CSR compliance checks and can proceed to optimization."
                      : compliance.status === "REJECT"
                      ? "The project failed one or more CSR compliance checks."
                      : "The project requires human review before optimization."}
                  </p>
                </div>

                <div className="text-right">
                  <p className="text-xs uppercase tracking-wider text-slate-500">
                    Optimization Gate
                  </p>

                  <p
                    className={`text-xl font-bold mt-2 ${
                      compliance.eligible_for_optimization
                        ? "text-emerald-700"
                        : "text-red-600"
                    }`}
                  >
                    {compliance.eligible_for_optimization
                      ? "OPEN"
                      : "BLOCKED"}
                  </p>
                </div>

              </div>
            </section>

            {/* AI EXTRACTED INFORMATION */}
            <section className="bg-white rounded-2xl border border-slate-100 shadow-sm p-7">

              <h2 className="text-lg font-bold">
                AI Extracted Project Information
              </h2>

              <p className="text-sm text-slate-400 mt-1">
                Structured information generated from the proposal
              </p>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-5">

                <InfoCard
                  label="Project"
                  value={project?.project_name || "—"}
                />

                <InfoCard
                  label="Sector"
                  value={
                    analysis.classification.category ||
                    project?.intervention ||
                    "—"
                  }
                />

                <InfoCard
                  label="District"
                  value={project?.location?.district || "—"}
                />

                <InfoCard
                  label="State"
                  value={project?.location?.state || "—"}
                />

                <InfoCard
                  label="Project Budget"
                  value={formatLakhs(project?.budget)}
                />

                <InfoCard
                  label="Beneficiaries"
                  value={
                    project?.beneficiaries
                      ? project.beneficiaries.toLocaleString()
                      : "—"
                  }
                />

                <InfoCard
                  label="Beneficiary Group"
                  value={
                    project?.beneficiary_groups?.join(", ") || "—"
                  }
                />

                <InfoCard
                  label="Schedule VII"
                  value={
                    compliance.schedule_vii_category || "Review"
                  }
                  highlight
                />

              </div>
            </section>

            {/* COMPLIANCE CHECKS */}
            <section className="bg-white rounded-2xl border border-slate-100 shadow-sm p-7">

              <h2 className="text-lg font-bold">
                CSR Compliance Checks
              </h2>

              <p className="text-sm text-slate-400 mt-1">
                Deterministic compliance results applied after AI analysis
              </p>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-5">

                <CheckCard
                  label="Schedule VII Match"
                  value={
                    compliance.schedule_vii_match
                      ? "MATCHED"
                      : "REVIEW"
                  }
                  success={compliance.schedule_vii_match}
                />

                <CheckCard
                  label="CSR Eligibility"
                  value={
                    compliance.eligible
                      ? "ELIGIBLE"
                      : "NOT ELIGIBLE"
                  }
                  success={compliance.eligible}
                />

                <CheckCard
                  label="Optimization"
                  value={
                    compliance.eligible_for_optimization
                      ? "ALLOWED"
                      : "BLOCKED"
                  }
                  success={
                    compliance.eligible_for_optimization
                  }
                />

              </div>
            </section>

            {/* REASONING + FLAGS */}
            <section className="grid grid-cols-1 lg:grid-cols-2 gap-5">

              <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-7">

                <h2 className="text-lg font-bold">
                  Compliance Reasoning
                </h2>

                <div className="mt-5 space-y-3">

                  {compliance.reasons.length > 0 ? (
                    compliance.reasons.map((reason, index) => (
                      <div
                        key={index}
                        className="flex gap-3 text-sm text-slate-600"
                      >
                        <span className="text-blue-500 text-lg leading-4">
                          •
                        </span>

                        <span>{reason}</span>
                      </div>
                    ))
                  ) : (
                    <p className="text-sm text-slate-400">
                      No compliance reasoning available.
                    </p>
                  )}

                </div>
              </div>

              <div className="bg-white rounded-2xl border border-slate-100 shadow-sm p-7">

                <h2 className="text-lg font-bold">
                  Compliance Flags
                </h2>

                <div className="mt-5">

                  {compliance.flags.length > 0 ? (
                    <div className="space-y-2">
                      {compliance.flags.map((flag, index) => (
                        <div
                          key={index}
                          className="inline-block mr-2 mb-2 rounded-lg bg-amber-50 border border-amber-200 px-3 py-2 text-xs font-semibold text-amber-700"
                        >
                          {flag}
                        </div>
                      ))}
                    </div>
                  ) : (
                    <span className="inline-flex rounded-lg bg-emerald-50 border border-emerald-100 px-3 py-2 text-xs font-semibold text-emerald-700">
                      No compliance flags
                    </span>
                  )}

                </div>
              </div>

            </section>
          </>
        )}

      </main>
    </div>
  );
}

function InfoCard({
  label,
  value,
  highlight = false,
}: {
  label: string;
  value: string;
  highlight?: boolean;
}) {
  return (
    <div className="rounded-xl bg-slate-50 p-4">
      <p className="text-xs uppercase tracking-wider text-slate-500">
        {label}
      </p>

      <p
        className={`mt-2 font-bold ${
          highlight ? "text-blue-600" : "text-slate-800"
        }`}
      >
        {value}
      </p>
    </div>
  );
}

function CheckCard({
  label,
  value,
  success,
}: {
  label: string;
  value: string;
  success: boolean;
}) {
  return (
    <div className="rounded-xl border border-slate-100 p-5">
      <p className="text-xs uppercase tracking-wider text-slate-500">
        {label}
      </p>

      <p
        className={`mt-3 font-bold ${
          success ? "text-emerald-600" : "text-red-600"
        }`}
      >
        {value}
      </p>
    </div>
  );
}