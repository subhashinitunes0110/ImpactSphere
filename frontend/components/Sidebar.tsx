"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Sidebar() {
  const pathname = usePathname();

  const navItems = [
    { name: "Dashboard", href: "/" },
    { name: "Proposals", href: "/proposals" },
    { name: "What-If", href: "/what-if" },
    { name: "Impact Map", href: "/map" },
    { name: "Reports", href: "/reports" },
  ];

  return (
    <aside className="w-64 min-h-screen border-r border-slate-200 bg-white p-6 flex flex-col justify-between shrink-0">
      <div className="space-y-8">
        {/* Brand Header */}
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-slate-900 text-white font-bold text-lg">
            I
          </div>
          <div>
            <h2 className="font-bold text-slate-900 leading-tight">ImpactSphere</h2>
            <p className="text-xs text-slate-400">CSR Intelligence</p>
          </div>
        </div>

        {/* Navigation Links */}
        <nav className="space-y-1">
          {navItems.map((item) => {
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`block w-full rounded-xl px-4 py-3 text-left text-sm font-medium transition ${
                  isActive
                    ? "bg-slate-900 text-white font-semibold shadow-sm"
                    : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                }`}
              >
                {item.name}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* CSR Cycle Badge */}
      <div className="rounded-2xl bg-slate-50 p-4 border border-slate-100">
        <p className="text-xs font-medium text-slate-500">Current CSR Cycle</p>
        <p className="mt-1 text-sm font-semibold text-slate-900">FY 2026–27</p>
        <div className="mt-3 h-2 overflow-hidden rounded-full bg-slate-200">
          <div className="h-full w-[68%] rounded-full bg-slate-900" />
        </div>
        <p className="mt-2 text-xs text-slate-500">Planning in progress</p>
      </div>
    </aside>
  );
}