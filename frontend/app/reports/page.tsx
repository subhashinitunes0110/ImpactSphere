"use client";

import Sidebar from "@/components/Sidebar";

export default function ReportsPage() {
  return (
    <div className="flex min-h-screen bg-slate-50 text-slate-900">
      <Sidebar />
      <main className="flex-1 p-8 space-y-6">
        <header className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold">Board-Ready CSR Report</h1>
            <p className="text-sm text-slate-500">
              Export comprehensive portfolio compliance and impact audit documentation
            </p>
          </div>
          <button
            onClick={() => window.print()}
            className="px-5 py-2.5 bg-slate-900 text-white rounded-xl font-medium hover:bg-slate-800 transition"
          >
            Export to PDF
          </button>
        </header>

        <section className="bg-white p-8 rounded-2xl border border-slate-100 shadow-sm space-y-6">
          <div className="border-b pb-4">
            <h2 className="text-xl font-bold">Executive CSR Portfolio Summary</h2>
            <p className="text-sm text-slate-500">Statutory Cycle: FY 2026–27 | Schedule VII Compliant</p>
          </div>
          <div className="grid grid-cols-3 gap-6">
            <div className="p-4 bg-slate-50 rounded-xl">
              <p className="text-xs text-slate-500">Total Approved Capital</p>
              <p className="text-xl font-bold mt-1">₹2.45 Cr</p>
            </div>
            <div className="p-4 bg-slate-50 rounded-xl">
              <p className="text-xs text-slate-500">Statutory Admin Overhead</p>
              <p className="text-xl font-bold mt-1">4.2% (≤ 5% Legal Limit)</p>
            </div>
            <div className="p-4 bg-slate-50 rounded-xl">
              <p className="text-xs text-slate-500">Audit Status</p>
              <p className="text-xl font-bold mt-1 text-emerald-600">Passed (100% CSR-1 Verified)</p>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}