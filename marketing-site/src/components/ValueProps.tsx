const comparisons = [
  {
    challenge: "$15k kitchen renovation",
    traditional: '"You\'re way over budget!"',
    spearmint: "Separated as Capital Investment",
  },
  {
    challenge: "Work trip reimbursement",
    traditional: "Counted as personal spending",
    spearmint: "Tracked as Receivable",
  },
  {
    challenge: "Transfer between accounts",
    traditional: "Double-counted or confusing",
    spearmint: "Auto-detected and excluded",
  },
  {
    challenge: "Financial forecasting",
    traditional: "Basic or none",
    spearmint: "Statistical models with confidence intervals",
  },
  {
    challenge: "Your data",
    traditional: "Stored on their servers",
    spearmint: "Stored on YOUR hardware",
  },
  {
    challenge: "Cost",
    traditional: "$5\u201315/month subscription",
    spearmint: "Free forever",
  },
];

export function ValueProps() {
  return (
    <section className="bg-white py-20 md:py-28">
      <div className="mx-auto max-w-6xl px-6">
        <div className="text-center">
          <h2 className="text-3xl font-bold tracking-tight text-gray-900 md:text-4xl">
            Not another expense tracker
          </h2>
          <p className="mx-auto mt-4 max-w-2xl text-lg text-gray-500">
            Most personal finance apps track spending. Spearmint manages wealth
            &mdash; treating your household like a business with the analytical
            rigor of a CFO.
          </p>
        </div>

        <div className="mt-14 overflow-x-auto">
          <table className="w-full min-w-[600px] text-left text-sm">
            <caption className="sr-only">
              Comparison of Spearmint vs traditional finance apps
            </caption>
            <thead>
              <tr className="border-b border-gray-200">
                <th className="py-3 pr-4 font-semibold text-gray-900">
                  Challenge
                </th>
                <th className="py-3 pr-4 font-semibold text-gray-500">
                  Traditional Apps
                </th>
                <th className="py-3 font-semibold text-spearmint-dark">
                  Spearmint
                </th>
              </tr>
            </thead>
            <tbody>
              {comparisons.map((row) => (
                <tr
                  key={row.challenge}
                  className="border-b border-gray-100 last:border-0"
                >
                  <td className="py-4 pr-4 font-medium text-gray-900">
                    {row.challenge}
                  </td>
                  <td className="py-4 pr-4 text-gray-500">
                    {row.traditional}
                  </td>
                  <td className="py-4 font-medium text-spearmint-dark">
                    {row.spearmint}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
