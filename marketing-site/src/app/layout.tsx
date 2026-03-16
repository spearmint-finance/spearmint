import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import { OrganizationJsonLd } from "@/components/JsonLd";
import { SITE_URL } from "../config";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: "Spearmint — Business-Grade Personal Finance",
    template: "%s — Spearmint",
  },
  description:
    "Your personal CFO. A free, self-hosted financial engine that transforms bank data into professional-grade accounting intelligence.",
  openGraph: {
    title: "Spearmint — Business-Grade Personal Finance",
    description:
      "Your personal CFO. A free, self-hosted financial engine that transforms bank data into professional-grade accounting intelligence.",
    type: "website",
    siteName: "Spearmint",
    locale: "en_US",
  },
  twitter: {
    card: "summary_large_image",
    title: "Spearmint — Business-Grade Personal Finance",
    description:
      "Your personal CFO. A free, self-hosted financial engine that transforms bank data into professional-grade accounting intelligence.",
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="dns-prefetch" href="https://github.com" />
        <link rel="preconnect" href="https://github.com" crossOrigin="anonymous" />
      </head>
      <body
        className={`${geistSans.variable} ${geistMono.variable} font-sans antialiased`}
      >
        <OrganizationJsonLd />
        <Header />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  );
}
