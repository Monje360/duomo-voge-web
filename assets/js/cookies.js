/* ============================================================
   Banner de consentimiento de cookies (RGPD / LSSI)
   Guarda la elección en localStorage y no vuelve a mostrarse.
   La web actual solo usa cookies técnicas (fuentes, formulario
   y mapa). Si en el futuro añades analítica/marketing, cárgala
   SOLO dentro de la función activarCookiesOpcionales().
   ============================================================ */
(function () {
  var KEY = "duomo_cookie_consent";
  try { if (localStorage.getItem(KEY)) { init(localStorage.getItem(KEY)); return; } }
  catch (e) { /* localStorage no disponible */ }

  var bar = document.createElement("div");
  bar.className = "cookie-bar";
  bar.setAttribute("role", "dialog");
  bar.setAttribute("aria-label", "Aviso de cookies");
  bar.innerHTML =
    '<div class="cookie-bar__inner">' +
      '<p class="cookie-bar__txt">Usamos cookies propias y de terceros para el funcionamiento de la web y, con tu permiso, para analítica. ' +
        'Puedes aceptarlas, rechazarlas o consultar más en nuestra <a href="/politica-de-cookies/">Política de cookies</a>.</p>' +
      '<div class="cookie-bar__btns">' +
        '<button class="btn btn--ghost cookie-bar__reject" type="button">Rechazar</button>' +
        '<button class="btn btn--primary cookie-bar__accept" type="button">Aceptar</button>' +
      '</div>' +
    '</div>';
  document.body.appendChild(bar);

  function choose(value) {
    try { localStorage.setItem(KEY, value); } catch (e) {}
    bar.classList.add("cookie-bar--hide");
    setTimeout(function () { bar.remove(); }, 300);
    init(value);
  }
  bar.querySelector(".cookie-bar__accept").addEventListener("click", function () { choose("accepted"); });
  bar.querySelector(".cookie-bar__reject").addEventListener("click", function () { choose("rejected"); });
  requestAnimationFrame(function () { bar.classList.add("cookie-bar--show"); });

  function init(value) {
    if (value === "accepted") activarCookiesOpcionales();
  }

  function activarCookiesOpcionales() {
    /* Aquí iría la carga de analítica/marketing (Google Analytics, Meta Pixel…)
       SOLO si el usuario ha aceptado. Ahora mismo no hay ninguna. */
  }
})();
