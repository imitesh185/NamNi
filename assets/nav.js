// Injects a Contents toggle so the sidebar TOC is reachable on phones.
(function () {
  function init() {
    var nav = document.getElementById('toc');
    var wrap = document.querySelector('.hwrap');
    if (!nav || !wrap) return;

    var btn = document.createElement('button');
    btn.className = 'btn';
    btn.id = 'navToggle';
    btn.type = 'button';
    btn.textContent = 'Contents';
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-controls', 'toc');

    btn.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      btn.setAttribute('aria-expanded', String(open));
    });

    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        nav.classList.remove('open');
        btn.setAttribute('aria-expanded', 'false');
      }
    });

    var tagline = wrap.querySelector('.tagline');
    wrap.insertBefore(btn, tagline ? tagline.nextSibling : wrap.firstChild);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
