import { SITE_URL, GITHUB_URL } from "../config";

const organizationSchema = {
  "@context": "https://schema.org",
  "@type": "Organization",
  name: "Spearmint",
  url: SITE_URL,
  logo: `${SITE_URL}/icon.svg`,
  description:
    "A free, self-hosted financial engine that transforms bank data into professional-grade accounting intelligence.",
  sameAs: [GITHUB_URL],
};

const websiteSchema = {
  "@context": "https://schema.org",
  "@type": "WebSite",
  name: "Spearmint",
  url: SITE_URL,
};

const softwareSchema = {
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  name: "Spearmint",
  applicationCategory: "FinanceApplication",
  operatingSystem: "Cross-platform",
  offers: {
    "@type": "Offer",
    price: "0",
    priceCurrency: "USD",
  },
  description:
    "Business-grade personal finance. A free, self-hosted financial engine that transforms bank data into professional-grade accounting intelligence.",
};

export function OrganizationJsonLd() {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{
        __html: JSON.stringify([organizationSchema, websiteSchema]),
      }}
    />
  );
}

export function SoftwareJsonLd() {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(softwareSchema) }}
    />
  );
}

interface BreadcrumbItem {
  name: string;
  path: string;
}

export function BreadcrumbJsonLd({ items }: { items: BreadcrumbItem[] }) {
  const schema = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    itemListElement: [
      { "@type": "ListItem", position: 1, name: "Home", item: SITE_URL },
      ...items.map((item, i) => ({
        "@type": "ListItem",
        position: i + 2,
        name: item.name,
        item: `${SITE_URL}${item.path}`,
      })),
    ],
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}
