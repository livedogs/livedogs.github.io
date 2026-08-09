# Live Dogs Design Co. — v2 (brand-guide rebuild)

A ground-up, SEO-first rebuild of livedogs.ca following the Live Dogs brand guide:
editorial serif (Fraunces), Work Sans, parchment/ink/ember/sea/gold palette, arch and
topography motifs, paper-grain texture. 13 pages of hand-written HTML/CSS with zero
frameworks.

## Structure (pillar → child SEO silo)

```
/                                    Home — brand story, four worlds, all 9 services
/brand-design/                       Pillar + packages ($900 / $1,350 / $3,450–$5,650)
  /branding-culture-identity/
  /logo-design/
  /business-cards/
  /swag/
/web-design/                         Pillar + packages ($299–$499/mo …)
/advertising/                        Pillar + packages ($1,750 … $26,950)
  /social-media-posts/
  /email-marketing/
  /video-storytelling/
/pricing/                            All nine tiers on one page
/start-a-project/                    Typeform intake (tWRedBac)
sitemap.xml · robots.txt
```

Every service/pillar page follows the content spec: ~250 words on the company as it
relates to the service, ~300 words on the service in detail, 3 customer-phrased FAQs,
and a summary band — plus published pricing.

## SEO features

- Unique title + meta description per page, keyworded for "«service» Airdrie"
- One H1 per page, clean heading hierarchy, semantic landmarks, breadcrumbs
- JSON-LD on every page: ProfessionalService (home), Service + Offers, FAQPage,
  BreadcrumbList
- sitemap.xml + robots.txt generated
- Fast by construction: 2 font families, no jQuery/frameworks, inline SVG textures,
  lazy images with dimensions set, canonical URLs

## Editing

`build.py` is the generator — all copy, pricing, and page structure live in it.
Edit it and run:

```bash
python3 /Users/jessefehr/livedogs-v2/build.py
```

Or edit the HTML files directly (they're plain, readable HTML).

## Run locally

```bash
python3 -m http.server 8124 --directory /Users/jessefehr/livedogs-v2
```

## Before deploying

1. Point DNS at any static host (Cloudflare Pages / Netlify — free tier is plenty).
   301 the non-canonical host (apex vs www) to https://www.livedogs.ca.
2. Images/fonts for the hero are still hotlinked from the Webflow CDN — download and
   self-host before cancelling Webflow.
3. Port or create /privacy-policy and /terms-conditions (footer links to them).
4. Add your GA4 tag (G-L1971YELGJ) to the shell in build.py if you want analytics.
5. Google Business Profile: make sure categories match the service pages
   (logo design, web design, advertising) — the site's schema reinforces it.
