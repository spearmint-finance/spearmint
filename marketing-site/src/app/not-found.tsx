import Link from "next/link";

export default function NotFound() {
  return (
    <section className="flex min-h-[60vh] items-center justify-center bg-white">
      <div className="text-center px-6">
        <p className="text-6xl font-bold text-spearmint">404</p>
        <h1 className="mt-4 text-2xl font-bold text-gray-900">
          Page not found
        </h1>
        <p className="mt-2 text-gray-500">
          The page you&apos;re looking for doesn&apos;t exist or has been moved.
        </p>
        <Link
          href="/"
          className="mt-6 inline-flex rounded-full bg-spearmint px-6 py-2.5 text-sm font-semibold text-white transition-colors hover:bg-spearmint-dark"
        >
          Back to Home
        </Link>
      </div>
    </section>
  );
}
