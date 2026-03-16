import { GITHUB_URL } from "../config";

export function Hero() {
  return (
    <section className="relative overflow-hidden bg-mint-bg">
      <div className="mx-auto max-w-6xl px-6 py-24 md:py-32">
        <div className="max-w-2xl">
          <p className="text-sm font-semibold uppercase tracking-wide text-spearmint-dark">
            Free &amp; Open-Source
          </p>

          <h1 className="mt-4 text-4xl font-bold leading-tight tracking-tight text-gray-900 md:text-5xl lg:text-6xl">
            Business-Grade
            <br />
            <span className="text-spearmint">Personal Finance</span>
          </h1>

          <p className="mt-6 max-w-lg text-lg leading-relaxed text-gray-600">
            Your personal CFO. A self-hosted financial engine that transforms
            bank data into professional-grade accounting intelligence &mdash; at
            zero cost.
          </p>

          <div className="mt-8 flex flex-col gap-4 sm:flex-row">
            <a
              href={GITHUB_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center rounded-full bg-spearmint px-8 py-3 text-base font-semibold text-white transition-colors hover:bg-spearmint-dark"
            >
              Get Started &mdash; It&apos;s Free
            </a>
            <a
              href="/how-it-works"
              className="inline-flex items-center justify-center rounded-full border border-gray-300 bg-white px-8 py-3 text-base font-semibold text-gray-700 transition-colors hover:border-spearmint hover:text-spearmint-dark"
            >
              See How It Works
            </a>
          </div>
        </div>
      </div>

      {/* Decorative gradient blob */}
      <div
        aria-hidden="true"
        className="pointer-events-none absolute -right-32 -top-32 h-96 w-96 rounded-full bg-spearmint/10 blur-3xl"
      />
    </section>
  );
}
