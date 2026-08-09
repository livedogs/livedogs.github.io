#!/usr/bin/env python3
"""Generate the Live Dogs v2 static site (pure HTML output)."""
import json, os

ROOT = "/Users/jessefehr/livedogs-v2"
BASE = "https://www.livedogs.ca"
CDN = "https://cdn.prod.website-files.com/64821e469d97603460b34a34"
LOGO_DARK = "/assets/live-dogs-icon.svg"
LOGO_LIGHT = "/assets/live-dogs-icon-light.svg"
HERO_IMG = "/assets/home-banner-p-1080.webp"
FAVICON = "/assets/live-dogs-favicon.png"
WEBCLIP = "/assets/live-dogs-webclip.png"
FONTS = "https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT,WONK@0,9..144,100..900,0..100,0..1;1,9..144,100..900,0..100,0..1&family=Work+Sans:ital,wght@0,300..800;1,300..800&display=swap"

TOPO = """<svg class="topo" viewBox="0 0 1200 60" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true" preserveAspectRatio="none"><path d="M0 30 C150 10 250 50 400 30 S650 10 800 30 1050 50 1200 30"/><path d="M0 45 C150 25 250 65 400 45 S650 25 800 45 1050 65 1200 45"/><path d="M0 15 C150 -5 250 35 400 15 S650 -5 800 15 1050 35 1200 15"/></svg>"""

NAV_ITEMS = [
    ("Home", "/", []),
    ("Brand Design", "/brand-design/", [
        ("Branding & Culture Identity", "/brand-design/branding-culture-identity/"),
        ("Logo Design", "/brand-design/logo-design/"),
        ("Business Cards", "/brand-design/business-cards/"),
        ("Swag & Apparel", "/brand-design/swag/"),
    ]),
    ("Web Design", "/web-design/", []),
    ("Advertising", "/advertising/", [
        ("Social Media Posts", "/advertising/social-media-posts/"),
        ("Email Marketing", "/advertising/email-marketing/"),
        ("Video Storytelling", "/advertising/video-storytelling/"),
    ]),
    ("Pricing", "/pricing/", []),
]


def nav_html(current: str) -> str:
    items = []
    for label, url, subs in NAV_ITEMS:
        cur = ' aria-current="page"' if url == current else ""
        if subs:
            sub_lis = "".join(
                f'<li><a href="{u}"{" aria-current=\"page\"" if u == current else ""}>{l}</a></li>'
                for l, u in subs
            )
            in_section = current.startswith(url) and current != url
            cur = ' aria-current="true"' if in_section else cur
            items.append(
                f'<li class="has-sub"><a href="{url}"{cur}>{label}</a>'
                f'<ul class="subnav">{sub_lis}</ul></li>'
            )
        else:
            items.append(f'<li><a href="{url}"{cur}>{label}</a></li>')
    items.append('<li class="site-nav__cta"><a class="button" href="/start-a-project/">Start a project</a></li>')
    return "".join(items)


def shell(*, path, title, meta, body, schema=None, og_title=None, og_desc=None):
    canonical = BASE + path
    schema_tag = ""
    if schema:
        schema_tag = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'
    return f"""<!DOCTYPE html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{meta}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Live Dogs Design Co.">
<meta property="og:title" content="{og_title or title}">
<meta property="og:description" content="{og_desc or meta}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{BASE}/assets/og-banner.jpg">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{og_title or title}">
<meta name="twitter:description" content="{og_desc or meta}">
<meta name="twitter:image" content="{BASE}/assets/og-banner.jpg">
<link rel="icon" href="{FAVICON}">
<link rel="apple-touch-icon" href="{WEBCLIP}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="/css/main.css">
<script defer src="/js/main.js"></script>
{schema_tag}
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
<filter id="rough-ink" x="-15%" y="-15%" width="130%" height="130%">
<feTurbulence type="fractalNoise" baseFrequency="0.09" numOctaves="3" seed="7" result="n"/>
<feDisplacementMap in="SourceGraphic" in2="n" scale="3.2" xChannelSelector="R" yChannelSelector="G"/>
</filter>
<filter id="rough-ink-big" x="-10%" y="-10%" width="120%" height="120%">
<feTurbulence type="fractalNoise" baseFrequency="0.025" numOctaves="3" seed="11" result="n"/>
<feDisplacementMap in="SourceGraphic" in2="n" scale="7" xChannelSelector="R" yChannelSelector="G"/>
</filter>
</defs></svg>
<header class="site-header">
  <div class="wrap site-header__inner">
    <a class="site-header__logo" href="/" aria-label="Live Dogs Design Co. — home">
      <img src="{LOGO_DARK}" alt="" width="56" height="27">
    </a>
    <nav class="site-nav" aria-label="Main">
      <button class="site-nav__toggle" aria-expanded="false" aria-controls="nav-menu">
        <span class="site-nav__toggle-box" aria-hidden="true"><span></span><span></span><span></span></span>
        <span class="visually-hidden">Menu</span>
      </button>
      <ul id="nav-menu" class="site-nav__list">{nav_html(path)}</ul>
    </nav>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap site-footer__grid">
    <div class="site-footer__brand">
      <img src="{LOGO_LIGHT}" alt="Live Dogs Design Co." width="72" height="35" loading="lazy">
      <p>A brand agency in Airdrie, Alberta. Storytellers, explorers, and craftsmen — designing brands that aren't just seen, but felt.</p>
    </div>
    <nav class="site-footer__col" aria-label="Services">
      <h3>Services</h3>
      <ul>
        <li><a href="/brand-design/">Brand Design</a></li>
        <li><a href="/web-design/">Web Design</a></li>
        <li><a href="/advertising/">Advertising</a></li>
        <li><a href="/pricing/">Pricing</a></li>
      </ul>
    </nav>
    <nav class="site-footer__col" aria-label="Company">
      <h3>Company</h3>
      <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/start-a-project/">Start a project</a></li>
        <li><a href="https://goo.gl/maps/V6p1ajsqmN32Wqcu5" rel="noopener">Find us on Google</a></li>
      </ul>
    </nav>
    <nav class="site-footer__col" aria-label="Social media">
      <h3>Socials</h3>
      <ul>
        <li><a href="https://www.instagram.com/livedogsdesignco" rel="noopener">Instagram</a></li>
        <li><a href="https://www.linkedin.com/in/jesse-fehr/" rel="noopener">LinkedIn</a></li>
        <li><a href="https://www.tiktok.com/@livedogsdesignco" rel="noopener">TikTok</a></li>
      </ul>
    </nav>
  </div>
  <div class="wrap site-footer__bottom">
    <p>Live Dogs Design Co. © <span class="year">2026</span> · Airdrie, Alberta</p>
    <ul>
      <li><a href="/privacy-policy">Privacy</a></li>
      <li><a href="/terms-conditions">T's &amp; C's</a></li>
    </ul>
  </div>
</footer>
</body>
</html>
"""


CONSTELLATION = """<svg class="constellation" viewBox="-10 -10 320 280" fill="none" aria-hidden="true">
<g filter="url(#rough-ink-big)">
<g stroke="currentColor" stroke-width="1" opacity=".7">
<polyline points="60,40 110,70 150,50"/>
<polyline points="110,70 200,90 170,140 120,160 90,210"/>
<polyline points="170,140 210,190 150,220 90,210"/>
</g>
<g fill="currentColor">
<circle cx="60" cy="40" r="5"/><circle cx="110" cy="70" r="2.5"/><circle cx="150" cy="50" r="2"/>
<circle cx="200" cy="90" r="2.5"/><circle cx="170" cy="140" r="3"/><circle cx="120" cy="160" r="2"/>
<circle cx="90" cy="210" r="3"/><circle cx="150" cy="220" r="2.5"/><circle cx="210" cy="190" r="3"/>
</g>
<path d="M60 40 l0 -12 M60 40 l0 12 M60 40 l-12 0 M60 40 l12 0" stroke="currentColor" stroke-width="1" opacity=".8"/>
</g>
</svg>"""


def ink(paths, cls="ink-icon"):
    return (f'<svg class="{cls}" viewBox="-4 -4 56 56" fill="none" stroke="currentColor" '
            f'stroke-width="3.1" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true"><g filter="url(#rough-ink)">{paths}</g></svg>')

# Hand-drawn ink icon set — motifs straight from the moodboard
ICONS = {
"/brand-design/": ink('<circle cx="24" cy="24" r="17"/><path d="M24 9 L27 21 L39 24 L27 27 L24 39 L21 27 L9 24 L21 21 Z" fill="currentColor" stroke="none" opacity=".9"/><circle cx="24" cy="24" r="2.5" fill="var(--parchment)" stroke="none"/>'),
"/brand-design/logo-design/": ink('<path d="M24 6 C30 14 36 18 36 27 a12 12 0 0 1 -24 0 C12 18 18 14 24 6 Z"/><path d="M24 21 c3 4 5.5 6 5.5 9.5 a5.5 5.5 0 0 1 -11 0 c0 -3.5 2.5 -5.5 5.5 -9.5 Z" fill="currentColor" stroke="none" opacity=".85"/>'),
"/brand-design/branding-culture-identity/": ink('<path d="M24 8 C28 14 31 16.5 31 22 a7 7 0 0 1 -14 0 c0 -5.5 3 -8 7 -14 Z"/><path d="M9 40 L39 33 M9 33 L39 40"/><circle cx="14" cy="24" r="1.2" fill="currentColor" stroke="none"/><circle cx="35" cy="20" r="1.2" fill="currentColor" stroke="none"/>'),
"/brand-design/business-cards/": ink('<rect x="9" y="15" width="30" height="19" rx="2"/><path d="M14 22 h12 M14 27 h8"/><path d="M33 20.5 l1.2 2.4 2.6 .4 -1.9 1.9 .45 2.6 -2.35 -1.25 -2.35 1.25 .45 -2.6 -1.9 -1.9 2.6 -.4 Z" fill="currentColor" stroke="none"/>'),
"/brand-design/swag/": ink('<path d="M17 9 L8 15 L12 21 L16 18.5 V39 H32 V18.5 L36 21 L40 15 L31 9 A7.5 5 0 0 1 17 9 Z"/><path d="M20 27 l2.5 2.5 5 -5.5"/>'),
"/web-design/": ink('<path d="M20.5 19 L18.5 39 H29.5 L27.5 19 Z"/><path d="M19.5 14 h9 v5 h-9 Z M24 7.5 l-6.5 6.5 M24 7.5 l6.5 6.5"/><path d="M9 11 L15 15.5 M39 11 L33 15.5 M24 2.5 v4"/><path d="M13.5 39 h21"/><path d="M20 24 h8 M19.4 30 h9.2"/>'),
"/advertising/": ink('<path d="M24 21.5 a2.5 2.5 0 0 1 2.5 2.5 a5 5 0 0 1 -5 5 a7.5 7.5 0 0 1 -7.5 -7.5 a10 10 0 0 1 10 -10 a12.5 12.5 0 0 1 12.5 12.5 a15 15 0 0 1 -15 15 a17.5 17.5 0 0 1 -17.5 -17.5"/>'),
"/advertising/social-media-posts/": ink('<path d="M24 7 L27.5 20.5 L41 24 L27.5 27.5 L24 41 L20.5 27.5 L7 24 L20.5 20.5 Z"/><circle cx="38" cy="10" r="1.4" fill="currentColor" stroke="none"/><circle cx="10" cy="37" r="1.4" fill="currentColor" stroke="none"/>'),
"/advertising/email-marketing/": ink('<circle cx="24" cy="6.5" r="2.5"/><path d="M18.5 13 h11 l-2 -4 h-7 Z"/><path d="M19 13 c-2.5 7 -2.5 11.5 0 17.5 h10 c2.5 -6 2.5 -10.5 0 -17.5"/><path d="M16.5 30.5 h15 l-1.5 5 h-12 Z"/><path d="M24 20 c1.6 2 2.4 3.2 2.4 4.8 a2.4 2.4 0 0 1 -4.8 0 c0 -1.6 .8 -2.8 2.4 -4.8 Z" fill="currentColor" stroke="none" opacity=".85"/>'),
"/advertising/video-storytelling/": ink('<path d="M24 13.5 C20 9.5 13.5 9.5 9.5 11.5 V35 c4 -2 10.5 -2 14.5 1.5 c4 -3.5 10.5 -3.5 14.5 -1.5 V11.5 C34.5 9.5 28 9.5 24 13.5 Z"/><path d="M24 13.5 V36"/><path d="M14 18 h5.5 M14 23 h5.5 M28.5 18 h5.5 M28.5 23 h5.5"/>'),
}


