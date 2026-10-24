#!/usr/bin/env python3
"""Audit source typography at responsive widths. This is NOT a browser layout test."""
from pathlib import Path
from bs4 import BeautifulSoup
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
# Parse actual CSS and selector specificity, including :not(), using PostCSS.
parsed = subprocess.run(['node', '-'], cwd=ROOT, text=True, capture_output=True, check=True, input=r'''
const fs=require('fs'),postcss=require('postcss'),selectors=require('postcss-selector-parser');
const root=postcss.parse(fs.readFileSync('assets/css/styles.css','utf8')+'\n'+fs.readFileSync('assets/css/homepage.css','utf8'));
function specificity(node){
 const s=[0,0,0];
 for(const n of node.nodes||[]){
  if(n.type==='id')s[0]++;
  else if(n.type==='class'||n.type==='attribute')s[1]++;
  else if(n.type==='tag')s[2]++;
  else if(n.type==='pseudo'){
   if(n.value.startsWith('::'))s[2]++;
   else if([':not',':is',':has'].includes(n.value)){
    const candidates=n.nodes.map(specificity).sort((a,b)=>b[0]-a[0]||b[1]-a[1]||b[2]-a[2]);
    candidates[0]?.forEach((v,i)=>s[i]+=v);
   }else if(n.value!==':where')s[1]++;
  }
 }
 return s;
}
const rules=[];
root.walkRules(r=>{
 let p=r.parent,media=[];
 while(p){if(p.type==='atrule'){if(p.name.includes('keyframes'))return;if(p.name==='media')media.push(p.params);}p=p.parent;}
 const decls=r.nodes.filter(n=>n.type==='decl').map(d=>[d.prop,d.value,!!d.important]);
 selectors().astSync(r.selector).nodes.forEach(s=>rules.push({selector:String(s),specificity:specificity(s),media,decls}));
});
console.log(JSON.stringify(rules));
''')
RULES = json.loads(parsed.stdout)


def media_matches(params, width):
    if 'prefers-reduced-motion:reduce' in params.replace(' ', ''):
        return False
    for bound, value in re.findall(r'(min|max)-width\s*:\s*(\d+)px', params):
        if bound == 'min' and width < int(value) or bound == 'max' and width > int(value):
            return False
    return True


CACHE = {}

def values(tag, width):
    key=(id(tag),width)
    if key in CACHE:
        return CACHE[key]
    result, winners = {}, {}
    for order, rule in enumerate(RULES):
        if any(not media_matches(m, width) for m in rule['media']):
            continue
        selector = rule['selector']
        if '::' in selector or any(p in selector for p in [':hover', ':focus', ':active', ':visited']):
            continue
        if not tag.css.match(selector):
            continue
        for index, (prop, value, important) in enumerate(rule['decls']):
            if prop == 'font':
                if value == 'inherit':
                    prop, value = 'font-size', 'inherit'
                else:
                    match = re.search(r'(var\(--body-size\)|\d+(?:\.\d+)?px|clamp\([^)]*\))\s*(?:/|\s)', value)
                    if not match:
                        continue
                    prop, value = 'font-size', match.group(1)
            priority = (important, *rule['specificity'], order, index)
            if priority >= winners.get(prop, (-1,)):
                winners[prop] = priority
                result[prop] = value
    CACHE[key]=result
    return result


def numeric(value, variables, width):
    value=value.strip()
    for _ in range(5):
        if 'var(' not in value:
            break
        value = re.sub(r'var\((--[^)]+)\)', lambda m: variables[m[1]], value).strip()
    def single(v):
        v=v.strip()
        return float(v[:-2])*width/100 if v.endswith('vw') else float(v.removesuffix('px'))
    if value.startswith('clamp('):
        a,b,c = [single(v) for v in value[6:-1].split(',')]
        return max(a,min(b,c))
    return single(value)


def inherited(tag, prop, width, default):
    while getattr(tag, 'name', None):
        value=values(tag,width).get(prop)
        if value and value != 'inherit':
            return value
        tag=tag.parent
    return default


def rgb(hex_color):
    color=hex_color.removeprefix('#')
    return [int(color[i:i+2],16)/255 for i in [0,2,4]]


def contrast(fg,bg):
    def luminance(c):
        return sum(w*(v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4) for v,w in zip(rgb(c),[.2126,.7152,.0722]))
    a,b=sorted([luminance(fg),luminance(bg)])
    return (b+.05)/(a+.05)


