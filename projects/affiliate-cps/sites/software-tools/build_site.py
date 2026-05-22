#!/usr/bin/env python3
"""Build static HTML affiliate site from markdown articles."""
import os, re, glob

BASE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(BASE, "content")
OUT = BASE

HEADER = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} — Workflow Tools Review</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
<header class="site-header">
<div class="header-inner">
<a href="index.html" class="site-logo">Workflow<span>Tools</span></a>
<nav>
<a href="index.html">Home</a>
<a href="index.html#articles">Articles</a>
<a href="#disclosure">Disclosure</a>
</nav>
</div>
</header>
<main class="article-layout">
<article>
<div class="article-header">
<h1>{title}</h1>
<div class="article-meta"><span>📅 {date}</span><span>📂 {category}</span><span>⏱ {read_time} min read</span></div>
</div>
<div class="article-body">
"""

FOOTER = """
</div>
<div class="cta-box" id="disclosure">
<p><strong>Want to try it yourself?</strong></p>
<a href="#" class="cta-btn">Check Latest Price →</a>
<p class="affiliate-disclosure">This article contains affiliate links. We may earn a commission at no extra cost to you. See our full <a href="index.html#disclosure">affiliate disclosure</a>.</p>
</div>
</article>
</main>
<footer class="site-footer">
<div class="footer-inner">
<p>© 2026 Workflow Tools Review</p>
<p class="footer-disclosure">Affiliate Disclosure: Some links on this site are affiliate links. We may receive compensation if you click through and make a purchase. This does not affect our editorial integrity.</p>
</div>
</footer>
</body>
</html>
"""

ARTICLES = [
    ("best-domain-registrars-for-affiliate-websites.md", "Domain & Hosting", "Best Domain Registrars for Affiliate Websites in 2026"),
    ("best-mac-cleaner-security-tools-for-creators.md", "Mac Tools", "Best Mac Cleaner & Security Tools for Creators"),
    ("best-backup-software-solo-businesses.md", "Backup & Recovery", "Best Backup Software for Solo Businesses"),
    ("best-vpns-remote-workers.md", "VPN & Security", "Best VPNs for Remote Workers in 2026"),
    ("best-ai-photo-editor-background-remover.md", "Photo & Design", "Best AI Photo Editor & Background Remover Tools"),
    ("wps-office-review-small-teams.md", "Office & Productivity", "WPS Office Review for Small Teams"),
    ("best-data-recovery-software-for-creators.md", "Backup & Recovery", "Best Data Recovery Software for Creators"),
    ("datacamp-review-learning-data-skills.md", "Online Learning", "DataCamp Review: Best Platform for Learning Data Skills?"),
    ("preply-english-tutors-review.md", "Online Learning", "Preply English Tutors Review: Is It Worth It?"),
    ("best-software-stack-one-person-business.md", "Productivity Stack", "Solopreneur Software Stack: Best Tools for One-Person Businesses"),
]

def md_to_html(text):
    """Basic markdown to HTML conversion."""
    html = text
    # Code blocks
    html = re.sub(r'```(\w*)\n(.*?)```', r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)
    # Inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    # Tables
    lines = html.split('\n')
    in_table = False
    result = []
    for line in lines:
        stripped = line.strip()
        if '|' in stripped and stripped.startswith('|'):
            cells = [c.strip() for c in stripped.split('|')[1:-1]]
            if not in_table:
                result.append('<table>')
                result.append('<thead><tr>' + ''.join(f'<th>{c}</th>' for c in cells) + '</tr></thead>')
                result.append('<tbody>')
                in_table = True
            elif all(set(c) <= set('- :') for c in cells):
                continue  # separator row
            else:
                result.append('<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>')
        else:
            if in_table:
                result.append('</tbody></table>')
                in_table = False
            result.append(line)
    if in_table:
        result.append('</tbody></table>')
    html = '\n'.join(result)
    # Headers
    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    # Bold / italic
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
    # Links
    html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
    # Images
    html = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1" loading="lazy">', html)
    # Blockquotes
    html = re.sub(r'^> (.+)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
    # Unordered lists
    html = re.sub(r'^- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*</li>\n?)+', lambda m: '<ul>' + m.group(0) + '</ul>', html)
    # Paragraphs — wrap loose lines
    html = re.sub(r'(?<![>\n])\n(?!\n|<|[=-])', r'<br>\n', html)
    # Clean up excess br
    html = re.sub(r'(<br>\n?){2,}', '\n\n', html)
    return html

def word_count(text):
    return len(text.split())

def build_articles():
    cards = []
    for fname, category, title in ARTICLES:
        fpath = os.path.join(CONTENT, fname)
        if not os.path.exists(fpath):
            print(f"  SKIP: {fname} not found")
            continue
        with open(fpath) as f:
            md = f.read()
        
        # Skip YAML frontmatter if present
        content = md
        if md.startswith('---'):
            parts = md.split('---', 2)
            if len(parts) >= 3:
                content = parts[2].strip()
        
        wc = word_count(content)
        read_time = max(3, wc // 200)
        # Extract first paragraph as description (skip headers, skip disclosure blockquote)
        first_para = re.search(r'(?:\n|^)([^#\n>].{50,200})', content)
        if first_para:
            desc = re.sub(r'[#*\[\]\>]', '', first_para.group(1)).strip().replace('\n', ' ')[:160]
        else:
            desc = re.sub(r'[#*\[\]\>]', '', content[:160]).strip().replace('\n', ' ')
        slug = fname.replace('.md', '.html')
        
        body_html = md_to_html(content)
        
        page = HEADER.format(title=title, desc=desc, date="May 2026", category=category, read_time=read_time)
        page += body_html
        page += FOOTER
        
        out_path = os.path.join(OUT, slug)
        with open(out_path, 'w') as f:
            f.write(page)
        print(f"  ✅ {slug} ({wc} words, ~{read_time} min read)")
        
        excerpt = re.sub(r'[#*\[\]>]', '', content[:200]).strip().replace('\n', ' ') + '...'
        cards.append({
            'slug': slug,
            'title': title,
            'category': category,
            'excerpt': excerpt,
            'read_time': read_time,
        })
    return cards

def build_index(cards):
    card_html = ""
    for c in cards:
        card_html += f"""
