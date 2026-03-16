import Link from "next/link";
import { GITHUB_URL, GITHUB_DOCS_URL } from "../config";

const footerLinks = {
  Product: [
    { href: "/features", label: "Features" },
    { href: "/how-it-works", label: "How It Works" },
    { href: "/pricing", label: "Pricing" },
  ],
  Resources: [
    {
      href: GITHUB_URL,
      label: "GitHub",
      external: true,
    },
    {
      href: GITHUB_DOCS_URL,
      label: "Documentation",
      external: true,
    },
  ],
};

export function Footer() {
  return (
    <footer className="border-t border-gray-100 bg-gray-50">
      <div className="mx-auto max-w-6xl px-6 py-12">
        <div className="grid grid-cols-2 gap-8 md:grid-cols-4">
          <div className="col-span-2 md:col-span-2">
            <Link
              href="/"
              className="text-xl font-bold"
            >
              <span className="text-spearmint">$</span>pearmint
            </Link>
            <p className="mt-3 max-w-xs text-sm text-gray-500">
              Business-grade personal finance. Free, open-source, self-hosted.
              Your data stays on your hardware.
            </p>
          </div>

          {Object.entries(footerLinks).map(([heading, links]) => (
            <div key={heading}>
              <p className="text-sm font-semibold text-gray-900">{heading}</p>
              <ul className="mt-3 space-y-2">
                {links.map((link) => (
                  <li key={link.href}>
                    <a
                      href={link.href}
                      {...("external" in link && link.external
                        ? { target: "_blank", rel: "noopener noreferrer" }
                        : {})}
                      className="text-sm text-gray-500 transition-colors hover:text-spearmint-dark"
                    >
                      {link.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-10 border-t border-gray-200 pt-6 text-center text-xs text-gray-500">
          &copy; {new Date().getFullYear()} Spearmint Finance. Open-source under
          MIT License.
        </div>
      </div>
    </footer>
  );
}