def float_nav(label, links):
    """Floating chip nav for the top-left of a page header."""
    chips = "".join(f'<a href="{u}">{l}</a>' for l, u in links)
    return (f'<nav class="float-nav reveal" aria-label="{label}">'
            f'<span class="float-nav__label">{label}</span>{chips}</nav>')


def crumbs(items):
    lis = "".join(
        f'<li><a href="{u}">{l}</a></li>' if u else f'<li aria-current="page">{l}</li>'
        for l, u in items
    )
    return f'<nav class="crumbs" aria-label="Breadcrumb"><div class="wrap"><ol>{lis}</ol></div></nav>'


def crumb_schema(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": l, **({"item": BASE + u} if u else {})}
            for i, (l, u) in enumerate(items)
        ],
    }


def faq_schema(faqs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }


def faq_html(faqs):
    out = "".join(
        f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs
    )
    return f'<div class="faq reveal">{out}</div>'


def tiers_html(tiers):
    cards = []
    for t in tiers:
        feat = " tier--featured" if t.get("featured") else ""
        items = "".join(f"<li>{i}</li>" for i in t["items"])
        note = f'<p class="tier__note">{t["note"]}</p>' if t.get("note") else ""
        cards.append(
            f'<div class="tier{feat} reveal"><div class="tier__head"><h3>{t["name"]}</h3>'
            f'<span class="tier__price">{t["price"]}</span></div>'
            f"<ul>{items}</ul>{note}</div>"
        )
    return f'<div class="tiers">{"".join(cards)}</div>'


def service_page(s):
    """Standard service page: 250w company / 300w detail / 3 FAQs / summary."""
    trail = [("Home", "/"), (s["pillar_name"], s["pillar_url"]), (s["name"], None)]
    faqs = s["faqs"]
    schema = [
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": s["name"],
            "serviceType": s["name"],
            "description": s["meta"],
            "areaServed": ["Airdrie AB", "Calgary AB", "Rocky View County"],
            "provider": {"@type": "ProfessionalService", "name": "Live Dogs Design Co.",
                         "url": BASE, "address": {"@type": "PostalAddress",
                         "addressLocality": "Airdrie", "addressRegion": "AB", "addressCountry": "CA"}},
            "offers": [{"@type": "Offer", "name": n, "price": p, "priceCurrency": "CAD"}
                       for n, p in s.get("offers", [])],
        },
        faq_schema(faqs),
        crumb_schema(trail),
    ]
    siblings = [(l.replace(" & Apparel", "").replace("Branding & Culture Identity", "Branding & Culture"), u)
                for label, url, subs in NAV_ITEMS if url == s["pillar_url"]
                for l, u in subs if u != s["url"]]
    fnav = float_nav(f'In {s["pillar_name"].lower()}',
                     siblings + [("Packages", s["pillar_url"] + "#pricing")])
    body = f"""
{crumbs(trail)}
<section class="hero">
  {CONSTELLATION}
  <div class="wrap">
    {fnav}
    {ICONS.get(s["url"], "")}
    <p class="eyebrow reveal">{s["pillar_name"]} · Airdrie, AB</p>
    <h1 class="reveal">{s["h1"]}</h1>
    <p class="lede hero__lede reveal">{s["lede"]}</p>
    <div class="hero__actions reveal">
      <a class="button" href="/start-a-project/">Start a project</a>
      <a class="button button--ghost" href="/pricing/">See pricing</a>
    </div>
  </div>
</section>
{TOPO}
<section class="section article">
  <div class="wrap">
    <h2 class="reveal">Why Live Dogs for {s["short"]}</h2>
    {s["about_company"]}
    <blockquote class="pull reveal">{s["pull"]}</blockquote>
    <h2 class="reveal">{s["detail_heading"]}</h2>
    {s["detail"]}
    <h2 id="faq" class="reveal">Questions we hear</h2>
    {faq_html(faqs)}
    <div class="summary-band reveal">
      <h2>In short</h2>
      <p>{s["summary"]}</p>
      <a class="button" href="/start-a-project/">Start a project</a>
    </div>
  </div>
</section>
"""
    return shell(path=s["url"], title=s["title"], meta=s["meta"], body=body, schema=schema)


def pillar_page(p):
    trail = [("Home", "/"), (p["name"], None)]
    schema = [
        {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": p["name"],
            "serviceType": p["name"],
            "description": p["meta"],
            "areaServed": ["Airdrie AB", "Calgary AB", "Rocky View County"],
            "provider": {"@type": "ProfessionalService", "name": "Live Dogs Design Co.", "url": BASE},
            "offers": [{"@type": "Offer", "name": n, "price": pr, "priceCurrency": "CAD"}
                       for n, pr in p.get("offers", [])],
        },
        faq_schema(p["faqs"]),
        crumb_schema(trail),
    ]
    children = ""
    if p.get("children"):
        cards = "".join(
            f'<a class="svc-card reveal" href="{u}">{ICONS.get(u, "")}<h3>{n}</h3><p>{d}</p>'
            f'<span class="svc-card__go">Explore {n.lower()}</span></a>'
            for n, u, d in p["children"]
        )
        children = f"""
<section class="section section--deep">
  <div class="wrap">
    <p class="eyebrow reveal">Inside {p["name"].lower()}</p>
    <h2 class="reveal">{p["children_heading"]}</h2>
    <div class="svc-grid">{cards}</div>
  </div>
</section>"""
    child_links = [(l.replace(" & Apparel", "").replace("Branding & Culture Identity", "Branding & Culture"), u)
                   for label, url, subs in NAV_ITEMS if url == p["url"] for l, u in subs]
    fnav = float_nav("In this section",
                     child_links + [("Packages", "#pricing"), ("Questions", "#faq")])
    body = f"""
{crumbs(trail)}
<section class="hero">
  {CONSTELLATION}
  <div class="wrap">
    {fnav}
    {ICONS.get(p["url"], "")}
    <p class="eyebrow reveal">{p["eyebrow"]}</p>
    <h1 class="reveal">{p["h1"]}</h1>
    <p class="lede hero__lede reveal">{p["lede"]}</p>
    <div class="hero__actions reveal">
      <a class="button" href="/start-a-project/">Start a project</a>
      <a class="button button--ghost" href="#pricing">See packages</a>
    </div>
  </div>
</section>
{TOPO}
<section class="section article">
  <div class="wrap">
    <h2 class="reveal">Why Live Dogs for {p["short"]}</h2>
    {p["about_company"]}
    <blockquote class="pull reveal">{p["pull"]}</blockquote>
    <h2 class="reveal">{p["detail_heading"]}</h2>
    {p["detail"]}
  </div>
</section>
{children}
<section class="section" id="pricing">
  <div class="wrap">
    <p class="eyebrow reveal">Packages &amp; pricing</p>
    <h2 class="reveal">{p["pricing_heading"]}</h2>
    <p class="lede reveal">Every package can be mixed and matched — start where the need is loudest.</p>
    {tiers_html(p["tiers"])}
  </div>
</section>
<section class="section article" style="padding-top:0">
  <div class="wrap">
    <h2 id="faq" class="reveal">Questions we hear</h2>
    {faq_html(p["faqs"])}
    <div class="summary-band reveal">
      <h2>In short</h2>
      <p>{p["summary"]}</p>
      <a class="button" href="/start-a-project/">Start a project</a>
    </div>
  </div>
</section>
"""
    return shell(path=p["url"], title=p["title"], meta=p["meta"], body=body, schema=schema)


# ============================== CONTENT ==============================

P = lambda *ps: "".join(f'<p class="reveal">{x}</p>' for x in ps)

