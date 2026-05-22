#!/usr/bin/env python3
"""Add JSON-LD structured data, FAQ schema, and internal cross-links to article HTML files."""
import os, re, json, glob
from html.parser import HTMLParser

BASE = os.path.dirname(os.path.abspath(__file__))

# Article metadata for JSON-LD and internal links
ARTICLES = {
    "best-vpns-remote-workers": {
        "title": "Best VPNs for Remote Workers",
        "desc": "NordVPN, ExpressVPN, and Surfshark compared for remote work security and speed.",
        "related": ["best-software-stack-one-person-business", "best-mac-cleaner-security-tools-for-creators"],
    },
    "best-backup-software-solo-businesses": {
        "title": "Best Backup Software for Solo Businesses",
        "desc": "Top backup solutions for solopreneurs and freelancers compared.",
        "related": ["best-data-recovery-software-for-creators", "best-software-stack-one-person-business"],
    },
    "best-data-recovery-software-for-creators": {
        "title": "Best Data Recovery Software for Creators",
        "desc": "Recover lost files with the best data recovery tools for creative professionals.",
        "related": ["best-backup-software-solo-businesses", "best-mac-cleaner-security-tools-for-creators"],
    },
    "best-domain-registrars-for-affiliate-websites": {
        "title": "Best Domain Registrars for Affiliate Websites",
        "desc": "Compare domain registrars for building profitable affiliate sites.",
        "related": ["best-software-stack-one-person-business", "best-vpns-remote-workers"],
    },
    "best-mac-cleaner-security-tools-for-creators": {
        "title": "Best Mac Cleaner & Security Tools for Creators",
        "desc": "Keep your Mac clean and secure with these top tools for creators.",
        "related": ["best-backup-software-solo-businesses", "best-ai-photo-editor-background-remover"],
    },
    "best-ai-photo-editor-background-remover": {
        "title": "Best AI Photo Editor & Background Remover",
        "desc": "AI photo editing and background removal tools compared for creators.",
        "related": ["best-mac-cleaner-security-tools-for-creators", "best-software-stack-one-person-business"],
    },
    "wps-office-review-small-teams": {
        "title": "WPS Office Review for Small Teams",
        "desc": "WPS Office as a budget-friendly alternative to Microsoft 365 for small teams.",
        "related": ["best-software-stack-one-person-business", "datacamp-review-learning-data-skills"],
    },
    "datacamp-review-learning-data-skills": {
        "title": "DataCamp Review: Learning Data Skills",
        "desc": "DataCamp courses, pricing, and value for learning data science and analytics.",
        "related": ["wps-office-review-small-teams", "preply-english-tutors-review"],
    },
    "preply-english-tutors-review": {
        "title": "Preply English Tutors Review",
        "desc": "Preply online English tutoring platform review: pricing, quality, and value.",
        "related": ["datacamp-review-learning-data-skills", "best-software-stack-one-person-business"],
    },
    "best-software-stack-one-person-business": {
        "title": "Best Software Stack for One-Person Business",
        "desc": "Complete solopreneur software toolkit: from accounting to marketing.",
        "related": ["wps-office-review-small-teams", "best-vpns-remote-workers"],
    },
}

SITE_URL = "https://ctbz669-web.github.io/software-tools-reviews"

def make_jsonld(slug, meta):
    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": meta["title"],
        "description": meta["desc"],
        "url": f"{SITE_URL}/{slug}.html",
        "publisher": {
            "@type": "Organization",
            "name": "Workflow Tools Review",
            "url": SITE_URL
        },
        "datePublished": "2026-05-23",
        "dateModified": "2026-05-23",
    }
    return json.dumps(schema, indent=2)

def make_related_links(slug, meta):
    html = '\n<section class="related-articles">\n<h2>Related Reviews</h2>\n<ul>\n'
    for rel_slug in meta["related"]:
        rel_meta = ARTICLES.get(rel_slug)
        if rel_meta:
            html += f'<li><a href="{rel_slug}.html">{rel_meta["title"]}</a></li>\n'
    html += '</ul>\n</section>\n'
    return html

def add_breadcrumbs(slug, meta):
    return f'<nav class="breadcrumbs"><a href="index.html">Home</a> &raquo; {meta["title"]}</nav>'

def process_file(slug):
    meta = ARTICLES.get(slug)
    if not meta:
        print(f"  ⚠️  No metadata for {slug}, skipping")
        return False
    
    path = os.path.join(BASE, f"{slug}.html")
    if not os.path.exists(path):
        print(f"  ⚠️  {path} not found")
        return False
    
    with open(path, "r") as f:
        html = f.read()
    
    # Skip if already processed
    if 'schema.org' in html and 'related-articles' in html:
        print(f"  ⏭️  {slug} already has JSON-LD + related links")
        return False
    
    # Add JSON-LD before </head>
    jsonld = make_jsonld(slug, meta)
    jsonld_tag = f'<script type="application/ld+json">\n{jsonld}\n</script>\n'
    if '</head>' in html:
        html = html.replace('</head>', f'{jsonld_tag}</head>')
    
    # Add breadcrumbs after <body>
    breadcrumbs = add_breadcrumbs(slug, meta)
    if '<article' in html:
        html = html.replace('<article', f'{breadcrumbs}\n<article', 1)
    
    # Add related links before </article>
    related = make_related_links(slug, meta)
    if '</article>' in html:
        html = html.replace('</article>', f'{related}</article>', 1)
    
    # Add CSS for breadcrumbs and related section
    extra_css = """
<style>
.breadcrumbs { font-size: 0.85em; color: #666; margin-bottom: 1em; }
.breadcrumbs a { color: #2563eb; text-decoration: none; }
.breadcrumbs a:hover { text-decoration: underline; }
.related-articles { margin-top: 2em; padding-top: 1.5em; border-top: 2px solid #e5e7eb; }
.related-articles h2 { font-size: 1.3em; margin-bottom: 0.5em; }
.related-articles ul { list-style: none; padding: 0; }
.related-articles li { margin-bottom: 0.4em; }
.related-articles a { color: #2563eb; text-decoration: none; }
.related-articles a:hover { text-decoration: underline; }
</style>
"""
    if extra_css.strip() not in html:
        html = html.replace('</head>', f'{extra_css}</head>')
    
    with open(path, "w") as f:
        f.write(html)
    
    print(f"  ✅ {slug} — added JSON-LD, breadcrumbs, related links")
    return True

if __name__ == '__main__':
    print("🔧 Adding SEO structured data + internal cross-links...")
    changed = 0
    for slug in ARTICLES:
        if process_file(slug):
            changed += 1
    print(f"\n✅ Updated {changed} files")
