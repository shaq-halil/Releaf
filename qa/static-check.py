#!/usr/bin/env python3
"""Check static integrity and a clean export without a browser or network."""
from pathlib import Path
from urllib.parse import urlsplit, unquote
from collections import Counter
from bs4 import BeautifulSoup
from PIL import Image
import json
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
results = {'scope':'2026-10-25 centered direct WhatsApp contact, forms removed', 'browserQA':'blocked by sandbox; pending', 'pages':[]}
for rel in ['index.html','our-story/index.html']:
    page=ROOT/rel
    soup=BeautifulSoup(page.read_text(),'html.parser')
    ids=[t['id'] for t in soup.select('[id]')]
    assert all(n==1 for n in Counter(ids).values()), f'Duplicate IDs: {rel}'
    assert len(soup.select('h1'))==1
    assert soup.title and soup.select_one('meta[name=description]')
    assert soup.select_one('main#main[tabindex="-1"]')
    assert not soup.select('form,input,textarea,select,.draft-preview,.form-status,[data-select-journey]')
    contact=soup.select_one('#conversation')
    assert contact and len(contact.select('h2'))==1 and len(contact.select('p'))==1 and len(contact.select('a'))==1
    assert contact.h2.get_text(strip=True)=="Let's get connected."
    assert contact.p.get_text(strip=True)=="Have an idea, a question, or an opportunity to collaborate? We'd love to hear from you."
    button=contact.select_one('a.contact-button')
    assert button['href']=='https://wa.me/233555401859' and button['target']=='_blank'
    assert {'noopener','noreferrer'}.issubset(button['rel'])
    assert button.select_one('svg.whatsapp-icon path') and button.select_one('span').get_text(strip=True)=='Contact Us'
    assert contact.select_one(':scope > .site-container.contact-content')
    assert not soup.select('script[src$="whatsapp.js"],script[src$="config.js"]')
    links=0
    for tag in soup.select('[href],[src],[srcset]'):
        urls=[tag.get('href',''),tag.get('src','')]
        urls.extend(part.strip().split()[0] for part in tag.get('srcset','').split(',') if part.strip())
        for url in filter(None,urls):
            parsed=urlsplit(url)
            if parsed.scheme or parsed.netloc: continue
            target=(page.parent/unquote(parsed.path)).resolve() if parsed.path else page
            if target.is_dir(): target=target/'index.html'
            assert target.is_file(),f'Missing {url} from {rel}'
            if parsed.fragment:
                dest=BeautifulSoup(target.read_text(),'html.parser')
                assert dest.find(id=parsed.fragment),f'Missing anchor {url} from {rel}'
            links+=1
    images=[]
    for tag in soup.select('img'):
        assert 'alt' in tag.attrs
        assert tag.get('width') and tag.get('height')
        target=(page.parent/unquote(urlsplit(tag['src']).path)).resolve()
        if target.suffix!='.svg':
            with Image.open(target) as im:
                im.verify()
            with Image.open(target) as im:
                assert im.size==(int(tag['width']),int(tag['height']))
                images.append({'file':str(target.relative_to(ROOT)),'dimensions':list(im.size)})
    if rel.startswith('our-story'):
        assert [tag.get_text(' ',strip=True) for tag in soup.select('.leader h3')]==['Atika Yakubu','Rosemary Elorn','Halleo Shaq']
    else:
        assert 'AI-generated concept' in soup.select_one('.hero-image img')['alt']
        look=soup.select_one('#after-the-page')
        assert len(look.select('img'))==1 and len(look.select('h2'))==1
        assert not look.select('figcaption,.small-index,.editorial-heading')
        assert look.select_one('.section-label').get_text(strip=True)=='01 / LOOK AGAIN'
        assert look.h2.get_text(strip=True)=='Every page deserves another life.'
        assert look.select_one('.editorial-copy p:not(.section-label)').get_text(strip=True)=="Old schoolbooks shouldn't become forgotten waste. We're creating a way to recover their value and give something back to education."
        assert look.select_one('a')['href']=='our-story/'
        collective=soup.select_one('#opportunities')
        assert collective.h2.get_text(strip=True)=='Where you fit.'
        assert not collective.select('.eyebrow,.section-label')
        cards=collective.select('a.participation-card')
        assert len(cards)==3
        assert [c.h3.get_text(strip=True) for c in cards]==['Schools & PTAs','Recovery & Industry','Businesses']
        assert [c.p.get_text(strip=True) for c in cards]==['Explore school participation.','Explore working together.','Explore paper packaging.']
        assert all(a['href']=='#conversation' for a in collective.select('a'))
        sections=soup.select('main > .section')
        assert len(sections)==6
        assert all(len(section.select('h2'))==1 for section in sections)
        assert len(soup.select('main .section-label'))==2
        assert len(soup.select('.site-container .site-container'))==0
        assert all(len(section.select(':scope > .site-container'))==1 for section in sections)
        assert soup.select_one('.header-inner.site-container')
        assert soup.select_one('.hero > .hero-inner.site-container')
        assert soup.select_one('.site-footer > .site-container')
        assert soup.select_one('.faq-layout h2').get_text(' ',strip=True)=='Good questions. Clear answers.'
        assert [('section-light' in section['class']) for section in sections]==[True,False,True,False,True,False]

    results['pages'].append({'page':rel,'localReferencesChecked':links,'images':images,'contact':'direct WhatsApp link; no forms','passed':True})
