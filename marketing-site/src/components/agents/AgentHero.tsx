import { AgentOrchestrationGraphic } from "./AgentOrchestrationGraphic";

export function AgentHero() {
  return (
    <section className="relative overflow-hidden bg-mint-bg">
      <div className="mx-auto max-w-6xl px-6 py-24 md:py-32">
        <div className="items-center gap-12 md:flex">
          <div className="max-w-xl md:flex-1">
            <p className="text-sm font-semibold uppercase tracking-wide text-spearmint-dark">
              Autonomous Agents
            </p>

            <h1 className="mt-4 text-4xl font-bold leading-tight tracking-tight text-gray-900 md:text-5xl lg:text-6xl">
              AI that watches
              <br />
              <span className="text-spearmint">your finances for you</span>
            </h1>

            <p className="mt-6 max-w-lg text-lg leading-relaxed text-gray-600">
              Spearmint&apos;s specialized agents continuously monitor your
              spending, surface savings opportunities, and deliver personalized
              advice &mdash; proactively, not just when you ask.
            </p>
          </div>

          <div className="mt-12 md:mt-0 md:flex-1">
            <AgentOrchestrationGraphic />
          </div>
        </div>
      </div>

      <div
        aria-hidden="true"
        className="pointer-events-none absolute -right-32 -top-32 h-96 w-96 rounded-full bg-teal/10 blur-3xl"
      />
    </section>
  );
}
