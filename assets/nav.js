// Site navigation for lesson pages: breadcrumb + sibling contents + prev/next.
// Also injects the Contents toggle so a sidebar TOC is reachable on phones.
(function () {

  // [site-relative path, chip label]. Paths must be unique; filenames need not be.
  var TRACKS = [
    {
      name: 'Python · Object Model',
      items: [
        ['tracks/python/object-model/1.1-identity-type-value.html', '1.1 Identity'],
        ['tracks/python/object-model/1.2-namespaces.html',          '1.2 Namespaces'],
        ['tracks/python/object-model/1.3-references-aliasing.html', '1.3 References'],
        ['tracks/python/object-model/cram.html',                    'Cram 1.1–1.3']
      ]
    },
    {
      name: 'Python · Data Model',
      items: [
        ['tracks/python/data-model/2.1-special-methods.html', '2.1 Special methods']
      ]
    },
    {
      name: 'Python · Runtime',
      items: [
        ['tracks/python/runtime/the-write-path.html', 'The write path']
      ]
    },
    {
      name: 'Systems Thinking',
      items: [
        ['tracks/systems-thinking/overview.html', 'Overview']
      ]
    },
    {
      name: 'Game Theory & Signalling',
      items: [
        ['tracks/game-theory/overview.html', 'Overview']
      ]
    },
    {
      name: 'Predictive Processing',
      items: [
        ['tracks/predictive-processing/overview.html', 'Overview']
      ]
    },
    {
      name: 'Metacognition',
      items: [
        ['tracks/metacognition/overview.html', 'Overview']
      ]
    }
  ];

  // The base.css link already encodes this page's relative path to the site root.
  function rootPrefix() {
    var link = document.querySelector('link[href$="assets/base.css"]');
    if (!link) return '';
    return link.getAttribute('href').replace(/assets\/base\.css$/, '');
  }

  function currentPath() {
    return decodeURIComponent(window.location.pathname);
  }

  function locate(path) {
    for (var t = 0; t < TRACKS.length; t++) {
      for (var i = 0; i < TRACKS[t].items.length; i++) {
        var p = TRACKS[t].items[i][0];
        if (path === p || path.slice(-(p.length + 1)) === '/' + p) {
          return { track: TRACKS[t], index: i };
        }
      }
    }
    return null;
  }

  function link(href, text, cls) {
    var a = document.createElement('a');
    a.href = href;
    if (text) a.textContent = text;
    if (cls) a.className = cls;
    return a;
  }

  function buildSiteBar(root, spot) {
    var bar = document.createElement('div');
    bar.className = 'sitebar';

    var inner = document.createElement('div');
    inner.className = 'sbwrap';

    var crumb = document.createElement('div');
    crumb.className = 'sbcrumb';
    crumb.appendChild(link(root + 'index.html', 'Home'));
    crumb.appendChild(document.createTextNode('/'));
    crumb.appendChild(link(root + 'tracks/index.html', 'Tracks'));
    crumb.appendChild(document.createTextNode('/'));
    var here = document.createElement('span');
    here.textContent = spot.track.name;
    crumb.appendChild(here);
    inner.appendChild(crumb);

    if (spot.track.items.length > 1) {
      var chips = document.createElement('div');
      chips.className = 'sbchips';
      spot.track.items.forEach(function (item, i) {
        chips.appendChild(link(root + item[0], item[1], i === spot.index ? 'chip cur' : 'chip'));
      });
      inner.appendChild(chips);
    }

    bar.appendChild(inner);
    return bar;
  }

  function buildPageNav(root, spot) {
    var items = spot.track.items;
    var prev = spot.index > 0 ? items[spot.index - 1] : null;
    var next = spot.index < items.length - 1 ? items[spot.index + 1] : null;

    var wrap = document.createElement('nav');
    wrap.className = 'pagenav';

    if (prev) {
      var p = link(root + prev[0], null, 'pn prev');
      p.appendChild(kicker('Previous'));
      p.appendChild(title(prev[1]));
      wrap.appendChild(p);
    }

    var up = link(root + 'tracks/index.html', null, 'pn up');
    up.appendChild(kicker('All'));
    up.appendChild(title('Tracks'));
    wrap.appendChild(up);

    if (next) {
      var n = link(root + next[0], null, 'pn next');
      n.appendChild(kicker('Next'));
      n.appendChild(title(next[1]));
      wrap.appendChild(n);
    }
    return wrap;
  }

  function kicker(text) {
    var s = document.createElement('span');
    s.className = 'pnk';
    s.textContent = text;
    return s;
  }

  function title(text) {
    var s = document.createElement('span');
    s.className = 'pnt';
    s.textContent = text;
    return s;
  }

  function contentsToggle() {
    var toc = document.getElementById('toc');
    var wrap = document.querySelector('.hwrap');
    if (!toc || !wrap) return;

    var btn = document.createElement('button');
    btn.className = 'btn';
    btn.id = 'navToggle';
    btn.type = 'button';
    btn.textContent = 'Contents';
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-controls', 'toc');

    btn.addEventListener('click', function () {
      var open = toc.classList.toggle('open');
      btn.setAttribute('aria-expanded', String(open));
    });

    toc.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        toc.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
      }
    });

    var tagline = wrap.querySelector('.tagline');
    wrap.insertBefore(btn, tagline ? tagline.nextSibling : wrap.firstChild);
  }

  function init() {
    contentsToggle();

    var spot = locate(currentPath());
    if (!spot) return;

    var root = rootPrefix();
    var header = document.querySelector('header');
    if (header && header.parentNode) {
      header.parentNode.insertBefore(buildSiteBar(root, spot), header.nextSibling);
    }

    var footer = document.querySelector('footer');
    var pagenav = buildPageNav(root, spot);
    if (footer && footer.parentNode) footer.parentNode.insertBefore(pagenav, footer);
    else document.body.appendChild(pagenav);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