css=(ROOT/'assets/css/styles.css').read_text()+'\n'+(ROOT/'assets/css/homepage.css').read_text()
for url in re.findall(r'url\([\'"]?([^\)\'\"]+)',css):
    assert (ROOT/'assets/css'/url).is_file(),url
assert 'prefers-reduced-motion:reduce' in css
assert 'blur(' not in css
for file in ['assets/js/main.js','qa/browser-check.cjs','qa/subpath-check.cjs']:
    subprocess.run(['node','--check',str(ROOT/file)],check=True)
ET.parse(ROOT/'sitemap.xml')
with tempfile.TemporaryDirectory(prefix='releaf-export-') as tmp:
    destination=Path(tmp)/'site'
    subprocess.run(['python3',str(ROOT/'scripts/export.py'),'--output',str(destination)],check=True)
    assert (destination/'index.html').is_file()
    assert (destination/'our-story/index.html').is_file()
    assert not (destination/'assets/js/whatsapp.js').exists()
    assert not (destination/'assets/js/config.js').exists()
    assert not any((destination/name).exists() for name in ['moooi','floema','chariTywaTer','qa','images','scripts'])
    results['export']={'passed':True,'files':len(list(p for p in destination.rglob('*') if p.is_file())),'bytes':sum(p.stat().st_size for p in destination.rglob('*') if p.is_file())}
# Verify canonical/sitemap generation under a repository subpath in an isolated copy.
with tempfile.TemporaryDirectory(prefix='releaf-metadata-') as tmp:
    import shutil
    root=Path(tmp)
    (root/'scripts').mkdir();(root/'our-story').mkdir()
    shutil.copy2(ROOT/'scripts/build.py',root/'scripts/build.py')
    subprocess.run(['python3',str(root/'scripts/build.py')],check=True)
    for route in ['', 'our-story/']:
        assert (root/route/'index.html').read_text()==(ROOT/route/'index.html').read_text(), f'Authoring helper does not reproduce {route or "home"}'
    subprocess.run(['python3',str(root/'scripts/build.py'),'--site-url','https://example.invalid/releaf'],check=True)
    for route in ['', 'our-story/']:
        soup=BeautifulSoup((root/route/'index.html').read_text(),'html.parser')
        assert soup.select_one('link[rel=canonical]')['href']=='https://example.invalid/releaf/'+route
        assert soup.select_one('meta[property="og:image"]')['content']=='https://example.invalid/releaf/assets/images/social-preview.jpg'
    urls=ET.parse(root/'sitemap.xml').getroot()
    assert len(urls)==2
    assert 'Sitemap: https://example.invalid/releaf/sitemap.xml' in (root/'robots.txt').read_text()
results['metadataGeneration']={'passed':True,'repositorySubpath':True,'testHostOnly':'example.invalid, isolated temp copy'}
results['passed']=True
(ROOT/'qa/static-results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
