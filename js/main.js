/* Live Dogs Design Co. — vanilla JS, ~1 KB. */

document.documentElement.classList.add('js');

// Auto copyright year.
document.querySelectorAll('.year').forEach((el) => {
  el.textContent = new Date().getFullYear();
});

// Mobile nav toggle.
const toggle = document.querySelector('.site-nav__toggle');
const menu = document.getElementById('nav-menu');
if (toggle && menu) {
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') === 'true';
    toggle.setAttribute('aria-expanded', String(!open));
    menu.classList.toggle('is-open', !open);
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && menu.classList.contains('is-open')) {
      toggle.setAttribute('aria-expanded', 'false');
      menu.classList.remove('is-open');
      toggle.focus();
    }
  });
}

// Shrink the top nav once the page scrolls.
const header = document.querySelector('.site-header');
if (header) {
  let ticking = false;
  const update = () => {
    header.classList.toggle('is-shrunk', window.scrollY > 40);
    ticking = false;
  };
  window.addEventListener('scroll', () => {
    if (!ticking) { requestAnimationFrame(update); ticking = true; }
  }, { passive: true });
  update();
}

// Constellation side rail: track which section owns the viewport.
const rail = document.querySelector('.star-rail');
if (rail) {
  const items = [...rail.querySelectorAll('.star-rail__item')];
  const targets = items.map((a) => {
    const href = a.getAttribute('href');
    return href === '#' ? document.body : document.querySelector(href);
  });
  const spy = () => {
    const probe = window.scrollY + window.innerHeight * 0.35;
    let active = 0;
    targets.forEach((t, i) => { if (t && t.offsetTop <= probe) active = i; });
    items.forEach((a, i) => {
      a.classList.toggle('is-active', i === active);
      a.classList.toggle('is-passed', i < active);
    });
  };
  let railTick = false;
  const onMove = () => {
    if (!railTick) { requestAnimationFrame(() => { spy(); railTick = false; }); railTick = true; }
  };
  window.addEventListener('scroll', onMove, { passive: true });
  window.addEventListener('resize', onMove, { passive: true });
  window.addEventListener('load', spy);
  spy();
}

// Scroll reveals.
const reveals = document.querySelectorAll('.reveal');
if ('IntersectionObserver' in window) {
  const io = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        io.unobserve(entry.target);
      }
    }
  }, { threshold: 0.12, rootMargin: '0px 0px -4% 0px' });
  reveals.forEach((el) => io.observe(el));
} else {
  reveals.forEach((el) => el.classList.add('is-visible'));
}