PILLARS = [
# ---------------------------------------------------------------- BRAND DESIGN
{
"url": "/brand-design/", "name": "Brand Design", "short": "brand design",
"title": "Brand Design & Logo Packages in Airdrie | Live Dogs Design Co.",
"meta": "Brand design in Airdrie, AB — logos, brand identity, business cards and swag. Hand-drawn concepts, no robot logos. Packages from $900.",
"eyebrow": "Brand design · Airdrie, AB",
"h1": "Brand design that gives your business <em>a pulse</em>",
"lede": "Your brand is the personality people meet before they meet you. We build it by hand — word maps, sketches, and stories first, pixels second — so the mark on your truck, your storefront, and your invoice all say the same true thing about you.",
"pull": "You can be Netflix or you can be Blockbuster — but you can't be both.",
"about_company": P(
  "Live Dogs Design Co. started with a conviction: small businesses deserve branding with the same care the big players buy — without the big-agency runaround. We're a brand agency in Airdrie, Alberta, and brand design is the trunk of everything we do. Logos, websites, ads, swag: they all grow from the identity work done here.",
  "We pull from four worlds — storytelling, exploration, culinary arts, and the local church — and it shows in how we work. Storytelling means your brand gets a narrative, not just a mark. Exploration means we go looking for the answer instead of settling for the first safe idea. The culinary world taught us that presentation is persuasion. And the church taught us that gathering people around something they believe in is the whole point.",
  "With nearly a decade in the industry we've seen great design, terrible design, and everything in between. Our promise is simple: research before drawing, drawing before digital, and a finished identity that's different from the industry norm — and built to last longer than the trend cycle that produced it."),
"detail_heading": "What brand design includes, in detail",
"detail": P(
  "Brand design at Live Dogs is a process, not a product drop. It starts with a working session about your business — who you serve, who you're up against, what you want to be known for. From there we word-map, sketch hand-drawn concepts, and only then move to digital drafts. You see real options with real reasoning, never three fonts slapped on a circle.",
  "Depending on your package, your identity can include the logo suite (icon, horizontal and vertical lockups), a colour palette with usage rules, typography styles, a custom typeface, logo animation, business cards and print materials, swag, custom icons, and full brand guidelines — the rulebook that keeps your brand consistent whether it's on a hoodie or a highway sign.",
  "Packages start at <strong>$900</strong> for Logo Design Basic (logo, business cards, and three social images) and scale to the full <strong>Brand Identity Max</strong> at $3,450–$5,650. Everything mixes and matches — because a shop that already has great cards doesn't need to buy them twice."),
"children_heading": "The four crafts inside brand design",
"children": [
  ("Branding & Culture Identity", "/brand-design/branding-culture-identity/", "The soul work — values, voice, and visual identity that align your team and your audience."),
  ("Logo Design", "/brand-design/logo-design/", "Hand-drawn concepts to finished mark. The face of your business, built to last."),
  ("Business Cards", "/brand-design/business-cards/", "The handshake that stays behind. Print that feels as good as it looks."),
  ("Swag & Apparel", "/brand-design/swag/", "Shirts, hats and hoodies your team actually wants to wear."),
],
"pricing_heading": "Brand design packages",
"tiers": [
  {"name": "Logo Design Basic", "price": "$900",
   "items": ["<strong>Logo design</strong> — $750 value", "<strong>Business cards</strong> — $75", "<strong>3 images for socials</strong> — $75"],
   "note": "The essentials to show up looking sharp."},
  {"name": "Logo Design +", "price": "$1,350", "featured": True,
   "items": ["Everything in <strong>Logo Design Basic</strong>", "<strong>Logo layouts</strong> — icon, horizontal &amp; vertical — $150", "<strong>Custom typeface</strong> — $150", "<strong>Logo animation</strong> — $150"],
   "note": "Our most popular starting point."},
  {"name": "Brand Identity Max", "price": "$3,450–$5,650",
   "items": ["Everything in <strong>Logo Design +</strong>", "<strong>Swag</strong> — $500–$1,000", "<strong>Custom icons</strong> — $300–$800", "<strong>Photo session pattern</strong> — $1,000–$2,000", "<strong>Brand guidelines</strong> — $300–$500"],
   "note": "The full identity, documented and built to scale."},
],
"offers": [("Logo Design Basic", "900"), ("Logo Design +", "1350"), ("Brand Identity Max", "3450")],
"faqs": [
  ("How much does brand design cost in Airdrie?",
   "Our packages run from $900 for Logo Design Basic to $3,450–$5,650 for Brand Identity Max, and every package can be mixed and matched to what your business actually needs."),
  ("What's the difference between a logo and a brand identity?",
   "A logo is the face; the brand identity is the whole personality — colours, typography, voice, and guidelines. If the logo is your handshake, the identity is everything people remember after it."),
  ("How long does the brand design process take?",
   "Most logo projects run two to four weeks from kickoff to final files, and a full brand identity typically takes four to eight weeks depending on scope and how fast decisions come back."),
],
"summary": "Brand design at Live Dogs is hand-crafted identity work — research, sketches, and story before a single pixel — delivered in mix-and-match packages from $900 to full brand identities at $3,450–$5,650. It's the foundation every other marketing dollar stands on.",
},
# ---------------------------------------------------------------- WEB DESIGN
{
"url": "/web-design/", "name": "Web Design", "short": "web design",
"title": "Web Design in Airdrie | Custom Websites from $299/mo | Live Dogs",
"meta": "Custom, responsive web design in Airdrie, AB from $299/month — hosting and updates included. On-brand websites that convert for small businesses.",
"eyebrow": "Web design · Airdrie, AB",
"h1": "Websites that work as hard <em>as you do</em>",
"lede": "Your website is your online building — open 24 hours, greeting every customer Google sends. We design custom, responsive, on-brand sites for small businesses from $299/month, hosting and updates included, so it never quietly rots while you're busy running the company.",
"pull": "Your website is your online building — and it shows when the builder cut corners.",
"about_company": P(
  "Live Dogs is a brand agency first, and that's exactly why our websites work. Most web shops start with a template and pour your content into it; we start with your identity — the story, colours, and voice we've either built with you or absorbed from what you have — and design the site around it. The result reads like your business, not like a theme 40,000 other companies bought.",
  "We're based in Airdrie and we build for the businesses around us: trades, shops, and services with $1–2 million in revenue who need their website to actually produce work, not just exist. Being local matters here — we know what your customers search for, we can shoot photos at your shop, and when you call, a person you've met answers.",
  "And because we believe websites are a service rather than a one-time stunt, we price them like one. Hosting, updates, and care are part of the monthly rate. You'll never discover your site is three years out of date and be quoted a five-figure rebuild — it just keeps getting tended, like anything alive."),
"detail_heading": "What web design includes, in detail",
"detail": P(
  "Every Live Dogs website is custom-designed and fully responsive — it works on the phone in your customer's pocket first, because that's where most of Airdrie is browsing. We architect pages around what you want visitors to do: call, book, request a quote. Then we build it clean and fast, because speed is a ranking factor and slow sites bleed customers.",
  "<strong>Web Design Basic</strong> ($299–$499/month) covers complete web design with hosting and ongoing updates. <strong>Web Design +</strong> adds the assets that lift a site from good to convincing: a professional photo session ($1,000–$2,500), colour palette, and custom icons. <strong>Web Design Max</strong> brings e-commerce ($99–$999/month), a CMS for blogging ($49–$499/month), copywriting, and web animation for the businesses ready to sell and publish online.",
  "Search optimization is baked in, not bolted on: proper page structure, local keywords, fast load times, and the technical details — titles, descriptions, structured data — that help Google understand exactly what you do and where you do it."),
"children_heading": "",
"children": [],
"pricing_heading": "Web design packages",
"tiers": [
  {"name": "Web Design Basic", "price": "$299–$499<small>/mo</small>",
   "items": ["<strong>Complete custom web design</strong>", "<strong>Hosting included</strong>", "<strong>Ongoing updates</strong> — your site never goes stale"],
   "note": "One monthly rate. No surprise rebuild bills."},
  {"name": "Web Design +", "price": "$1,375–$3,375 <small>+ $299–$499/mo</small>", "featured": True,
   "items": ["Everything in <strong>Web Design Basic</strong>", "<strong>Photo session</strong> — $1,000–$2,500", "<strong>Colour palette</strong> — $75", "<strong>Custom icons</strong> — $300–$800"],
   "note": "Real photography changes everything."},
  {"name": "Web Design Max", "price": "$1,675–$5,475 <small>+ $447–$1,997/mo</small>",
   "items": ["Everything in <strong>Web Design +</strong>", "<strong>E-commerce store</strong> — $99–$999/mo", "<strong>CMS &amp; blog</strong> — $49–$499/mo", "<strong>Copywriting</strong> — $150–$600", "<strong>Web animation</strong> — $150–$1,500"],
   "note": "Sell, publish, and grow — all under one roof."},
],
"offers": [("Web Design Basic (monthly)", "299"), ("Web Design +", "1375"), ("Web Design Max", "1675")],
"faqs": [
  ("How much does a website cost in Airdrie?",
   "Our websites run $299–$499 per month including design, hosting, and updates — with one-time add-ons like photography or e-commerce if you need them. No five-figure surprise invoices."),
  ("Can't I just build my own website?",
   "You can — but your website is your online building, and it shows when the builder cut corners or lacked vision. We charge to design it well and to be your guide in the digital landscape afterward."),
  ("Will my website show up on Google?",
   "That's the point of how we build. Clean structure, fast load times, local keywords, and proper technical SEO are part of every build — and the monthly service means it keeps improving instead of decaying."),
],
"summary": "Live Dogs builds custom, responsive, SEO-ready websites for Airdrie-area small businesses from $299/month with hosting and updates included — sites designed from your brand outward, built to convert visitors into calls, and tended continuously so they never go stale.",
},
# ---------------------------------------------------------------- ADVERTISING
{
"url": "/advertising/", "name": "Advertising", "short": "advertising",
"title": "Advertising Agency in Airdrie | Social, Email & Video Ads | Live Dogs",
"meta": "Advertising in Airdrie, AB — social media, email campaigns, digital ads and video. Brand-first campaigns that compound. Packages from $1,750.",
"eyebrow": "Advertising · Airdrie, AB",
"h1": "Advertising that <em>compounds</em>, not just spends",
"lede": "Brand advertising works like investing: the earlier you start, the greater the growth. We build campaigns across social, email, digital and video that keep your business in front of the right people — consistently, recognizably, relentlessly.",
"pull": "It takes ten touches before someone trusts your brand. Every ad is one more.",
"about_company": P(
  "Advertising is where Live Dogs' brand-first philosophy pays out. Anyone can boost a post; the businesses that win locally are the ones whose ads are instantly recognizable — same voice, same look, same promise — across every channel. Because we build brands for a living, every campaign we run strengthens the identity instead of diluting it.",
  "We watched the Airbnb case study closely: brand-focused advertising outperformed product-based ads even for a tech giant. You don't need their scale to use their playbook. You need a clear story, consistent creative, and the patience to show up repeatedly — which is precisely what a small local agency can deliver without a big-city retainer.",
  "We serve Airdrie first and the Calgary region beyond it, and we're happiest working with trades and small businesses who want to grow. Our job is to make email and social media work for you — not the other way around, where you're feeding the platforms every evening after a full day's work."),
"detail_heading": "What advertising includes, in detail",
"detail": P(
  "Live Dogs advertising spans the channels a small business actually uses. <strong>Ad Basic</strong> ($1,750–$1,850) covers twelve social images, five shirts or hats — because your crew is a walking billboard — and three digital ads. <strong>Ad +</strong> ($4,350–$4,450) layers in three email campaigns, five hoodies, and a motion-graphics ad that stops the scroll.",
  "<strong>Ad Max</strong> ($21,850–$26,950) is the full campaign engine: a directed video ad ($5,000), a year-long ad campaign creation ($10,000–$15,000), nine email campaigns, and an outdoor ad spot starting around $500 depending on location. It's for the business ready to own its market, not just visit it.",
  "Every campaign starts from your brand guidelines and your goals — more calls, more quotes, more butts in seats — and we report in those terms. No vanity-metric fog. If you're already posting and emailing, we'll tell you honestly what to keep, what to cut, and where money is quietly leaking."),
"children_heading": "The three engines inside advertising",
"children": [
  ("Social Media Posts", "/advertising/social-media-posts/", "On-brand posts that keep you in front of your audience without eating your evenings."),
  ("Email Marketing", "/advertising/email-marketing/", "The channel you own. Campaigns that land, read well, and get clicked."),
  ("Video Storytelling", "/advertising/video-storytelling/", "Motion graphics to directed video — stories that stop the scroll."),
],
"pricing_heading": "Advertising packages",
"tiers": [
  {"name": "Ad Basic", "price": "$1,750–$1,850",
   "items": ["<strong>12 social images</strong> — $600", "<strong>5 shirts or hats</strong> — $250–$350", "<strong>3 digital ads</strong> — $900"],
   "note": "A steady, recognizable presence."},
  {"name": "Ad +", "price": "$4,350–$4,450", "featured": True,
   "items": ["Everything in <strong>Ad Basic</strong>", "<strong>3 email campaigns</strong> — $900", "<strong>5 hoodies</strong> — $700", "<strong>Motion graphics ad</strong> — $1,000"],
   "note": "Multi-channel momentum."},
  {"name": "Ad Max", "price": "$21,850–$26,950",
   "items": ["Everything in <strong>Ad +</strong>", "<strong>Directed video ad</strong> — $5,000", "<strong>1-year ad campaign creation</strong> — $10,000–$15,000", "<strong>9 email campaigns</strong> — $2,500", "<strong>Outdoor ad spot</strong> — from $500 by location"],
   "note": "Own the market, don't just visit it."},
],
"offers": [("Ad Basic", "1750"), ("Ad +", "4350"), ("Ad Max", "21850")],
"faqs": [
  ("Do I need a big budget to advertise well?",
   "No — you need consistency more than scale. Our Ad Basic package at $1,750–$1,850 keeps a small business visibly present across social and digital, and brand advertising compounds the longer you run it."),
  ("Should I do brand ads or promotional ads?",
   "Both have a place, but brand-focused advertising is what builds long-term demand — even Airbnb found it outperformed product ads. We balance the two based on your goals and season."),
  ("Can you work with the ads I'm already running?",
   "Yes. We'll audit what you're running, keep what's working, and bring the creative in line with your brand so every channel reinforces the same story."),
],
"summary": "Live Dogs advertising is brand-first campaign work across social, email, digital, video and even outdoor — packaged from $1,750 to full-year campaign engines — built so every dollar spent makes your business more recognizable, not just briefly louder.",
},
]

