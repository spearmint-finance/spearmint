import type { Metadata } from "next";
import { Features } from "@/components/Features";
import { CTA } from "@/components/CTA";
import { BreadcrumbJsonLd } from "@/components/JsonLd";

export const metadata: Metadata = {
  title: "Features",
  description:
    "Smart classification, relationship detection, statistical forecasting, and more. See what makes Spearmint different.",
  alternates: { canonical: "/features" },
  openGraph: {
    title: "Features — Spearmint",
    description:
      "Smart classification, relationship detection, statistical forecasting, and more. See what makes Spearmint different.",
    url: "/features",
  },
};

export default function FeaturesPage() {
  return (
    <>
      <BreadcrumbJsonLd items={[{ name: "Features", path: "/features" }]} />
      <section className="bg-mint-bg py-16 md:py-20">
        <div className="mx-auto max-w-6xl px-6">
          <h1 className="text-4xl font-bold tracking-tight text-gray-900 md:text-5xl">
            Features
          </h1>
          <p className="mt-4 max-w-2xl text-lg text-gray-600">
            Professional-grade financial tools that treat your household like
            the business it is.
          </p>
        </div>
      </section>
      <Features />
      <CTA />
    </>
  );
}
