import type { Metadata } from "next";
import { Hero } from "@/components/Hero";
import { ValueProps } from "@/components/ValueProps";
import { Features } from "@/components/Features";
import { CTA } from "@/components/CTA";

export const metadata: Metadata = {
  alternates: { canonical: "/" },
  openGraph: {
    url: "/",
  },
};

export default function Home() {
  return (
    <>
      <Hero />
      <ValueProps />
      <Features />
      <CTA />
    </>
  );
}