report={'kind':'source-derived typography and spacing audit; no browser rendering', 'browserQA':'blocked: Chromium sandbox startup denied', 'viewports':[]}
core='.editorial-heading>p:last-child,.editorial-copy p:not(.section-label),.model-ledger p,.founder-copy p:not(.eyebrow),.section-heading>p,.faq-list details p,.story-title>p,.story-chapter-copy>p:not(.eyebrow),.leader p,.principle-columns p,.where-now>p:not(.eyebrow),.hero-content>p:not(.hero-kicker),.footer-top p'
for route in ['index.html','our-story/index.html']:
    soup=BeautifulSoup((ROOT/route).read_text(),'html.parser')
    CACHE.clear()
    soup.body['class']=[*soup.body.get('class',[]),'js']
    assert not soup.select('main>section[hidden], main>section.waiting'), 'Main section hidden by source markup'
    assert not soup.select('main p br'), 'Forced paragraph line break remains'
    for width in [320,360,390,650,651,768,840,841,900,1024,1440,1920]:
        variables={k:v for k,v in values(soup.html,width).items() if k.startswith('--')}
        variables.update({k:v for k,v in values(soup.body,width).items() if k.startswith('--')})
        target=17 if width<=650 else 18
        for tag in soup.select(core):
            size=numeric(inherited(tag,'font-size',width,'16px'),variables,width)
            assert size==target, (route,width,tag.get('class'),tag.text[:40],size)
        headings=[]
        for tag in soup.select('main h2'):
            size=numeric(inherited(tag,'font-size',width,'16px'),variables,width)
            assert (36<=size<=44 if width<=650 else 40<=size<=56),(route,width,tag.text,size)
            headings.append(round(size,1))
        for tag in soup.select('figcaption,.hero-caption,.model-footnote p,.site-header nav a,.button'):
            size=numeric(inherited(tag,'font-size',width,'16px'),variables,width)
            assert size>=14,(route,width,tag.get('class'),size)
        padding=numeric(variables['--section-space'],variables,width)
        assert padding<=72
        contact=soup.select_one('#conversation')
        assert values(contact.select_one('.contact-content'),width).get('text-align')=='center'
        assert values(contact,width).get('background')=='var(--forest)'
        assert numeric(inherited(contact.p,'font-size',width,'16px'),variables,width)==(16 if width<=650 else 18)
        assert inherited(contact.p,'color',width,'')=='#fff'
        assert inherited(contact.h2,'color',width,'')=='#fff'
        button=contact.select_one('.contact-button')
        assert values(button,width).get('background')=='#fff'
        assert values(button,width).get('color')=='var(--forest)'
        nav=values(soup.select_one('#site-nav'),width)
        assert (nav.get('position')=='static')==(width<=840)
        if route=='index.html':
            backgrounds=[values(section,width).get('background') for section in soup.select('main > .section')]
            assert backgrounds==['#fff','var(--forest)','#fff','var(--forest)','#fff','var(--forest)'],backgrounds
            assert len(soup.select('.site-container'))==9
            assert not soup.select('.site-container .site-container')
            containers=soup.select('.site-container')
            widths=[values(c,width).get('width') for c in containers]
            assert len(set(widths))==1 and widths[0]=='min(calc(100% - (var(--page-gutter) * 2)), var(--page-max-width))',widths
            for c in containers:
                assert values(c,width).get('padding-inline','0')=='0'
            assert values(soup.select_one('.feature-layout'),width).get('max-width')=='none'
            labels=soup.select('main .section-label')
            assert len(labels)==2
            assert all(l.parent.get('class') in [['editorial-copy'],['founder-copy']] for l in labels)
            label_sizes=[numeric(inherited(l,'font-size',width,'16px'),variables,width) for l in labels]
            assert label_sizes==[12,12],label_sizes
            card_grid=values(soup.select_one('.participation-grid'),width).get('grid-template-columns')
            assert card_grid==('minmax(0, 1fr)' if width<=900 else 'repeat(3, minmax(0, 1fr))'),card_grid
            if width<=900:
                for selector in ['.feature-layout','.model-ledger','.faq-layout','.participation-grid']:
                    grid=values(soup.select_one(selector),width).get('grid-template-columns','')
                    assert grid.strip() in ['minmax(0, 1fr)','1fr'],(width,selector,grid)
        report['viewports'].append({'page':route,'width':width,'bodyPx':target,'headingPx':headings[0],'sectionPaddingPx':round(padding,1),'contentLeftPx':round((width-min(width-2*max(20,min(width*.05,72)),1200))/2,1) if route=='index.html' else None,'navigation':'disclosure' if width<=840 else 'connected capsules','passed':True})
report['contrast']=[{'foreground':fg,'background':bg,'ratio':round(contrast(fg,bg),2)} for fg,bg in [('#262f28','#f7f5ee'),('#465345','#f7f5ee'),('#465345','#e9e4d8'),('#173d30','#eae7dd'),('#e3e7df','#173d30'),('#f7f5ee','#173d30'),('#262f28','#ffffff'),('#173d30','#ffffff'),('#ffded2','#173d30')]]
assert all(p['ratio']>=4.5 for p in report['contrast'])
report['passed']=True
(ROOT/'qa/readability-results.json').write_text(json.dumps(report,indent=2)+'\n')
print(f"Passed source checks for {len(report['viewports'])} page/viewport combinations; minimum sampled solid-colour contrast {min(p['ratio'] for p in report['contrast']):.2f}:1. Browser layout/contrast over imagery remains unverified.")
