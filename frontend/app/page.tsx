"use client";

import { useState } from "react";

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
    name: "Clean Water Initiative",
    sector: "Water & Sanitation",
    location: "District A",
    budget: "₹42 L",
    beneficiaries: "7,200",
    need: 94,
    impact: 91,
    efficiency: 86,
    status: "Recommended",
  },
  {
    name: "Women Skill Development",
    sector: "Livelihood",
    location: "District D",
    budget: "₹28 L",
    beneficiaries: "4,300",
    need: 82,
    impact: 79,
    efficiency: 88,
    status: "Review",
  },
];

export default function Home() {
  const [activePage, setActivePage] = useState("Dashboard");

  return (
    <main className="min-h-screen bg-[#f7f8fa] text-slate-900">
      <div className="flex min-h-screen">

        {/* SIDEBAR */}
        <aside className="hidden w-64 flex-col border-r border-slate-200 bg-white px-5 py-6 md:flex">

          {/* Logo */}
          <div className="mb-10">
            <div className="flex items-center gap-3">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-900 text-lg font-bold text-white">
                I
              </div>

              <div>
                <h1 className="text-lg font-bold">ImpactSphere</h1>
                <p className="text-xs text-slate-500">CSR Intelligence</p>
              </div>
            </div>
          </div>

          {/* Navigation */}
          <nav className="space-y-2">

            {[
              "Dashboard",
              "Proposals",
              "What-If",
              "Impact Map",
              "Reports",
            ].map((item) => (
              <button
                key={item}
                onClick={() => setActivePage(item)}
                className={`w-full rounded-xl px-4 py-3 text-left text-sm font-medium transition ${
                  activePage === item
                    ? "bg-slate-900 text-white"
                    : "text-slate-600 hover:bg-slate-100"
                }`}
              >
                {item}
              </button>
            ))}

          </nav>

          {/* Bottom */}
          <div className="mt-auto rounded-2xl bg-slate-50 p-4">
            <p className="text-xs font-medium text-slate-500">
              Current CSR Cycle
            </p>

            <p className="mt-1 text-sm font-semibold">
              FY 2026–27
            </p>

            <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-200">
              <div className="h-full w-[68%] rounded-full bg-slate-900" />
            </div>

            <p className="mt-2 text-xs text-slate-500">
              Planning in progress
            </p>
          </div>
        </aside>

        {/* MAIN */}
        <section className="flex-1">

          {/* HEADER */}
          <header className="flex items-center justify-between border-b border-slate-200 bg-white px-6 py-5 lg:px-10">

            <div>
              <p className="text-sm text-slate-500">
                CSR Planning / FY 2026–27
              </p>

              <h2 className="mt-1 text-2xl font-bold tracking-tight">
                Good morning, CSR Team
              </h2>
            </div>

            <button className="rounded-xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white hover:bg-slate-800">
              + Upload Proposal
            </button>

          </header>

          <div className="px-6 py-8 lg:px-10">

            {/* HERO */}
            <div className="mb-8 rounded-3xl bg-slate-900 p-8 text-white">

              <div className="max-w-3xl">

                <p className="mb-3 text-sm font-medium text-slate-300">
                  MAXIMUM IMPACT, NOT MAXIMUM SPEND
                </p>

                <h3 className="text-3xl font-bold tracking-tight lg:text-4xl">
                  Where can your CSR budget change the most lives?
                </h3>

                <p className="mt-4 max-w-2xl text-sm leading-6 text-slate-300">
                  ImpactSphere evaluates proposals using community need,
                  expected impact, cost efficiency and CSR eligibility —
                  then recommends where limited funds can create the
                  greatest expected social impact.
                </p>

                <button className="mt-6 rounded-xl bg-white px-5 py-3 text-sm font-semibold text-slate-900 hover:bg-slate-100">
                  View Recommended Portfolio →
                </button>

              </div>

            </div>

            {/* METRICS */}
            <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-5">

              <Metric
                title="Available Budget"
                value="₹5 Cr"
                subtitle="CSR planning budget"
              />

              <Metric
                title="Proposals"
                value="20"
                subtitle="Received this cycle"
              />

              <Metric
                title="Eligible"
                value="17"
                subtitle="Passed compliance"
              />

              <Metric
                title="Recommended"
                value="7"
                subtitle="Projects selected"
              />

              <Metric
                title="Expected Reach"
                value="32K"
                subtitle="People projected"
              />

            </div>

            {/* CONTENT GRID */}
            <div className="mt-8 grid gap-6 xl:grid-cols-3">

              {/* PROJECTS */}
              <div className="rounded-3xl border border-slate-200 bg-white p-6 xl:col-span-2">

                <div className="flex items-center justify-between">

                  <div>
                    <h3 className="text-lg font-bold">
                      Recommended Projects
                    </h3>

                    <p className="mt-1 text-sm text-slate-500">
                      Projects ranked by expected social impact
                    </p>
                  </div>

                  <button className="text-sm font-semibold text-slate-700 hover:underline">
                    View all
                  </button>

                </div>

                <div className="mt-6 space-y-4">

                  {projects.map((project) => (
                    <ProjectCard
                      key={project.name}
                      project={project}
                    />
                  ))}

                </div>

              </div>

              {/* IMPACT SUMMARY */}
              <div className="rounded-3xl border border-slate-200 bg-white p-6">

                <h3 className="text-lg font-bold">
                  Portfolio Impact
                </h3>

                <p className="mt-1 text-sm text-slate-500">
                  Current recommended allocation
                </p>

                <div className="mt-8 flex items-center justify-center">

                  <div className="flex h-44 w-44 items-center justify-center rounded-full border-[18px] border-slate-900">

                    <div className="text-center">
                      <p className="text-4xl font-bold">87.4</p>
                      <p className="text-xs text-slate-500">
                        Impact Score
                      </p>
                    </div>

                  </div>

                </div>

                <div className="mt-8 space-y-4">

                  <SummaryRow
                    label="Budget allocated"
                    value="₹4.92 Cr"
                  />

                  <SummaryRow
                    label="Projects funded"
                    value="7"
                  />

                  <SummaryRow
                    label="Expected beneficiaries"
                    value="32,000"
                  />

                  <SummaryRow
                    label="Underserved allocation"
                    value="27%"
                  />

                </div>

              </div>

            </div>

            {/* WHAT-IF */}
            <div className="mt-6 rounded-3xl border border-slate-200 bg-white p-6">

              <div className="flex flex-col justify-between gap-5 md:flex-row md:items-center">

                <div>
                  <div className="flex items-center gap-2">
                    <span className="rounded-lg bg-slate-100 px-2 py-1 text-xs font-bold">
                      WHAT-IF
                    </span>

                    <span className="text-sm text-slate-500">
                      Scenario simulator
                    </span>
                  </div>

                  <h3 className="mt-3 text-xl font-bold">
                    What happens if your priorities change?
                  </h3>

                  <p className="mt-2 max-w-2xl text-sm leading-6 text-slate-500">
                    Change the budget, beneficiary priority or geographic
                    constraints and instantly compare the resulting portfolio.
                  </p>
                </div>

                <button
                  onClick={() => setActivePage("What-If")}
                  className="whitespace-nowrap rounded-xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white hover:bg-slate-800"
                >
                  Open What-If Engine →
                </button>

              </div>

            </div>

          </div>

        </section>

      </div>
    </main>
  );
}


