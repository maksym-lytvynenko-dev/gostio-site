// Burger menu, sticky-header state and scroll reveal. No dependencies.
(function () {
  var burger = document.getElementById('burger');
  var nav = document.getElementById('siteNav');
  if (burger && nav) {
    burger.addEventListener('click', function () {
      var open = nav.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', String(open));
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        nav.classList.remove('is-open');
        burger.setAttribute('aria-expanded', 'false');
      }
    });
  }

  var header = document.getElementById('siteHeader');
  if (header) {
    var onScroll = function () { header.classList.toggle('is-stuck', window.scrollY > 8); };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  var reveals = document.querySelectorAll('.reveal');
  if (!reveals.length) return;
  if (!('IntersectionObserver' in window) || matchMedia('(prefers-reduced-motion: reduce)').matches) {
    reveals.forEach(function (el) { el.classList.add('is-visible'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) { entry.target.classList.add('is-visible'); io.unobserve(entry.target); }
    });
  }, { rootMargin: '0px 0px -10% 0px' });
  reveals.forEach(function (el) { io.observe(el); });
})();

/* Демо-форма: ничего не отправляет, только подтверждает нажатие.
   Бэкенда у презентации нет — это заглушка, и честно об этом пишет. */
(function () {
  var btn = document.querySelector('[data-demo-submit]');
  if (!btn) return;
  btn.addEventListener('click', function () {
    var form = btn.closest('form');
    var out = form.querySelector('.form-result');
    out.textContent = 'Это демо-версия: заявка никуда не ушла. Напишите нам в WhatsApp или на почту — ответим сами.';
    out.hidden = false;
  });
})();
