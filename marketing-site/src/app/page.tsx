import type { Metadata } from "next";
import { Hero } from "@/components/Hero";
import { ValueProps } from "@/components/ValueProps";
import { Features } from "@/components/Features";
import { CTA } from "@/components/CTA";
import { SoftwareJsonLd } from "@/components/JsonLd";

export const metadata: Metadata = {
  alternates: { canonical: "/" },
  openGraph: {
    url: "/",
  },
};

export default function Home() {
  return (
    <>
      <SoftwareJsonLd />
      <Hero />
      <ValueProps />
      <Features />
      <CTA />
    </>
  );
}
