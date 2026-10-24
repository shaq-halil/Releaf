// Isolated event/state regression check; this is not a browser/layout test.
const vm=require('node:vm');
const fs=require('node:fs');
const assert=require('node:assert/strict');
const path=require('node:path');
function element(){
 const classes=new Set(),attrs=new Map(),events={};
 return {events,attrs,classList:{add:c=>classes.add(c),remove:c=>classes.delete(c),contains:c=>classes.has(c),toggle(c,on){on=on??!classes.has(c);on?classes.add(c):classes.delete(c);return on;}},
  setAttribute:(k,v)=>attrs.set(k,v),getAttribute:k=>attrs.get(k),addEventListener:(k,fn)=>events[k]=fn,focus(){this.focused=true;}};
}
const header=element(),toggle=element(),nav=element(),body=element(),shape=element();
toggle.setAttribute('aria-expanded','false');
nav.querySelector=()=>({querySelector:()=>shape});
nav.querySelectorAll=()=>[];
nav.getBoundingClientRect=()=>({width:0,height:0});
const domEvents={},winEvents={},frames=[];
const mobile={matches:false,addEventListener(k,fn){this.change=fn;}};
const motion={matches:false,addEventListener(k,fn){this.change=fn;}};
const window={scrollY:0,matchMedia:q=>q.includes('840px')?mobile:motion,addEventListener:(k,fn)=>winEvents[k]=fn};
const document={body,querySelector:s=>({'.menu-toggle':toggle,'#site-nav':nav,'.site-header':header}[s]||null),addEventListener:(k,fn)=>domEvents[k]=fn};
const context={document,window,performance:{now:()=>0},requestAnimationFrame:fn=>{frames.push(fn);return frames.length},cancelAnimationFrame:()=>{}};
vm.runInNewContext(fs.readFileSync(path.join(__dirname,'../assets/js/main.js'),'utf8'),context);
const flush=()=>{while(frames.length)frames.shift()(1000);};
flush();assert.equal(header.classList.contains('is-scrolled'),false);
window.scrollY=200;winEvents.scroll();flush();assert.equal(header.classList.contains('is-scrolled'),true);
window.scrollY=0;winEvents.scroll();flush();assert.equal(header.classList.contains('is-scrolled'),false);
toggle.events.click();assert.equal(header.classList.contains('menu-open'),true);assert.equal(toggle.getAttribute('aria-expanded'),'true');
domEvents.keydown({key:'Escape'});assert.equal(header.classList.contains('menu-open'),false);assert.equal(toggle.focused,true);
toggle.events.click();mobile.matches=true;mobile.change();flush();assert.equal(header.classList.contains('menu-open'),false);
console.log('Header event/state checks passed: initial, scroll, return to top, menu open, Escape focus return and breakpoint change.');
