"use client";

import { useState } from "react";
import Sidebar from "@/components/Sidebar";

interface OptimizedResult {
  status: string;
  allocated_budget: number;
  unspent_budget: number;
  total_impact: number;
  average_impact: number;
  selected_proposals: Array<{
    id: string;
    name: string;
    sector: string;
    district: string;
    budget: number;
    impactScore: number;
  }>;
}

export default function WhatIfPage() {
  const [budgetLimit, setBudgetLimit] = useState<number>(15000000); // 1.5 Cr default
  const [backwardRatio, setBackwardRatio] = useState<number>(20); // 20% default
  const [loading, setLoading] = useState<boolean>(false);
  const [result, setResult] = useState<OptimizedResult | null>(null);

  const handleSimulate = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/api/optimize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          budget_limit: budgetLimit,
          min_backward_ratio: backwardRatio / 100,
          sector_preference: "All",
        }),
      });
      if (!response.ok) throw new Error("Optimization request failed");
      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error("Failed to connect to backend optimizer:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-slate-50 text-slate-900">
      <Sidebar />
      <main className="flex-1 p-8 space-y-6">
        <header>
          <h1 className="text-2xl font-bold">What-If Allocation Simulator</h1>
          <p className="text-sm text-slate-500">
            Tune budget ceilings and district quotas to run OR-Tools integer programming optimization.
          </p>
        </header>

        {/* Simulation Controls */}
        <section className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <div className="flex justify-between items-center mb-2">
                <label className="text-sm font-semibold text-slate-700">
                  Total Budget Ceiling
                </label>
                <span className="text-sm font-bold text-blue-600">
                  ₹{(budgetLimit / 100000).toFixed(0)} Lakhs
                </span>
              </div>
              <input
                type="range"
                min={3000000}
                max={25000000}
                step={500000}
                value={budgetLimit}
                onChange={(e) => setBudgetLimit(Number(e.target.value))}
                className="w-full accent-blue-600 cursor-pointer"
              />
            </div>

            <div>
              <div className="flex justify-between items-center mb-2">
                <label className="text-sm font-semibold text-slate-700">
                  Min. Backward District Quota
                </label>
                <span className="text-sm font-bold text-emerald-600">
                  {backwardRatio}%
                </span>
              </div>
              <input
                type="range"
                min={0}
                max={60}
                step={5}
                value={backwardRatio}
                onChange={(e) => setBackwardRatio(Number(e.target.value))}
                className="w-full accent-emerald-600 cursor-pointer"
              />
            </div>
          </div>

          <button
            onClick={handleSimulate}
            disabled={loading}
            className="w-full py-3 bg-blue-600 hover:bg-blue-700 text-white font-semibold rounded-xl transition shadow disabled:opacity-50"
          >
            {loading ? "Running Mathematical Solver..." : "Run Portfolio Optimization"}
          </button>
        </section>

        {/* Solver Results */}
        {result && (
          <section className="space-y-6">
            <div className="grid grid-cols-1 sm:grid-cols-4 gap-4">
              <div className="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm">
                <p className="text-xs text-slate-500 uppercase">Solver Status</p>
                <p className="text-xl font-bold capitalize text-emerald-600 mt-1">
                  {result.status}
                </p>
              </div>
              <div className="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm">
                <p className="text-xs text-slate-500 uppercase">Allocated Budget</p>
                <p className="text-xl font-bold mt-1">
                  ₹{(result.allocated_budget / 100000).toFixed(1)} L
                </p>
              </div>
              <div className="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm">
                <p className="text-xs text-slate-500 uppercase">Unspent Budget</p>
                <p className="text-xl font-bold mt-1 text-slate-500">
                  ₹{(result.unspent_budget / 100000).toFixed(1)} L
                </p>
              </div>
              <div className="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm">
                <p className="text-xs text-slate-500 uppercase">Avg Impact Score</p>
                <p className="text-xl font-bold text-blue-600 mt-1">
                  {result.average_impact} / 100
                </p>
              </div>
            </div>

            <div className="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden">
              <div className="p-4 border-b border-slate-100 font-semibold">
                Optimized Project Selection ({result.selected_proposals.length} Projects Selected)
              </div>
              <table className="w-full text-left text-sm">
                <thead className="bg-slate-50 text-slate-500 font-medium">
                  <tr>
                    <th className="p-4">Project</th>
                    <th className="p-4">Sector</th>
                    <th className="p-4">District</th>
                    <th className="p-4">Budget</th>
                    <th className="p-4">Impact</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {result.selected_proposals.map((proj) => (
                    <tr key={proj.id} className="hover:bg-slate-50/70">
                      <td className="p-4 font-medium">{proj.name}</td>
                      <td className="p-4 text-slate-600">{proj.sector}</td>
                      <td className="p-4 text-slate-600">{proj.district}</td>
                      <td className="p-4 font-semibold">₹{(proj.budget / 100000).toFixed(0)} L</td>
                      <td className="p-4 font-bold text-emerald-600">{proj.impactScore}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}