"use client";

import { motion } from "framer-motion";
import { AgentOrchestrationGraphic } from "./AgentOrchestrationGraphic";

export function AgentHero() {
  return (
    <section className="relative overflow-hidden bg-mint-bg">
      <div className="mx-auto max-w-6xl px-6 py-24 md:py-32">
        <div className="items-center gap-12 md:flex">
          <div className="max-w-xl md:flex-1">
            <motion.p
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4 }}
              className="text-sm font-semibold uppercase tracking-wide text-spearmint-dark"
            >
              Autonomous Agents
            </motion.p>

            <motion.h1
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.1 }}
              className="mt-4 text-4xl font-bold leading-tight tracking-tight text-gray-900 md:text-5xl lg:text-6xl"
            >
              AI that watches
              <br />
              <span className="text-spearmint">your finances for you</span>
            </motion.h1>

            <motion.p
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="mt-6 max-w-lg text-lg leading-relaxed text-gray-600"
            >
              Spearmint&apos;s specialized agents continuously monitor your
              spending, surface savings opportunities, and deliver personalized
              advice &mdash; proactively, not just when you ask.
            </motion.p>
          </div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="mt-12 md:mt-0 md:flex-1"
          >
            <AgentOrchestrationGraphic />
          </motion.div>
        </div>
      </div>

      <div
        aria-hidden="true"
        className="pointer-events-none absolute -right-32 -top-32 h-96 w-96 rounded-full bg-teal/10 blur-3xl"
      />
    </section>
  );
}
