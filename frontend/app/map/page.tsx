"use client";

import { useState } from "react";
import Sidebar from "@/components/Sidebar";

const projects = [
  {
    name: "Rural Healthcare Initiative",
    sector: "Healthcare",
    location: "District X",
    budget: "₹50 L",
    beneficiaries: "12,000",
    need: 91,
    impact: 88,
    efficiency: 82,
    status: "Recommended",
  },
  {
    name: "Digital Education Access",
    sector: "Education",
    location: "District C",
    budget: "₹35 L",
    beneficiaries: "8,500",
    need: 87,
    impact: 85,
    efficiency: 79,
    status: "Recommended",
  },
  {
    name: "Clean Water Infrastructure",
    sector: "Water & Sanitation",
    location: "District Y",
    budget: "₹45 L",
    beneficiaries: "15,000",
    need: 84,
    impact: 82,
    efficiency: 85,
    status: "Recommended",
  },
  {
    name: "Solar Micro-Grids",
    sector: "Renewable Energy",
    location: "District Z",
    budget: "₹60 L",
    beneficiaries: "6,000",
    need: 78,
    impact: 80,
    efficiency: 75,
    status: "Under Review",
  },
];

export default function DashboardPage() {
  return (
    <div className="flex min-h-screen bg-slate-50 text-slate-900">
      <Sidebar />
      <main className="flex-1 p-8 space-y-6">
        <header className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold">Portfolio Overview</h1>
            <p className="text-sm text-slate-500">
              Corporate Social Responsibility allocation & impact dashboard
            </p>
          </div>
          <span className="px-3.5 py-1.5 bg-emerald-50 text-emerald-700 text-xs font-semibold rounded-full border border-emerald-200">
            Active Cycle: FY 2026–27
          </span>
        </header>

        {/* Quick KPI Stat Cards */}
        <section className="grid grid-cols-1 sm:grid-cols-4 gap-4">
          <div className="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm">
            <p className="text-xs text-slate-500 uppercase tracking-wider">Mandatory CSR Budget</p>
            <p className="text-2xl font-bold mt-1">₹2.50 Cr</p>
          </div>
          <div className="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm">
            <p className="text-xs text-slate-500 uppercase tracking-wider">Proposals Evaluated</p>
            <p className="text-2xl font-bold mt-1">20 Projects</p>
          </div>
          <div className="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm">
            <p className="text-xs text-slate-500 uppercase tracking-wider">Recommended Portfolio</p>
            <p className="text-2xl font-bold mt-1 text-blue-600">7 Projects</p>
          </div>
          <div className="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm">
            <p className="text-xs text-slate-500 uppercase tracking-wider">Avg Portfolio Impact</p>
            <p className="text-2xl font-bold mt-1 text-emerald-600">86.4 / 100</p>
          </div>
        </section>

        {/* Active Projects Table */}
        <section className="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden">
          <div className="p-5 border-b border-slate-100 font-semibold text-slate-800">
            Top Recommended CSR Projects
          </div>
          <table className="w-full text-left text-sm">
            <thead className="bg-slate-50 text-slate-500 font-medium">
              <tr>
                <th className="p-4">Project</th>
                <th className="p-4">Sector</th>
                <th className="p-4">Location</th>
                <th className="p-4">Budget</th>
                <th className="p-4">Beneficiaries</th>
                <th className="p-4">Impact</th>
                <th className="p-4">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {projects.map((proj, idx) => (
                <tr key={idx} className="hover:bg-slate-50/80">
                  <td className="p-4 font-medium text-slate-900">{proj.name}</td>
                  <td className="p-4 text-slate-600">{proj.sector}</td>
                  <td className="p-4 text-slate-600">{proj.location}</td>
                  <td className="p-4 font-semibold text-slate-900">{proj.budget}</td>
                  <td className="p-4 text-slate-600">{proj.beneficiaries}</td>
                  <td className="p-4 font-bold text-emerald-600">{proj.impact}</td>
                  <td className="p-4">
                    <span
                      className={`px-2.5 py-1 rounded-full text-xs font-semibold ${
                        proj.status === "Recommended"
                          ? "bg-blue-50 text-blue-700"
                          : "bg-amber-50 text-amber-700"
                      }`}
                    >
                      {proj.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>
      </main>
    </div>
  );
}