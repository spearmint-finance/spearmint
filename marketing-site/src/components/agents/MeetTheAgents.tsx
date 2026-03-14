"use client";

import { motion } from "framer-motion";

const agents = [
  {
    name: "Minty",
    subtitle: "AI Financial Assistant",
    description:
      "Your conversational interface to Spearmint. Ask questions in plain English, delegate routine bookkeeping, and get instant insights without navigating a single page.",
    capabilities: [
      "Natural-language financial queries",
      "Automated transaction categorization",
      "Routine bookkeeping delegation",
      "Household-friendly — anyone can use it",
    ],
    example: '"How much did I spend on dining out last quarter?"',
    color: "bg-spearmint/10 text-spearmint-dark",
    borderColor: "border-spearmint/20",
  },
  {
    name: "Budget Advisor",
    subtitle: "Autonomous Spending Analyst",
    description:
      "Continuously monitors your spending patterns and proactively surfaces personalized savings opportunities. Doesn't wait for you to ask — it tells you when something needs attention.",
    capabilities: [
      "Proactive spending anomaly alerts",
      "Personalized budget generation",
      "Prioritized savings recommendations",
      "Month-over-month trend tracking",
    ],
    example:
      '"Your dining spending is up 40% this week. You started ordering delivery after your move — meal prepping could save ~$80/month."',
    color: "bg-teal/10 text-teal",
    borderColor: "border-teal/20",
  },
  {
    name: "Subscription Auditor",
    subtitle: "Recurring Cost Detective",
    description:
      "Scans your transactions for duplicate, unused, or overlapping subscriptions. Finds the charges you forgot about.",
    capabilities: [
      "Duplicate subscription detection",
      "Unused service identification",
      "Overlap analysis across similar services",
      "Annual cost projection per subscription",
    ],
    example:
      '"You\'re paying for both Spotify Premium and YouTube Music — $11.99/month overlap."',
    color: "bg-amber-500/10 text-amber-600",
    borderColor: "border-amber-500/20",
  },
  {
    name: "Bill Negotiator",
    subtitle: "Cost Reduction Advisor",
    description:
      "Identifies recurring bills where switching providers or renegotiating could save money. Compares your rates against market benchmarks.",
    capabilities: [
      "Provider switching recommendations",
      "Rate comparison analysis",
      "Seasonal deal timing",
      "Estimated savings per action",
    ],
    example:
      '"Your internet bill is $89/month — comparable plans in your area start at $55. Estimated annual savings: $408."',
    color: "bg-blue-500/10 text-blue-600",
    borderColor: "border-blue-500/20",
  },
  {
    name: "Tax Optimizer",
    subtitle: "Deduction & Classification Agent",
    description:
      "Scans for missed deductions and suggests tax-efficient categorization. Especially useful for freelancers and side-income earners.",
    capabilities: [
      "Missed deduction detection",
      "Tax-efficient categorization suggestions",
      "Quarterly estimated tax reminders",
      "Home office & mileage tracking prompts",
    ],
    example:
      '"You have $2,400 in uncategorized home office expenses that may be deductible."',
    color: "bg-purple-500/10 text-purple-600",
    borderColor: "border-purple-500/20",
  },
];

const container = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.1 } },
};

const item = {
  hidden: { opacity: 0, y: 24 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.45 } },
};

export function MeetTheAgents() {
  return (
    <section className="bg-gray-50 py-20 md:py-28">
      <div className="mx-auto max-w-6xl px-6">
        <div className="text-center">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 md:text-4xl">
            Meet the agents
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-lg text-gray-500">
            Each agent is a specialist. They work independently, coordinate with
            each other, and report back to you with clear, actionable advice.
          </p>
        </div>

        <motion.div
          variants={container}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, margin: "-80px" }}
          className="mt-14 space-y-6"
        >
          {agents.map((agent) => (
            <motion.div
              key={agent.name}
              variants={item}
              className={`rounded-xl border ${agent.borderColor} bg-white p-6 md:p-8`}
            >
              <div className="md:flex md:items-start md:gap-8">
                <div className="md:flex-1">
                  <div className="flex items-center gap-3">
                    <span
                      className={`inline-flex rounded-lg px-3 py-1 text-xs font-semibold ${agent.color}`}
                    >
                      {agent.name}
                    </span>
                    <span className="text-sm text-gray-400">
                      {agent.subtitle}
                    </span>
                  </div>

                  <p className="mt-3 text-gray-600">{agent.description}</p>

                  <ul className="mt-4 grid gap-2 sm:grid-cols-2">
                    {agent.capabilities.map((cap) => (
                      <li
                        key={cap}
                        className="flex items-start gap-2 text-sm text-gray-500"
                      >
                        <svg
                          className="mt-0.5 h-4 w-4 shrink-0 text-spearmint"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                          strokeWidth={2}
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            d="M4.5 12.75l6 6 9-13.5"
                          />
                        </svg>
                        {cap}
                      </li>
                    ))}
                  </ul>
                </div>

                <div className="mt-4 md:mt-0 md:w-80 md:shrink-0">
                  <div className="rounded-lg bg-gray-50 p-4">
                    <p className="text-xs font-medium uppercase tracking-wide text-gray-400">
                      Example
                    </p>
                    <p className="mt-2 text-sm italic text-gray-600">
                      {agent.example}
                    </p>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </section>
  );
}
