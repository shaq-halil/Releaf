#!/usr/bin/env python3
"""Build the two review pages as portable, dependency-free static HTML."""
from pathlib import Path
from html import escape
from urllib.parse import urlparse
import argparse
ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--site-url', default='', help='Final HTTPS hosting URL, including any repository subpath')
args = parser.parse_args()
SITE = args.site_url.rstrip('/')
if SITE and (urlparse(SITE).scheme != 'https' or not urlparse(SITE).netloc or urlparse(SITE).query or urlparse(SITE).fragment):
    parser.error('--site-url must be an absolute HTTPS URL without a query or fragment')
WA = 'https://wa.me/233555401859'
ARROW = '<span aria-hidden="true">↗</span>'
CHAT = '<svg class="whatsapp-icon" width="24" height="24" fill="currentColor" aria-hidden="true" focusable="false" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><!--! Font Awesome Free 6.7.2 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License) Copyright 2024 Fonticons, Inc. --><path d="M380.9 97.1C339 55.1 283.2 32 223.9 32c-122.4 0-222 99.6-222 222 0 39.1 10.2 77.3 29.6 111L0 480l117.7-30.9c32.4 17.7 68.9 27 106.1 27h.1c122.3 0 224.1-99.6 224.1-222 0-59.3-25.2-115-67.1-157zm-157 341.6c-33.2 0-65.7-8.9-94-25.7l-6.7-4-69.8 18.3L72 359.2l-4.4-7c-18.5-29.4-28.2-63.3-28.2-98.2 0-101.7 82.8-184.5 184.6-184.5 49.3 0 95.6 19.2 130.4 54.1 34.8 34.9 56.2 81.2 56.1 130.5 0 101.8-84.9 184.6-186.6 184.6zm101.2-138.2c-5.5-2.8-32.8-16.2-37.9-18-5.1-1.9-8.8-2.8-12.5 2.8-3.7 5.6-14.3 18-17.6 21.8-3.2 3.7-6.5 4.2-12 1.4-32.6-16.3-54-29.1-75.5-66-5.7-9.8 5.7-9.1 16.3-30.3 1.8-3.7.9-6.9-.5-9.7-1.4-2.8-12.5-30.1-17.1-41.2-4.5-10.8-9.1-9.3-12.5-9.5-3.2-.2-6.9-.2-10.6-.2-3.7 0-9.7 1.4-14.8 6.9-5.1 5.6-19.4 19-19.4 46.3 0 27.3 19.9 53.7 22.6 57.4 2.8 3.7 39.1 59.7 94.8 83.8 35.2 15.2 49 16.5 66.6 13.9 10.7-1.6 32.8-13.4 37.4-26.4 4.6-13 4.6-24.1 3.2-26.4-1.3-2.5-5-3.9-10.5-6.6z"/></svg>'
IMAGES = {
    'paper-next-chapter': (1672,941,[640,1024,1672]),
    'atika-portrait': (1086,1448,[360,640,1086]),
    'bundled-paper': (1086,1448,[360,720,1086]),
    'archive-paper': (1278,1230,[480,800,1278]),
    'schoolbooks': (736,968,[360,736]),
}
def photo(name, alt, prefix='', eager=False, sizes='(max-width: 700px) 90vw, 360px'):
    width,height,widths=IMAGES[name]
    base=prefix+'assets/images/'+name
    srcset=', '.join(f'{base}-{w}.webp {w}w' for w in widths)
    return f'<img src="{base}-{width}.webp" srcset="{srcset}" sizes="{sizes}" width="{width}" height="{height}" alt="{escape(alt)}" {"fetchpriority=high" if eager else "loading=lazy"} decoding="async">'

def header(prefix, story=False):
    home='../' if story else './'
    return f'''<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="site-container header-inner"><a class="wordmark" href="{home}" aria-label="ReLeaf Collective home"><img src="{prefix}assets/icons/leaf.svg" width="28" height="34" alt=""><span>ReLeaf<small>COLLECTIVE</small></span></a>
<button class="menu-toggle" aria-controls="site-nav" aria-expanded="false">Menu <span aria-hidden="true">＋</span></button>
<nav id="site-nav" aria-label="Main navigation"><svg class="nav-membrane" aria-hidden="true" focusable="false"><path class="nav-shape"/></svg><a class="nav-pill" href="{home}" {'' if story else 'aria-current="page"'}>Home</a><a class="nav-pill" href="{prefix}our-story/" {'aria-current="page"' if story else ''}>Our story</a><a class="nav-pill" href="{prefix}#model">The idea</a><a class="nav-contact" href="#conversation">Let’s talk {ARROW}</a></nav></div></header>'''