SERVICES = [
# ------------------------------------------------ BRANDING & CULTURE IDENTITY
{
"url": "/brand-design/branding-culture-identity/",
"pillar_name": "Brand Design", "pillar_url": "/brand-design/",
"name": "Branding & Culture Identity", "short": "branding & culture identity",
"title": "Branding & Culture Identity in Airdrie | Live Dogs Design Co.",
"meta": "Branding and culture identity for Airdrie small businesses — values, voice, and visuals aligned so your team and your customers believe the same story.",
"h1": "Branding &amp; culture identity: a brand your team <em>believes in</em>",
"lede": "A brand isn't what you say about yourself — it's what your crew repeats when you're not in the room. We align your values, voice, and visuals into one identity that recruits customers and keeps your best people proud of the shirt they wear.",
"pull": "Culture is the brand your employees experience. Customers can always tell.",
"about_company": P(
  "Of the four worlds Live Dogs draws from, this service leans hardest on the local church — not in doctrine, but in craft: nothing gathers people around a shared identity better. We've seen what happens when a group knows exactly what it stands for, and we've spent nearly a decade translating that into business branding for companies across Airdrie and the Calgary region.",
  "Most agencies stop at the visual layer. We don't, because we've watched beautiful rebrands die in the parking lot — the logo changed but the crew never bought in, and customers felt the gap between the promise and the experience. Our approach treats your internal culture and your external brand as one project, because to your customer, they are.",
  "We're storytellers by conviction. Before we touch visuals we dig for the narrative that's already true about your company — how you started, what you refuse to do, why your best customers stay. That story becomes the filter for every decision that follows, from tagline to team values to the tone of your invoices. It's the difference between decoration and identity."),
"detail_heading": "Branding & culture identity, in detail",
"detail": P(
  "The work starts with discovery: interviews with you and, where it helps, your team and best customers. We map your values as they're actually lived — not aspirational poster words — and define your voice: how your company talks when it's being most itself. Then we build the visual system around that truth: logo direction, colour, typography, and the imagery rules that keep everything coherent.",
  "Deliverables scale with your package, from a focused identity refresh inside <strong>Logo Design +</strong> ($1,350) to the full <strong>Brand Identity Max</strong> ($3,450–$5,650) with brand guidelines ($300–$500) that document the whole system — values, voice, logo usage, palette, and type — so anyone who touches your brand keeps it consistent.",
  "The culture side is practical, not fluffy: language your team can actually use with customers, internal rollout of the new identity so your people hear the story first, and swag they'll genuinely wear. When the crew believes it, the market believes it — that's the multiplier most branding projects leave on the table."),
"offers": [("Brand Identity Max", "3450"), ("Brand guidelines", "300")],
"faqs": [
  ("What's the difference between branding and culture identity?",
   "Branding is how your company looks and speaks to the market; culture identity is what your team believes and repeats inside the walls. We build them together because customers always sense when they don't match."),
  ("How much does a brand identity cost?",
   "A focused identity starts inside our $1,350 Logo Design + package, and the full Brand Identity Max with guidelines, icons, swag and photography patterns runs $3,450–$5,650."),
  ("We already have a logo — is this still useful?",
   "Very often, yes. If the mark is good we keep it and build the missing system around it: voice, values, guidelines, and the consistency that makes the logo mean something."),
],
"summary": "Branding & culture identity aligns what your company says, shows, and believes into one system — story-first discovery, a lived set of values, a defined voice, and the visual identity to carry it — so your team and your customers finally tell the same story about you.",
},
# ------------------------------------------------------------------ LOGO DESIGN
{
"url": "/brand-design/logo-design/",
"pillar_name": "Brand Design", "pillar_url": "/brand-design/",
"name": "Logo Design", "short": "logo design",
"title": "Logo Design in Airdrie | Hand-Drawn, No Robot Logos | Live Dogs",
"meta": "Custom logo design in Airdrie, AB from $750 — word-mapping, hand-drawn concepts, and digital refinement. No AI templates, no robot logos.",
"h1": "Logo design in Airdrie — drawn by hand, <em>built to last</em>",
"lede": "Your logo is the hardest-working employee you'll ever hire: on every truck, invoice, and hat, saying who you are before you get a word in. We design it the craftsman's way — word maps and pencil sketches before pixels — from $750.",
"pull": "You're not getting a robot-made logo. You're getting a mark someone sweat over.",
"about_company": P(
  "Logo design is where Live Dogs started and it's still the craft we're known for across Airdrie and the Calgary area. Our own teeth mark came the same way yours will: sketched, argued over, refined, and tested at every size from favicon to fleet wrap — so we hold your mark to the standard we hold our own.",
  "We work like craftsmen because we learned from worlds where shortcuts show. A chef doesn't microwave the sauce; we don't type your company name into a generator and pick the least-bad option. Every engagement begins with word-mapping — the associations, feelings, and promises your business owns — then moves through hand-drawn concepts before anything touches a screen.",
  "That process matters more now, not less. AI tools have flooded the market with logos that look fine for a week and forgettable forever. The businesses that stand out in a crowded local market are the ones whose marks carry an actual idea. With twenty-plus custom logos behind us and a hundred percent of those clients happy, our portfolio is our argument: distinct beats decorated, every time."),
"detail_heading": "Logo design, in detail",
"detail": P(
  "The process runs in four stages. <strong>Word-mapping:</strong> we mine your business for the ideas your mark should own. <strong>Hand-drawn concepts:</strong> loose, honest sketches that explore directions cheaply and bravely. <strong>Digitization:</strong> the strongest concepts are rebuilt as precise vector art. <strong>Mockups:</strong> you see the finalists on trucks, signs, cards and shirts — where a logo actually lives — before you choose.",
  "Logo design alone is <strong>$750</strong>. Most clients choose <strong>Logo Design Basic ($900)</strong>, which adds business cards and three social images so the new mark launches with momentum, or <strong>Logo Design + ($1,350)</strong>, which adds the full layout system (icon, horizontal, vertical), a custom typeface, and logo animation for video and web.",
  "You receive every file format your future printer, embroiderer, or web developer will ever ask for — vector masters, transparent PNGs, and colour variants for light and dark backgrounds — plus usage notes so the mark never gets stretched, squished, or lime-greened by a well-meaning nephew."),
"offers": [("Logo design", "750"), ("Logo Design Basic", "900"), ("Logo Design +", "1350")],
"faqs": [
  ("How much does a logo design cost?",
   "Logo design alone is $750; the Logo Design Basic package with business cards and social images is $900, and Logo Design + with layouts, a custom typeface, and animation is $1,350."),
  ("How many concepts do I get to see?",
   "You'll see the strongest directions from our sketch round — typically two to three genuinely different concepts, presented as real-world mockups, with the reasoning behind each one."),
  ("What files do I get when it's done?",
   "Everything: vector masters (AI/SVG/EPS), print-ready PDFs, transparent PNGs, and light/dark colour variants, plus simple usage guidelines so the logo stays sharp everywhere."),
],
"summary": "Live Dogs logo design is a four-stage craft — word-mapping, hand-drawn concepts, vector digitization, and real-world mockups — starting at $750, with packages to $1,350 that add layouts, custom type, and animation. No templates, no AI slurry: a mark with an idea in it, built to outlive trends.",
},
# --------------------------------------------------------------- BUSINESS CARDS
{
"url": "/brand-design/business-cards/",
"pillar_name": "Brand Design", "pillar_url": "/brand-design/",
"name": "Business Cards", "short": "business cards",
"title": "Business Card Design in Airdrie | Print That Lands | Live Dogs",
"meta": "Business card design in Airdrie from $75 — on-brand, print-ready cards that turn a handshake into a saved contact and a callback.",
"h1": "Business cards: the handshake <em>that stays behind</em>",
"lede": "Ninety seconds after you leave, your card is still on the counter making your case. For $75 as an add-on — or bundled into every logo package — we design cards people keep, because in the trades a good card still closes work.",
"pull": "A card is the smallest billboard you'll ever buy — and the only one people pocket.",
"about_company": P(
  "It would be easy for a design agency to sneer at business cards in 2026. We don't, because we serve Airdrie's trades and small businesses, and we've watched how work actually gets won here: a job site conversation, a quick recommendation, a card pressed into a hand. When the moment comes, the card either looks like a company worth calling or it doesn't.",
  "Print is also where our craft standards show fastest. The culinary world taught us plating — the same food reads completely differently depending on presentation. A flimsy, cluttered card plates your business like a gas-station sandwich. Good stock, clear hierarchy, and a confident mark plate it like something worth paying for.",
  "Because we design your cards inside your larger identity, they never drift off-brand. Same palette, same typography, same voice as your signage and website — which is exactly the consistency that makes a small business feel established. It's a $75 line item that quietly does the work of a much bigger marketing budget every time it changes hands."),
"detail_heading": "Business card design, in detail",
"detail": P(
  "We design both faces of the card with intention. The front carries your mark with room to breathe; the back works — phone, email, services, and whatever your customer needs in the moment they're deciding to call. Every element earns its place; clutter is the enemy of the callback.",
  "Cards are <strong>$75</strong> as a standalone design and included in <strong>Logo Design Basic ($900)</strong>, so a new identity always launches with print in hand. We deliver press-ready files with bleed and safe margins, set up for whichever local or online printer you prefer, and we'll gladly recommend stocks and finishes — a thick matte card with a spot of colour outperforms glossy clutter nearly every time.",
  "Need more than cards? The same care extends to your wider stationery — quote forms, invoices, letterhead, thank-you inserts — priced within our mix-and-match model. Every printed piece is one more place your brand either compounds or leaks; we make sure it compounds."),
"offers": [("Business card design", "75")],
"faqs": [
  ("How much does business card design cost?",
   "Card design is $75, or included in the $900 Logo Design Basic package. Printing is billed by your printer of choice — we hand over press-ready files and stock recommendations."),
  ("Do you handle the printing too?",
   "We prepare print-ready files with bleed and margins and can recommend trusted local and online printers, so you get trade pricing without a markup from us."),
  ("Are business cards still worth it?",
   "In local service businesses, absolutely — jobs are still won on driveways and job sites. A well-designed card makes you the contractor whose number actually gets saved."),
],
"summary": "Business card design at Live Dogs is $75 of disproportionate leverage — both faces designed with intention, perfectly on-brand, delivered press-ready with printer recommendations. Included in every logo package, because a new identity should land in people's hands, not just their feeds.",
},
# ------------------------------------------------------------------------ SWAG
{
"url": "/brand-design/swag/",
"pillar_name": "Brand Design", "pillar_url": "/brand-design/",
"name": "Swag & Apparel", "short": "swag & apparel",
"title": "Branded Swag & Apparel in Airdrie | Shirts, Hats, Hoodies | Live Dogs",
"meta": "Branded apparel design in Airdrie — shirts, hats and hoodies your crew actually wears. Swag packages from $250, designed to your brand.",
"h1": "Swag your crew <em>actually wants to wear</em>",
"lede": "A crew in matching, well-designed gear reads as organized, established, and worth the quote — on the job site, at the supply store, in every customer's driveway. We design shirts, hats and hoodies from $250 that turn your team into your best ad channel.",
"pull": "Nobody wears an ugly company shirt on Saturday. That's the whole test.",
"about_company": P(
  "Live Dogs prints its own teeth on shirts and hats, and we hold client swag to the same bar: if the crew wouldn't wear it off the clock, the design isn't done. That standard comes from our exploration world — good gear gets chosen again and again because it earns its place. Your branded apparel should pass the same test.",
  "Swag sits at the crossroads of brand design and advertising, which is why we treat it as strategy rather than merch. A hoodie your foreman wears to the rink on Sunday is an ad impression money can't easily buy — local, trusted, and repeated weekly. Multiply that across a crew and the math beats a lot of paid placements.",
  "Because the apparel is designed inside your brand system, it never looks like clip-art on a blank. Placement, scale, colourways, and which lockup goes where — cap front versus chest versus sleeve — are all decisions we make deliberately, so the twenty-dollar shirt carries the same authority as the truck wrap."),
"detail_heading": "Swag & apparel, in detail",
"detail": P(
  "We design for real garments, not mockup fantasies: tees, work shirts, caps, toques, and hoodies from blanks that hold up to job-site wash cycles. Artwork is prepared for the right decoration method — screen print, embroidery, or heat transfer — because a design that embroiders beautifully can print terribly, and vice versa.",
  "Pricing is straightforward: <strong>five shirts or hats for $250–$350</strong>, <strong>five hoodies for $700</strong>, and larger swag programs at <strong>$500–$1,000</strong> inside Brand Identity Max. Apparel also slots into our Ad packages, because crew gear is advertising — the kind that gets worn into every coffee shop in Airdrie.",
  "We handle the fiddly production details — colour matching to your palette, decoration-ready file prep, and coordinating with your printer or ours. You approve a real proof before anything runs, and reorders are painless because the system is documented in your brand files."),
"offers": [("5 shirts or hats", "250"), ("5 hoodies", "700"), ("Swag program", "500")],
"faqs": [
  ("How much does branded apparel cost?",
   "Design plus five shirts or hats runs $250–$350, five hoodies $700, and full swag programs $500–$1,000 inside our Brand Identity Max package."),
  ("Can you match our exact brand colours on clothing?",
   "Yes — we colour-match garments and decoration to your palette and choose the print or embroidery method that reproduces it faithfully on each fabric."),
  ("What if we just need our current logo put on shirts?",
   "We can absolutely do that — we'll prep your existing mark properly for the garment and placement so it looks intentional, not ironed-on."),
],
"summary": "Live Dogs swag is brand strategy you can wear: shirts, hats and hoodies designed inside your identity system, prepped correctly for print or embroidery, from $250 for five pieces. If your crew reaches for it on the weekend, your advertising is working while you sleep.",
},
# --------------------------------------------------------------- SOCIAL MEDIA
{
"url": "/advertising/social-media-posts/",
"pillar_name": "Advertising", "pillar_url": "/advertising/",
"name": "Social Media Posts", "short": "social media posts",
"title": "Social Media Post Design in Airdrie | On-Brand Content | Live Dogs",
"meta": "Social media post design for Airdrie small businesses — 12 on-brand images for $600. Stay in front of your audience without eating your evenings.",
"h1": "Social media posts without the <em>nightly scramble</em>",
"lede": "It takes about ten touches before someone trusts your brand — and social media is the cheapest touch there is. We design batches of on-brand posts (12 images for $600) so you stay in front of Airdrie without spending your evenings fighting Canva.",
"pull": "Make social media work for you — not the other way around.",
"about_company": P(
  "We built this service after watching too many good Airdrie business owners burn their evenings making graphics. The admin becomes the social media team, the posts drift off-brand, the feed goes quiet during busy season — precisely when customers are looking. Live Dogs exists to lift that weight, and social content is one of the heaviest, most constant pieces of it.",
  "Our spirited side runs this department. Feeds are loud, and polite wallpaper gets scrolled past; posts need energy, a point of view, and the visual consistency that makes someone stop and think 'that's them again.' Because we're a brand agency first, every post we design compounds your identity — same palette, type, and voice as your trucks and your website.",
  "We're also realists about what social is for. For a local service business it's not about going viral; it's about being reliably, recognizably present so that when the furnace dies or the fence sags, you're the name they already feel they know. Consistency beats cleverness — and consistency is exactly what a batch system delivers."),
"detail_heading": "Social media posts, in detail",
"detail": P(
  "The core offer is simple: <strong>twelve custom images for $600</strong> — a month or more of presence, designed in your brand system and sized for the platforms you actually use. A starter <strong>three-pack ($75)</strong> is included in Logo Design Basic so a new identity hits the feed on day one.",
  "Each batch starts with a short planning pass: what's coming up for the business — seasonal pushes, hiring, finished projects worth showing off — and what mix of post types serves it: proof-of-work, offers, team, and trust-builders like reviews. Then we design the set at once, so your month is handled in one approval instead of thirty tiny decisions.",
  "Posts arrive ready to publish, with suggested captions in your brand voice if you want them. Pair the batch with our email campaigns and the same creative works twice — one story, told everywhere your customer looks. That's how small budgets act big."),
"offers": [("12 social images", "600"), ("3 social images", "75")],
"faqs": [
  ("How much do social media posts cost?",
   "Twelve custom-designed images run $600 — that's a month or more of consistent presence. A three-image starter pack is $75 and comes inside Logo Design Basic."),
  ("Do you post them for us or just design them?",
   "The core package delivers ready-to-publish designs with optional captions; if you want scheduling and posting handled too, we'll scope that as part of an ongoing advertising engagement."),
  ("What should a small business even post about?",
   "Finished work, your team, honest reviews, and seasonal offers — proof over polish. We plan the mix with you each batch so the feed sells quietly instead of shouting."),
],
"summary": "Live Dogs designs social media posts in on-brand batches — twelve images for $600, planned around your real business calendar and delivered ready to publish — so your company stays visibly, consistently present in the Airdrie feed while you get your evenings back.",
},
# -------------------------------------------------------------- EMAIL MARKETING
{
"url": "/advertising/email-marketing/",
"pillar_name": "Advertising", "pillar_url": "/advertising/",
"name": "Email Marketing", "short": "email marketing",
"title": "Email Marketing for Airdrie Small Businesses | Live Dogs Design Co.",
"meta": "Email marketing campaigns for Airdrie businesses — designed, written and built to get opened. 3 campaigns for $900, on-brand and measurable.",
"h1": "Email marketing: the audience <em>you actually own</em>",
"lede": "Algorithms rent you their audience; your email list is yours forever. We design and write campaigns that get opened, read, and clicked — three campaigns for $900 — turning past customers into repeat work and referrals.",
"pull": "Your list is the only marketing asset the platforms can't take away.",
"about_company": P(
  "Live Dogs treats email as storytelling with a measurable ending. Of our four worlds, this one leans on the storyteller: an inbox is a quiet room, not a noisy feed, and the businesses that respect that — writing like a person, designing with restraint — get read while the shouty stuff gets archived.",
  "We came to email through our clients' actual numbers. For local service businesses, the cheapest job you'll ever win is from someone who already hired you — yet most small businesses never email their past customers at all. That list you've quietly accumulated in your invoicing software is an asset with real dollar value, sitting idle.",
  "Because we build brands first, our emails don't look like templates with your logo dropped in. Typography, colour, voice, and imagery all match your identity, so the email that lands in an inbox feels like the same company that wrapped the truck and built the website. Consistency is trust, and trust is open rates."),
"detail_heading": "Email marketing, in detail",
"detail": P(
  "A Live Dogs campaign covers the full craft: strategy (who gets it, why now, what's the one action), copywriting in your brand voice, design that renders cleanly in every inbox, and the send setup in your platform of choice. Subject lines get real attention — the best email in the world dies unopened.",
  "Pricing is package-simple: <strong>three campaigns for $900</strong> inside Ad +, or <strong>nine campaigns for $2,500</strong> in Ad Max — enough for a real seasonal rhythm: spring push, summer reminder, fall booking, winter thank-you, and the offers between. One-off campaigns can be scoped through our mix-and-match model.",
  "Every send reports back in plain numbers — opens, clicks, replies, booked work where we can trace it — and each campaign teaches the next one. Over a year, that compounding loop is how a modest list quietly becomes one of your most profitable channels."),
"offers": [("3 email campaigns", "900"), ("9 email campaigns", "2500")],
"faqs": [
  ("How much does email marketing cost?",
   "Three fully designed and written campaigns run $900; nine campaigns — a full seasonal rhythm — are $2,500 inside our Ad Max package."),
  ("We only have a small email list — is it worth it?",
   "Yes. A few hundred past customers is a goldmine for a service business, because they've already trusted you once. Repeat and referral work from a small list routinely beats cold advertising."),
  ("Will you write the emails or just design them?",
   "Both — strategy, copywriting in your brand voice, design, and send setup. You approve everything before it goes out."),
],
"summary": "Email marketing at Live Dogs is designed, written, and measured end-to-end — three campaigns for $900 or nine for $2,500 — aimed at the audience you already own: past customers who'll hire you again if you simply stay worth remembering.",
},
# ---------------------------------------------------------- VIDEO STORYTELLING
{
"url": "/advertising/video-storytelling/",
"pillar_name": "Advertising", "pillar_url": "/advertising/",
"name": "Video Storytelling", "short": "video storytelling",
"title": "Video Storytelling & Motion Ads in Airdrie | Live Dogs Design Co.",
"meta": "Video storytelling for Airdrie businesses — motion graphics ads from $1,000 and directed brand videos from $5,000. Stories that stop the scroll.",
"h1": "Video storytelling that <em>stops the scroll</em>",
"lede": "Nothing builds trust faster than seeing real people do real work well. From motion-graphics ads at $1,000 to directed brand films at $5,000, we turn what your company actually does into stories your market stops to watch.",
"pull": "People skip ads. They don't skip stories.",
"about_company": P(
  "Video is where all four Live Dogs worlds meet at once: the storyteller shapes the narrative, the explorer finds the unexpected angle, the culinary eye plates every frame, and the church taught us how a room leans in when a story is told honestly. That combination is why our video work feels crafted rather than manufactured.",
  "We built this service for the businesses we serve — trades and local companies whose best marketing asset is the work itself. A furnace swap, a framing job, a finished yard: shot and told well, that's more persuasive than any stock-footage montage, because your customer can see themselves in it.",
  "As with everything we make, brand consistency is the quiet engine. Your video opens, moves, and sounds like your company — same palette, type, and voice as the website and the trucks — so every view compounds recognition. One story, told everywhere, is worth ten disconnected clever ideas."),
"detail_heading": "Video storytelling, in detail",
"detail": P(
  "We work at two altitudes. <strong>Motion graphics ads ($1,000)</strong> animate your brand — logo, type, message — into sharp 15–30 second spots built for social feeds and digital placements. They're the fastest way to look established online, and they slot straight into our Ad + package.",
  "<strong>Directed video ads ($5,000)</strong> are the full craft: concept, script, shoot day at your business, direction, edit, colour, and sound. Real crew, real customers, real work — cut into a story with a spine. Inside Ad Max, video anchors a year-long campaign ($10,000–$15,000) where one shoot feeds months of content across every channel.",
  "Every project ships in the formats the platforms want — vertical for Reels and TikTok, square and horizontal for feeds and YouTube — plus cutdowns so a single story works as a thirty-second ad, a six-second bumper, and a website hero. You buy the story once; it works everywhere."),
"offers": [("Motion graphics ad", "1000"), ("Directed video ad", "5000")],
"faqs": [
  ("How much does a video ad cost?",
   "Motion-graphics ads run $1,000; a fully directed video ad — script, shoot, edit, sound — is $5,000, with year-long campaign engines from $10,000."),
  ("We're not comfortable on camera — can this still work?",
   "Completely. The work itself is the star: hands, tools, before-and-afters, satisfied customers. We direct everything so nobody has to perform — just do the job well."),
  ("Where will the videos actually run?",
   "Everywhere your audience is: Instagram, TikTok, Facebook, YouTube, your website, and digital ad placements. We deliver every format and cutdown so one story covers all of it."),
],
"summary": "Video storytelling at Live Dogs runs from $1,000 motion-graphics ads to $5,000 directed brand films — concept through final cut, delivered in every format the platforms demand — built on the belief that your real work, told honestly, out-sells any stock-footage ad.",
},
]

