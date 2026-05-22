#!/usr/bin/env python3
"""Fix meta descriptions and add JSON-LD structured data to all affiliate articles."""
import os, re, json, glob

SITE_DIR = "/Users/kevin/.openclaw/workspace/projects/affiliate-cps/sites/software-tools"
BASE_URL = "https://ctbz669-web.github.io/software-tools-reviews"

ARTICLES = {
    "best-domain-registrars-for-affiliate-websites.html": {
        "title": "Best Domain Registrars for Affiliate Websites (2026)",
        "description": "Compare Namecheap, Cloudflare, Porkbun, Google Domains and more for affiliate sites. Pricing, features, and honest recommendations.",
        "date": "2026-05-23",
    },
    "best-mac-cleaner-security-tools-for-creators.html": {
        "title": "Best Mac Cleaner & Security Tools for Creators (2026)",
        "description": "Honest reviews of CleanMyMac X, Malwarebytes, and Intego for creative professionals. Keep your Mac fast and secure.",
        "date": "2026-05-23",
    },
    "best-backup-software-solo-businesses.html": {
        "title": "Best Backup Software for Solo Businesses (2026)",
        "description": "Compare Backblaze, Carbonite, Acronis, and iDrive for one-person businesses. Reliable backup protects your livelihood.",
        "date": "2026-05-23",
    },
    "best-vpns-remote-workers.html": {
        "title": "Best VPNs for Remote Workers (2026)",
        "description": "NordVPN, ExpressVPN, and Surfshark compared for remote work. Speed, security, and value for distributed teams.",
        "date": "2026-05-23",
    },
    "best-ai-photo-editor-background-remover.html": {
        "title": "Best AI Photo Editor & Background Remover (2026)",
        "description": "Top AI photo editors and background removal tools compared. Canva, Remove.bg, Luminar, and more reviewed.",
        "date": "2026-05-23",
    },
    "best-data-recovery-software-for-creators.html": {
        "title": "Best Data Recovery Software for Creators (2026)",
        "description": "Don't lose your creative work. Compare Disk Drill, EaseUS, Stellar, and Recuva for photo and video recovery.",
        "date": "2026-05-23",
    },
    "datacamp-review-learning-data-skills.html": {
        "title": "DataCamp Review: Is It Worth It for Learning Data Skills? (2026)",
        "description": "In-depth DataCamp review covering courses, pricing, certificates, and career paths for data science learners.",
        "date": "2026-05-23",
    },
    "preply-english-tutors-review.html": {
        "title": "Preply English Tutors Review (2026)",
        "description": "Honest Preply review: tutor quality, pricing, platform experience, and whether it's worth it for English learners.",
        "date": "2026-05-23",
    },
    "wps-office-review-small-teams.html": {
        "title": "WPS Office Review for Small Teams (2026)",
        "description": "WPS Office Premium review for small teams. Features, pricing, compatibility, and whether it can replace Microsoft 365.",
        "date": "2026-05-23",
    },
    "best-software-stack-one-person-business.html": {
        "title": "Best Software Stack for One-Person Businesses (2026)",
        "description": "The complete solopreneur software stack: accounting, project management, communication, and marketing tools reviewed.",
        "date": "2026-05-23",
    },
}

def fix_meta_description(html, correct_desc):
    """Replace broken meta description with correct one."""
    pattern = r'<meta name="description" content="[^"]*">'
    replacement = f'<meta name="description" content="{correct_desc}">'
    new_html, count = re.subn(pattern, replacement, html)
    return new_html, count > 0

def add_jsonld(html, filename, info):
    """Add JSON-LD Article structured data before </head>."""
    url = f"{BASE_URL}/{filename}"
    jsonld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": info["title"],
        "description": info["description"],
        "datePublished": info["date"],
        "dateModified": info["date"],
        "author": {
            "@type": "Organization",
            "name": "Workflow Tools Review"
        },
        "publisher": {
            "@type": "Organization",
            "name": "Workflow Tools Review",
            "url": BASE_URL
        },
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": url
        },
        "url": url
    }
    script = f'\n<script type="application/ld+json">\n{json.dumps(jsonld, indent=2, ensure_ascii=False)}\n</script>\n'
    if 'application/ld+json' in html:
        return html, False  # Already has JSON-LD
    new_html = html.replace('</head>', script + '</head>')
    return new_html, True

def add_internal_links(html, filename):
    """Add related articles section before the disclosure/footer."""
    related = []
    for fname, info in ARTICLES.items():
        if fname != filename:
            related.append(f'<li><a href="{fname}">{info["title"]}</a></li>')
    
    related_html = (
        '\n<section class="related-articles">\n'
        '<h2>Related Reviews</h2>\n'
        '<ul>\n' + '\n'.join(related[:5]) + '\n</ul>\n'
        '</section>\n'
    )
    
    if 'related-articles' in html:
        return html, False
    
    # Insert before the disclosure section
    if '<section id="disclosure"' in html:
        html = html.replace('<section id="disclosure"', related_html + '\n<section id="disclosure"')
        return html, True
    return html, False

def main():
    stats = {"desc_fixed": 0, "jsonld_added": 0, "links_added": 0}
    
    for filename, info in ARTICLES.items():
        filepath = os.path.join(SITE_DIR, filename)
        if not os.path.exists(filepath):
            print(f"  SKIP {filename} (not found)")
            continue
        
        with open(filepath, 'r') as f:
            html = f.read()
        
        original = html
        
        # Fix meta description
        html, changed = fix_meta_description(html, info["description"])
        if changed:
            stats["desc_fixed"] += 1
            print(f"  FIXED desc: {filename}")
        
        # Add JSON-LD
        html, changed = add_jsonld(html, filename, info)
        if changed:
            stats["jsonld_added"] += 1
            print(f"  ADDED JSON-LD: {filename}")
        
        # Add internal links
        html, changed = add_internal_links(html, filename)
        if changed:
            stats["links_added"] += 1
            print(f"  ADDED links: {filename}")
        
        if html != original:
            with open(filepath, 'w') as f:
                f.write(html)
    
    print(f"\nSummary: {stats['desc_fixed']} descriptions fixed, {stats['jsonld_added']} JSON-LD added, {stats['links_added']} internal links added")

if __name__ == "__main__":
    main()
