/* Optional QA tool; no dependency is needed by the published site.
   PLAYWRIGHT_MODULE=/path/to/playwright node qa/browser-check.cjs
*/
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('fs');
const assert = require('node:assert/strict');
const path = require('path');
const base = process.env.RELEAF_PREVIEW_URL || 'http://127.0.0.1:8080/';
const axePath = process.env.AXE_CORE_PATH;
const output = path.join(__dirname, 'previews');
fs.mkdirSync(output, {recursive:true});
(async () => {
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 const results={responsive:[],readability:[],contacts:[],accessibility:[],keyboard:[],progressiveEnhancement:[],screenshots:[]};
 for(const route of ['', 'our-story/']) {
  const page=await browser.newPage({bypassCSP:true});const errors=[];
  page.on('pageerror',e=>errors.push(e.message));

  for(const width of [320,360,390,650,651,768,840,841,900,1024,1440,1920]) {
   await page.setViewportSize({width,height:width<600?844:1000});
   const response=await page.goto(base+route,{waitUntil:'networkidle'});assert.equal(response.status(),200);
   await page.evaluate(()=>document.fonts.ready);
   const audit=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,h1:document.querySelectorAll('h1').length,errors:[...document.images].filter(i=>i.complete&&!i.naturalWidth).map(i=>i.src)}));
   assert.equal(audit.overflow,false,route+width+' overflows');assert.equal(audit.h1,1);assert.deepEqual(audit.errors,[]);assert.deepEqual(errors,[]);
   const readability=await page.evaluate(()=>{
    const size=e=>parseFloat(getComputedStyle(e).fontSize);
    const core=[...document.querySelectorAll('.editorial-copy p:not(.section-label),.model-ledger p,.founder-copy p:not(.eyebrow),.section-heading>p,.faq-list details p,.story-title>p,.story-chapter-copy>p:not(.eyebrow),.leader p,.principle-columns p,.where-now>p:not(.eyebrow),.hero-content>p:not(.hero-kicker),.footer-top p')];
    const headings=[...document.querySelectorAll('main h2')];
    const active=e=>!e.closest('[hidden]')&&e.getClientRects().length;
    const controls=[...document.querySelectorAll('.button,.site-header nav a,.menu-toggle')].filter(active);
    const captions=[...document.querySelectorAll('figcaption,.hero-caption')];
    const invisible=[...document.querySelectorAll('main>section')].filter(e=>{const c=getComputedStyle(e);return c.display==='none'||c.visibility==='hidden'||parseFloat(c.opacity)===0;});
    return {body:core.map(size),headings:headings.map(size),captions:captions.map(size),smallTargets:controls.filter(e=>e.getBoundingClientRect().height<43.5).map(e=>e.className),invisible:invisible.map(e=>e.className),sectionPadding:[...document.querySelectorAll('.section')].map(e=>parseFloat(getComputedStyle(e).paddingTop))};
   });
   assert.ok(readability.body.every(v=>v===(width<=650?17:18)),route+width+' body size');
   assert.ok(readability.headings.every(v=>width<=650?v>=36&&v<=44:v>=40&&v<=56),route+width+' headings');
   assert.ok(readability.captions.every(v=>v>=14),route+width+' captions');
   assert.deepEqual(readability.smallTargets,[],route+width+' small interactive targets');
   assert.deepEqual(readability.invisible,[],route+width+' invisible main sections');
   assert.ok(readability.sectionPadding.every(v=>v<=72),route+width+' excessive section padding');
   if(!route){
    const boundaries=await page.locator('.site-container').evaluateAll(es=>es.map(e=>{const b=e.getBoundingClientRect();return {left:b.left,right:b.right};}));
    assert.equal(boundaries.length,9);
    assert.ok(boundaries.every(b=>Math.abs(b.left-boundaries[0].left)<1&&Math.abs(b.right-boundaries[0].right)<1),JSON.stringify(boundaries));
    const labels=await page.locator('main .section-label').evaluateAll(es=>es.map(e=>e.getBoundingClientRect().left));
    assert.ok(Math.abs(labels[0]-labels[1])<1,'Feature labels must share the text-column edge');
    assert.equal(await page.locator('.participation-card').count(),3);
    const cards=await page.locator('.participation-card').evaluateAll(es=>es.map(e=>{const b=e.getBoundingClientRect();return {top:b.top,left:b.left,height:b.height};}));
    if(width>900){
     assert.ok(cards.every(c=>Math.abs(c.top-cards[0].top)<1&&Math.abs(c.height-cards[0].height)<1));
    }else{
     assert.ok(cards.every(c=>Math.abs(c.left-cards[0].left)<1));
     assert.ok(cards[1].top>cards[0].top&&cards[2].top>cards[1].top);
    }
    const backgrounds=await page.locator('main > .section').evaluateAll(es=>es.map(e=>getComputedStyle(e).backgroundColor));
    assert.deepEqual(backgrounds,['rgb(255, 255, 255)','rgb(23, 61, 48)','rgb(255, 255, 255)','rgb(23, 61, 48)','rgb(255, 255, 255)','rgb(23, 61, 48)']);
    const book=await page.locator('#after-the-page img').boundingBox();
    assert.ok(book.width<=width&&book.height<=(width<=650?280:360));
    if(width<=900){
     for(const selector of ['.feature-layout','.model-ledger','.faq-layout','.participation-grid']){
      assert.equal(await page.locator(selector).first().evaluate(e=>getComputedStyle(e).gridTemplateColumns.split(' ').length),1,selector+' must stack');
     }
    }
   }
   results.readability.push({page:route||'home',width,passed:true,bodySize:width<=650?17:18});
   results.responsive.push({page:route||'home',width,passed:true});
  }
  // All photos must decode. This also makes full-page captures deterministic for native lazy loading.
  await page.setViewportSize({width:1440,height:1000});await page.goto(base+route,{waitUntil:'networkidle'});
  await page.evaluate(async()=>{await document.fonts.ready;await Promise.all([...document.images].map(i=>{i.loading='eager';return i.decode()}));document.querySelectorAll('.waiting').forEach(e=>e.classList.remove('waiting'));});
  await page.waitForTimeout(800);
  const name=route?'our-story':'home';
  for(const [width,label] of [[1440,'desktop'],[768,'tablet'],[390,'mobile']]){
   await page.setViewportSize({width,height:width===390?844:1000});await page.evaluate(()=>scrollTo(0,0));await page.waitForTimeout(400);
   const screenshot=path.join(output,`${name}-${label}.jpg`);await page.screenshot({path:screenshot,type:'jpeg',quality:88});results.screenshots.push(path.relative(__dirname,screenshot));
   await page.screenshot({path:path.join(output,`${name}-${label}-full.jpg`),fullPage:true,type:'jpeg',quality:83});
  }
  await page.setViewportSize({width:1440,height:1000});
  // The founder portrait remains a supporting image; leadership sits in one row.
  assert.ok(await page.locator('.founder-photo').evaluate(e=>e.getBoundingClientRect().width)<=360);
  if(route){
   assert.deepEqual(await page.locator('.leader h3').evaluateAll(es=>es.map(e=>e.textContent.replace(/\s+/g,' ').trim())),['Atika Yakubu','Rosemary Elorn','Halleo Shaq']);
   const top=await page.locator('.leader').evaluateAll(es=>es.map(e=>e.getBoundingClientRect().top));
   assert.ok(top.every(y=>Math.abs(y-top[0])<2));
  } else {
   assert.ok((await page.locator('.hero-image img').getAttribute('alt')).includes('AI-generated concept'));
  }
  if(!route){
   await page.evaluate(()=>scrollTo({top:300,behavior:'instant'}));
   await page.waitForFunction(()=>document.querySelector('.site-header').classList.contains('is-scrolled'));
   await page.waitForTimeout(300);
   assert.equal(await page.locator('.site-header').evaluate(e=>getComputedStyle(e).backgroundColor),'rgb(255, 255, 255)');
   await page.evaluate(()=>scrollTo({top:0,behavior:'instant'}));
   await page.waitForFunction(()=>!document.querySelector('.site-header').classList.contains('is-scrolled'));
  }
  const membrane=page.locator('.nav-shape');
  assert.ok((await membrane.getAttribute('d')).length>50);
  const before=await membrane.getAttribute('d');
  await page.locator('.nav-pill').nth(1).hover();await page.waitForTimeout(750);
  assert.notEqual(await membrane.getAttribute('d'),before);
  await page.mouse.move(0,0);await page.waitForTimeout(750);
  if(axePath){await page.addScriptTag({path:axePath});const axe=await page.evaluate(async()=>await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}}));results.accessibility.push({page:name,violations:axe.violations.map(v=>({id:v.id,impact:v.impact,description:v.description,nodes:v.nodes.map(n=>({target:n.target,summary:n.failureSummary}))}))});}
  assert.equal(await page.locator('form,input,textarea,select,.draft-preview,.form-status').count(),0);
  const contactLink=page.locator('#conversation .contact-button');
  assert.equal(await contactLink.getAttribute('href'),'https://wa.me/233555401859');
  assert.equal(await contactLink.getAttribute('target'),'_blank');
  assert.equal(await contactLink.locator('svg.whatsapp-icon').count(),1);
  if(!route){
   for(const card of await page.locator('.participation-card').all()){
    await card.click();assert.equal(new URL(page.url()).hash,'#conversation');
    assert.ok(await page.locator('#conversation').isVisible());
   }
  }
  for(const width of [360,390,768,1024,1440]){
   await page.setViewportSize({width,height:844});
   const center=await page.locator('.contact-content').evaluate(e=>{const box=e.getBoundingClientRect();const items=[...e.children].map(c=>{const b=c.getBoundingClientRect();return b.left+b.width/2});const p=e.querySelector('p'),s=getComputedStyle(p);return {center:box.left+box.width/2,items,lines:Math.round(p.getBoundingClientRect().height/parseFloat(s.lineHeight))};});
   assert.ok(center.items.every(x=>Math.abs(x-center.center)<1));
   assert.ok(center.lines<=2,'Contact copy should fit in at most two lines at '+width);
  }
  results.contacts.push({page:name,href:'https://wa.me/233555401859',noForms:true});
  await page.setViewportSize({width:390,height:844});await page.evaluate(()=>scrollTo(0,0));
  const toggle=page.locator('.menu-toggle');await toggle.focus();await page.keyboard.press('Enter');assert.equal(await toggle.getAttribute('aria-expanded'),'true');await page.keyboard.press('Tab');assert.equal(await page.evaluate(()=>document.activeElement.textContent.trim()),'Home');await page.keyboard.press('Escape');assert.equal(await toggle.getAttribute('aria-expanded'),'false');assert.ok(await toggle.evaluate(e=>e===document.activeElement));
  await page.locator('.skip-link').focus();await page.keyboard.press('Enter');
  if(!route){const disclosure=page.locator('.faq-list summary').first();await disclosure.focus();await page.keyboard.press('Enter');assert.equal(await disclosure.evaluate(e=>e.parentElement.open),true);}
  results.keyboard.push({page:name,menu:'Enter, Tab and Escape pass; focus returns',skipLink:true,faq:route?'not applicable':'native disclosure tested'});
  await page.emulateMedia({reducedMotion:'reduce'});assert.equal(await page.evaluate(()=>getComputedStyle(document.documentElement).scrollBehavior),'auto');assert.equal(await page.locator('.hero-content').count()?await page.locator('.hero-content').evaluate(e=>getComputedStyle(e).animationName):'none','none');
  await page.close();
  const plain=await browser.newPage({javaScriptEnabled:false,viewport:{width:390,height:844}});await plain.goto(base+route);assert.equal(await plain.locator('nav a').count(),4);assert.ok(await plain.locator('h1').isVisible());assert.equal(await plain.locator('form,input,select,textarea').count(),0);assert.ok(await plain.locator('#conversation .contact-button').isVisible());results.progressiveEnhancement.push({page:name,passed:true});await plain.close();
 }
 fs.writeFileSync(path.join(__dirname,'results.json'),JSON.stringify(results,null,2));
 console.log(JSON.stringify(results,null,2));await browser.close();
 if(results.accessibility.some(r=>r.violations.length))process.exitCode=1;
})().catch(e=>{console.error(e);process.exit(1)});
