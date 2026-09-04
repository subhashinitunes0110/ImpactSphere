"use client";

import { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import { fetchFromAPI } from "@/lib/api";
import { ProjectProposal } from "@/types/csr";

const fallbackProjects: ProjectProposal[] = [
  {
    id: "1",
    name: "Rural Healthcare Initiative",
    sector: "Healthcare",
    location: "District X",
    district: "District X",
    budget: 5000000,
    beneficiaries: 12000,
    needScore: 91,
    impactScore: 88,
    efficiencyScore: 82,
    status: "Recommended",
  },
  {
    id: "2",
    name: "Digital Education Access",
    sector: "Education",
    location: "District C",
    district: "District C",
    budget: 3500000,
    beneficiaries: 8500,
    needScore: 87,
    impactScore: 85,
    efficiencyScore: 79,
    status: "Recommended",
  },
  {
    id: "3",
    name: "Clean Water Infrastructure",
    sector: "Water & Sanitation",
    location: "District Y",
    district: "District Y",
    budget: 4500000,
    beneficiaries: 15000,
    needScore: 84,
    impactScore: 82,
    efficiencyScore: 85,
    status: "Recommended",
  },
  {
    id: "4",
    name: "Solar Micro-Grids",
    sector: "Renewable Energy",
    location: "District Z",
    district: "District Z",
    budget: 6000000,
    beneficiaries: 6000,
    needScore: 78,
    impactScore: 80,
    efficiencyScore: 75,
    status: "Under Review",
  },
];

export default function DashboardPage() {
  const [projects, setProjects] = useState<ProjectProposal[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      const data = await fetchFromAPI<ProjectProposal[]>("/api/proposals", fallbackProjects);
      setProjects(data);
      setLoading(false);
    }
    loadData();
  }, []);

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

        <section className="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden">
          <div className="p-5 border-b border-slate-100 font-semibold text-slate-800">
            Top Recommended CSR Projects
          </div>

          {loading ? (
            <div className="p-8 space-y-4 animate-pulse">
              <div className="h-6 bg-slate-200 rounded w-1/3"></div>
              <div className="h-6 bg-slate-100 rounded w-full"></div>
              <div className="h-6 bg-slate-100 rounded w-full"></div>
              <div className="h-6 bg-slate-100 rounded w-full"></div>
            </div>
          ) : (
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
                {projects.map((proj) => (
                  <tr key={proj.id} className="hover:bg-slate-50/80">
                    <td className="p-4 font-medium text-slate-900">{proj.name}</td>
                    <td className="p-4 text-slate-600">{proj.sector}</td>
                    <td className="p-4 text-slate-600">{proj.location}</td>
                    <td className="p-4 font-semibold text-slate-900">
                      ₹{(proj.budget / 100000).toFixed(0)} L
                    </td>
                    <td className="p-4 text-slate-600">{proj.beneficiaries.toLocaleString()}</td>
                    <td className="p-4 font-bold text-emerald-600">{proj.impactScore}</td>
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
          )}
        </section>
      </main>
    </div>
  );
}