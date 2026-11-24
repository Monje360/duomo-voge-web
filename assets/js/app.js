/* ============================================================
   Voge Madrid Sur — lógica común
   Menú, cabecera, slider, animaciones, filtros, colores,
   y formulario (FormSubmit).
   ============================================================ */
(function () {
  "use strict";
  var cfg = window.DUOMO || {};
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* --- Menú móvil --- */
  var toggle = document.querySelector(".nav__toggle");
  var links = document.getElementById("menu");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      var open = links.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      toggle.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
    });
    links.addEventListener("click", function (e) {
      if (e.target.closest("a")) { links.classList.remove("open"); toggle.setAttribute("aria-expanded", "false"); }
    });
  }

  /* --- Sombra en la cabecera al hacer scroll --- */
  var header = document.querySelector(".site-header");
  if (header) {
    var onScroll = function () { header.classList.toggle("scrolled", window.scrollY > 10); };
    window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
  }

  /* --- Slider del hero --- */
  var slides = document.querySelectorAll(".hero__slide");
  var dots = document.querySelectorAll(".hero__dots button");
  if (slides.length > 1) {
    var cur = 0, timer;
    var go = function (n) {
      slides[cur].classList.remove("is-active"); if (dots[cur]) dots[cur].classList.remove("is-active");
      cur = (n + slides.length) % slides.length;
      var img = slides[cur].querySelector("img"); if (img && img.loading === "lazy") img.loading = "eager";
      slides[cur].classList.add("is-active"); if (dots[cur]) dots[cur].classList.add("is-active");
    };
    var start = function () { if (!reduce) timer = setInterval(function () { go(cur + 1); }, 6500); };
    dots.forEach(function (d, i) { d.addEventListener("click", function () { clearInterval(timer); go(i); start(); }); });
    start();
  }

  /* --- Animaciones de entrada al hacer scroll --- */
  var revealEls = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revealEls.forEach(function (el) { io.observe(el); });
  } else {
    revealEls.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* --- Contadores animados --- */
  var counters = document.querySelectorAll("[data-count]");
  if ("IntersectionObserver" in window && !reduce && counters.length) {
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, end = parseInt(el.getAttribute("data-count"), 10), from = end > 1000 ? end - 60 : 0, t0 = null;
        var step = function (ts) {
          if (!t0) t0 = ts; var p = Math.min((ts - t0) / 1400, 1), v = Math.round(from + (end - from) * (1 - Math.pow(1 - p, 3)));
          el.textContent = v; if (p < 1) requestAnimationFrame(step);
        };
        requestAnimationFrame(step); co.unobserve(el);
      });
    }, { threshold: 0.6 });
    counters.forEach(function (c) { co.observe(c); });
  }

  /* --- Filtro de la gama por categoría --- */
  var bar = document.getElementById("cat-bar");
  var grid = document.getElementById("models-grid");
  if (bar && grid) {
    bar.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return;
      bar.querySelectorAll("button").forEach(function (x) { x.classList.remove("active"); x.setAttribute("aria-pressed", "false"); });
      b.classList.add("active"); b.setAttribute("aria-pressed", "true");
      var f = b.getAttribute("data-filter");
      grid.querySelectorAll(".card").forEach(function (c) {
        var show = f === "Todas" || c.getAttribute("data-cat") === f;
        c.classList.toggle("is-hidden", !show);
        if (show) c.classList.add("is-in");
      });
    });
  }

  /* --- Selector de color en la ficha --- */
  var photo = document.getElementById("model-photo");
  var colorName = document.getElementById("color-name");
  document.querySelectorAll(".swatch").forEach(function (sw) {
    var pre = new Image(); pre.src = sw.getAttribute("data-img");
    sw.addEventListener("click", function () {
      document.querySelectorAll(".swatch").forEach(function (x) { x.classList.remove("active"); x.setAttribute("aria-pressed", "false"); });
      sw.classList.add("active"); sw.setAttribute("aria-pressed", "true");
      if (colorName) colorName.textContent = sw.getAttribute("data-name");
      if (photo) {
        photo.classList.remove("is-first"); photo.classList.add("is-swapping");
        setTimeout(function () {
          photo.src = sw.getAttribute("data-img");
          photo.alt = photo.alt.replace(/en color .*/, "en color " + sw.getAttribute("data-name").toLowerCase());
          photo.classList.remove("is-swapping");
        }, reduce ? 0 : 200);
      }
    });
  });

  /* --- Preseleccionar el modelo en el formulario (?modelo=...) --- */
  var cform = document.getElementById("contact-form");
  if (cform) {
    var modelo = new URLSearchParams(location.search).get("modelo");
    if (modelo) {
      var sel = cform.querySelector('[name="modelo"]');
      if (sel && sel.tagName === "SELECT") {
        var opt = Array.prototype.find.call(sel.options, function (o) { return o.value === modelo || o.textContent.trim() === modelo; });
        if (opt) sel.value = opt.value;
      }
      var msg = cform.querySelector('[name="mensaje"]');
      if (msg && !msg.value) msg.value = "Hola, me interesa la Voge " + modelo + ". ¿Me podéis dar más información?";
    }

    /* --- Envío vía FormSubmit (AJAX), igual que en la web de Suzuki --- */
    var status = document.getElementById("form-status");
    cform.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!cform.checkValidity()) {
        cform.reportValidity();
        return;
      }
      var btn = cform.querySelector('button[type="submit"]');
      var original = btn.textContent;
      btn.disabled = true; btn.textContent = "Enviando…";
      if (status) status.hidden = true;
      var data = new FormData(cform);
      data.append("pagina", location.href);
      fetch("https://formsubmit.co/ajax/" + encodeURIComponent(cfg.email || "info@duomomotor.com"), {
        method: "POST", headers: { "Accept": "application/json" }, body: data
      }).then(function (res) {
        return res.json().catch(function () { return {}; }).then(function (j) {
          if (!res.ok || j.success === "false" || j.success === false) throw new Error(j.message || "error");
        });
      }).then(function () {
        cform.reset();
        if (status) {
          status.className = "form-status form-status--ok";
          status.textContent = "¡Gracias! Hemos recibido tu solicitud. Te contactamos lo antes posible.";
        }
      }).catch(function () {
        if (status) {
          status.className = "form-status form-status--err";
          status.innerHTML = 'No se ha podido enviar. Inténtalo de nuevo o llámanos al <a href="tel:+34910409276">910 409 276</a>.';
        }
      }).finally(function () {
        if (status) { status.hidden = false; status.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "nearest" }); }
        btn.disabled = false; btn.textContent = original;
      });
    });
  }

  /* Colores de la ficha: pestañas y miniaturas */
  document.querySelectorAll(".ctab").forEach(function (t) {
    t.addEventListener("click", function () {
      var i = t.getAttribute("data-color");
      document.querySelectorAll(".ctab").forEach(function (x) { var on = x === t; x.classList.toggle("active", on); x.setAttribute("aria-selected", on ? "true" : "false"); });
      document.querySelectorAll(".cpane").forEach(function (p) { var on = p.getAttribute("data-color") === i; p.classList.toggle("active", on); p.hidden = !on; });
    });
  });
  document.querySelectorAll(".cthumb").forEach(function (b) {
    b.addEventListener("click", function () {
      var pane = b.closest(".cpane"); if (!pane) return;
      var big = pane.querySelector(".cpane__big img");
      var im = b.querySelector("img");
      big.src = b.getAttribute("data-src");
      if (im) { big.width = im.width && im.naturalWidth ? im.naturalWidth : big.width; big.height = im.naturalHeight || big.height; }
      pane.querySelectorAll(".cthumb").forEach(function (x) { x.classList.toggle("active", x === b); });
    });
  });
})();
