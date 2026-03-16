import type { Metadata } from "next";
import { BreadcrumbJsonLd } from "@/components/JsonLd";
import { GITHUB_URL } from "../../config";

export const metadata: Metadata = {
  title: "Pricing",
  description:
    "Spearmint is free and open-source. No subscriptions, no hidden costs, no data monetization.",
  alternates: { canonical: "/pricing" },
  openGraph: {
    title: "Pricing — Spearmint",
    description:
      "Spearmint is free and open-source. No subscriptions, no hidden costs, no data monetization.",
    url: "/pricing",
  },
};

export default function PricingPage() {
  return (
    <>
      <BreadcrumbJsonLd items={[{ name: "Pricing", path: "/pricing" }]} />
      <section className="bg-mint-bg py-16 md:py-20">
        <div className="mx-auto max-w-6xl px-6">
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 md:text-5xl">
            Pricing
          </h1>
          <p className="mt-4 max-w-2xl text-lg text-gray-600">
            Simple. It&apos;s free.
          </p>
        </div>
      </section>

      <section className="bg-white py-20">
        <div className="mx-auto max-w-lg px-6">
          <div className="rounded-2xl border-2 border-spearmint bg-white p-8 text-center shadow-sm">
            <p className="text-sm font-semibold uppercase tracking-wide text-spearmint-dark">
              Self-Hosted
            </p>
            <p className="mt-4 text-5xl font-bold text-gray-900">$0</p>
            <p className="mt-1 text-gray-500">forever</p>

            <ul className="mt-8 space-y-3 text-left text-sm text-gray-600">
              {[
                "All features included",
                "Unlimited accounts & transactions",
                "Statistical forecasting & scenarios",
                "CapEx / OpEx separation",
                "Relationship detection",
                "CSV & Excel import",
                "Runs on your hardware",
                "No data collection",
                "Community support via GitHub",
              ].map((item) => (
                <li key={item} className="flex items-start gap-3">
                  <svg
                    className="mt-0.5 h-5 w-5 shrink-0 text-spearmint"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={2}
                    aria-hidden="true"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M4.5 12.75l6 6 9-13.5"
                    />
                  </svg>
                  {item}
                </li>
              ))}
            </ul>

            <a
              href={GITHUB_URL}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-8 inline-flex w-full items-center justify-center rounded-full bg-spearmint px-8 py-3 text-base font-semibold text-white transition-colors hover:bg-spearmint-dark"
            >
              Get Started on GitHub
            </a>
          </div>
        </div>
      </section>
    </>
  );
}