# ---- Depth pass: extra paragraphs to reach the 250/300-word spec ----
EXTRA = {
"/brand-design/": (
  "That standard shapes who we work with, too. Our best projects come from decisive owners — often in the trades — doing one to two million in revenue, who know their business cold and trust us to know ours. The way an electrician trusts a painter with the paint, they hand us the brand and get back to the work only they can do. If that sounds like you, we'll get along famously, and your brand will show it.",
  "A typical engagement runs like this: a kickoff conversation, a word-mapping session, sketch review, digital concepts presented as real-world mockups, one or two refinement rounds, and final delivery of every file your printer, embroiderer, or web developer will ever request. You're consulted at each gate, never ambushed at the end. And because the process is documented, the identity survives handoffs — new staff, new vendors, new trucks — without drifting into the mismatched mess that quietly costs small businesses credibility every single day."),
"/web-design/": (
  "There's a mission behind the model, too: we aim to help 24 small businesses refresh their brand and visibility by the end of 2026. A website is usually where that visibility becomes measurable — calls booked, quotes requested, directions tapped. So we treat your site as the working end of your brand, the place where recognition finally turns into revenue, and we hold it to that standard every month you're with us.",
  "Behind the design, the technical work is done properly: semantic structure so search engines understand every page, responsive layouts tested on real phones, image optimization so pages load fast on rural connections, and analytics wired in so you can see what's working. We register your business correctly with Google, connect your reviews, and keep the site's content fresh — because Google rewards tended sites and quietly buries abandoned ones. It's unglamorous work, and it's exactly why our clients' sites keep climbing while template sites stall."),
"/advertising/": (
  "We also believe advertising should respect the person seeing it. The guide inside our own walls says we don't shock just for the reaction — we rise above the noise so a meaningful message stands out the way it should. That restraint is a competitive advantage in a feed full of desperation: your ads read as confident because the brand behind them actually is.",
  "Every engagement begins with a simple audit: where are you visible today, what does it cost, and what's it returning? From there we build a calendar — seasonal pushes, steady presence, and the occasional big swing — and produce all the creative in batches so quality stays high and costs stay predictable. You approve everything before it runs. Then we measure, report in plain language, and adjust. Advertising isn't a slot machine; run this loop for a year and you'll know precisely which dollars work."),
"/brand-design/branding-culture-identity/": (
  "It's also the work our mission depends on. We've committed to helping 24 small businesses — each worth one to two million dollars — refresh their branding by the end of 2026. Culture identity is where those refreshes either take root or wither, so we invest the discovery time up front and it pays back for years.",
  "Timeline-wise, expect four to eight weeks depending on how deep we go and how quickly decisions come back. The rhythm is steady: discovery interviews, a story-and-values draft you react to, visual territory exploration, then system build-out and documentation. We present reasoning with every round — never a mood board dump — so choices get easier as we go instead of harder. By the end, you hold a playbook your whole team can run: what you say, how you look, and why it's true. That's what makes the next hire, the next truck, and the next ad all feel unmistakably like you."),
"/brand-design/logo-design/": (
  "We're also stubborn about longevity. Trends are loud and short; your mark has to survive a decade of trucks, signage, and reprints. So we test every concept against time: will this still look confident when the gradient fad dies? Marks built on ideas age well; marks built on effects age like milk. We build on ideas.",
  "Timeline: most logo projects run two to four weeks from kickoff to final files, driven mostly by how fast feedback returns. You'll be consulted at every gate — sketches, digital drafts, refinement — so the final reveal is a confirmation, not a gamble. And when the mark is done, it plugs straight into the rest of the system: business cards launch it, swag wears it, the website carries it, and our brand guidelines document exactly how to keep it sharp. A logo isn't the whole brand, but everything else stands on it — so we make it load-bearing."),
"/brand-design/business-cards/": (
  "There's a rhythm to how cards fit our larger promise, too. Our mission is to help two dozen small businesses become more visible by the end of 2026 — and visibility isn't only digital. It's the counter at the supply shop, the community board at the rink, the wallet of the customer who swears by you. Cards live there.",
  "The process is quick and painless: we design from your existing identity (or build the identity first if you're starting fresh), you review a proof, and we deliver press-ready PDFs with bleed, safe margins, and colour profiles set for your chosen printer. Turnaround is typically a few days, not weeks. We'll also advise on quantities and finishes so you don't overbuy — five hundred great cards beat five thousand mediocre ones. When you reorder or add a new hire, the files are documented and ready, so consistency never depends on anyone's memory."),
"/brand-design/swag/": (
  "Swag also feeds the culture side of our branding work: a crew that's proud of the gear is a crew that believes the story, and customers can feel that belief from the driveway. It's why apparel shows up in our biggest identity packages — it's the brand made wearable, the values with sleeves.",
  "The process respects your time: we pull artwork from your brand system, propose garments and placements, and show you real proofs before anything is decorated. We coordinate production with trusted decorators — or your preferred shop — and document the specs so reorders take one email. Sizing runs, seasonal drops for toques and tees, and new-hire kits are all easy once the system exists. The goal is simple: gear that shows up on job sites Monday and hockey rinks Saturday, quietly compounding your brand every place a billboard could never reach."),
"/advertising/social-media-posts/": (
  "This service also connects straight to our culture belief: what you show is more important than what you say. A feed of real jobs, real people, and consistent design shows competence without claiming it — and in a trust business, shown competence is the whole sale.",
  "Logistics are simple: a short planning call or message thread, one batch designed and delivered together, one approval pass, and you're stocked for the month. Posts arrive sized for Instagram, Facebook, and wherever else you show up, with captions drafted in your voice if you want them. When a batch teaches us something — which posts got calls, which got crickets — the next batch gets smarter. And if you'd rather never touch the scheduler at all, we'll fold posting and management into a broader advertising engagement so the whole channel runs without you."),
"/advertising/email-marketing/": (
  "Email also rewards the patient, which suits how we think. Our advertising philosophy is compounding — the earlier you start and the steadier you show up, the greater the growth. A list nurtured quarterly for two years becomes an asset competitors simply cannot buy, borrow, or outbid you for.",
  "Getting started is lighter than most owners expect. We help you gather the addresses you already have — invoicing software, quote requests, contact forms — into a proper list with consent handled correctly under Canadian anti-spam rules. Then we set the rhythm: which seasons drive your business, what your customers should hear before each one, and which single action every send should ask for. You approve copy and design in one pass. Within two or three campaigns you'll have open-rate and click benchmarks specific to your audience — real numbers to steer by instead of industry folklore."),
"/advertising/video-storytelling/": (
  "Video is also where our mission gets its proof. Helping 24 businesses become more visible by 2026 means showing, not telling — and nothing shows like footage of your crew doing the work right. It's the difference between claiming quality and letting people watch it happen.",
  "Production is built around your schedule, not a film crew's ego: shoot days are planned tight, on your site, with minimal disruption to actual work. From one well-planned day we typically cut a hero piece plus a bench of shorter cuts — enough to feed your social channels and ad placements for months. Everything is colour-graded and sound-mixed to your brand, captioned for silent viewing, and delivered organized so you're never hunting for the right file. When the campaign evolves, the footage library keeps paying — one shoot, many stories, told your way."),
}
EXTRA2 = {
"/brand-design/": (None,
  "One more promise: nothing we build locks you in. Your files, your fonts, your guidelines — all yours, delivered and documented, usable with any printer or developer you ever choose. Great brands are owned, not rented, and we build yours accordingly."),
"/web-design/": (None,
  "And when your business changes — new service, new crew, new town — the site changes with it inside your monthly rate. Growth shouldn't trigger a renegotiation; it should just show up on the website that same week, looking like it was always planned."),
"/advertising/": (None,
  "If you're not sure where to begin, begin with the audit conversation. It costs you an hour, we'll tell you honestly what to keep and what to cut, and you'll leave with a clearer picture of your marketing than most businesses ever get."),
"/brand-design/branding-culture-identity/": (None,
  "And if parts of your culture are still forming — most growing companies are mid-story — that's not a blocker, it's the opportunity. We'd rather help you name what you're becoming than laminate what you were."),
"/brand-design/logo-design/": (None,
  "One quiet bonus: a documented mark saves money forever after. Every future designer, printer, and sign shop starts from clean files and clear rules instead of redrawing from a fuzzy JPEG — so the $750 you invest here keeps paying you back on every job that touches your brand."),
"/brand-design/business-cards/": (None,
  "And if you're between identities right now, cards are a smart forcing function: designing a great card surfaces every decision your brand needs to make anyway — mark, colour, type, tone — at the smallest, cheapest possible scale."),
"/brand-design/swag/": (None,
  "Swag also makes the best thank-you: a hoodie for the customer who referred three jobs beats any discount code, and it keeps advertising long after the thank-you is forgotten. We'll help you plan gear as gratitude, not just uniform."),
"/advertising/social-media-posts/": (None,
  "And because every image is built from your brand system, the batches keep their value: this month's posts still look like your company next year, and your feed reads as one long, confident story instead of a scrapbook of experiments."),
"/advertising/email-marketing/": (
  "It suits our storytelling roots too: an email is a small chapter, sent to people who already chose to hear from you. Written well, it reads less like marketing and more like a good neighbour with useful news — which is exactly what a local business should be.",
  "The final piece is deliverability — the unglamorous craft of actually reaching inboxes. Clean list hygiene, proper sender authentication, and honest subject lines keep you out of spam folders and in good standing, so every campaign you invest in actually gets its chance to work."),
"/advertising/video-storytelling/": (
  "We also keep it human. Polished doesn't mean corporate: the best local video feels like meeting the crew, not watching a commercial. That warmth is a Live Dogs signature, and it's why our clients' videos get shared by the very customers who appear in them.",
  "Every video project also ships with a simple usage plan: where each cut runs, in what order, and for how long — so the film works as a campaign, not a one-week spike. Great footage deserves a schedule, and we deliver both together."),
}
for coll in (PILLARS, SERVICES):
    for x in coll:
        c_extra, d_extra = EXTRA[x["url"]]
        c2, d2 = EXTRA2[x["url"]]
        x["about_company"] += P(c_extra) + (P(c2) if c2 else "")
        x["detail"] += P(d_extra) + P(d2)