def footer(prefix):
    return f'''<footer class="site-footer"><div class="site-container"><div class="footer-top"><a class="footer-brand" href="{prefix or './'}">ReLeaf<span>COLLECTIVE</span></a><p>A second life for paper. A shared possibility for education.</p><a href="#main" class="round-link" aria-label="Back to top">↑</a></div><div class="footer-bottom"><span>© 2026 ReLeaf Collective · Ghana</span><a href="{prefix}our-story/#people">The people behind ReLeaf</a><a href="#conversation">Contact us</a></div></div></footer><a class="floating-contact" href="{WA}" target="_blank" rel="noopener noreferrer" aria-label="Talk to ReLeaf on WhatsApp (opens a new tab)">{CHAT}<span>WhatsApp</span></a>'''

def contact():
    return f'''<section class="contact-section section section-dark" id="conversation" aria-labelledby="contact-title"><div class="site-container contact-content"><h2 id="contact-title">Let's get connected.</h2><p>Have an idea, a question, or an opportunity to collaborate? We'd love to hear from you.</p><a class="button contact-button" href="{WA}" target="_blank" rel="noopener noreferrer" aria-label="Contact Us on WhatsApp (opens a new tab)">{CHAT}<span>Contact Us</span>{ARROW}</a></div></section>'''


def founder(prefix='', full=False):
    intro = 'Before there was ReLeaf,<br>there was a mother’s question.' if full else 'It began with <em>what came home.</em>'
    kicker = '<p class="section-label eyebrow">THE FOUNDING STORY</p>' if full else '<p class="section-label eyebrow">A VERY HUMAN BEGINNING</p>'
    opening = '<div class="site-container">' if not full else ''
    closing = '</div>' if not full else ''
    layout = 'founder-layout feature-layout' if not full else 'founder-layout'
    return f'''<section class="founder-section section {'founder-full' if full else 'section-light'}" id="founder">{opening}<div class="{layout}"><figure class="founder-photo">{photo('atika-portrait','Atika Yakubu, Founder and CEO of ReLeaf Collective',prefix,eager=full)}<figcaption><span>Atika Yakubu</span><span>Founder & CEO</span></figcaption></figure><div class="founder-copy">{kicker}<h2>{intro}</h2><p>As a mother, Atika Yakubu saw used papers and exercise books coming home with her children. Term after term, the pages accumulated.</p><p>She imagined an organised way to recover that paper—and explore how its value could find a way back to education.</p>{'<p>That everyday observation became the starting point for ReLeaf Collective: a Ghanaian initiative developing connections between schools, responsible recovery and useful new materials.</p>' if full else '<a class="text-link" href="our-story/">The story behind ReLeaf '+ARROW+'</a>'}</div></div>{closing}</section>'''

