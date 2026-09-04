"use client";

import { useState, useEffect } from "react";
import Sidebar from "@/components/Sidebar";

interface Project {
  id?: string;
  name?: string;
  title?: string;
  sector: string;
  district?: string;
  location?: string;
  budget: number;
  score?: number;
  impact_score?: number;
}

interface SimulationSummary {
  allocated_budget: number;
  funded_count: number;
  total_candidate_projects: number;
  average_impact_score: number;
  underserved_share_percent: number;
}

interface SimulationResult {
  status: string;
  summary: SimulationSummary;
  allocated_projects: Project[];
}

export default function WhatIfPage() {
  const [budget, setBudget] = useState<number>(25000000);
  const [underservedMin, setUnderservedMin] = useState<number>(20);
  const [priority, setPriority] = useState<string>("maximum_impact");
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<SimulationResult | null>(null);

  const runSimulation = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("http://localhost:8000/optimization/what-if", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          budget: Number(budget),
          priority: priority,
          underserved_min_percent: Number(underservedMin),
          project_cap: 7500000,
          candidate_projects: null,
        }),
      });

      if (!res.ok) {
        throw new Error(`Server returned status ${res.status}: ${res.statusText}`);
      }

      const data: SimulationResult = await res.json();
      setResults(data);
    } catch (err: any) {
      console.error("Simulation error:", err);
      setError(
        err.message || "Could not reach FastAPI backend. Make sure port 8000 is open."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runSimulation();
  }, []);

  return (
    <div className="flex min-h-screen bg-slate-50 text-slate-900">
      <Sidebar />
      <main className="flex-1 p-8 space-y-6">
        <header className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h1 className="text-2xl font-bold">What-If Allocation Simulator</h1>
            <p className="text-sm text-slate-500">
              Interactive scenario modeling powered by OR-Tools MIP solver
            </p>
          </div>
          <button
            onClick={runSimulation}
            disabled={loading}
            className="px-5 py-2.5 bg-blue-600 hover:bg-blue-700 active:scale-95 text-white rounded-xl font-medium transition disabled:opacity-50"
          >
            {loading ? "Optimizing..." : "Re-Run Optimization"}
          </button>
        </header>

        {error && (
          <div className="p-4 rounded-xl border border-red-200 bg-red-50 text-red-700 text-sm flex items-center justify-between">
            <span>{error}</span>
            <span className="text-xs text-red-500">Ensure backend runs at localhost:8000</span>
          </div>
        )}

        {/* Input Parameters */}
        <section className="grid grid-cols-1 md:grid-cols-3 gap-6 bg-white p-6 rounded-2xl shadow-sm border border-slate-100">
          <div>
            <div className="flex justify-between items-center mb-2">
              <label className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                CSR Budget Cap
              </label>
              <span className="text-sm font-bold text-blue-600">
                ₹{(budget / 10000000).toFixed(2)} Cr
              </span>
            </div>
            <input
              type="range"
              min="5000000"
              max="50000000"
              step="1000000"
              value={budget}
              onChange={(e) => setBudget(Number(e.target.value))}
              className="w-full accent-blue-600 cursor-pointer"
            />
          </div>

          <div>
            <div className="flex justify-between items-center mb-2">
              <label className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                Underserved Districts Min
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
              onChange={(e) => setUnderservedMin(Number(e.target.value))}
              className="w-full accent-blue-600 cursor-pointer"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
              Objective Function
            </label>
            <select
              value={priority}
              onChange={(e) => setPriority(e.target.value)}
              className="w-full border border-slate-200 rounded-xl p-2.5 text-sm bg-slate-50 focus:bg-white transition"
            >
              <option value="maximum_impact">Maximize Total Impact Score</option>
              <option value="balanced_equity">Balanced Regional Equity</option>
              <option value="cost_efficiency">Maximize Cost Efficiency</option>
            </select>
          </div>
        </section>

        {/* Dynamic Solution Metrics */}
        {results?.summary && (
          <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <div className="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm">
              <p className="text-xs text-slate-500 uppercase tracking-wider">Allocated Capital</p>
              <p className="text-2xl font-bold mt-1 text-slate-900">
                ₹{(results.summary.allocated_budget / 100000).toFixed(1)} L
              </p>
            </div>
            <div className="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm">
              <p className="text-xs text-slate-500 uppercase tracking-wider">Selected Portfolio</p>
              <p className="text-2xl font-bold mt-1 text-slate-900">
                {results.summary.funded_count}{" "}
                <span className="text-sm font-normal text-slate-400">
                  / {results.summary.total_candidate_projects} projects
                </span>
              </p>
            </div>
            <div className="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm">
              <p className="text-xs text-slate-500 uppercase tracking-wider">Portfolio Avg Impact</p>
              <p className="text-2xl font-bold mt-1 text-emerald-600">
                {results.summary.average_impact_score}
              </p>
            </div>
            <div className="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm">
              <p className="text-xs text-slate-500 uppercase tracking-wider">Underserved Share</p>
              <p className="text-2xl font-bold mt-1 text-blue-600">
                {results.summary.underserved_share_percent}%
              </p>
            </div>
          </section>
        )}

        {/* Allocation Decision Table */}
        <section className="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden">
          <div className="p-5 border-b border-slate-100 font-semibold text-slate-800">
            Selected Optimal Allocations
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm">
              <thead className="bg-slate-50 text-slate-500 font-medium">
                <tr>
                  <th className="p-4">Project Name</th>
                  <th className="p-4">Sector</th>
                  <th className="p-4">Target Region</th>
                  <th className="p-4">Budget</th>
                  <th className="p-4">Composite Score</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {results?.allocated_projects?.length ? (
                  results.allocated_projects.map((proj, idx) => (
                    <tr key={idx} className="hover:bg-slate-50/80 transition">
                      <td className="p-4 font-medium text-slate-900">
                        {proj.title || proj.name || `Project #${idx + 1}`}
                      </td>
                      <td className="p-4 text-slate-600">{proj.sector}</td>
                      <td className="p-4 text-slate-600">
                        {proj.district || proj.location || "Underserved"}
                      </td>
                      <td className="p-4 font-medium text-slate-900">
                        ₹{(proj.budget / 100000).toFixed(1)} L
                      </td>
                      <td className="p-4 font-semibold text-emerald-600">
                        {proj.impact_score || proj.score || 85}
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan={5} className="p-6 text-center text-slate-400">
                      {loading ? "Running solver..." : "No allocated projects found for current parameters."}
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </section>
      </main>
    </div>
  );
}