<div class="article-card">
<div class="card-category">{c['category']}</div>
<h2 class="card-title"><a href="{c['slug']}">{c['title']}</a></h2>
<p class="card-excerpt">{c['excerpt']}</p>
<a href="{c['slug']}" class="card-link">Read Full Review →</a>
</div>
"""
    
    index = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Workflow Tools Review — Best Software for Creators, Remote Workers & Solopreneurs</title>
<meta name="description" content="Honest, in-depth reviews of the best software tools for creators, remote workers, and solopreneurs. VPNs, backup, Mac tools, AI editors, and more.">
<link rel="stylesheet" href="css/style.css">
</head>
<body>
<header class="site-header">
<div class="header-inner">
<a href="index.html" class="site-logo">Workflow<span>Tools</span></a>
<nav>
<a href="index.html">Home</a>
<a href="#articles">Articles</a>
<a href="#disclosure">Disclosure</a>
</nav>
</div>
</header>

<section class="hero">
<h1>Find the Right Tools for Your Workflow</h1>
<p>In-depth, unbiased reviews of software for creators, remote workers, and one-person businesses. We test so you don't have to.</p>
<a href="#articles" class="hero-cta">Browse All Reviews →</a>
</section>

<section class="section" id="articles">
<h2 class="section-title">Latest Reviews & Guides</h2>
<div class="article-grid">
{card_html}
</div>
</section>

<section class="section" id="disclosure">
<h2 class="section-title">Affiliate Disclosure</h2>
<p style="max-width:700px;color:var(--text-muted);">Some links on Workflow Tools Review are affiliate links. If you click through and make a purchase, we may earn a commission at no extra cost to you. Our editorial opinions remain our own. We only recommend tools we genuinely believe add value.</p>
</section>

<footer class="site-footer">
<div class="footer-inner">
<p>© 2026 Workflow Tools Review</p>
<p class="footer-disclosure">This site participates in affiliate programs. Content is for informational purposes only and does not constitute professional advice.</p>
</div>
</footer>
</body>
</html>
"""
    
    with open(os.path.join(OUT, "index.html"), 'w') as f:
        f.write(index)
    print(f"  ✅ index.html ({len(cards)} articles)")

if __name__ == '__main__':
    print("🔨 Building Workflow Tools Review site...")
    cards = build_articles()
    build_index(cards)
    print(f"\n✅ Done! {len(cards)} article pages + index.html")
