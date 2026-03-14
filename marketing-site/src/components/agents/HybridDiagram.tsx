"use client";

import { motion } from "framer-motion";

export function HybridDiagram() {
  return (
    <div className="flex items-center justify-center">
      <svg
        viewBox="0 0 480 280"
        className="h-auto w-full max-w-lg"
        role="img"
        aria-label="Diagram showing the hybrid architecture: transaction data flows through the deterministic layer for calculations, then the LLM layer for personalized interpretation."
      >
        {/* Background */}
        <rect x="0" y="0" width="480" height="280" rx="12" fill="#F9FAFB" />

        {/* Input: Transaction Data */}
        <motion.g
          initial={{ opacity: 0, x: -20 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4 }}
        >
          <rect x="16" y="100" width="90" height="60" rx="8" fill="white" stroke="#D1D5DB" strokeWidth={1.5} />
          <text x="61" y="122" textAnchor="middle" fontSize="9" fontWeight="600" fill="#374151">Transaction</text>
          <text x="61" y="136" textAnchor="middle" fontSize="9" fontWeight="600" fill="#374151">Data</text>
          <text x="61" y="150" textAnchor="middle" fontSize="7" fill="#9CA3AF">CSV / Bank Feed</text>
        </motion.g>

        {/* Arrow 1 */}
        <motion.path
          d="M106 130 L135 130"
          stroke="#D1D5DB"
          strokeWidth={2}
          fill="none"
          markerEnd="url(#arrowGray)"
          initial={{ pathLength: 0 }}
          whileInView={{ pathLength: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.3, delay: 0.2 }}
        />

        {/* Deterministic Layer */}
        <motion.g
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4, delay: 0.3 }}
        >
          <rect x="135" y="60" width="130" height="140" rx="10" fill="#E8F5E9" stroke="#43A047" strokeWidth={1.5} />
          <text x="200" y="82" textAnchor="middle" fontSize="9" fontWeight="700" fill="#2E7D32">DETERMINISTIC</text>
          <text x="200" y="94" textAnchor="middle" fontSize="7" fill="#43A047">Fast &bull; Precise &bull; Auditable</text>

          {/* Sub-components */}
          <rect x="148" y="106" width="104" height="26" rx="5" fill="white" stroke="#66BB6A" strokeWidth={1} />
          <text x="200" y="122" textAnchor="middle" fontSize="8" fill="#2E7D32">Spending Analyzer</text>

          <rect x="148" y="140" width="104" height="26" rx="5" fill="white" stroke="#66BB6A" strokeWidth={1} />
          <text x="200" y="156" textAnchor="middle" fontSize="8" fill="#2E7D32">Savings Recommender</text>

          <rect x="148" y="174" width="104" height="18" rx="4" fill="#C8E6C9" />
          <text x="200" y="186" textAnchor="middle" fontSize="7" fill="#2E7D32">+12.5% dining trend</text>
        </motion.g>

        {/* Arrow 2 */}
        <motion.path
          d="M265 130 L294 130"
          stroke="#D1D5DB"
          strokeWidth={2}
          fill="none"
          markerEnd="url(#arrowGray)"
          initial={{ pathLength: 0 }}
          whileInView={{ pathLength: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.3, delay: 0.5 }}
        />

        {/* Animated pulse on arrow */}
        <motion.circle
          r={3}
          fill="#43A047"
          initial={{ cx: 265, cy: 130, opacity: 0 }}
          animate={{ cx: [265, 294], cy: [130, 130], opacity: [0, 1, 1, 0] }}
          transition={{ duration: 1.5, repeat: Infinity, repeatDelay: 2, delay: 1 }}
        />

        {/* LLM Reasoning Layer */}
        <motion.g
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4, delay: 0.6 }}
        >
          <rect x="294" y="60" width="130" height="140" rx="10" fill="#E0F2F1" stroke="#26A69A" strokeWidth={1.5} />
          <text x="359" y="82" textAnchor="middle" fontSize="9" fontWeight="700" fill="#00897B">LLM REASONING</text>
          <text x="359" y="94" textAnchor="middle" fontSize="7" fill="#26A69A">Context &bull; Personal &bull; Adaptive</text>

          {/* Sub-components */}
          <rect x="307" y="106" width="104" height="26" rx="5" fill="white" stroke="#4DB6AC" strokeWidth={1} />
          <text x="359" y="122" textAnchor="middle" fontSize="8" fill="#00897B">Signal Interpreter</text>

          <rect x="307" y="140" width="104" height="26" rx="5" fill="white" stroke="#4DB6AC" strokeWidth={1} />
          <text x="359" y="156" textAnchor="middle" fontSize="8" fill="#00897B">Advice Generator</text>

          <rect x="307" y="174" width="104" height="18" rx="4" fill="#B2DFDB" />
          <text x="359" y="186" textAnchor="middle" fontSize="6" fill="#00897B">Try meal prep: ~$80/mo</text>
        </motion.g>

        {/* Arrow 3 — output */}
        <motion.path
          d="M424 130 L453 130"
          stroke="#D1D5DB"
          strokeWidth={2}
          fill="none"
          markerEnd="url(#arrowGray)"
          initial={{ pathLength: 0 }}
          whileInView={{ pathLength: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.3, delay: 0.8 }}
        />

        {/* Output: Personalized Advice */}
        <motion.g
          initial={{ opacity: 0, x: 20 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4, delay: 0.9 }}
        >
          <circle cx="462" cy="130" r="14" fill="#43A047" />
          <text x="462" y="131" textAnchor="middle" dominantBaseline="central" fontSize="12" fill="white" fontWeight="700">!</text>
          <text x="462" y="156" textAnchor="middle" fontSize="7" fill="#6B7280">Actionable</text>
          <text x="462" y="166" textAnchor="middle" fontSize="7" fill="#6B7280">Advice</text>
        </motion.g>

        {/* Bottom labels */}
        <motion.g
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          viewport={{ once: true }}
          transition={{ duration: 0.4, delay: 1 }}
        >
          <text x="200" y="224" textAnchor="middle" fontSize="8" fill="#9CA3AF">Numbers are never hallucinated</text>
          <text x="359" y="224" textAnchor="middle" fontSize="8" fill="#9CA3AF">Interpretation is personalized</text>
        </motion.g>

        {/* Arrow marker */}
        <defs>
          <marker id="arrowGray" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">
            <path d="M0,0 L8,3 L0,6" fill="#D1D5DB" />
          </marker>
        </defs>
      </svg>
    </div>
  );
}