/* ---------------- COMPONENTS ---------------- */

function Metric({
  title,
  value,
  subtitle,
}: {
  title: string;
  value: string;
  subtitle: string;
}) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5">

      <p className="text-xs font-medium text-slate-500">
        {title}
      </p>

      <p className="mt-2 text-2xl font-bold">
        {value}
      </p>

      <p className="mt-1 text-xs text-slate-400">
        {subtitle}
      </p>

    </div>
  );
}


function ProjectCard({
  project,
}: {
  project: {
    name: string;
    sector: string;
    location: string;
    budget: string;
    beneficiaries: string;
    need: number;
    impact: number;
    efficiency: number;
    status: string;
  };
}) {
  return (
    <div className="rounded-2xl border border-slate-200 p-5 transition hover:border-slate-300 hover:shadow-sm">

      <div className="flex flex-col justify-between gap-4 md:flex-row">

        <div>

          <div className="flex flex-wrap items-center gap-2">

            <h4 className="font-bold">
              {project.name}
            </h4>

            <span
              className={`rounded-full px-2.5 py-1 text-xs font-medium ${
                project.status === "Recommended"
                  ? "bg-slate-100 text-slate-700"
                  : "bg-amber-50 text-amber-700"
              }`}
            >
              {project.status}
            </span>

          </div>

          <p className="mt-1 text-sm text-slate-500">
            {project.sector} · {project.location}
          </p>

        </div>

        <div className="text-left md:text-right">

          <p className="font-bold">
            {project.budget}
          </p>

          <p className="text-xs text-slate-500">
            {project.beneficiaries} beneficiaries
          </p>

        </div>

      </div>

      <div className="mt-5 grid gap-4 sm:grid-cols-3">

        <Score label="Community Need" value={project.need} />

        <Score label="Expected Impact" value={project.impact} />

        <Score label="Cost Efficiency" value={project.efficiency} />

      </div>

    </div>
  );
}


function Score({
  label,
  value,
}: {
  label: string;
  value: number;
}) {
  return (
    <div>

      <div className="mb-1 flex justify-between text-xs">

        <span className="text-slate-500">
          {label}
        </span>

        <span className="font-semibold">
          {value}
        </span>

      </div>

      <div className="h-2 overflow-hidden rounded-full bg-slate-100">

        <div
          className="h-full rounded-full bg-slate-900"
          style={{ width: `${value}%` }}
        />

      </div>

    </div>
  );
}


function SummaryRow({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="flex items-center justify-between border-b border-slate-100 pb-3">

      <span className="text-sm text-slate-500">
        {label}
      </span>

      <span className="text-sm font-bold">
        {value}
      </span>

    </div>
  );
}