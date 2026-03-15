import type { Metadata } from "next";
import { CTA } from "@/components/CTA";
import { BreadcrumbJsonLd } from "@/components/JsonLd";

export const metadata: Metadata = {
  title: "How It Works",
  description:
    "Import your bank data, let Spearmint classify and analyze it, and get professional-grade financial insights — all self-hosted.",
  alternates: { canonical: "/how-it-works" },
  openGraph: {
    title: "How It Works — Spearmint",
    description:
      "Import your bank data, let Spearmint classify and analyze it, and get professional-grade financial insights — all self-hosted.",
    url: "/how-it-works",
  },
};

const steps = [
  {
    number: "01",
    title: "Export your bank data",
    description:
      "Download CSV or Excel files from your bank, credit card, or brokerage. Spearmint works with any standard export format.",
  },
  {
    number: "02",
    title: "Import & classify",
    description:
      "Drag and drop into Spearmint. Smart format detection maps columns automatically. Transactions are classified into operating expenses, capital investments, transfers, and receivables.",
  },
  {
    number: "03",
    title: "Analyze & forecast",
    description:
      "See your true burn rate, cash flow patterns, and statistical forecasts with confidence intervals. Run scenario planning for life changes.",
  },
  {
    number: "04",
    title: "Stay in control",
    description:
      "Everything runs on your hardware. No cloud dependency, no subscriptions, no data sharing. Update at your own pace.",
  },
];

export default function HowItWorksPage() {
  return (
    <>
      <BreadcrumbJsonLd
        items={[{ name: "How It Works", path: "/how-it-works" }]}
      />
      <section className="bg-mint-bg py-16 md:py-20">
        <div className="mx-auto max-w-6xl px-6">
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 md:text-5xl">
            How It Works
          </h1>
          <p className="mt-4 max-w-2xl text-lg text-gray-600">
            From bank export to financial intelligence in four steps.
          </p>
        </div>
      </section>

      <section className="bg-white py-20">
        <div className="mx-auto max-w-3xl px-6">
          <div className="space-y-16">
            {steps.map((step) => (
              <div key={step.number} className="flex gap-6">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-spearmint text-lg font-bold text-white">
                  {step.number}
                </div>
                <div>
                  <h2 className="text-xl font-semibold text-gray-900">
                    {step.title}
                  </h2>
                  <p className="mt-2 text-gray-600">{step.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <CTA />
    </>
  );
}