HOME = '''<section aria-labelledby="hero-title" class="hero"><div class="hero-image">{hero_photo}</div><div class="hero-shade"></div><div class="site-container hero-inner"><div class="hero-topline"><span>ROOTED IN GHANA. MADE OF POSSIBILITY.</span><span class="hero-edition">RELEAF COLLECTIVE — 01</span></div><div class="hero-content"><h1 id="hero-title">Every page<br/>deserves<br/><em>another life.</em></h1><p>We’re developing a way to recover school paper and return its value to education.</p><div class="hero-actions"><a class="button light" href="#model">Discover the idea <span aria-hidden="true">↘</span></a><a class="hero-story-link" href="our-story/">Our story {arrow}</a></div></div><div class="hero-bottom"><a class="hero-scroll" href="#after-the-page"><span aria-hidden="true" class="scroll-line"></span>The next chapter <span aria-hidden="true">↓</span></a></div></div></section>
<section aria-labelledby="look-again-title" class="paper-editorial section section-light" id="after-the-page"><div class="site-container"><div class="editorial-spread feature-layout"><figure class="material-photo">{book_photo}</figure><div class="editorial-copy"><p class="section-label eyebrow">01 / LOOK AGAIN</p><h2 id="look-again-title">Every page deserves another life.</h2><p>Old schoolbooks shouldn't become forgotten waste. We're creating a way to recover their value and give something back to education.</p><a class="text-link" href="our-story/">Discover our story <span aria-hidden="true">↗</span></a></div></div></div></section>
<section class="model-section section section-dark" id="model"><div class="site-container"><div class="section-heading"><h2>From learning. <em>Back to learning.</em></h2><p>A proposed cycle, built with people who know each part of the journey.</p></div><ol class="model-ledger"><li><span class="step-number">01</span><h3>Gather.</h3><p>Agree a practical way for schools to set suitable paper aside.</p></li><li><span class="step-number">02</span><h3>Recover.</h3><p>Work with partners to collect, sort and confirm what can be recycled.</p></li><li><span class="step-number">03</span><h3>Reimagine.</h3><p>Explore useful materials and packaging with manufacturing partners.</p></li><li><span class="step-number">04</span><h3>Return.</h3><p>Explore an agreed share of value for educational resources.</p></li></ol><div class="model-footnote"><span aria-hidden="true" class="status-dot"></span><p>In development. Collection arrangements and school benefits depend on viable economics and partner agreements.</p></div></div></section>
{founder}
<section aria-labelledby="collective-title" class="opportunities section section-dark" id="opportunities"><div class="site-container"><h2 id="collective-title">
    Where you fit.
  </h2><div class="participation-grid"><a class="participation-card" href="#conversation"><h3>Schools &amp; PTAs</h3><p>Explore school participation.</p><span aria-hidden="true" class="card-arrow">↗</span></a><a class="participation-card" href="#conversation"><h3>Recovery &amp; Industry</h3><p>Explore working together.</p><span aria-hidden="true" class="card-arrow">↗</span></a><a class="participation-card" href="#conversation"><h3>Businesses</h3><p>Explore paper packaging.</p><span aria-hidden="true" class="card-arrow">↗</span></a></div></div></section>
<section class="faq-section section section-light"><div class="site-container faq-layout"><h2>Good questions.<br/>Clear answers.</h2><div class="faq-list"><details><summary>Are you collecting paper now?</summary><p>We’re developing our model and seeking partners. There is no confirmed collection service or pickup schedule yet.</p></details><details><summary>How could schools benefit?</summary><p>We’re exploring how recovered value could support educational resources. Any benefit will depend on the economics and an agreement with the school.</p></details><details><summary>Can businesses order packaging?</summary><p>We welcome enquiries while we explore manufacturing partnerships. Specifications, supply and availability need to be agreed before any order can be confirmed.</p></details></div></div></section>
{contact}'''

STORY = '''<section class="story-opening section"><p class="eyebrow">OUR STORY</p><div class="story-title"><h1>A small observation.<br><em>A different future.</em></h1><p>It started with the paper her children brought home.</p></div><div class="story-opening-bottom"><span>PEOPLE, PAPER & A PURPOSE.</span><a class="text-link" href="#founder">Start at the beginning <span aria-hidden="true">↓</span></a></div></section>
{founder}
<section class="story-chapters section"><div class="story-chapter-copy"><p class="eyebrow">A MATERIAL CONNECTION. A HUMAN PURPOSE.</p><h2>More than<br><em>what paper becomes.</em></h2><p>Recovery is one part of the idea. Keeping a connection to education is what gives it purpose.</p><p>We want to bring schools, recovery specialists and manufacturing partners into a shared conversation. Together, we can explore useful next uses for paper and a practical way for value to return to learning.</p><a class="text-link" href="../#model">Explore the proposed model {arrow}</a></div><figure class="story-material">{stack_photo}<figcaption>Owner-supplied paper image · not evidence of a ReLeaf collection.</figcaption></figure></section>
<section class="people-section section" id="people"><div class="section-heading"><div><p class="eyebrow">THE PEOPLE BEHIND RELEAF</p><h2>It takes<br><em>a collective.</em></h2></div><p>Three people. A shared direction.</p></div><div class="leadership-grid"><article class="leader"><span class="leader-number">01 / FOUNDING VISION</span><h3>Atika <br><em>Yakubu</em></h3><p>Founder & Chief Executive Officer <span>(CEO)</span></p></article><article class="leader"><span class="leader-number">02 / OPERATIONS</span><h3>Rosemary <br><em>Elorn</em></h3><p>Chief Operations Officer <span>(COO)</span></p></article><article class="leader"><span class="leader-number">03 / TECHNOLOGY</span><h3>Halleo <br><em>Shaq</em></h3><p>Chief Technology Officer <span>(CTO)</span></p></article></div></section>
<section class="principles section"><div class="section-heading"><div><p class="eyebrow">WHAT GUIDES US</p><h2>Care in<br><em>every connection.</em></h2></div><p>The principles we want to build into the work.</p></div><div class="principle-columns"><div><span>01</span><h3>Start with people.</h3><p>Listen to schools and learn from the expertise already in the recovery chain.</p></div><div><span>02</span><h3>Make the terms clear.</h3><p>Agree permissions, suitable materials and any school benefit before a pilot begins.</p></div><div><span>03</span><h3>Let evidence lead.</h3><p>Be clear about what we’re developing. Publish results when they can be verified.</p></div></div></section>
<section class="where-now section"><p class="eyebrow">WHERE WE ARE TODAY</p><h2>At the beginning.<br><em>With a purpose.</em></h2><p>ReLeaf is developing its model and seeking partners. Our next chapter will be built through conversation.</p><a class="text-link" href="#conversation">Be part of it {arrow}</a></section>
{contact}'''


