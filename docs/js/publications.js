const buttons = [...document.querySelectorAll('.pub-filter-btn')];
const cards = [...document.querySelectorAll('.pub-card')];
const headings = [...document.querySelectorAll('.pub-year-heading')];
const search = document.querySelector('#publication-search');
const resultStatus = document.querySelector('#publication-results');
const yearNav = document.querySelector('.year-nav');
const siteHeader = document.querySelector('.site-header');
const params = new URLSearchParams(location.search);

let topic = params.get('topic') || 'all';
let query = params.get('q') || '';

if (!buttons.some((button) => button.dataset.filter === topic)) topic = 'all';
if (search) search.value = query;
setActiveButton(topic);
filterPublications(false);

buttons.forEach((button) => {
  button.addEventListener('click', () => {
    topic = button.dataset.filter || 'all';
    setActiveButton(topic);
    filterPublications();
  });
});

let searchFrame = 0;
search?.addEventListener('input', () => {
  query = search.value;
  cancelAnimationFrame(searchFrame);
  searchFrame = requestAnimationFrame(() => filterPublications());
});

function setActiveButton(activeTopic) {
  buttons.forEach((button) => {
    const active = button.dataset.filter === activeTopic;
    button.classList.toggle('active', active);
    button.setAttribute('aria-pressed', String(active));
  });
}

function filterPublications(updateUrl = true) {
  const normalizedQuery = query.trim().toLocaleLowerCase();
  let visibleCount = 0;

  cards.forEach((card) => {
    const keywords = (card.dataset.keywords || '').split(',');
    const topicMatch = topic === 'all' || keywords.includes(topic);
    const queryMatch =
      !normalizedQuery ||
      (card.dataset.search || '').toLocaleLowerCase().includes(normalizedQuery);
    const visible = topicMatch && queryMatch;
    card.hidden = !visible;
    if (visible) visibleCount += 1;
  });

  headings.forEach((heading) => {
    let sibling = heading.nextElementSibling;
    let hasVisible = false;
    while (sibling && !sibling.classList.contains('pub-year-heading')) {
      if (sibling.classList.contains('pub-card') && !sibling.hidden) {
        hasVisible = true;
        break;
      }
      sibling = sibling.nextElementSibling;
    }
    heading.hidden = !hasVisible;
    const link = document.querySelector(
      `.year-nav a[data-year="${heading.dataset.year}"]`,
    );
    if (link) link.closest('li').hidden = !hasVisible;
  });

  if (resultStatus) {
    resultStatus.textContent = `${visibleCount} publication${visibleCount === 1 ? '' : 's'}`;
  }

  if (updateUrl) {
    const next = new URL(location.href);
    if (topic === 'all') next.searchParams.delete('topic');
    else next.searchParams.set('topic', topic);
    if (normalizedQuery) next.searchParams.set('q', query.trim());
    else next.searchParams.delete('q');
    history.replaceState({}, '', next);
  }
}

function pinYearNav() {
  if (yearNav && siteHeader) {
    yearNav.style.top = `${siteHeader.offsetHeight - 1}px`;
  }
}
pinYearNav();
addEventListener('resize', pinYearNav, { passive: true });

const yearLinks = [...document.querySelectorAll('.year-nav a')];
if (yearLinks.length && 'IntersectionObserver' in window) {
  const linkFor = Object.fromEntries(
    yearLinks.map((link) => [link.dataset.year, link]),
  );
  const visibleYears = new Set();
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        const year = entry.target.dataset.year;
        if (entry.isIntersecting) visibleYears.add(year);
        else visibleYears.delete(year);
      });
      const year = [...visibleYears].sort().reverse()[0];
      yearLinks.forEach((link) => link.classList.remove('current'));
      if (!year || !linkFor[year]) return;
      const current = linkFor[year];
      current.classList.add('current');
      const list = current.closest('.year-nav__list');
      if (list && list.scrollWidth > list.clientWidth) {
        const target =
          current.offsetLeft - (list.clientWidth - current.offsetWidth) / 2;
        list.scrollTo({ left: Math.max(0, target), behavior: 'smooth' });
      }
    },
    { rootMargin: '-96px 0px -55% 0px' },
  );
  headings.forEach((heading) => observer.observe(heading));
}
