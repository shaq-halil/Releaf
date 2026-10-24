'use strict';
document.body.classList.add('js');
const menuToggle = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#site-nav');
const siteHeader = document.querySelector('.site-header');
const mobile = window.matchMedia('(max-width: 840px)');
const motion = window.matchMedia('(prefers-reduced-motion: reduce)');
function closeMenu(returnFocus = false) {
  const wasOpen = menuToggle.getAttribute('aria-expanded') === 'true';
  navigation.classList.remove('open');
  siteHeader.classList.remove('menu-open');
  menuToggle.setAttribute('aria-expanded', 'false');
  if (returnFocus && wasOpen) menuToggle.focus();
}
menuToggle.addEventListener('click', () => {
  const open = menuToggle.getAttribute('aria-expanded') !== 'true';
  menuToggle.setAttribute('aria-expanded', String(open));
  navigation.classList.toggle('open', open);
  siteHeader.classList.toggle('menu-open', open);
});
navigation.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
document.addEventListener('click', event => { if (!event.target.closest('.site-header')) closeMenu(); });
document.addEventListener('keydown', event => { if (event.key === 'Escape') closeMenu(true); });
mobile.addEventListener('change', () => { closeMenu(); animateMembrane(); });

// Original capsule-and-neck geometry. Follow the actual link boxes only while
// their finite CSS transition is running; no perpetual animation or filters.
const membrane = navigation.querySelector('.nav-membrane');
const shape = membrane.querySelector('path');
const pills = [...navigation.querySelectorAll('.nav-pill')];
let frame = 0;
let animateUntil = 0;
function drawMembrane() {
  if (mobile.matches) return;
  const origin = navigation.getBoundingClientRect();
  if (!origin.width || !origin.height) return;
  membrane.setAttribute('viewBox', `0 0 ${origin.width} ${origin.height}`);
  const boxes = pills.map(link => {
    const rect = link.getBoundingClientRect();
    return {x:rect.left-origin.left,y:rect.top-origin.top,w:rect.width,h:rect.height};
  });
  const paths = boxes.map(({x,y,w,h}) => {
    const r = h / 2;
    return `M${x+r},${y} H${x+w-r} A${r},${r} 0 0 1 ${x+w},${y+r} A${r},${r} 0 0 1 ${x+w-r},${y+h} H${x+r} A${r},${r} 0 0 1 ${x},${y+r} A${r},${r} 0 0 1 ${x+r},${y} Z`;
  });
  for (let index=0; index<boxes.length-1; index++) {
    const a=boxes[index], b=boxes[index+1];
    const left=a.x+a.w-a.h*.22, right=b.x+b.h*.22;
    const centerY=a.y+a.h/2, upper=a.y+a.h*.23, lower=a.y+a.h*.77;
    const mid=(left+right)/2;
    paths.push(`M${left},${upper} C${mid},${centerY-5} ${mid},${centerY-5} ${right},${upper} L${right},${lower} C${mid},${centerY+5} ${mid},${centerY+5} ${left},${lower} Z`);
  }
  shape.setAttribute('d', paths.join(' '));
  navigation.classList.add('nav-ready');
}
function tick(time) {
  drawMembrane();
  if (!mobile.matches && !motion.matches && time<animateUntil) frame=requestAnimationFrame(tick);
  else frame=0;
}
function animateMembrane() {
  if (motion.matches) { drawMembrane(); return; }
  animateUntil=performance.now()+650;
  if (!frame) frame=requestAnimationFrame(tick);
}
pills.forEach(link => {
  for (const event of ['pointerenter','pointerleave','focus','blur']) link.addEventListener(event, animateMembrane);
});
if ('ResizeObserver' in window) new ResizeObserver(animateMembrane).observe(navigation);
window.addEventListener('resize', animateMembrane, {passive:true});
motion.addEventListener('change', () => {
  if (frame) cancelAnimationFrame(frame);
  frame=0;
  drawMembrane();
});
if (document.fonts) document.fonts.ready.then(animateMembrane);
animateMembrane();

const floatingContact = document.querySelector('.floating-contact');
const contactSection = document.querySelector('#conversation');
if ('IntersectionObserver' in window && floatingContact && contactSection) {
  new IntersectionObserver(entries => {
    floatingContact.classList.toggle('contact-visible', entries[0].isIntersecting);
  }, {threshold:0}).observe(contactSection);
}

// Class updates preserve the navigation geometry.
let headerFrame = 0;
function updateHeader() {
  siteHeader.classList.toggle('is-scrolled', window.scrollY > 24);
  headerFrame = 0;
}
window.addEventListener('scroll', () => {
  if (!headerFrame) headerFrame = requestAnimationFrame(updateHeader);
}, {passive: true});
window.addEventListener('pageshow', updateHeader);
updateHeader();
