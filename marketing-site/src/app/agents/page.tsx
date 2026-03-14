import type { Metadata } from "next";
import { AgentHero } from "@/components/agents/AgentHero";
import { WhyAgents } from "@/components/agents/WhyAgents";
import { MeetTheAgents } from "@/components/agents/MeetTheAgents";
import { HybridArchitecture } from "@/components/agents/HybridArchitecture";
import { A2AProtocol } from "@/components/agents/A2AProtocol";
import { AgentCTA } from "@/components/agents/AgentCTA";

export const metadata: Metadata = {
  title: "Autonomous Financial Agents — Spearmint",
  description:
    "Meet the AI agents that continuously monitor your finances, surface savings opportunities, and deliver personalized advice — proactively, not just when you ask.",
};

export default function AgentsPage() {
  return (
    <>
      <AgentHero />
      <WhyAgents />
      <MeetTheAgents />
      <HybridArchitecture />
      <A2AProtocol />
      <AgentCTA />
    </>
  );
}
