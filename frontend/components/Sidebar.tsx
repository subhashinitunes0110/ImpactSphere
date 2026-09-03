import Link from "next/link";

export default function Sidebar() {
  return (
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

        <Link
          href="/"
          className="block w-full rounded-xl px-4 py-3 text-left text-sm font-medium text-slate-600 transition hover:bg-slate-100"
        >
          Dashboard
        </Link>

        <Link
          href="/proposals"
          className="block w-full rounded-xl px-4 py-3 text-left text-sm font-medium text-slate-600 transition hover:bg-slate-100"
        >
          Proposals
        </Link>

        <Link
          href="/what-if"
          className="block w-full rounded-xl px-4 py-3 text-left text-sm font-medium text-slate-600 transition hover:bg-slate-100"
        >
          What-If
        </Link>

        <Link
          href="/map"
          className="block w-full rounded-xl px-4 py-3 text-left text-sm font-medium text-slate-600 transition hover:bg-slate-100"
        >
          Impact Map
        </Link>

        <Link
          href="/reports"
          className="block w-full rounded-xl px-4 py-3 text-left text-sm font-medium text-slate-600 transition hover:bg-slate-100"
        >
          Reports
        </Link>

      </nav>

      {/* Current CSR Cycle */}
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
  );
}