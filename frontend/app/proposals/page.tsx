"use client";

import { useState, useEffect } from "react";
import Sidebar from "@/components/Sidebar";

interface DistrictMetric {
  district: string;
  state: string;
  composite_need: number;
  saturation_index: number;
  unmet_need_score: number;
  category: "High Priority" | "Moderate" | "Saturated";
}

const DEFAULT_DISTRICTS: DistrictMetric[] = [
  {
    district: "Kishanganj",
    state: "Bihar",
    composite_need: 94,
    saturation_index: 18,
    unmet_need_score: 91,
    category: "High Priority",
  },
  {
    district: "Shrawasti",
    state: "Uttar Pradesh",
    composite_need: 91,
    saturation_index: 22,
    unmet_need_score: 87,
    category: "High Priority",
  },
  {
    district: "Nuh",
    state: "Haryana",
    composite_need: 86,
    saturation_index: 31,
    unmet_need_score: 82,
    category: "High Priority",
  },
  {
    district: "Barwani",
    state: "Madhya Pradesh",
    composite_need: 83,
    saturation_index: 29,
    unmet_need_score: 79,
    category: "Moderate",
  },
  {
    district: "Bengaluru Urban",
    state: "Karnataka",
    composite_need: 24,
    saturation_index: 92,
    unmet_need_score: 12,
    category: "Saturated",
  },
  {
    district: "Pune",
    state: "Maharashtra",
    composite_need: 28,
    saturation_index: 88,
    unmet_need_score: 16,
    category: "Saturated",
  },
];

export default function ImpactMapPage() {
  const [districts, setDistricts] = useState<DistrictMetric[]>(DEFAULT_DISTRICTS);

  useEffect(() => {
    fetch("http://localhost:8000/impact/need-index")
      .then((res) => {
        if (!res.ok) throw new Error("API not ready");
        return res.json();
      })
      .then((data) => {
        if (data?.districts && data.districts.length > 0) {
          setDistricts(data.districts);
        }
      })
      .catch(() => {
        // Keeps DEFAULT_DISTRICTS on network/backend fallback
      });
  }, []);

  return (
    <div className="flex min-h-screen bg-slate-50 text-slate-900">
      <Sidebar />
      <main className="flex-1 p-8 space-y-6">
        <div>
          <h1 className="text-2xl font-bold">District Need & Saturation Map</h1>
          <p className="text-sm text-slate-500">
            Identifying CSR impact deserts vs. donor-saturated regions
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {districts.map((d, i) => (
            <div
              key={i}
              className="bg-white p-5 rounded-2xl border border-slate-100 shadow-sm space-y-4"
            >
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-bold text-lg text-slate-900">{d.district}</h3>
                  <p className="text-xs text-slate-400">{d.state}</p>
                </div>
                <span
                  className={`text-xs px-2.5 py-1 rounded-full font-semibold ${
                    d.unmet_need_score >= 80
                      ? "bg-rose-100 text-rose-700"
                      : d.unmet_need_score >= 50
                      ? "bg-amber-100 text-amber-700"
                      : "bg-slate-100 text-slate-600"
                  }`}
                >
                  {d.unmet_need_score >= 80 ? "Impact Desert" : "Donor Saturated"}
                </span>
              </div>

              <div className="space-y-2 text-sm pt-2 border-t border-slate-50">
                <div className="flex justify-between">
                  <span className="text-slate-500">Vulnerability Score:</span>
                  <span className="font-semibold text-slate-700">{d.composite_need}/100</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">CSR Saturation:</span>
                  <span className="font-semibold text-slate-700">{d.saturation_index}/100</span>
                </div>
                <div className="flex justify-between border-t border-slate-100 pt-2 font-medium">
                  <span className="text-slate-800">Unmet Need Score:</span>
                  <span className="font-bold text-blue-600">{d.unmet_need_score}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}