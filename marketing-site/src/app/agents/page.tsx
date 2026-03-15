import type { Metadata } from "next";
import { BreadcrumbJsonLd } from "@/components/JsonLd";
import { AgentHero } from "@/components/agents/AgentHero";
import { WhyAgents } from "@/components/agents/WhyAgents";
import { MeetTheAgents } from "@/components/agents/MeetTheAgents";
import { HybridArchitecture } from "@/components/agents/HybridArchitecture";
import { A2AProtocol } from "@/components/agents/A2AProtocol";
import { AgentCTA } from "@/components/agents/AgentCTA";

export const metadata: Metadata = {
  title: "Autonomous Financial Agents",
  description:
    "Meet the AI agents that continuously monitor your finances, surface savings opportunities, and deliver personalized advice — proactively, not just when you ask.",
  alternates: { canonical: "/agents" },
  openGraph: {
    title: "Autonomous Financial Agents — Spearmint",
    description:
      "Meet the AI agents that continuously monitor your finances, surface savings opportunities, and deliver personalized advice — proactively, not just when you ask.",
    url: "/agents",
  },
};

export default function AgentsPage() {
  return (
    <>
      <BreadcrumbJsonLd items={[{ name: "Agents", path: "/agents" }]} />
      <AgentHero />
      <WhyAgents />
      <MeetTheAgents />
      <HybridArchitecture />
      <A2AProtocol />
      <AgentCTA />
    </>
  );
}
