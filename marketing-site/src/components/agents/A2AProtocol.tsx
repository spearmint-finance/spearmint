"use client";

import { motion } from "framer-motion";

const capabilities = [
  {
    label: "Proactive",
    description:
      "Agents initiate conversations. The Budget Advisor doesn't wait for you to ask — it pushes alerts when spending spikes.",
  },
  {
    label: "Specialized",
    description:
      "Each agent focuses on one domain. The Subscription Auditor only audits subscriptions. The Tax Optimizer only optimizes taxes.",
  },
  {
    label: "Orchestrating",
    description:
      "The Budget Advisor delegates to sub-agents (Subscription Auditor, Bill Negotiator, Tax Optimizer) and merges their findings into unified advice.",
  },
  {
    label: "Stateful",
    description:
      "Agents remember past interactions and track goals across months. They follow up on previous recommendations and adjust as your habits change.",
  },
  {
    label: "Negotiating",
    description:
      'When data is insufficient, agents don\'t guess — they explain trade-offs: "I have 2 months of data. Proceed with lower confidence, or wait for more?"',
  },
  {
    label: "Extensible",
    description:
      "Third parties can build and deploy their own agents via the A2A protocol. Connect an independent financial advisor to your Spearmint instance.",
  },
];

export function A2AProtocol() {
  return (
    <section className="bg-gray-50 py-20 md:py-28">
      <div className="mx-auto max-w-6xl px-6">
        <div className="max-w-2xl">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 md:text-4xl">
            Agent-to-Agent protocol
          </h2>
          <p className="mt-4 text-lg text-gray-500">
            Spearmint agents communicate through a standard A2A protocol. They
            discover each other, delegate tasks, and coordinate results &mdash;
            creating a multi-agent financial advisory team that works together.
          </p>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-60px" }}
          transition={{ duration: 0.5 }}
          className="mt-14"
        >
          {/* Flow diagram */}
          <div className="mb-12 overflow-x-auto">
            <div className="flex min-w-[600px] items-center justify-between gap-2 rounded-xl border border-gray-200 bg-white p-6">
              {[
                { label: "You ask Minty", sub: '"How can I save money?"' },
                { label: "Minty delegates", sub: "→ Budget Advisor" },
                { label: "Advisor orchestrates", sub: "→ Sub-agents" },
                { label: "Results synthesized", sub: "Unified advice" },
                { label: "You get answers", sub: "Prioritized & actionable" },
              ].map((step, i) => (
                <div key={i} className="flex items-center gap-2">
                  <div className="text-center">
                    <div className="flex h-10 w-10 mx-auto items-center justify-center rounded-full bg-spearmint text-sm font-bold text-white">
                      {i + 1}
                    </div>
                    <p className="mt-2 text-xs font-semibold text-gray-900">
                      {step.label}
                    </p>
                    <p className="mt-0.5 text-xs text-gray-500">{step.sub}</p>
                  </div>
                  {i < 4 && (
                    <svg
                      className="h-4 w-4 shrink-0 text-gray-300"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                      strokeWidth={2}
                      aria-hidden="true"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3"
                      />
                    </svg>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Capability grid */}
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {capabilities.map((cap, i) => (
              <motion.div
                key={cap.label}
                initial={{ opacity: 0, y: 16 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.35, delay: i * 0.06 }}
                className="rounded-xl border border-gray-200 bg-white p-5"
              >
                <p className="font-semibold text-gray-900">{cap.label}</p>
                <p className="mt-2 text-sm leading-relaxed text-gray-500">
                  {cap.description}
                </p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
}
