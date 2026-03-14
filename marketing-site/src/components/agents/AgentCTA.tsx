"use client";

import { motion } from "framer-motion";

export function AgentCTA() {
  return (
    <section className="bg-spearmint-dark py-20 md:py-28">
      <div className="mx-auto max-w-6xl px-6 text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
        >
          <h2 className="text-3xl font-bold tracking-tight text-white md:text-4xl">
            Stop checking. Start knowing.
          </h2>
          <p className="mx-auto mt-4 max-w-xl text-lg text-white/80">
            Let autonomous agents watch your finances so you don&apos;t have to.
            Deploy Spearmint and get a team of financial specialists working for
            you &mdash; 24/7, on your own hardware.
          </p>
          <div className="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
            <a
              href="https://github.com/spearmint-finance/spearmint"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center rounded-full bg-white px-8 py-3 text-base font-semibold text-spearmint-dark transition-colors hover:bg-mint-bg"
            >
              Get Started on GitHub
            </a>
            <a
              href="/features"
              className="inline-flex items-center justify-center rounded-full border border-white/30 px-8 py-3 text-base font-semibold text-white transition-colors hover:bg-white/10"
            >
              See All Features
            </a>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