# ============================== HOME ==============================

HOME_SCHEMA = [{
    "@context": "https://schema.org",
    "@type": "ProfessionalService",
    "name": "Live Dogs Design Co.",
    "description": "Brand agency in Airdrie, Alberta — brand design, logo design, web design and advertising for small businesses.",
    "url": BASE + "/",
    "logo": FAVICON,
    "image": f"{BASE}/assets/og-banner.jpg",
    "address": {"@type": "PostalAddress", "addressLocality": "Airdrie", "addressRegion": "AB", "addressCountry": "CA"},
    "areaServed": ["Airdrie", "Calgary", "Rocky View County"],
    "priceRange": "$$",
    "sameAs": [
        "https://www.instagram.com/livedogsdesignco",
        "https://www.linkedin.com/in/jesse-fehr/",
        "https://www.tiktok.com/@livedogsdesignco",
    ],
    "hasOfferCatalog": {
        "@type": "OfferCatalog", "name": "Design services",
        "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": n}}
            for n in ["Brand Design", "Logo Design", "Web Design", "Advertising",
                      "Social Media Posts", "Email Marketing", "Video Storytelling",
                      "Business Cards", "Swag & Apparel"]
        ],
    },
}]

SVC_CARDS = [
    ("Branding & Culture Identity", "/brand-design/branding-culture-identity/", "Brand Design",
     "Values, voice, and visuals aligned — a brand your team believes and your market remembers."),
    ("Logo Design", "/brand-design/logo-design/", "Brand Design",
     "Word maps, pencil sketches, digital craft. Marks with an idea in them, from $750."),
    ("Web Design", "/web-design/", "Web Design",
     "Custom, responsive, SEO-ready websites from $299/mo — hosting and updates included."),
    ("Advertising", "/advertising/", "Advertising",
     "Brand-first campaigns across every channel. Ads that compound, not just spend."),
    ("Social Media Posts", "/advertising/social-media-posts/", "Advertising",
     "Twelve on-brand images for $600 — a month of presence without the nightly scramble."),
    ("Email Marketing", "/advertising/email-marketing/", "Advertising",
     "The audience you own. Campaigns designed, written and measured — 3 for $900."),
    ("Video Storytelling", "/advertising/video-storytelling/", "Advertising",
     "Motion ads from $1,000, directed films from $5,000. Stories that stop the scroll."),
    ("Business Cards", "/brand-design/business-cards/", "Brand Design",
     "The handshake that stays behind — designed both sides, press-ready, $75."),
    ("Swag & Apparel", "/brand-design/swag/", "Brand Design",
     "Shirts, hats and hoodies your crew wears on Saturdays. From $250 for five."),
]