def document(title, description, body, prefix='', story=False):
    route='our-story/' if story else ''
    url=SITE+'/'+route if SITE else ''
    canonical=f'<link rel="canonical" href="{escape(url)}"><meta property="og:url" content="{escape(url)}">' if SITE else ''
    social_image=(SITE+'/' if SITE else prefix)+'assets/images/social-preview.jpg'
    homepage_style = f'<link rel="stylesheet" href="{prefix}assets/css/homepage.css">' if not story else ''
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#173d30"><meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' data:; style-src 'self'; font-src 'self'; script-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action https://wa.me"><title>{escape(title)}</title><meta name="description" content="{escape(description)}">{canonical}<meta property="og:type" content="website"><meta property="og:site_name" content="ReLeaf Collective"><meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(description)}"><meta property="og:image" content="{social_image}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="ReLeaf Collective — Every page deserves another life"><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="{prefix}assets/icons/leaf.svg" type="image/svg+xml"><link rel="preload" href="{prefix}assets/fonts/sans-variable.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="{prefix}assets/fonts/editorial-regular.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="{prefix}assets/css/styles.css">{homepage_style}<script src="{prefix}assets/js/main.js" defer></script></head><body class="{'story-page' if story else 'home-page'}">{header(prefix,story)}<main id="main" tabindex="-1">{body}</main>{footer(prefix)}</body></html>'''

home=HOME.format(hero_photo=photo('paper-next-chapter','AI-generated concept illustration: loose school and office papers settling toward a stack in a sunlit interior',eager=True,sizes='100vw'),book_photo=photo('schoolbooks','A stack of used schoolbooks and papers',sizes='(max-width: 700px) 90vw, 460px'),founder=founder(),arrow=ARROW,contact=contact())
story=STORY.format(founder=founder('../',True),stack_photo=photo('bundled-paper','Bundled papers and exercise books beside a green-framed entrance','../',sizes='(max-width: 700px) 90vw, 420px'),arrow=ARROW,contact=contact())
(ROOT/'index.html').write_text(document('ReLeaf Collective | Every Page Deserves Another Life','A Ghanaian initiative developing school paper recovery, useful new materials and a return of value to education. Help shape the next chapter with ReLeaf.',home))
(ROOT/'our-story/index.html').write_text(document('Our Story | The People & Purpose of ReLeaf Collective','Meet founder Atika Yakubu and leaders Rosemary Elorn and Halleo Shaq. Discover the everyday observation behind ReLeaf’s vision for paper and education.',story,'../',True))
(ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\n'+(f'Sitemap: {SITE}/sitemap.xml\n' if SITE else ''))
entries=''.join(f'<url><loc>{escape(SITE+"/"+route)}</loc></url>' for route in ['', 'our-story/']) if SITE else ''
(ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n'+('<!-- Set the final site URL before publication. -->\n' if not SITE else '')+'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+entries+'</urlset>\n')
print('Generated Home and Our Story. '+('Canonical host: '+SITE if SITE else 'Review build; final hosting URL pending.'))
