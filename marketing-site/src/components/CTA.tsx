export function CTA() {
  return (
    <section className="bg-spearmint-dark py-20 md:py-28">
      <div className="mx-auto max-w-6xl px-6 text-center">
        <h2 className="text-3xl font-bold tracking-tight text-white md:text-4xl">
          Take control of your finances today
        </h2>
        <p className="mx-auto mt-4 max-w-xl text-lg text-white/95">
          Free, open-source, and self-hosted. Deploy in minutes with Docker.
          No credit card, no subscriptions, no data sharing.
        </p>
        <div className="mt-8 flex flex-col items-center justify-center gap-4 sm:flex-row">
          <a
            href="https://github.com/spearmint-finance/spearmint"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center rounded-full bg-white px-8 py-3 text-base font-semibold text-spearmint-dark transition-colors hover:bg-mint-bg"
          >
            View on GitHub
          </a>
          <a
            href="/how-it-works"
            className="inline-flex items-center justify-center rounded-full border border-white/30 px-8 py-3 text-base font-semibold text-white transition-colors hover:bg-white/10"
          >
            Learn More
          </a>
        </div>
      </div>
    </section>
  );
}
