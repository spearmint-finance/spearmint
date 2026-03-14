"use client";

import { motion } from "framer-motion";

const agents = [
  { label: "Subscription\nAuditor", angle: 0, color: "#F59E0B", bg: "#FEF3C7" },
  { label: "Bill\nNegotiator", angle: 72, color: "#3B82F6", bg: "#DBEAFE" },
  { label: "Tax\nOptimizer", angle: 144, color: "#8B5CF6", bg: "#EDE9FE" },
  { label: "Budget\nAdvisor", angle: 216, color: "#26A69A", bg: "#E0F2F1" },
  { label: "Minty", angle: 288, color: "#43A047", bg: "#E8F5E9" },
];

function polarToCartesian(angle: number, radius: number) {
  const rad = ((angle - 90) * Math.PI) / 180;
  return { x: 200 + radius * Math.cos(rad), y: 200 + radius * Math.sin(rad) };
}

function DataPulse({
  x1,
  y1,
  x2,
  y2,
  delay,
  color,
}: {
  x1: number;
  y1: number;
  x2: number;
  y2: number;
  delay: number;
  color: string;
}) {
  return (
    <motion.circle
      r={3}
      fill={color}
      initial={{ cx: x1, cy: y1, opacity: 0 }}
      animate={{
        cx: [x1, x2],
        cy: [y1, y2],
        opacity: [0, 1, 1, 0],
      }}
      transition={{
        duration: 2.5,
        delay,
        repeat: Infinity,
        repeatDelay: 1.5,
        ease: "easeInOut",
      }}
    />
  );
}

export function AgentOrchestrationGraphic() {
  const radius = 140;
  const positions = agents.map((a) => polarToCartesian(a.angle, radius));
  const cx = 200;
  const cy = 200;

  return (
    <div className="flex items-center justify-center">
      <svg
        viewBox="0 0 400 400"
        className="h-auto w-full max-w-md"
        role="img"
        aria-label="Diagram showing Spearmint's autonomous agents connected to a central orchestration hub. Animated data pulses flow between agents."
      >
        {/* Connection lines */}
        {positions.map((pos, i) => (
          <line
            key={`line-${i}`}
            x1={cx}
            y1={cy}
            x2={pos.x}
            y2={pos.y}
            stroke={agents[i].color}
            strokeWidth={1.5}
            strokeOpacity={0.25}
            strokeDasharray="4 4"
          />
        ))}

        {/* Cross-connections between adjacent agents */}
        {positions.map((pos, i) => {
          const next = positions[(i + 1) % positions.length];
          return (
            <line
              key={`cross-${i}`}
              x1={pos.x}
              y1={pos.y}
              x2={next.x}
              y2={next.y}
              stroke="#D1D5DB"
              strokeWidth={1}
              strokeOpacity={0.3}
              strokeDasharray="2 6"
            />
          );
        })}

        {/* Animated data pulses — hub to agents */}
        {positions.map((pos, i) => (
          <DataPulse
            key={`pulse-out-${i}`}
            x1={cx}
            y1={cy}
            x2={pos.x}
            y2={pos.y}
            delay={i * 0.8}
            color={agents[i].color}
          />
        ))}

        {/* Animated data pulses — agents to hub */}
        {positions.map((pos, i) => (
          <DataPulse
            key={`pulse-in-${i}`}
            x1={pos.x}
            y1={pos.y}
            x2={cx}
            y2={cy}
            delay={i * 0.8 + 1.2}
            color={agents[i].color}
          />
        ))}

        {/* Central hub */}
        <motion.circle
          cx={cx}
          cy={cy}
          r={38}
          fill="white"
          stroke="#43A047"
          strokeWidth={2.5}
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ duration: 0.5, type: "spring" }}
        />
        <motion.circle
          cx={cx}
          cy={cy}
          r={50}
          fill="none"
          stroke="#43A047"
          strokeWidth={1}
          strokeOpacity={0.15}
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ duration: 0.6, delay: 0.1 }}
        />

        {/* Hub icon — dollar sign */}
        <text
          x={cx}
          y={cy + 1}
          textAnchor="middle"
          dominantBaseline="central"
          className="text-2xl font-bold"
          fill="#43A047"
          fontSize={22}
        >
          $
        </text>
        <text
          x={cx}
          y={cy + 18}
          textAnchor="middle"
          dominantBaseline="central"
          fill="#6B7280"
          fontSize={7}
          fontWeight={600}
        >
          ORCHESTRATOR
        </text>

        {/* Agent nodes */}
        {positions.map((pos, i) => {
          const agent = agents[i];
          const lines = agent.label.split("\n");
          return (
            <motion.g
              key={`agent-${i}`}
              initial={{ opacity: 0, scale: 0 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.4, delay: 0.15 + i * 0.1, type: "spring" }}
            >
              {/* Outer glow */}
              <circle
                cx={pos.x}
                cy={pos.y}
                r={36}
                fill={agent.bg}
                opacity={0.5}
              />
              {/* Node circle */}
              <circle
                cx={pos.x}
                cy={pos.y}
                r={28}
                fill="white"
                stroke={agent.color}
                strokeWidth={2}
              />
              {/* Label */}
              {lines.map((line, j) => (
                <text
                  key={j}
                  x={pos.x}
                  y={pos.y + (j - (lines.length - 1) / 2) * 11}
                  textAnchor="middle"
                  dominantBaseline="central"
                  fill={agent.color}
                  fontSize={8}
                  fontWeight={600}
                >
                  {line}
                </text>
              ))}
            </motion.g>
          );
        })}

        {/* Orbiting ring */}
        <motion.circle
          cx={cx}
          cy={cy}
          r={radius}
          fill="none"
          stroke="#E5E7EB"
          strokeWidth={1}
          strokeDasharray="2 8"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1, delay: 0.5 }}
        />
      </svg>
    </div>
  );
}
