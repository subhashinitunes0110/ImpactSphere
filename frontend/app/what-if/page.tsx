"use client";

import { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import { postToAPI } from "@/lib/api";

interface ImpactMetrics {
  need_score: number;
  unmet_need: number;
  reach_score: number;
  cost_efficiency: number;
  impact_score: number;
  geographic_score: number;
}

interface Project {
  id?: string;
  name?: string;
  title?: string;
  sector?: string;
  district?: string;
  state?: string;
  location?: string;
  budget: number;
  beneficiaries?: number;
  underserved?: boolean;
  impact_metrics?: ImpactMetrics;
  score?: number;
  impact_score?: number;
}

interface OptimizationResult {
  funded_projects: string[];
  not_funded_projects: string[];
  budget_allocated: number;
  remaining_budget: number;
  projects_funded: number;
  beneficiaries: number;
  underserved_percent: number;
  impact_score: number;
  funded_project_details?: Project[];
  solver: string;
  status: string;
  reasons: Record<string, string>;
}

const FALLBACK_PROJECTS: Project[] = [
  {
    id: "P001",
    name: "Rural Healthcare Initiative",
    sector: "healthcare",
    district: "Dharwad",
    state: "Karnataka",
    budget: 5000000,
    beneficiaries: 10000,
    underserved: false,
    impact_metrics: {
      need_score: 86.6,
      unmet_need: 56.29,
      reach_score: 80.0,
      cost_efficiency: 30.0,
      impact_score: 66.34,
      geographic_score: 56.29,
    },
  },
  {
    id: "P002",
    name: "Rural Education Access",
    sector: "education",
    district: "District A",
    state: "Karnataka",
    budget: 4000000,
    beneficiaries: 8000,
    underserved: true,
    impact_metrics: {
      need_score: 80.0,
      unmet_need: 60.0,
      reach_score: 75.0,
      cost_efficiency: 35.0,
      impact_score: 70.0,
      geographic_score: 60.0,
    },
  },
];

const DEFAULT_RESULT: OptimizationResult = {
  funded_projects: [],
  not_funded_projects: [],
  budget_allocated: 0,
  remaining_budget: 25000000,
  projects_funded: 0,
  beneficiaries: 0,
  underserved_percent: 0,
  impact_score: 0,
  funded_project_details: [],
  solver: "Google OR-Tools (SCIP)",
  status: "READY",
  reasons: {},
};

function formatCrore(value: number) {
  return (value / 10000000).toFixed(2);
}

function formatLakh(value: number) {
  return (value / 100000).toFixed(1);
}

export default function WhatIfPage() {
  const [budget, setBudget] = useState<number>(25000000);
  const [underservedMin, setUnderservedMin] = useState<number>(20);
  const [priority, setPriority] = useState<string>("maximum_impact");

  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const [results, setResults] =
    useState<OptimizationResult>(DEFAULT_RESULT);

  const [usingFallback, setUsingFallback] = useState<boolean>(false);

  const runSimulation = async () => {
    setLoading(true);
    setError(null);
    setUsingFallback(false);

    try {
      const data = await postToAPI<
        {
          budget: number;
          priority: string;
          underserved_min_percent: number;
          beneficiary_group: string | null;
          project_cap: number;
          candidate_projects: null;
        },
        OptimizationResult
      >("/optimization/solve-optimal", {
        budget: Number(budget),
        priority,
        underserved_min_percent: Number(underservedMin),
        beneficiary_group: null,
        project_cap: 7500000,
        candidate_projects: null,
      });

      setResults(data);
    } catch (err) {
      console.error("Optimization error:", err);

      setError(
        err instanceof Error
          ? err.message
          : "Could not reach the FastAPI backend."
      );

      setUsingFallback(true);

      const fallbackFunded = FALLBACK_PROJECTS.filter(
        (project) => (project.budget || 0) <= budget
      );

      const allocated = fallbackFunded.reduce(
        (sum, project) => sum + project.budget,
        0
      );

      const beneficiaries = fallbackFunded.reduce(
        (sum, project) => sum + (project.beneficiaries || 0),
        0
      );

      const impactScores = fallbackFunded
        .map(
          (project) =>
            project.impact_metrics?.impact_score ??
            project.impact_score ??
            project.score ??
            0
        )
        .filter((score) => score > 0);

      const averageImpact =
        impactScores.length > 0
          ? impactScores.reduce((a, b) => a + b, 0) /
            impactScores.length
          : 0;

      setResults({
        ...DEFAULT_RESULT,
        funded_projects: fallbackFunded.map(
          (project) => project.id || ""
        ),
        budget_allocated: allocated,
        remaining_budget: budget - allocated,
        projects_funded: fallbackFunded.length,
        beneficiaries,
        underserved_percent: 20,
        impact_score: Number(averageImpact.toFixed(2)),
        funded_project_details: fallbackFunded,
        solver: "Fallback demo data",
        status: "FALLBACK",
      });
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runSimulation();
  }, []);

  const fundedProjects = results.funded_project_details || [];

  return (
    <div className="flex min-h-screen bg-slate-50 text-slate-900">
      <Sidebar />

      <main className="flex-1 p-8 space-y-6">
        {/* HEADER */}
        <header className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h1 className="text-2xl font-bold">
              What-If Allocation Simulator
            </h1>

            <p className="text-sm text-slate-500">
              Interactive scenario modeling powered by Google OR-Tools
            </p>
          </div>

          <button
            onClick={runSimulation}
            disabled={loading}
            className="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 active:scale-95 text-white rounded-xl font-medium transition disabled:opacity-50"
          >
            {loading ? "Optimizing..." : "Run Optimization"}
          </button>
        </header>

        {/* ERROR / FALLBACK */}
        {error && (
          <div className="p-4 rounded-xl border border-amber-200 bg-amber-50 text-amber-800 text-sm">
            <div className="font-semibold">
              Backend connection issue
            </div>

            <div className="mt-1">
              {error}
            </div>

            {usingFallback && (
              <div className="mt-1 text-xs">
                Showing demo data until the backend is available.
              </div>
            )}
          </div>
        )}

        {/* INPUT PARAMETERS */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-6 bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
          {/* BUDGET */}
          <div>
            <div className="flex justify-between items-center mb-2">
              <label className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                CSR Budget Cap
              </label>

              <span className="text-sm font-bold text-blue-600">
                ₹{formatCrore(budget)} Cr
              </span>
            </div>

            <input
              type="range"
              min="5000000"
              max="50000000"
              step="1000000"
              value={budget}
              onChange={(e) =>
                setBudget(Number(e.target.value))
              }
              className="w-full accent-blue-600 cursor-pointer"
            />

            <div className="flex justify-between text-[11px] text-slate-400 mt-1">
              <span>₹0.50 Cr</span>
              <span>₹5.00 Cr</span>
            </div>
          </div>

          {/* UNDERSERVED */}
          <div>
            <div className="flex justify-between items-center mb-2">
              <label className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                Underserved Allocation
              </label>

              <span className="text-sm font-bold text-blue-600">
                {underservedMin}%
              </span>
            </div>

            <input
              type="range"
              min="0"
              max="60"
              step="5"
              value={underservedMin}
              onChange={(e) =>
                setUnderservedMin(Number(e.target.value))
              }
              className="w-full accent-blue-600 cursor-pointer"
            />

            <div className="flex justify-between text-[11px] text-slate-400 mt-1">
              <span>0%</span>
              <span>60%</span>
            </div>
          </div>

          {/* PRIORITY */}
          <div>
            <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
              Objective Function
            </label>

            <select
              value={priority}
              onChange={(e) =>
                setPriority(e.target.value)
              }
              className="w-full border border-slate-200 rounded-xl p-2.5 text-sm bg-slate-50 focus:bg-white transition"
            >
              <option value="maximum_impact">
                Maximum Impact
              </option>

              <option value="geographic_equity">
                Geographic Equity
              </option>

              <option value="csr_alignment">
                CSR Alignment
              </option>
            </select>
          </div>
        </section>

        {/* SIMULATE BUTTON */}
        <div className="flex justify-end">
          <button
            onClick={runSimulation}
            disabled={loading}
            className="px-6 py-3 rounded-xl bg-slate-900 text-white font-semibold hover:bg-slate-800 transition disabled:opacity-50"
          >
            {loading
              ? "Calculating Optimal Portfolio..."
              : "Simulate Scenario"}
          </button>
        </div>

        {/* SUMMARY METRICS */}
        <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
          <div className="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm">
            <p className="text-xs text-slate-500 uppercase tracking-wider">
              Allocated Capital
            </p>

            <p className="text-2xl font-bold mt-1">
              ₹{formatLakh(results.budget_allocated)} L
            </p>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm">
            <p className="text-xs text-slate-500 uppercase tracking-wider">
              Remaining Budget
            </p>

            <p className="text-2xl font-bold mt-1">
              ₹{formatLakh(results.remaining_budget)} L
            </p>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm">
            <p className="text-xs text-slate-500 uppercase tracking-wider">
              Selected Projects
            </p>

            <p className="text-2xl font-bold mt-1">
              {results.projects_funded}
            </p>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm">
            <p className="text-xs text-slate-500 uppercase tracking-wider">
              Beneficiaries
            </p>

            <p className="text-2xl font-bold mt-1">
              {results.beneficiaries.toLocaleString()}
            </p>
          </div>

          <div className="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm">
            <p className="text-xs text-slate-500 uppercase tracking-wider">
              Avg Impact Score
            </p>

            <p className="text-2xl font-bold mt-1 text-emerald-600">
              {results.impact_score}
            </p>
          </div>
        </section>

        {/* CONSTRAINT STATUS */}
        <section className="bg-white rounded-2xl border border-slate-100 shadow-sm p-5">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <p className="text-xs text-slate-500 uppercase tracking-wider">
                Optimization Status
              </p>

              <p className="font-semibold mt-1">
                {results.status}
              </p>
            </div>

            <div>
              <p className="text-xs text-slate-500 uppercase tracking-wider">
                Solver
              </p>

              <p className="font-semibold mt-1">
                {results.solver}
              </p>
            </div>

            <div>
              <p className="text-xs text-slate-500 uppercase tracking-wider">
                Underserved Share
              </p>

              <p className="font-semibold mt-1 text-blue-600">
                {results.underserved_percent}%
              </p>
            </div>

            <div>
              <p className="text-xs text-slate-500 uppercase tracking-wider">
                Required Minimum
              </p>

              <p className="font-semibold mt-1">
                {underservedMin}%
              </p>
            </div>
          </div>
        </section>

        {/* ALLOCATION TABLE */}
        <section className="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden">
          <div className="p-5 border-b border-slate-100">
            <div className="font-semibold text-slate-800">
              Selected Optimal Allocations
            </div>

            <p className="text-xs text-slate-400 mt-1">
              Projects selected by the global optimization engine
            </p>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-50 text-slate-500 font-medium">
                <tr>
                  <th className="p-4">
                    Project
                  </th>

                  <th className="p-4">
                    Sector
                  </th>

                  <th className="p-4">
                    District
                  </th>

                  <th className="p-4">
                    Budget
                  </th>

                  <th className="p-4">
                    Beneficiaries
                  </th>

                  <th className="p-4">
                    Impact
                  </th>
                </tr>
              </thead>

              <tbody className="divide-y divide-slate-100">
                {fundedProjects.length > 0 ? (
                  fundedProjects.map((project, index) => {
                    const impact =
                      project.impact_metrics
                        ?.impact_score ??
                      project.impact_score ??
                      project.score ??
                      0;

                    return (
                      <tr
                        key={
                          project.id ||
                          `project-${index}`
                        }
                        className="hover:bg-slate-50/80 transition"
                      >
                        <td className="p-4 font-medium text-slate-900">
                          {project.name ||
                            project.title ||
                            `Project #${index + 1}`}
                        </td>

                        <td className="p-4 text-slate-600">
                          {project.sector ||
                            "General"}
                        </td>

                        <td className="p-4 text-slate-600">
                          {project.district ||
                            project.location ||
                            "—"}
                        </td>

                        <td className="p-4 font-medium">
                          ₹
                          {formatLakh(
                            project.budget
                          )}{" "}
                          L
                        </td>

                        <td className="p-4 text-slate-600">
                          {(
                            project.beneficiaries ||
                            0
                          ).toLocaleString()}
                        </td>

                        <td className="p-4 font-bold text-emerald-600">
                          {impact}
                        </td>
                      </tr>
                    );
                  })
                ) : (
                  <tr>
                    <td
                      colSpan={6}
                      className="p-10 text-center text-slate-400"
                    >
                      {loading
                        ? "Running global optimization..."
                        : "No projects selected for the current scenario."}
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </section>

        {/* NOT FUNDED */}
        {results.not_funded_projects.length > 0 && (
          <section className="bg-white rounded-2xl border border-slate-100 shadow-sm p-5">
            <h2 className="font-semibold text-slate-800">
              Allocation Decisions
            </h2>

            <div className="mt-4 space-y-2">
              {results.not_funded_projects.map(
                (projectId) => (
                  <div
                    key={projectId}
                    className="flex justify-between items-center p-3 rounded-xl bg-slate-50 text-sm"
                  >
                    <span className="font-medium">
                      {projectId}
                    </span>

                    <span className="text-slate-500">
                      {results.reasons?.[
                        projectId
                      ] ||
                        "Not selected"}
                    </span>
                  </div>
                )
              )}
            </div>
          </section>
        )}
      </main>
    </div>
  );
}