svc_cards_html = "".join(
    f'<a class="svc-card reveal" href="{u}"><span class="svc-card__pillar">{p}</span>'
    f'{ICONS.get(u, "")}<h3>{n}</h3><p>{d}</p><span class="svc-card__go">Explore</span></a>'
    for n, u, p, d in SVC_CARDS
)

HOME_FAQS = [
    ("What does a brand agency actually do?",
     "We design how your business looks, sounds, and shows up — logo, website, ads, and everything between — so customers recognize and trust you before you say a word."),
    ("Who do you work with?",
     "Small businesses around Airdrie and the Calgary region — many in the trades — typically doing $1–2M in revenue and hungry to grow. Decisive people who trust experts get our best work."),
    ("What does it cost to work with Live Dogs?",
     "Logos from $750, websites from $299/month, advertising from $1,750 — all published openly on our pricing page, all mix-and-match. No mystery quotes."),
]

HOME_FNAV = float_nav("Explore", [
    ("The four worlds", "#ethos"),
    ("Services", "#services"),
    ("Why us", "#craft"),
    ("Mission", "#mission"),
    ("Questions", "#faq"),
])

CONST_DARK = CONSTELLATION
HOME_BODY = f"""
<section class="hero">
  {CONSTELLATION}
  <div class="wrap">{HOME_FNAV}</div>
  <div class="wrap hero--arch">
    <div>
      <p class="eyebrow reveal">Brand agency · Airdrie, Alberta</p>
      <h1 class="reveal">Your business is too important to be <em>invisible</em></h1>
      <p class="lede hero__lede reveal">We're Live Dogs Design Co. — storytellers, explorers, and craftsmen designing brands that aren't just seen, but <strong>felt</strong>. Branding, logos, websites, and advertising for small businesses that intend to grow.</p>
      <div class="hero__actions reveal">
        <a class="button" href="/start-a-project/">Start a project</a>
        <a class="button button--ghost" href="/pricing/">See pricing</a>
      </div>
    </div>
    <div class="arch-frame reveal">
      <img src="{HERO_IMG}" width="1080" height="1350" fetchpriority="high"
        alt="EZ Plumbing &amp; Heating service vans wearing their Live Dogs fleet rebrand in Airdrie">
    </div>
  </div>
</section>
<hr class="glass-line" style="margin-top:var(--space)">
<section class="section section--dark on-dark" id="ethos">
  <div class="wrap">
    {CONST_DARK}<p class="eyebrow reveal">The Live Dogs ethos</p>
    <h2 class="reveal">We pull from four worlds to build brands <em>with a pulse</em></h2>
    <p class="lede reveal">Storytelling, exploration, culinary arts, and the local church — four crafts that taught us how attention is earned, journeys are made, presentation persuades, and people gather around what they believe.</p>
    <ul class="values">
      <li class="reveal"><h3>Imaginative</h3><p>Visionary and original — layered, unexpected work that pushes creative boundaries instead of decorating the norm.</p></li>
      <li class="reveal"><h3>Relentless</h3><p>Bold and determined. We refuse to settle, and we build brands for people who refuse to settle too.</p></li>
      <li class="reveal"><h3>Harmonious</h3><p>Balanced and emotionally intelligent — every element placed with intention, nothing shouting over the message.</p></li>
      <li class="reveal"><h3>Spirited</h3><p>Energetic and adventurous, full of life. Brands should feel alive, because live dogs beat dead lions.</p></li>
    </ul>
  </div>
</section>
<section class="section" id="services">
  <div class="wrap">
    <p class="eyebrow reveal">What we do</p>
    <h2 class="reveal">Nine crafts. Three disciplines. <em>One story</em> — yours.</h2>
    <p class="lede reveal">Everything below mixes and matches. Start where the need is loudest; the brand system ties it all together.</p>
    <div class="svc-grid">{svc_cards_html}</div>
  </div>
</section>
{TOPO}
<section class="section article" id="craft">
  <div class="wrap">
    <p class="eyebrow reveal">Why Live Dogs</p>
    <h2 class="reveal">The craft approach, close to home</h2>
    <p class="reveal">We put in the time to find the right answer: research first, hand-drawn concepts before anything digital, and honest reasoning behind every recommendation. You're not getting a robot-made logo or a recycled template — you're getting work someone sweat over, from an agency twenty minutes away, priced for small business and packaged to mix and match.</p>
    <blockquote class="pull reveal">An electrician knows to trust the painter with the paint. Trust us with the brand — it's the trade we've mastered.</blockquote>
  </div>
</section>
<section class="section" id="mission" style="padding-top:0">
  <div class="wrap">
    <div class="summary-band reveal">
      <h2>Our mission, in one sentence</h2>
      <p>Help 24 small businesses — each worth $1–2&nbsp;million — refresh their branding to increase visibility and attract more customers by the end of 2026, so they stand out in a crowded market and grow sustainably. Our vision is bigger: small businesses thriving as an economic pillar for our province and nation.</p>
      <a class="button" href="/start-a-project/">Be one of the 24</a>
    </div>
  </div>
</section>
<section class="section article" id="faq" style="padding-top:0">
  <div class="wrap">
    <h2 class="reveal">Straight answers</h2>
    {faq_html(HOME_FAQS)}
  </div>
</section>
<section class="section section--deep cta">
  <div class="wrap">
    <h2 class="reveal">Ready to be <em>impossible to ignore?</em></h2>
    <p class="lede reveal">Tell us where your business is headed. We'll bring the map, the sketchbook, and the fire. Happy to just chat and teach, too — no pressure, no jargon.</p>
    <a class="button reveal" href="/start-a-project/">Start a project</a>
  </div>
</section>
"""

