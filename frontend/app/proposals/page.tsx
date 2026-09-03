

const proposals = [
  {
    id: 1,
    name: "Rural Healthcare Initiative",
    sector: "Healthcare",
    location: "District X",
    budget: "₹50 L",
    beneficiaries: "12,000",
    need: 91,
    impact: 88,
    efficiency: 82,
    compliance: "Eligible",
    recommendation: "Recommended",
  },
  {
    id: 2,
    name: "Digital Education Access",
    sector: "Education",
    location: "District C",
    budget: "₹35 L",
    beneficiaries: "8,500",
    need: 87,
    impact: 85,
    efficiency: 79,
    compliance: "Eligible",
    recommendation: "Recommended",
  },
  {
    id: 3,
    name: "Clean Water Initiative",
    sector: "Water & Sanitation",
    location: "District A",
    budget: "₹42 L",
    beneficiaries: "7,200",
    need: 94,
    impact: 91,
    efficiency: 86,
    compliance: "Eligible",
    recommendation: "Recommended",
  },
  {
    id: 4,
    name: "Women Skill Development",
    sector: "Livelihood",
    location: "District D",
    budget: "₹28 L",
    beneficiaries: "4,300",
    need: 82,
    impact: 79,
    efficiency: 88,
    compliance: "Eligible",
    recommendation: "Review",
  },
  {
    id: 5,
    name: "Urban Green Spaces",
    sector: "Environment",
    location: "District B",
    budget: "₹22 L",
    beneficiaries: "3,100",
    need: 64,
    impact: 70,
    efficiency: 74,
    compliance: "Eligible",
    recommendation: "Review",
  },
];

export default function ProposalsPage() {
  const [filter, setFilter] = useState("All");

  const filteredProposals =
    filter === "All"
      ? proposals
      : proposals.filter((proposal) => proposal.compliance === filter);

  return (
    <main className="min-h-screen bg-[#f7f8fa] text-slate-900">

      {/* HEADER */}
      <header className="border-b border-slate-200 bg-white px-6 py-5 lg:px-10">
        <div className="flex flex-col justify-between gap-4 md:flex-row md:items-center">

          <div>
            <p className="text-sm text-slate-500">
              CSR Planning / FY 2026–27
            </p>

            <h1 className="mt-1 text-2xl font-bold tracking-tight">
              CSR Proposals
            </h1>

            <p className="mt-1 text-sm text-slate-500">
              Review and compare submitted CSR project proposals.
            </p>
          </div>

          <button className="rounded-xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white hover:bg-slate-800">
            + Upload Proposal
          </button>

        </div>
      </header>

      <div className="px-6 py-8 lg:px-10">

        {/* SUMMARY CARDS */}
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">

          <StatCard
            label="Total Proposals"
            value="20"
            description="Received this cycle"
          />

          <StatCard
            label="Eligible"
            value="17"
            description="Passed compliance"
          />

          <StatCard
            label="Recommended"
            value="7"
            description="High expected impact"
          />

          <StatCard
            label="Needs Review"
            value="3"
            description="Requires attention"
          />

        </div>

        {/* FILTERS */}
        <div className="mt-8 flex flex-wrap gap-2">

          {["All", "Eligible", "Review"].map((item) => (
            <button
              key={item}
              onClick={() => setFilter(item)}
              className={`rounded-xl px-4 py-2 text-sm font-medium ${
                filter === item
                  ? "bg-slate-900 text-white"
                  : "border border-slate-200 bg-white text-slate-600 hover:bg-slate-50"
              }`}
            >
              {item}
            </button>
          ))}

        </div>

        {/* PROPOSAL TABLE */}
        <div className="mt-5 overflow-hidden rounded-3xl border border-slate-200 bg-white">

          <div className="overflow-x-auto">

            <table className="w-full min-w-[1000px] text-left">

              <thead className="border-b border-slate-200 bg-slate-50">

                <tr>
                  <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Proposal
                  </th>

                  <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Budget
                  </th>

                  <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Beneficiaries
                  </th>

                  <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Need
                  </th>

                  <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Impact
                  </th>

                  <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Efficiency
                  </th>

                  <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Compliance
                  </th>

                  <th className="px-6 py-4 text-xs font-semibold uppercase tracking-wide text-slate-500">
                    Decision
                  </th>
                </tr>

              </thead>

              <tbody className="divide-y divide-slate-100">

                {filteredProposals.map((proposal) => (

                  <tr
                    key={proposal.id}
                    className="transition hover:bg-slate-50"
                  >

                    <td className="px-6 py-5">

                      <p className="font-semibold">
                        {proposal.name}
                      </p>

                      <p className="mt-1 text-xs text-slate-500">
                        {proposal.sector} · {proposal.location}
                      </p>

                    </td>

                    <td className="px-6 py-5 font-semibold">
                      {proposal.budget}
                    </td>

                    <td className="px-6 py-5 text-sm">
                      {proposal.beneficiaries}
                    </td>

                    <td className="px-6 py-5">
                      <Score value={proposal.need} />
                    </td>

                    <td className="px-6 py-5">
                      <Score value={proposal.impact} />
                    </td>

                    <td className="px-6 py-5">
                      <Score value={proposal.efficiency} />
                    </td>

                    <td className="px-6 py-5">

                      <span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-semibold text-slate-700">
                        {proposal.compliance}
                      </span>

                    </td>

                    <td className="px-6 py-5">

                      <span
                        className={`rounded-full px-3 py-1 text-xs font-semibold ${
                          proposal.recommendation === "Recommended"
                            ? "bg-slate-900 text-white"
                            : "bg-amber-50 text-amber-700"
                        }`}
                      >
                        {proposal.recommendation}
                      </span>

                    </td>

                  </tr>

                ))}

              </tbody>

            </table>

          </div>

        </div>

      </div>

    </main>
  );
}


/* ---------------- COMPONENTS ---------------- */

function StatCard({
  label,
  value,
  description,
}: {
  label: string;
  value: string;
  description: string;
}) {
  return (
    <div className="rounded-2xl border border-slate-200 bg-white p-5">

      <p className="text-xs font-medium text-slate-500">
        {label}
      </p>

      <p className="mt-2 text-2xl font-bold">
        {value}
      </p>

      <p className="mt-1 text-xs text-slate-400">
        {description}
      </p>

    </div>
  );
}


function Score({
  value,
}: {
  value: number;
}) {
  return (
    <div className="flex items-center gap-3">

      <span className="w-7 text-sm font-semibold">
        {value}
      </span>

      <div className="h-2 w-20 overflow-hidden rounded-full bg-slate-100">

        <div
          className="h-full rounded-full bg-slate-900"
          style={{ width: `${value}%` }}
        />

      </div>

    </div>
  );
}