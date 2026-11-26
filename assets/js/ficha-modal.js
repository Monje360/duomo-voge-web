/* Pop-up de ficha rápida (mismo comportamiento que la web de Suzuki).
   Al pulsar una moto se abre su ficha; "Más información" lleva a la landing del modelo.
   El enlace de la tarjeta se mantiene en el HTML para buscadores y para abrir en otra pestaña. */
(function () {
  "use strict";
  var DATA = null, loading = null, modal = null, lastFocus = null;

  function load() {
    if (DATA) return Promise.resolve(DATA);
    if (!loading) {
      loading = fetch("/assets/js/fichas.json", { credentials: "same-origin" })
        .then(function (r) { return r.json(); })
        .then(function (d) { DATA = d; return d; })
        .catch(function () { loading = null; return null; });
    }
    return loading;
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function eur(n) {
    if (n == null || n === "") return "";
    return String(Math.round(Number(n))).replace(/\B(?=(\d{3})+(?!\d))/g, ".") + " €";
  }

  function ensureModal() {
    if (modal) return modal;
    modal = document.createElement("div");
    modal.className = "fmodal";
    modal.id = "ficha-modal";
    modal.setAttribute("role", "dialog");
    modal.setAttribute("aria-modal", "true");
    modal.setAttribute("aria-hidden", "true");
    modal.innerHTML = '<div class="fmodal__panel" tabindex="-1"></div>';
    document.body.appendChild(modal);
    modal.addEventListener("click", function (e) {
      if (e.target === modal || e.target.closest(".fmodal__close")) close();
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
    return modal;
  }

  function open(m) {
    var el = ensureModal(), cfg = DATA._site || {};
    var colors = m.colors && m.colors.length ? m.colors : [{ name: "", img: m.img }];
    var c0 = colors[0];
    var rows = (m.specs || []).map(function (r) {
      return "<tr><th>" + esc(r[0]) + "</th><td>" + esc(r[1]) + "</td></tr>";
    }).join("");
    var sw = colors.length > 1 ?
      '<div class="fmodal__colors"><div class="fmodal__colors-label">Colores disponibles · <span data-cname>' + esc(c0.name) + "</span></div>" +
      '<div class="fmodal__swatches">' + colors.map(function (c, i) {
        return '<button type="button" class="fswatch' + (i === 0 && !m.img ? " active" : "") + '" data-i="' + i + '" title="' + esc(c.name) + '" aria-label="Color ' + esc(c.name) + '"><img src="/' + esc(c.thumb || c.img) + '" alt="" loading="lazy"></button>';
      }).join("") + "</div></div>" : "";
    var price = c0.price != null ? c0.price : m.price;
    var priceHTML = price ? '<div class="fmodal__price">' + (m.pvp ? "<del>" + eur(m.pvp) + "</del>" : "") +
      "<span data-price>" + (m.desde ? "<small>Desde </small>" : "") + eur(price) + "</span><small>" + esc(cfg.priceNote || "PVP · IVA incluido") + "</small></div>" : "";
    var q = encodeURIComponent(m.name);
    var second = cfg.wa ?
      '<a class="btn fmodal__wa" href="https://wa.me/' + esc(cfg.wa) + "?text=" + encodeURIComponent("Hola, me interesa la " + m.full + ". ¿Me podéis dar más información?") + '" target="_blank" rel="noopener">WhatsApp</a>' :
      '<a class="btn btn--ghost" href="/contacto/?modelo=' + q + '#solicita">Pedir presupuesto</a>';
    el.querySelector(".fmodal__panel").innerHTML =
      '<button type="button" class="fmodal__close" aria-label="Cerrar">&times;</button>' +
      '<div class="fmodal__media"><img src="/' + esc(m.img || c0.img) + '" alt="' + esc(m.full) + '" data-photo></div>' +
      '<div class="fmodal__info">' +
        (m.cat ? '<span class="fmodal__cat">' + esc(m.cat) + "</span>" : "") +
        '<h2 class="fmodal__title">' + esc(m.full) + "</h2>" +
        (m.desc ? '<p class="fmodal__desc">' + esc(m.desc) + "</p>" : "") +
        sw +
        (rows ? '<table class="fspec"><tbody>' + rows + "</tbody></table>" : "") +
        priceHTML +
        '<div class="fmodal__actions">' +
          '<a class="btn btn--primary btn--block fmodal__more" href="' + esc(m.url) + '">Más información <i>&rsaquo;</i></a>' +
          '<div class="fmodal__row">' +
            '<a class="btn btn--ghost" href="/solicitud-de-prueba/?modelo=' + q + '">Solicitar prueba</a>' + second +
          "</div>" +
        "</div>" +
      "</div>";
    var photo = el.querySelector("[data-photo]"), cname = el.querySelector("[data-cname]"), pr = el.querySelector("[data-price]");
    el.querySelectorAll(".fswatch").forEach(function (b) {
      b.addEventListener("click", function () {
        var c = colors[+b.getAttribute("data-i")];
        el.querySelectorAll(".fswatch").forEach(function (x) { x.classList.remove("active"); });
        b.classList.add("active");
        photo.src = "/" + c.img;
        if (cname) cname.textContent = c.name;
        if (pr && c.price != null) pr.innerHTML = (m.desde ? "<small>Desde </small>" : "") + eur(c.price);
      });
    });
    lastFocus = document.activeElement;
    el.classList.add("open");
    el.setAttribute("aria-hidden", "false");
    document.documentElement.classList.add("fmodal-lock");
    el.querySelector(".fmodal__panel").focus({ preventScroll: true });
    if (window.dataLayer) window.dataLayer.push({ event: "ficha_popup", modelo: m.name });
  }

  function close() {
    if (!modal || !modal.classList.contains("open")) return;
    modal.classList.remove("open");
    modal.setAttribute("aria-hidden", "true");
    document.documentElement.classList.remove("fmodal-lock");
    if (lastFocus && lastFocus.focus) lastFocus.focus({ preventScroll: true });
  }

  document.addEventListener("click", function (e) {
    if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
    var card = e.target.closest(".card[data-slug]");
    if (!card) return;
    var slug = card.getAttribute("data-slug");
    var href = (card.querySelector("a[href]") || {}).href;
    e.preventDefault();
    load().then(function (d) {
      if (d && d[slug]) open(d[slug]);
      else if (href) location.href = href;
    });
  });

  // Precarga la ficha cuando el navegador está libre o al acercar el ratón/dedo a una moto
  var pre = function () { load(); };
  if ("requestIdleCallback" in window) requestIdleCallback(function () { if (document.querySelector(".card[data-slug]")) pre(); }, { timeout: 4000 });
  document.addEventListener("pointerover", function (e) { if (e.target.closest && e.target.closest(".card[data-slug]")) pre(); }, { passive: true, once: true });
})();