# ============================== PRICING ==============================

PRICING_FNAV_PLACEHOLDER = True
PRICING_BODY_INTRO = f"""
<section class="hero">
  {CONSTELLATION}
  <div class="wrap">
    {float_nav("Jump to", [("Brand design", "#brand-design"), ("Web design", "#web-design"), ("Advertising", "#advertising"), ("Questions", "#faq")])}
    <p class="eyebrow reveal">Pricing · no mystery quotes</p>
    <h1 class="reveal">Honest packages, <em>published openly</em></h1>
    <p class="lede hero__lede reveal">Every price we charge is on this page. Packages mix and match — start where the need is loudest, and never pay twice for something you already have.</p>
  </div>
</section>
"""

PRICING_FAQS = [
    ("Why do some prices show a range?",
     "Ranges reflect real scope differences — a five-page website and a fifteen-page one aren't the same job. You'll always get an exact number in writing before we start."),
    ("Can I combine pieces from different packages?",
     "Yes — mix-and-match is the whole model. Already have great business cards? We'll swap that value toward what you actually need."),
    ("Do you require long contracts?",
     "Project work is project work. Monthly services like web design continue as long as they're earning their keep — that's our retention strategy."),
]


def pricing_page():
    sections = []
    for p in PILLARS:
        sections.append(f"""
<section class="section" id="{p['url'].strip('/').replace('/', '-')}" style="padding-top:0">
  <div class="wrap">
    <p class="eyebrow reveal">{p["name"]}</p>
    <h2 class="reveal">{p["pricing_heading"]}</h2>
    {tiers_html(p["tiers"])}
    <p class="lede reveal" style="margin-top:1.5rem">Full details on the <a href="{p['url']}">{p["name"].lower()} page</a>.</p>
  </div>
</section>""")
    body = PRICING_BODY_INTRO + TOPO + "".join(sections) + f"""
<section class="section article" style="padding-top:0">
  <div class="wrap" id="faq">
    <h2 class="reveal">Pricing questions</h2>
    {faq_html(PRICING_FAQS)}
    <div class="summary-band reveal">
      <h2>In short</h2>
      <p>Logos from $750. Websites from $299/month, hosting and updates included. Advertising from $1,750. Everything mixes and matches, every number is public, and an exact written quote always comes before work begins.</p>
      <a class="button" href="/start-a-project/">Get an exact quote</a>
    </div>
  </div>
</section>
"""
    trail = [("Home", "/"), ("Pricing", None)]
    return shell(
        path="/pricing/",
        title="Pricing | Brand, Web & Advertising Packages | Live Dogs Design Co.",
        meta="Live Dogs Design Co. pricing — logos from $750, websites from $299/mo, advertising from $1,750. Every package published openly. Mix and match.",
        body=crumbs(trail) + body,
        schema=[faq_schema(PRICING_FAQS), crumb_schema(trail)],
    )


# ============================== START A PROJECT ==============================

SAP_BODY = f"""
<section class="hero">
  {CONSTELLATION}
  <div class="wrap">
    {float_nav("Explore", [("Brand design", "/brand-design/"), ("Web design", "/web-design/"), ("Advertising", "/advertising/"), ("Pricing", "/pricing/")])}
    <p class="eyebrow reveal">Start a project</p>
    <h1 class="reveal">Let's make you <em>impossible to ignore</em></h1>
    <p class="lede hero__lede reveal">Tell us about your business and where it's headed. We'll come back with straight answers and an honest scope — and if you're not ready to buy, we're genuinely happy to just chat and teach.</p>
  </div>
</section>
<section class="section" aria-label="Project intake form" style="padding-top:2rem">
  <div class="wrap">
    <div data-tf-widget="tWRedBac" data-tf-opacity="100" data-tf-medium="snippet" style="width:100%;height:560px;"></div>
    <script src="https://embed.typeform.com/next/embed.js"></script>
    <noscript><p>The project form needs JavaScript. Prefer another way? Reach us on
    <a href="https://www.instagram.com/livedogsdesignco">Instagram</a> or
    <a href="https://www.linkedin.com/in/jesse-fehr/">LinkedIn</a>.</p></noscript>
  </div>
</section>
"""

# ============================== WRITE FILES ==============================

pages = {
    "/": (shell(
        path="/",
        title="Live Dogs Design Co. | Brand Agency in Airdrie — Branding, Web Design & Advertising",
        meta="Live Dogs Design Co. is a brand agency in Airdrie, AB. Hand-crafted branding, logo design, web design and advertising for small businesses that intend to grow.",
        body=HOME_BODY, schema=HOME_SCHEMA)),
    "/pricing/": pricing_page(),
    "/start-a-project/": shell(
        path="/start-a-project/",
        title="Start a Project | Live Dogs Design Co.",
        meta="Tell Live Dogs Design Co. about your project — branding, logo design, web design or advertising in Airdrie, AB. Straight answers, honest scope.",
        body=SAP_BODY),
}
for p in PILLARS:
    pages[p["url"]] = pillar_page(p)
for s in SERVICES:
    pages[s["url"]] = service_page(s)


NOTFOUND_BODY = f"""
<section class="hero">
  {CONSTELLATION}
  <div class="wrap">
    {float_nav("Explore", [("Brand design", "/brand-design/"), ("Web design", "/web-design/"), ("Advertising", "/advertising/"), ("Pricing", "/pricing/")])}
    <p class="eyebrow reveal">404 · lost the scent</p>
    <h1 class="reveal">This page has gone <em>exploring</em></h1>
    <p class="lede hero__lede reveal">Even the best trackers lose a trail sometimes. The page you're after has moved, or never existed. Follow the stars back home.</p>
    <div class="hero__actions reveal"><a class="button" href="/">Back to home</a><a class="button button--ghost" href="/start-a-project/">Start a project</a></div>
  </div>
</section>
"""
pages["/404.html"] = shell(path="/404.html", title="Page Not Found | Live Dogs Design Co.",
    meta="That page has gone exploring. Head back to Live Dogs Design Co.", body=NOTFOUND_BODY)

for url, html in pages.items():
    if url == "/":
        path = os.path.join(ROOT, "index.html")
    elif url.endswith(".html"):
        path = os.path.join(ROOT, url.strip("/"))
    else:
        path = os.path.join(ROOT, url.strip("/"), "index.html")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(html)
    print(f"wrote {path}")

# sitemap + robots
urls = sorted(u for u in pages.keys() if not u.endswith(".html"))
sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    sm.append(f"  <url><loc>{BASE}{u}</loc></url>")
sm.append("</urlset>")
with open(os.path.join(ROOT, "sitemap.xml"), "w") as f:
    f.write("\n".join(sm))
with open(os.path.join(ROOT, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
print("wrote sitemap.xml, robots.txt")
print(f"\n{len(pages)} pages generated.")
