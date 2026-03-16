import { HybridDiagram } from "./HybridDiagram";

const layers = [
  {
    label: "Deterministic Layer",
    tagline: "Fast, trustworthy, explainable",
    description:
      "Handles structured financial math — category statistics, trend analysis, variance detection, duplicate identification. Results are precise and auditable.",
    example: "Dining trending up 12.5%, from $380 to $460/month over 3 months",
    color: "border-l-spearmint",
    bg: "bg-mint-bg",
  },
  {
    label: "LLM Reasoning Layer",
    tagline: "Contextual, personalized, adaptive",
    description:
      "Interprets the signals from the deterministic layer and generates advice tailored to your specific situation. Filters noise, prioritizes what matters, and explains in plain English.",
    example:
      "You started ordering delivery after moving to a new neighborhood — consider meal prepping on Sundays for ~$80/month in savings",
    color: "border-l-teal",
    bg: "bg-teal-light/10",
  },
];

export function HybridArchitecture() {
  return (
    <section className="bg-white py-20 md:py-28">
      <div className="mx-auto max-w-6xl px-6">
        <div className="max-w-2xl">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 md:text-4xl">
            Hybrid architecture: math you can trust, advice you can use
          </h2>
          <p className="mt-4 text-lg text-gray-500">
            Most AI finance tools are a black box. Spearmint agents combine
            deterministic calculations with LLM reasoning &mdash; so you get
            both precision and personalization.
          </p>
        </div>

        <div className="mt-14 mb-14">
          <HybridDiagram />
        </div>

        <div className="mt-14 space-y-6">
          {layers.map((layer) => (
            <div
              key={layer.label}
              className={`rounded-xl border-l-4 ${layer.color} ${layer.bg} p-6 md:p-8`}
            >
              <div className="md:flex md:items-start md:gap-8">
                <div className="md:flex-1">
                  <h3 className="text-lg font-semibold text-gray-900">
                    {layer.label}
                  </h3>
                  <p className="mt-1 text-sm font-medium text-gray-600">
                    {layer.tagline}
                  </p>
                  <p className="mt-3 text-gray-600">{layer.description}</p>
                </div>
                <div className="mt-4 md:mt-0 md:w-80 md:shrink-0">
                  <div className="rounded-lg bg-white/80 p-4">
                    <p className="text-xs font-medium uppercase tracking-wide text-gray-500">
                      Output
                    </p>
                    <p className="mt-2 text-sm text-gray-700">
                      {layer.example}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-10 rounded-xl border border-gray-200 bg-gray-50 p-6 md:p-8">
          <h3 className="text-lg font-semibold text-gray-900">
            Why does this matter?
          </h3>
          <ul className="mt-4 space-y-3 text-sm text-gray-600">
            <li className="flex gap-3">
              <span className="font-semibold text-spearmint-dark">
                Transparency:
              </span>
              Every recommendation shows the data behind it. No &ldquo;trust me&rdquo;
              black-box answers.
            </li>
            <li className="flex gap-3">
              <span className="font-semibold text-spearmint-dark">
                Accuracy:
              </span>
              Financial math is deterministic &mdash; no hallucinated numbers.
              The LLM only interprets, never calculates.
            </li>
            <li className="flex gap-3">
              <span className="font-semibold text-spearmint-dark">
                Honesty:
              </span>
              When data is insufficient, agents tell you instead of guessing.
              They propose alternatives and explain confidence levels.
            </li>
          </ul>
        </div>
      </div>
    </section>
  );
}
