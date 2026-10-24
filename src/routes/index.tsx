import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";

export const Route = createFileRoute("/")({
  head: () => ({
    meta: [
      { title: "AQLYNTOR Dashboard — Trustworthy AI Execution" },
      { name: "description", content: "Live pipeline, verified execution logs and safety policies for AQLYNTOR." },
      { property: "og:title", content: "AQLYNTOR Dashboard — Trustworthy AI Execution" },
      { property: "og:description", content: "Live pipeline, verified execution logs and safety policies for AQLYNTOR." },
    ],
  }),
  component: Dashboard,
});

type Tone = "success" | "warning" | "info" | "destructive";
const toneCls: Record<Tone, string> = {
  success: "text-success bg-success/10 border-success/30",
  warning: "text-warning bg-warning/10 border-warning/30",
  info: "text-info bg-info/10 border-info/30",
  destructive: "text-destructive bg-destructive/10 border-destructive/30",
};

const stats: { label: string; value: string; tone: Tone }[] = [
  { label: "Verified Success Rate", value: "88%", tone: "success" },
  { label: "Active Tasks", value: "2", tone: "info" },
  { label: "Bounded Recoveries", value: "4", tone: "warning" },
  { label: "Policy Violations Blocked", value: "0", tone: "success" },
];

const steps = [
  { name: "User Goal", desc: "Intent received and parsed into an objective with explicit success criteria." },
  { name: "Planner", desc: "Decomposes the goal into bounded, typed actions with postconditions." },
  { name: "Policy Gate", desc: "Every action checked against sandbox scope and approval rules." },
  { name: "Tool Adapter", desc: "Executes the action through a least-privilege tool interface." },
  { name: "Outcome Verifier", desc: "Compares observed state against declared postconditions." },
  { name: "Bounded Recovery", desc: "On failure, retries within a strict budget — or stops safely." },
  { name: "Audit Log", desc: "Immutable record of actions, evidence and verdicts." },
];

const logs: { id: string; goal: string; ts: string; status: "VERIFIED" | "RECOVERING" | "STOPPED"; evidence: string }[] = [
  { id: "TSK-0412", goal: "Inspect workspace and confirm summary.md exists", ts: "2026-10-24 09:12:41", status: "VERIFIED", evidence: "summary.md verified · 2.4 KB · sha256:9f3a…c21e" },
  { id: "TSK-0411", goal: "Refresh dependency report for api-service", ts: "2026-10-24 09:10:03", status: "RECOVERING", evidence: "attempt 2/3 · timeout on registry fetch" },
  { id: "TSK-0410", goal: "Delete stale build artifacts in /dist", ts: "2026-10-24 09:04:17", status: "STOPPED", evidence: "awaiting human approval · destructive op" },
  { id: "TSK-0409", goal: "Generate changelog from last 20 commits", ts: "2026-10-24 08:58:52", status: "VERIFIED", evidence: "CHANGELOG.md · 20 entries matched" },
];
const statusTone = { VERIFIED: "success", RECOVERING: "warning", STOPPED: "destructive" } as const;

function Tag({ tone, children }: { tone: Tone; children: React.ReactNode }) {
  return <span className={`inline-flex items-center gap-1.5 rounded-full border px-2.5 py-0.5 font-mono text-[11px] tracking-wider ${toneCls[tone]}`}><span className="size-1.5 rounded-full bg-current" />{children}</span>;
}

