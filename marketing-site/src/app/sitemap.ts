import type { MetadataRoute } from "next";
import { SITE_URL } from "../config";

export const dynamic = "force-static";

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    { url: `${SITE_URL}/`, priority: 1.0 },
    { url: `${SITE_URL}/features`, priority: 0.8 },
    { url: `${SITE_URL}/agents`, priority: 0.8 },
    { url: `${SITE_URL}/how-it-works`, priority: 0.7 },
    { url: `${SITE_URL}/pricing`, priority: 0.7 },
  ];
}