function Dashboard() {
  const [active, setActive] = useState(0);
  const [auto, setAuto] = useState(true);
  const [rules, setRules] = useState({ sandbox: true, postcondition: true, approval: true });

  useEffect(() => {
    if (!auto) return;
    const t = setInterval(() => setActive((a) => (a + 1) % steps.length), 1600);
    return () => clearInterval(t);
  }, [auto]);

  return (
    <div className="mx-auto max-w-7xl space-y-6 px-4 py-8 md:px-8">
      <header className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold tracking-[0.2em]">AQLYNTOR</h1>
          <p className="text-sm text-muted-foreground">Trustworthy AI Execution</p>
        </div>
        <Tag tone="success">SYSTEM NOMINAL</Tag>
      </header>

      <section className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        {stats.map((s) => (
          <div key={s.label} className="glass p-5">
            <p className="text-xs uppercase tracking-wider text-muted-foreground">{s.label}</p>
            <p className={`mt-2 font-mono text-4xl font-medium ${toneCls[s.tone].split(" ")[0]}`}>{s.value}</p>
          </div>
        ))}
      </section>

      <section className="glass p-6">
        <div className="mb-5 flex items-center justify-between">
          <h2 className="font-semibold">Live Task Execution Pipeline</h2>
          <button onClick={() => setAuto(!auto)} className="rounded-md border px-3 py-1 font-mono text-xs text-muted-foreground hover:text-foreground">{auto ? "❚❚ PAUSE" : "▶ RUN"}</button>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          {steps.map((s, i) => (
            <div key={s.name} className="flex items-center gap-2">
              <button
                onClick={() => { setAuto(false); setActive(i); }}
                className={`rounded-lg border px-4 py-3 text-sm transition-all ${i === active ? "border-primary bg-primary/15 text-primary shadow-[0_0_24px_-4px_var(--primary)]" : i < active ? "border-success/30 text-success" : "text-muted-foreground hover:text-foreground"}`}
              >
                <span className="mr-2 font-mono text-[10px] opacity-70">0{i + 1}</span>{s.name}
              </button>
              {i < steps.length - 1 && <span className={`font-mono ${i < active ? "text-success" : "text-muted-foreground/40"}`}>→</span>}
            </div>
          ))}
        </div>
        <div className="mt-5 rounded-lg border bg-background/40 p-4 font-mono text-sm">
          <span className="text-primary">[{steps[active].name}]</span> <span className="text-muted-foreground">{steps[active].desc}</span>
        </div>
      </section>

      <div className="grid gap-6 lg:grid-cols-3">
        <section className="glass overflow-hidden lg:col-span-2">
          <h2 className="p-6 pb-3 font-semibold">Execution Log</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="text-left text-xs uppercase tracking-wider text-muted-foreground">
                <tr className="border-b">{["Task ID", "Goal", "Timestamp", "Status", "Evidence"].map((h) => <th key={h} className="px-6 py-3 font-medium">{h}</th>)}</tr>
              </thead>
              <tbody>
                {logs.map((l) => (
                  <tr key={l.id} className="border-b last:border-0 hover:bg-accent/30">
                    <td className="px-6 py-4 font-mono text-primary">{l.id}</td>
                    <td className="px-6 py-4">{l.goal}</td>
                    <td className="whitespace-nowrap px-6 py-4 font-mono text-xs text-muted-foreground">{l.ts}</td>
                    <td className="px-6 py-4"><Tag tone={statusTone[l.status]}>{l.status}</Tag></td>
                    <td className="px-6 py-4 font-mono text-xs text-muted-foreground">{l.evidence}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </section>

        <section className="glass space-y-4 p-6">
          <h2 className="font-semibold">Safety & Policy Rules</h2>
          {([
            ["sandbox", "Least Privilege Sandbox", "Tools only access scoped paths."],
            ["postcondition", "Strict Postcondition Check", "Every step must prove its outcome."],
            ["approval", "Human Approval for Destructive Actions", "Deletes and writes pause for review."],
          ] as const).map(([k, label, desc]) => (
            <div key={k} className="flex items-start justify-between gap-4 rounded-lg border bg-background/30 p-4">
              <div>
                <p className="text-sm font-medium">{label}</p>
                <p className="mt-1 text-xs text-muted-foreground">{desc}</p>
              </div>
              <button
                role="switch"
                aria-checked={rules[k]}
                aria-label={label}
                onClick={() => setRules({ ...rules, [k]: !rules[k] })}
                className={`relative h-6 w-11 shrink-0 rounded-full border transition-colors ${rules[k] ? "border-success/50 bg-success/30" : "bg-muted"}`}
              >
                <span className={`absolute top-0.5 size-4.5 rounded-full transition-all ${rules[k] ? "left-5.5 bg-success" : "left-0.5 bg-muted-foreground"}`} />
              </button>
            </div>
          ))}
        </section>
      </div>
    </div>
  );
}
