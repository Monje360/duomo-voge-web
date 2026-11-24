#!/usr/bin/env python3
"""
Generador de la web Voge Madrid Sur (Duomo Motor Bikes): concesionarios oficiales Voge en Móstoles y Getafe.

Uso:  python3 _build/generar.py     (desde la raíz del repo)

Lee _build/modelos.json (precios, textos, colores, galerías y fotos de cada moto, sacados del WordPress)
y crea todas las páginas HTML estáticas, el sitemap.xml, el robots.txt, el llms.txt y el blog.
Para cambiar un precio: edita modelos.json y vuelve a ejecutar este script.
"""
import json, os, re, html, datetime
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = json.load(open(os.path.join(ROOT, "_build", "modelos.json"), encoding="utf-8"))
TODAY = datetime.date.today().isoformat()
MARCA = "Voge"

# ------------------------------------------------------------------ DATOS
SITE = "https://voge.duomomotor.com"
NEGOCIO = {
    "nombre": "Voge Madrid Sur · Duomo Motor Bikes",
    "razon": "DUOMO MOTOR BIKES S.L.",
    "cif": "B-88303029",
    "calle": "Calle Juan de la Cierva, 7-9",
    "cp": "28936",
    "ciudad": "Móstoles",
    "provincia": "Madrid",
    "tel": "910 409 276",
    "telIntl": "+34910409276",
    "email": "info@duomomotor.com",
    "instagram": "https://www.instagram.com/duomomotorbikes/",
    "instagramUser": "@duomomotorbikes",
    "horario": "Lunes a viernes de 10:00 a 14:00 y de 16:00 a 19:30 · Sábados de 10:00 a 14:00",
    "telTaller": "657 405 967",
    "telTallerIntl": "+34657405967",
    "horarioCorto": "L–V 10–14 · 16–19:30 · Sáb 10–14",
}
DIRECCION = f'{NEGOCIO["calle"]}, {NEGOCIO["cp"]} {NEGOCIO["ciudad"]}, {NEGOCIO["provincia"]}'
MAPS_EMBED = "https://www.google.com/maps?q=Duomo+Motor+Bikes,+Calle+Juan+de+la+Cierva+9,+28936+M%C3%B3stoles,+Madrid&output=embed"
MAPS_DIR = "https://www.google.com/maps/dir/?api=1&destination=Duomo+Motor+Bikes+Calle+Juan+de+la+Cierva+9+28936+M%C3%B3stoles"
GEO = {"@type": "GeoCoordinates", "latitude": 40.3156913, "longitude": -3.8449764}
GMAPS = "https://maps.google.com/?cid=11488602729117650723"  # ficha de Google de Duomo Motor Bikes (Móstoles)
GETAFE = {
    "nombre": "Voge Getafe · Duomo Motor Bikes",
    "calle": "Calle Barberán y Collar, 1", "cp": "28903", "ciudad": "Getafe", "provincia": "Madrid",
    "tel": "919 59 63 33", "telIntl": "+34919596333",
    "horario": NEGOCIO["horario"],
    "geo": {"@type": "GeoCoordinates", "latitude": 40.31114, "longitude": -3.72551},
    "gmaps": "https://maps.google.com/?cid=5326891658949733228",
    "embed": "https://www.google.com/maps?q=VOGE+Getafe,+Calle+Barberan+y+Collar+1,+28903+Getafe&output=embed",
    "dir": "https://www.google.com/maps/dir/?api=1&destination=VOGE+Getafe+Calle+Barberan+y+Collar+1+28903+Getafe",
}
DIR_GETAFE = f'{GETAFE["calle"]}, {GETAFE["cp"]} {GETAFE["ciudad"]}, {GETAFE["provincia"]}'
XMADRID = "a 5 minutos del X-Madrid"
INDEXNOW_KEY = "4d8a2f61c9e3b7054a1d6e9f8c2b3a71"
CREDENCIALES = "Tradición familiar en automoción desde 1960 y Duomo Motor Bikes, dedicado solo a las dos ruedas, desde 2020: más de 20 profesionales del motor, más de 1.500 motos entregadas y concesionarios oficiales Voge en Móstoles y Getafe."
ZONAS = ["Móstoles", "Getafe", "Alcorcón", "Fuenlabrada", "Leganés", "Parla", "Pinto", "Villaviciosa de Odón",
         "Navalcarnero", "Arroyomolinos", "Humanes de Madrid", "Madrid capital"]

CATS = [
    {"slug": "scooters", "name": "Scooters", "plural": "Scooters", "img": "motos-voge-scooters.webp",
     "corto": "Diseño moderno, agilidad urbana y máxima eficiencia para que cada trayecto sea cómodo, práctico y seguro",
     "h1": "Scooters Voge en Madrid Sur",
     "title": "Scooters Voge SR16, SR1, SR4 y SR450X · Móstoles y Getafe",
     "meta": "Scooters Voge SR16, SR1, SR1 ADV, SR3, SR4 Radar y SR450X en Duomo Motor Bikes, concesionarios oficiales en Móstoles y Getafe. Precios y prueba sin compromiso.",
     "intro": ["Los scooters Voge van desde los <b>125 cc</b> que puedes llevar con el carnet de coche (con tres años de antigüedad), como la <a href=\"/modelo/sr16/\">SR16</a>, la <a href=\"/modelo/sr1/\">SR1</a> o la <a href=\"/modelo/sr1-adv/\">SR1 ADV</a>, hasta la <a href=\"/modelo/sr3/\">SR3</a>, la <a href=\"/modelo/sr4-radar/\">SR4 Radar</a> con detección de ángulo muerto y la <a href=\"/modelo/sr450x/\">SR450X</a> para el carnet A2.",
               "Si buscas dejar el coche para ir a trabajar a Madrid, aparcar sin dar vueltas o hacer escapadas los fines de semana, aquí tienes toda la gama con precios actualizados. Ven a verlos a Voge Móstoles o Voge Getafe."]},
    {"slug": "naked", "name": "Naked", "plural": "Naked", "img": "motos-voge-naked.webp",
     "corto": "Carácter directo, diseño minimalista y una respuesta dinámica que conecta piloto y máquina en cada aceleración",
     "h1": "Motos naked Voge en Madrid Sur",
     "title": "Motos naked Voge 125R, 125RS y 625R · Móstoles y Getafe",
     "meta": "Naked Voge 125R, 125RS y 625R en Duomo Motor Bikes, concesionarios oficiales en Móstoles y Getafe. Carnet A1, B y A (625R con versión A2). Precios y prueba.",
     "intro": ["Las naked de Voge van desde las <a href=\"/modelo/125r/\">125R</a> y <a href=\"/modelo/125rs/\">125RS</a>, con 15 CV, el máximo para el carnet A1 (o el de coche con más de tres años), hasta la <a href=\"/modelo/625r/\">625R</a> bicilíndrica de 64 CV, también disponible en versión limitada a 35 kW para el A2.",
               "Diseño agresivo, buen equipamiento de serie y precios muy ajustados. Pásate por Voge Móstoles o Voge Getafe y compáralas una al lado de la otra."]},
    {"slug": "adventure", "name": "Adventure", "plural": "Adventure", "img": "motos-voge-adventure.webp",
     "corto": "Diseñada para quienes entienden la moto como libertad absoluta. Disfrútala en asfalto, tierra o largos viajes",
     "h1": "Motos adventure y trail Voge en Madrid Sur",
     "title": "Motos trail Voge 300 Rally, 525DSX, 625DSX, 900DSX · Precios",
     "meta": "Motos trail y adventure Voge 300 Rally, 525DSX, 625DSX, DS800 Rally y 900DSX en Duomo Motor Bikes, Móstoles y Getafe. Precios, carnets A2 y A y prueba.",
     "intro": ["La gama adventure de Voge cubre del carnet A2 al A: la <a href=\"/modelo/300-rally/\">300 Rally</a> y la <a href=\"/modelo/525dsx/\">525DSX</a> se llevan con el A2, y la <a href=\"/modelo/625dsx/\">625DSX</a>, la <a href=\"/modelo/ds800-rally/\">DS800 Rally</a> y la <a href=\"/modelo/900dsx/\">900DSX</a> suben a 64 y 95 CV para el carnet A.",
               "Son motos pensadas para viajar, hacer pistas y usarlas a diario. Te ayudamos a elegir la altura de asiento y la versión que mejor encaja contigo en Voge Móstoles o Voge Getafe."]},
]
CAT = {c["name"]: c for c in CATS}

LIC = {
    "A1": {"tag": "A1 · B", "label": "Carnet A1 o B (+3 años)", "corto": "A1 / B+3",
           "texto": "Es una moto de 125 cc, así que puedes llevarla con el carnet A1 o con el carnet de coche (B) si tiene más de tres años de antigüedad."},
    "A2": {"tag": "A2", "label": "Carnet A2", "corto": "A2",
           "texto": "Su potencia está dentro del límite de 35 kW (47,6 CV), así que puedes llevarla con el carnet A2."},
    "A":  {"tag": "A", "label": "Carnet A", "corto": "A",
           "texto": "Por su potencia necesitas el carnet A. Si tienes el A2, consúltanos qué Voge puedes llevar o cuándo podrás dar el salto."},
    "A-A2": {"tag": "A · A2", "label": "Carnet A (versión A2 disponible)", "corto": "A · A2 lim.",
           "texto": "Con 64 CV necesitas el carnet A, pero también está disponible en versión limitada a 35 kW, ideal para el carnet A2."},
}
LIC_ORDER = ["A1", "A2", "A-A2", "A"]

def e(s): return html.escape(str(s), quote=True)
def eur(n): return f"{n:,.0f}".replace(",", ".") + " €"
def model_url(m): return f"/modelo/{m['slug']}/"
def cat_url(c): return f"/categoria-producto/{c['slug']}/"
def full(m): return f"Voge {m['name']}"
def jsonld(obj): return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>"
def plain(s): return re.sub(r"<[^>]+>", "", s)
def mm(slug): return next(m for m in M if m["slug"] == slug)
def lic_ok_a2(m): return m["license"] in ("A2", "A-A2")

HORAS = [
    {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "10:00", "closes": "14:00"},
    {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "16:00", "closes": "19:30"},
    {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "10:00", "closes": "14:00"}]
DEALER_ID = SITE + "/#concesionario"
GETAFE_ID = SITE + "/concesionario-voge-madrid-sur/#voge-getafe"
DEALER = {
    "@context": "https://schema.org", "@type": "MotorcycleDealer", "@id": DEALER_ID,
    "name": "Voge Móstoles · Duomo Motor Bikes", "alternateName": "Voge Madrid Sur", "legalName": NEGOCIO["razon"], "url": SITE + "/",
    "image": SITE + "/assets/img/og/voge-madrid-sur.jpg", "logo": SITE + "/assets/img/logo/voge-madrid-sur-negro.png",
    "telephone": NEGOCIO["telIntl"], "email": NEGOCIO["email"], "priceRange": "€€",
    "address": {"@type": "PostalAddress", "streetAddress": NEGOCIO["calle"], "postalCode": NEGOCIO["cp"],
                "addressLocality": NEGOCIO["ciudad"], "addressRegion": "Comunidad de Madrid", "addressCountry": "ES"},
    "openingHoursSpecification": HORAS,
    "brand": {"@type": "Brand", "name": "Voge"},
    "geo": GEO, "hasMap": GMAPS, "sameAs": [NEGOCIO["instagram"], GMAPS],
    "foundingDate": "2020", "currenciesAccepted": "EUR", "paymentAccepted": "Efectivo, tarjeta, transferencia, financiación",
    "parentOrganization": {"@type": "Organization", "name": "Duomo Motor Bikes", "url": "https://duomomotor.com/"},
}
DEALER_GETAFE = {
    "@context": "https://schema.org", "@type": "MotorcycleDealer", "@id": GETAFE_ID,
    "name": GETAFE["nombre"], "legalName": NEGOCIO["razon"], "url": SITE + "/concesionario-voge-madrid-sur/",
    "image": SITE + "/assets/img/og/voge-madrid-sur.jpg", "logo": SITE + "/assets/img/logo/voge-madrid-sur-negro.png",
    "telephone": GETAFE["telIntl"], "email": NEGOCIO["email"], "priceRange": "€€",
    "address": {"@type": "PostalAddress", "streetAddress": GETAFE["calle"], "postalCode": GETAFE["cp"],
                "addressLocality": GETAFE["ciudad"], "addressRegion": "Comunidad de Madrid", "addressCountry": "ES"},
    "openingHoursSpecification": HORAS, "geo": GETAFE["geo"], "hasMap": GETAFE["gmaps"], "sameAs": [GETAFE["gmaps"]],
    "brand": {"@type": "Brand", "name": "Voge"},
    "parentOrganization": {"@type": "Organization", "name": "Duomo Motor Bikes", "url": "https://duomomotor.com/"},
}

# ------------------------------------------------------------------ PLANTILLA
def head(title, desc, path, og_img="/assets/img/og/voge-madrid-sur.jpg", ld=(), noindex=False, preload=None):
    canon = SITE + path
    ld_html = "\n".join(jsonld(x) for x in ld)
    pre = f'<link rel="preload" as="image" href="{preload}" fetchpriority="high">' if preload else ""
    robots = '<meta name="robots" content="noindex, follow">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'
    return f"""<!DOCTYPE html>
<html lang="es" class="no-js">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  {robots}
  <link rel="canonical" href="{canon}">
  <meta name="theme-color" content="#16171d">
  <meta name="geo.region" content="ES-MD">
  <meta name="geo.placename" content="Móstoles; Getafe">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="es_ES">
  <meta property="og:site_name" content="Voge Madrid Sur · Duomo Motor Bikes">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:url" content="{canon}">
  <meta property="og:image" content="{SITE}{og_img}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{e(title)}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="alternate" type="application/rss+xml" title="Blog Voge Madrid Sur" href="{SITE}/blog/feed.xml">
  <link rel="icon" href="/favicon.png" sizes="32x32">
  <link rel="apple-touch-icon" href="/assets/img/logo/icon-180.png">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet" media="print" onload="this.media='all'">
  <noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet"></noscript>
  {pre}
  <link rel="stylesheet" href="/assets/css/style.css">
  <script>document.documentElement.classList.remove('no-js')</script>
  {ld_html}
</head>"""

NAV = [("Inicio", "/", "inicio"), ("Modelos", "/#gama", "modelos"), ("Puntos de venta", "/concesionario-voge-madrid-sur/", "concesionario"),
       ("Blog", "/blog/", "blog"), ("Contacto", "/contacto/", "contacto")]
WHATSAPP = "34613915505"; WHATSAPP_TXT = "613 91 55 05"

def header(active=""):
    links = "".join(f'<a href="{u}"{" class=\"active\" aria-current=\"page\"" if k == active else ""}>{n}</a>' for n, u, k in NAV)
    return f"""<body>
  <a class="skip" href="#contenido">Saltar al contenido</a>
  <div class="topbar"><div class="wrap">
    <div class="topbar__info"><span>Concesionarios en Móstoles y Getafe</span></div>
    <span class="topbar__tels"><a href="tel:{NEGOCIO["telIntl"]}">910 40 92 76</a> · <a href="tel:{GETAFE["telIntl"]}">{GETAFE["tel"]}</a> · <a href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener">WhatsApp {WHATSAPP_TXT}</a> · <a href="{NEGOCIO["instagram"]}" target="_blank" rel="noopener" aria-label="Instagram">Instagram</a></span>
  </div></div>
  <header class="site-header">
    <div class="wrap nav">
      <a class="brand" href="/" aria-label="Voge Madrid Sur · Inicio">
        <img src="/assets/img/logo/voge-madrid-sur-negro.png" srcset="/assets/img/logo/voge-madrid-sur-negro@2x.png 2x" alt="Voge Madrid Sur" width="406" height="150">
      </a>
      <nav class="nav__links" id="menu" aria-label="Menú principal">
        {links}
        <a class="btn btn--primary" href="/solicitud-de-prueba/">Solicitar prueba</a>
      </nav>
      <button class="nav__toggle" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
    </div>
  </header>
  <main id="contenido">"""

def footer():
    cats = "".join(f'<a href="{cat_url(c)}">{c["plural"]}</a>' for c in CATS)
    return f"""  </main>
  <footer class="site-footer">
    <div class="wrap footer-grid">
      <div>
        <img class="footer-logo" src="/assets/img/logo/voge-madrid-sur-blanco.png" srcset="/assets/img/logo/voge-madrid-sur-blanco@2x.png 2x" alt="Voge Madrid Sur" width="406" height="150" loading="lazy">
        <p style="max-width:38ch">Duomo Motor Bikes · Concesionarios oficiales Voge en Móstoles y Getafe.</p>
        <p class="disclaimer">Voge y los nombres de sus modelos son marcas registradas de su fabricante. Esta web pertenece a un concesionario oficial, no es la web oficial de la marca. Precios orientativos sujetos a la tarifa y promociones vigentes.</p>
      </div>
      <div>
        <h2>Navegación</h2>
        <a href="/">Voge Madrid Sur</a>
        <a href="/solicitud-de-prueba/">Solicita una prueba</a>
        <a href="/concesionario-voge-madrid-sur/">Tu concesionario</a>
        <a href="/blog/">Blog</a>
        <a href="/contacto/">Contacto</a>
      </div>
      <div>
        <h2>Modelos</h2>
        {cats}
      </div>
      <div>
        <h2>Dónde estamos</h2>
        <address>
          <a href="{MAPS_DIR}" target="_blank" rel="noopener"><b>Voge Móstoles</b><br>{e(NEGOCIO["calle"])}<br>{NEGOCIO["cp"]} {e(NEGOCIO["ciudad"])} (Madrid)</a>
          <a href="tel:{NEGOCIO["telIntl"]}">910 40 92 76</a>
          <a href="{GETAFE["dir"]}" target="_blank" rel="noopener" style="margin-top:8px"><b>Voge Getafe</b><br>{e(GETAFE["calle"])}<br>{GETAFE["cp"]} {e(GETAFE["ciudad"])} (Madrid)</a>
          <a href="tel:{GETAFE["telIntl"]}">{GETAFE["tel"]}</a>
          <a href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener">WhatsApp {WHATSAPP_TXT}</a>
          <a href="mailto:{NEGOCIO["email"]}">{NEGOCIO["email"]}</a>
          <a href="{NEGOCIO["instagram"]}" target="_blank" rel="noopener">{NEGOCIO["instagramUser"]}</a>
        </address>
      </div>
    </div>
    <div class="wrap footer-bottom">
      <span>© <span id="year">{datetime.date.today().year}</span> {NEGOCIO["razon"]}. Todos los derechos reservados.</span>
      <span><a href="/aviso-legal/">Aviso Legal</a> · <a href="/politicas-de-cookies/">Políticas de Cookies</a> · <a href="/politicas-de-privacidad/">Políticas de Privacidad</a></span>
    </div>
  </footer>
  <script src="/assets/js/config.js"></script>
  <script src="/assets/js/app.js" defer></script>
  <script src="/assets/js/cookies.js" defer></script>
</body>
</html>
"""

def write(path, content):
    fp = os.path.join(ROOT, path.strip("/"), "index.html") if not path.endswith(".html") else os.path.join(ROOT, path.strip("/"))
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w", encoding="utf-8").write(content)

def crumbs_html(items):
    lis = "".join((f'<li><a href="{u}">{e(n)}</a></li>' if i < len(items) - 1 else f'<li aria-current="page">{e(n)}</li>') for i, (n, u) in enumerate(items))
    return f'<nav class="crumbs wrap" aria-label="Migas de pan"><ol>{lis}</ol></nav>'

def faq_html(qas):
    return '<div class="faq">' + "".join(f'<details class="reveal"><summary>{e(q)}</summary><p>{a}</p></details>' for q, a in qas) + "</div>"

def cta_band(title="Prueba tu Voge", text="Ven a Voge Móstoles o Voge Getafe y solicita tu prueba."):
    return f"""<section class="section"><div class="wrap"><div class="cta-band reveal">
      <h2>{title}</h2><p>{text}</p>
      <div class="hero__actions">
        <a class="btn btn--primary" href="/solicitud-de-prueba/">Solicitar prueba</a>
        <a class="btn btn--ghost-light" href="/contacto/">Pedir información</a>
      </div></div></div></section>"""

def visit_block(h="Ven a verlas a Móstoles o Getafe", tienda="ambas"):
    def un(nombre, direccion, tel, telI, dir_, embed, extra=""):
        return f"""<div class="visit reveal">
      <div class="visit__info">
        <span class="eyebrow">Concesionario oficial</span>
        <h2>{nombre}</h2>
        <div class="info-item"><div class="info-item__ico">{ICO["pin"]}</div><div><h3>Dirección</h3><p>{e(direccion)}</p></div></div>
        <div class="info-item"><div class="info-item__ico">{ICO["clock"]}</div><div><h3>Horario</h3><p>{e(NEGOCIO["horario"])}</p></div></div>
        <div class="info-item"><div class="info-item__ico">{ICO["tel"]}</div><div><h3>Teléfono</h3><a href="tel:{telI}">{tel}</a>{extra}</div></div>
        <div class="hero__actions"><a class="btn btn--primary" href="{dir_}" target="_blank" rel="noopener">Ver mapa</a><a class="btn btn--ghost-light" href="/solicitud-de-prueba/">Prueba tu Voge</a></div>
      </div>
      <iframe src="{embed}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Mapa de {e(nombre)}"></iframe>
    </div>"""
    mo = un("Voge Móstoles", DIRECCION, NEGOCIO["tel"], NEGOCIO["telIntl"], MAPS_DIR, MAPS_EMBED)
    ge = un("Voge Getafe", DIR_GETAFE, GETAFE["tel"], GETAFE["telIntl"], GETAFE["dir"], GETAFE["embed"])
    if tienda == "mostoles": return mo
    if tienda == "getafe": return ge
    return f'<h2 style="text-align:center;margin-bottom:28px">{h}</h2>' + mo + '<div style="height:28px"></div>' + ge

def card(m, lazy=True, h="h3"):
    badge = '<span class="card__badge">En promoción</span>' if m["promo"] else ""
    price = (f'<del>{eur(m["pvp"])}</del>' if m["pvp"] else "") + eur(m["price"])
    ncol = len(m["colors"])
    return f"""<article class="card reveal" data-cat="{m["cat"]}">
        <div class="card__media"><img src="/{m["main"]}" alt="{e(full(m))}" width="{m["mw"]}" height="{m["mh"]}"{' loading="lazy" decoding="async"' if lazy else ''}>{badge}</div>
        <div class="card__body">
          <span class="card__cat">{m["cat"]}</span>
          <{h} class="card__title"><a href="{model_url(m)}">{e(m["name"])}</a></{h}>
          <div class="card__specs">
            <span class="card__spec"><b>{m["cc"]} cc</b>Cilindrada</span>
            <span class="card__spec"><b>{m["cv"]} CV</b>Potencia</span>
            <span class="card__spec"><b>{m["nm"]} Nm</b>Par máx.</span>
          </div>
          {f'<div class="card__colors">{ncol} colores disponibles</div>' if ncol > 1 else ''}
          <div class="card__foot">
            <span class="card__price">{price}<small>PVP · IVA incluido</small></span>
            <span class="card__link">Ver moto <i>&rsaquo;</i></span>
          </div>
        </div>
      </article>"""

def precio_min(lic=None, cat=None):
    xs = [m["price"] for m in M if (lic is None or m["license"] == lic) and (cat is None or m["cat"] == cat)]
    return min(xs)

PRICE_NOTE = "PVP recomendado con IVA incluido. Consulta en el concesionario los gastos de matriculación y transporte, la disponibilidad y las condiciones de financiación."

def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}

def faq_ld(qas):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in qas]}

# ------------------------------------------------------------------ ICONOS
ICO = {
    "_wa": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M.057 24l1.687-6.163a11.867 11.867 0 01-1.587-5.945C.16 5.335 5.5 0 12.05 0a11.82 11.82 0 018.413 3.488 11.82 11.82 0 013.48 8.414c-.003 6.557-5.338 11.892-11.893 11.892a11.9 11.9 0 01-5.688-1.448L.057 24zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884a9.86 9.86 0 001.51 5.26l-.999 3.648 3.978-1.607zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.767.967-.94 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6a2.5 2.5 0 0 1 0 5.5z"/></svg>',
    "tel": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 4-8 5-8-5V6l8 5 8-5z"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm1 10.4 3.6 2.1-.8 1.3L11 13V7h2z"/></svg>',
    "ig": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10zm0 8.2a3.2 3.2 0 1 1 0-6.4 3.2 3.2 0 0 1 0 6.4zM17.2 5.6a1.2 1.2 0 1 0 0 2.4 1.2 1.2 0 0 0 0-2.4zM21.9 7.1c-.1-1.6-.4-3-1.6-4.2S17.7 1.3 16.1 1.2C14.4 1.1 9.6 1.1 7.9 1.2 6.3 1.3 4.9 1.6 3.7 2.8S2.1 5.5 2 7.1C1.9 8.8 1.9 15.2 2 16.9c.1 1.6.4 3 1.6 4.2s2.6 1.5 4.2 1.6c1.7.1 6.5.1 8.2 0 1.6-.1 3-.4 4.2-1.6s1.5-2.6 1.6-4.2c.2-1.7.2-8.1.1-9.8zm-2.2 11.6a3.3 3.3 0 0 1-1.9 1.9c-1.3.5-4.4.4-5.8.4s-4.5.1-5.8-.4a3.3 3.3 0 0 1-1.9-1.9c-.5-1.3-.4-4.4-.4-5.8s-.1-4.5.4-5.8a3.3 3.3 0 0 1 1.9-1.9c1.3-.5 4.4-.4 5.8-.4s4.5-.1 5.8.4a3.3 3.3 0 0 1 1.9 1.9c.5 1.3.4 4.4.4 5.8s.1 4.5-.4 5.8z"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 1 3 5v6c0 5.6 3.8 10.7 9 12 5.2-1.3 9-6.4 9-12V5zm-2 16-4-4 1.4-1.4L10 14.2l6.6-6.6L18 9z"/></svg>',
    "wrench": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22.7 19 13.6 9.9c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z"/></svg>',
    "star": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m12 17.3 6.2 3.7-1.6-7 5.4-4.7-7.1-.6L12 2 9.1 8.7 2 9.3l5.4 4.7-1.6 7z"/></svg>',
    "bike": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 11a4 4 0 1 0 0 8 4 4 0 0 0 0-8zm0 6.2a2.2 2.2 0 1 1 0-4.4 2.2 2.2 0 0 1 0 4.4zM19 11a4 4 0 1 0 0 8 4 4 0 0 0 0-8zm0 6.2a2.2 2.2 0 1 1 0-4.4 2.2 2.2 0 0 1 0 4.4zM15.6 6H13v1.8h1.7l1.3 2.2H9.5L8.3 8H10V6.2H5v1.8h1.2l1.6 2.6L6.1 13l1.5.9 1.6-2.4L11 15h3.4l2.3-3.8.8 1.3 1.5-.9z"/></svg>',
    "box": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 7.5 12 2 3 7.5v9L12 22l9-5.5zM12 4.3l6.1 3.7L12 11.7 5.9 8zM5 9.7l6 3.6v6.3l-6-3.7zm8 9.9v-6.3l6-3.6v6.2z"/></svg>',
    "euro": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 18.5A6.5 6.5 0 0 1 9.2 15H15l1-2H8.6a6 6 0 0 1 0-2H16l1-2H9.2A6.5 6.5 0 0 1 15 5.5c1.6 0 3.1.6 4.2 1.6L21 5.3A9 9 0 0 0 6.6 9H3l-1 2h4.1a9 9 0 0 0 0 2H3l-1 2h4.6A9 9 0 0 0 21 18.7l-1.8-1.8a6.4 6.4 0 0 1-4.2 1.6z"/></svg>',
    "key": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.7 10A6 6 0 1 0 7 18a6 6 0 0 0 5.7-4H17v4h4v-4h2v-4zM7 14a2 2 0 1 1 0-4 2 2 0 0 1 0 4z"/></svg>',
}


def data_box(resp="Titular"):
    return f"""<div class="data-box">
        <p><strong>{resp}:</strong> {NEGOCIO["razon"]}</p>
        <p><strong>CIF:</strong> {NEGOCIO["cif"]}</p>
        <p><strong>Domicilio:</strong> {e(DIRECCION)}</p>
        <p><strong>Teléfono:</strong> {NEGOCIO["tel"]} · <strong>Email:</strong> <a href="mailto:{NEGOCIO["email"]}">{NEGOCIO["email"]}</a></p>
      </div>"""

LEGAL = {
 "/aviso-legal/": ("Aviso legal", "Condiciones generales de uso del sitio web", f"""
      <h2>1. Titular del sitio web</h2>
      <p>En cumplimiento del artículo 10 de la Ley 34/2002, de 11 de julio, de Servicios de la Sociedad de la Información y de Comercio Electrónico (LSSI-CE), se informa de los datos del titular de este sitio web:</p>
      {data_box()}
      <p>En adelante, «el Titular». Este sitio es la web del concesionario oficial que presenta la gama Voge disponible en sus instalaciones.</p>
      <h2>2. Objeto</h2>
      <p>El presente aviso legal regula el uso del sitio web, que el Titular pone a disposición de los usuarios con carácter informativo sobre los modelos, promociones y servicios relacionados con la marca Voge. La navegación por el sitio atribuye la condición de usuario e implica la aceptación plena de las presentes condiciones.</p>
      <h2>3. Condiciones de uso</h2>
      <p>El usuario se compromete a hacer un uso adecuado y lícito del sitio web y de sus contenidos, absteniéndose de:</p>
      <ul>
        <li>Utilizar los contenidos con fines contrarios a la ley, la moral o el orden público.</li>
        <li>Introducir o difundir virus o cualquier otro sistema capaz de causar daños en los sistemas del Titular o de terceros.</li>
        <li>Intentar acceder, utilizar o manipular los datos del Titular o de terceros usuarios.</li>
        <li>Reproducir o copiar los contenidos sin autorización.</li>
      </ul>
      <h2>4. Propiedad intelectual e industrial</h2>
      <p>Los textos, el diseño y el código de este sitio son propiedad del Titular o cuentan con la correspondiente autorización para su uso. «Voge», su logotipo y las denominaciones de sus modelos son marcas registradas de su fabricante, utilizadas por el Titular en su condición de concesionario oficial. Las imágenes de los modelos son fotografías oficiales de la marca. Queda prohibida su reproducción sin autorización de sus respectivos titulares.</p>
      <h2>5. Exención de responsabilidad</h2>
      <p>Los precios, promociones, colores y especificaciones mostrados tienen carácter orientativo y pueden variar sin previo aviso según la tarifa y las campañas vigentes de la marca. No constituyen una oferta contractual vinculante. Para condiciones definitivas, consulta directamente con el concesionario. El Titular no se responsabiliza de los posibles errores tipográficos ni de la disponibilidad de las unidades.</p>
      <h2>6. Enlaces a terceros</h2>
      <p>Este sitio puede contener enlaces a páginas de terceros (por ejemplo, Instagram o servicios de mapas). El Titular no se hace responsable de los contenidos ni de las políticas de privacidad de dichos sitios.</p>
      <h2>7. Legislación aplicable</h2>
      <p>Las presentes condiciones se rigen por la legislación española. Para cualquier controversia, las partes se someten a los juzgados y tribunales que correspondan conforme a derecho.</p>"""),
 "/politicas-de-privacidad/": ("Política de privacidad", "Tratamiento de datos personales (RGPD y LOPDGDD)", f"""
      <h2>1. Responsable del tratamiento</h2>
      {data_box("Responsable")}
      <p>El Responsable trata los datos personales del usuario de conformidad con el Reglamento (UE) 2016/679 (RGPD) y la Ley Orgánica 3/2018, de 5 de diciembre (LOPDGDD).</p>
      <h2>2. ¿Con qué finalidad tratamos tus datos?</h2>
      <p>Tratamos los datos que nos facilitas a través de los formularios de contacto, de solicitud de prueba y de cita de taller, con las siguientes finalidades:</p>
      <ul>
        <li>Atender tu solicitud de información sobre modelos, promociones, financiación o servicios de posventa.</li>
        <li>Gestionar la relación comercial y, en su caso, la reserva o prueba de un vehículo.</li>
        <li>Si nos das tu consentimiento, remitirte comunicaciones comerciales sobre nuestros productos y servicios.</li>
      </ul>
      <h2>3. Legitimación</h2>
      <p>La base legal del tratamiento es el <strong>consentimiento</strong> que otorgas al enviar el formulario y la aplicación de medidas precontractuales a petición tuya. El envío de comunicaciones comerciales se basa en tu consentimiento expreso, revocable en cualquier momento.</p>
      <h2>4. ¿Durante cuánto tiempo conservamos los datos?</h2>
      <p>Los datos se conservarán mientras exista un interés mutuo o durante el tiempo necesario para cumplir con las obligaciones legales. Cuando ya no sean necesarios, se suprimirán con las medidas de seguridad adecuadas.</p>
      <h2>5. ¿A quién comunicamos tus datos?</h2>
      <p>No se cederán datos a terceros, salvo obligación legal o cuando sea necesario para la prestación del servicio (por ejemplo, proveedores tecnológicos que actúan como encargados del tratamiento —como el servicio de envío de formularios FormSubmit—, entidades financieras en caso de financiación, o la marca para gestionar garantías). No se realizan transferencias internacionales fuera del Espacio Económico Europeo sin las garantías adecuadas.</p>
      <h2>6. ¿Cuáles son tus derechos?</h2>
      <ul>
        <li><strong>Acceso:</strong> saber qué datos tuyos tratamos.</li>
        <li><strong>Rectificación:</strong> corregir datos inexactos.</li>
        <li><strong>Supresión:</strong> solicitar que se eliminen tus datos.</li>
        <li><strong>Oposición y limitación:</strong> oponerte o limitar el tratamiento.</li>
        <li><strong>Portabilidad:</strong> recibir tus datos en un formato estructurado.</li>
        <li><strong>Retirar el consentimiento</strong> en cualquier momento.</li>
      </ul>
      <p>Puedes ejercer estos derechos escribiendo a <a href="mailto:{NEGOCIO["email"]}">{NEGOCIO["email"]}</a> o por correo a nuestro domicilio, indicando el derecho que deseas ejercer. Si consideras que el tratamiento no se ajusta a la normativa, puedes reclamar ante la <a href="https://www.aepd.es" target="_blank" rel="noopener">Agencia Española de Protección de Datos (aepd.es)</a>.</p>
      <h2>7. Seguridad</h2>
      <p>El Responsable adopta las medidas técnicas y organizativas necesarias para garantizar la seguridad y confidencialidad de los datos y evitar su alteración, pérdida o acceso no autorizado.</p>"""),
 "/politicas-de-cookies/": ("Política de cookies", "Uso de cookies en este sitio web", """
      <h2>1. ¿Qué son las cookies?</h2>
      <p>Una cookie es un pequeño archivo de texto que un sitio web guarda en tu navegador cuando lo visitas. Sirven para que la web funcione correctamente, recordar tus preferencias y, en su caso, obtener datos estadísticos de uso.</p>
      <h2>2. ¿Qué cookies utilizamos?</h2>
      <p>Este sitio es una web estática con un uso mínimo de cookies. Actualmente utiliza únicamente las siguientes:</p>
      <table class="cookie-tbl">
        <thead><tr><th>Cookie</th><th>Tipo</th><th>Finalidad</th><th>Duración</th></tr></thead>
        <tbody>
          <tr><td>duomo_cookie_consent</td><td>Técnica (propia)</td><td>Recordar tu elección sobre el aviso de cookies para no volver a mostrarlo.</td><td>Persistente</td></tr>
          <tr><td>Google Fonts</td><td>Técnica (terceros)</td><td>Cargar la tipografía del sitio desde los servidores de Google.</td><td>De sesión</td></tr>
          <tr><td>Google Maps</td><td>Terceros</td><td>Mostrar el mapa de ubicación del concesionario.</td><td>Según Google</td></tr>
        </tbody>
      </table>
      <p>Los formularios se gestionan a través de un proveedor externo (FormSubmit), que puede establecer sus propias cookies al enviarlos, sujetas a su política.</p>
      <p>Si en el futuro se incorporan cookies de <strong>analítica o publicidad</strong> (por ejemplo, Google Analytics o píxeles de redes sociales), solo se activarán si aceptas su uso en el aviso de cookies.</p>
      <h2>3. ¿Cómo gestionar las cookies?</h2>
      <p>Al entrar en el sitio puedes <strong>aceptar</strong> o <strong>rechazar</strong> el uso de cookies no esenciales mediante el aviso que aparece en la parte inferior. Además, puedes configurar, bloquear o eliminar las cookies desde la configuración de tu navegador:</p>
      <ul>
        <li><a href="https://support.google.com/chrome/answer/95647" target="_blank" rel="noopener">Google Chrome</a></li>
        <li><a href="https://support.mozilla.org/es/kb/Borrar%20cookies" target="_blank" rel="noopener">Mozilla Firefox</a></li>
        <li><a href="https://support.apple.com/es-es/guide/safari/sfri11471/mac" target="_blank" rel="noopener">Safari</a></li>
        <li><a href="https://support.microsoft.com/es-es/microsoft-edge" target="_blank" rel="noopener">Microsoft Edge</a></li>
      </ul>
      <p>Ten en cuenta que desactivar las cookies técnicas puede afectar al correcto funcionamiento del sitio.</p>"""),
}

def page_legal(url, t, sub, content):
    body = f"""
  <section class="legal"><div class="wrap">
      <h1>{t}</h1>
      <p class="updated">{sub}</p>
      {content}
      <p style="margin-top:24px"><a href="/aviso-legal/">Aviso legal</a> · <a href="/politicas-de-privacidad/">Política de privacidad</a> · <a href="/politicas-de-cookies/">Política de cookies</a></p>
  </div></section>"""
    write(url, head(f"{t} · Voge Madrid Sur", f"{t} de la web de Duomo Motor Bikes, concesionario oficial Voge en Móstoles y Getafe.", url, noindex=True) + header() + body + footer())

def page_404():
    body = f"""
  <section class="hero hero--page"><div class="hero__bg"><img src="/assets/img/hero/concesionario-voge-madrid-sur-2.webp" alt="" width="1366" height="911"></div>
    <div class="wrap"><div class="hero__inner">
      <span class="eyebrow">Error 404</span>
      <h1>Esta página se ha salido de la carretera</h1>
      <p class="lead">Puede que el modelo haya cambiado de nombre o que el enlace ya no exista. Vuelve a la gama completa o escríbenos.</p>
      <div class="hero__actions"><a class="btn btn--primary" href="/#gama">Ver la gama Voge</a><a class="btn btn--ghost-light" href="/contacto/">Contactar</a></div>
    </div></div></section>"""
    write("/404.html", head("Página no encontrada · Voge Madrid Sur", "La página que buscas no existe.", "/404.html", noindex=True) + header() + body + footer())

# ------------------------------------------------------------------ SITEMAP / ROBOTS

BLOG_DIR = os.path.join(ROOT, "blog")
POSTS_JSON = os.path.join(BLOG_DIR, "posts.json")

def blog_posts():
    try:
        return json.load(open(POSTS_JSON, encoding="utf-8"))
    except Exception:
        return []

def bcard_html(p):
    return (f'<article class="bcard reveal"><a class="bcard__media" href="/blog/{p["slug"]}/" tabindex="-1" aria-hidden="true">'
            f'<img src="{e(p["imagen"])}" alt="{e(p["imagenAlt"])}" width="{p.get("w", 1200)}" height="{p.get("h", 800)}" loading="lazy" decoding="async"></a>'
            f'<div class="bcard__body"><span class="bcard__meta">{e(p["categoria"])} · {e(p["fechaTxt"])}</span>'
            f'<h2 class="bcard__title"><a href="/blog/{p["slug"]}/">{e(p["titulo"])}</a></h2>'
            f'<p>{e(p["descripcion"])}</p><a class="bcard__more" href="/blog/{p["slug"]}/">Leer artículo <i>&rsaquo;</i></a></div></article>')

BLOG_VACIO = '<p class="blog-empty">Muy pronto: novedades, rutas y consejos para motoristas de Madrid Sur.</p>'

def blog_index_template():
    url = "/blog/"
    crumbs = [("Inicio", "/"), ("Blog", url)]
    ld = [crumbs_ld(crumbs), {"@context": "https://schema.org", "@type": "Blog", "@id": SITE + "/blog/#blog", "name": "Blog Voge Madrid Sur", "url": SITE + url,
          "inLanguage": "es-ES", "publisher": {"@id": DEALER_ID}, "about": "Motos, rutas, carnet y mantenimiento en Madrid Sur"}]
    body = f"""
  <section class="hero hero--page">
    <div class="hero__bg"><img src="/assets/img/hero/concesionario-voge-madrid-sur-3.webp" alt="" width="1366" height="911"></div>
    <div class="wrap"><div class="hero__inner">
      <span class="eyebrow">Blog · Voge Madrid Sur</span>
      <h1>Blog <span class="hl">Voge Madrid Sur</span></h1>
      <p class="lead">Novedades, rutas, consejos y todo sobre la gama Voge, de la mano de Voge Móstoles y Voge Getafe.</p>
    </div></div>
  </section>
  {crumbs_html(crumbs)}
  <section class="section" style="padding-top:36px">
    <div class="wrap">
      <div class="bgrid" id="blog-list">%%LISTADO%%</div>
    </div>
  </section>
  {cta_band("Tu nueva Voge, en Móstoles o Getafe", "Ven a verla y pruébala en Voge Móstoles o Voge Getafe. Toda la gama y taller propio.")}
"""
    return head("Blog · Motos Voge Madrid Sur",
                "Novedades, rutas, consejos y todo sobre la gama Voge. Blog de Voge Madrid Sur, concesionarios oficiales en Móstoles y Getafe.",
                url, ld=ld) + header("blog") + body + footer()

def blog_article_template():
    body = f"""
  <nav class="crumbs wrap" aria-label="Migas de pan"><ol><li><a href="/">Inicio</a></li><li><a href="/blog/">Blog</a></li><li aria-current="page">%%H1_TEXTO%%</li></ol></nav>
  <article class="post">
    <header class="post__head wrap">
      <span class="eyebrow">%%CATEGORIA%% · <time datetime="%%FECHA_ISO%%">%%FECHA_TXT%%</time> · %%LECTURA%% min de lectura</span>
      <h1>%%H1%%</h1>
      <p class="lead">%%ENTRADILLA%%</p>
      <p class="post__byline">Por el equipo de <a href="/concesionario-voge-madrid-sur/">Voge Madrid Sur</a>, concesionarios oficiales Voge en Móstoles y Getafe</p>
    </header>
    <figure class="post__cover wrap"><img src="%%COVER_IMG%%" alt="%%COVER_ALT%%" width="%%COVER_W%%" height="%%COVER_H%%" fetchpriority="high"></figure>
    <div class="post__layout wrap">
      <div class="post__body">
        %%TLDR%%
        %%TOC%%
        %%CUERPO%%
        %%FAQ%%
        <div class="post__autor">
          <img src="/assets/img/logo/icon-180.png" alt="" width="64" height="64" loading="lazy">
          <div><p class="post__autor-t">Sobre Voge Madrid Sur</p>
          <p>Somos Duomo Motor Bikes, concesionarios oficiales Voge en Móstoles y Getafe, con taller propio, servicio postventa y recambios originales. <a href="/concesionario-voge-madrid-sur/">Conócenos</a>.</p></div>
        </div>
      </div>
      <aside class="post__aside">
        <div class="post__card">
          <span class="eyebrow">Voge Madrid Sur</span>
          <p class="post__card-t">%%CTA_TITULO%%</p>
          <p>%%CTA_TEXTO%%</p>
          %%CTA_MODELO%%
          <a class="btn btn--primary btn--block" href="/solicitud-de-prueba/%%CTA_QUERY%%">Pedir prueba</a>
          <a class="btn btn--ghost btn--block" href="/contacto/">Pedir información</a>
        </div>
        <div class="post__zonas">
          <p class="post__card-t">Modelos Voge</p>
          <a href="/categoria-producto/scooters/">Scooters Voge</a>
          <a href="/categoria-producto/naked/">Naked Voge</a>
          <a href="/categoria-producto/adventure/">Adventure Voge</a>
          <a href="/concesionario-voge-madrid-sur/">Puntos de venta</a>
        </div>
      </aside>
    </div>
  </article>
  <section class="section section--alt">
    <div class="wrap">
      <h2>Sigue leyendo</h2>
      <p class="sub">Más artículos del blog de Voge Madrid Sur.</p>
      <div class="bgrid">%%RELACIONADOS%%</div>
    </div>
  </section>
  %%CTA_BAND%%
"""
    h = head("%%TITLE%%", "%%META_DESC%%", "/blog/%%SLUG%%/", og_img="%%OG_IMAGE%%")
    h = h.replace('<meta property="og:type" content="website">', '<meta property="og:type" content="article">\n  <meta property="article:published_time" content="%%FECHA_ISO%%">\n  <meta property="article:section" content="%%CATEGORIA%%">')
    h = h.replace(f'{SITE}%%OG_IMAGE%%', '%%OG_IMAGE_ABS%%')
    h = h.replace("</head>", "  %%JSONLD%%\n</head>")
    return h + header("blog") + body + footer()

MAX_TARJETAS = 30

def blog_listado(posts):
    if not posts: return BLOG_VACIO
    resto = posts[MAX_TARJETAS:]
    out = "".join(bcard_html(p) for p in posts[:MAX_TARJETAS])
    if resto:
        out += ('</div><h2 style="margin-top:56px">Todos los artículos</h2><ul class="blog-archivo">'
                + "".join(f'<li><a href="/blog/{p["slug"]}/">{e(p["titulo"])}</a> <span>{e(p["categoria"])} · {e(p["fechaTxt"])}</span></li>' for p in resto)
                + '</ul><div>')
    return out

def blog_relacionados(p, posts):
    otros = [x for x in posts if x["slug"] != p["slug"]]
    orden = [x for x in otros if x["categoria"] == p["categoria"]] + [x for x in otros if x.get("modelo") == p.get("modelo")] + otros
    vistos, rel = set(), []
    for x in orden:
        if x["slug"] in vistos: continue
        vistos.add(x["slug"]); rel.append(x)
        if len(rel) == 3: break
    return "".join(bcard_html(x) for x in rel) or '<p class="blog-empty">Pronto habrá más artículos. Mientras, mira <a href="/#gama">toda la gama Voge</a>.</p>'

def blog_feed(posts):
    def rfc(d):
        dt = datetime.datetime.strptime(d, "%Y-%m-%d").replace(hour=8, tzinfo=datetime.timezone.utc)
        return dt.strftime("%a, %d %b %Y %H:%M:%S GMT")
    items = "".join(f'<item><title>{e(p["titulo"])}</title><link>{SITE}/blog/{p["slug"]}/</link><guid isPermaLink="true">{SITE}/blog/{p["slug"]}/</guid>'
                    f'<pubDate>{rfc(p["fecha"])}</pubDate><category>{e(p["categoria"])}</category><description>{e(p["descripcion"])}</description></item>' for p in posts[:30])
    last = rfc(posts[0]["fecha"]) if posts else rfc(TODAY)
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>Blog Voge Madrid Sur</title>'
            f'<link>{SITE}/blog/</link><atom:link href="{SITE}/blog/feed.xml" rel="self" type="application/rss+xml"/>'
            f'<description>Motos, rutas y consejos para motoristas de Madrid Sur. Voge Madrid Sur, concesionarios oficiales en Móstoles y Getafe.</description>'
            f'<language>es-ES</language><lastBuildDate>{last}</lastBuildDate>{items}</channel></rss>\n')

FILLS_DIR = os.path.join(ROOT, "_build", "blog", "posts")

def blog_rerender(tpl, posts):
    """Vuelve a generar cada artículo con la plantilla actual a partir de sus datos (_build/blog/posts/<slug>.json)."""
    band = cta_band("Tu nueva Voge, en Móstoles o Getafe", "Ven a verla y pruébala en Voge Móstoles o Voge Getafe. Toda la gama, financiación a medida y taller propio.")
    n = 0
    for p in posts:
        fp = os.path.join(FILLS_DIR, p["slug"] + ".json")
        if not os.path.exists(fp): continue
        fills = json.load(open(fp, encoding="utf-8"))
        fills["%%RELACIONADOS%%"] = blog_relacionados(p, posts)
        fills["%%CTA_BAND%%"] = band
        html_ = tpl
        for k, v in fills.items(): html_ = html_.replace(k, v)
        faltan = re.findall(r"%%[A-Z_]+%%", html_)
        if faltan: raise SystemExit(f"{p['slug']}: faltan marcadores {faltan}")
        write(f"/blog/{p['slug']}/", html_); n += 1
    return n

def page_blog():
    os.makedirs(os.path.join(ROOT, "_build", "blog"), exist_ok=True)
    tpl_idx = blog_index_template()
    tpl_art = blog_article_template()
    open(os.path.join(ROOT, "_build", "blog", "plantilla-indice.html"), "w", encoding="utf-8").write(tpl_idx)
    open(os.path.join(ROOT, "_build", "blog", "plantilla-articulo.html"), "w", encoding="utf-8").write(tpl_art)
    open(os.path.join(ROOT, "_build", "blog", "cta-band.html"), "w", encoding="utf-8").write(cta_band("Tu nueva Voge, en Móstoles o Getafe", "Ven a verla y pruébala en Voge Móstoles o Voge Getafe. Toda la gama, financiación a medida y taller propio."))
    posts = sorted(blog_posts(), key=lambda p: p["fecha"], reverse=True)
    os.makedirs(BLOG_DIR, exist_ok=True)
    open(os.path.join(BLOG_DIR, "index.html"), "w", encoding="utf-8").write(tpl_idx.replace("%%LISTADO%%", blog_listado(posts)))
    open(os.path.join(BLOG_DIR, "feed.xml"), "w", encoding="utf-8").write(blog_feed(posts))
    if not os.path.exists(POSTS_JSON):
        open(POSTS_JSON, "w", encoding="utf-8").write("[]\n")
    print("artículos regenerados:", blog_rerender(tpl_art, posts))

# ------------------------------------------------------------------ HOME
def page_home():
    counts = {c["name"]: sum(1 for m in M if m["cat"] == c["name"]) for c in CATS}
    tiles = "".join(f"""<a class="cattile reveal{' reveal-d1' if i % 2 else ''}" href="{cat_url(c)}">
        <img src="/assets/img/categorias/{c["img"]}" alt="Motos {e(c["plural"].lower())} Voge" width="1200" height="900" loading="lazy" decoding="async">
        <span class="cattile__txt"><strong>{c["name"] if c["name"] != "Scooters" else "Scooter"}</strong><span>{c["corto"]}.</span></span></a>""" for i, c in enumerate([CAT["Adventure"], CAT["Naked"], CAT["Scooters"]]))
    bar = '<button class="active" data-filter="Todas">Todas <small>' + str(len(M)) + '</small></button>' + "".join(
        f'<button data-filter="{c["name"]}">{c["plural"]} <small>{counts[c["name"]]}</small></button>' for c in CATS)
    cards = "\n".join(card(m) for m in M)
    hero_txt = [("Voge 625 DSX", "Diseñada para ser tu mejor aliada en cualquier terreno, esta motocicleta combina potencia, tecnología avanzada y un diseño robusto.", "625dsx"),
                ("Voge SR4 Radar", "Scooter de vanguardia dotado con tecnología de detección de obstáculos en ángulo muerto y alerta de colisión.", "sr4-radar"),
                ("Voge 900 DSX", "Combina tecnología de punta, un diseño y un precio increíblemente competitivo, que incorpora nuevas características diseñadas para maximizar tu experiencia de conducción.", "900dsx")]
    slides = "".join(f'''<div class="hero__slide{" is-active" if i == 0 else ""}"><img src="/assets/img/hero/concesionario-voge-madrid-sur-{i+1}.webp" alt="" width="1366" height="911"{"" if i == 0 else ' loading="lazy"'}></div>''' for i in range(3))
    textos = "".join(f'''<div class="hero__txt{" is-active" if i == 0 else ""}" data-slide="{i}"{"" if i == 0 else " hidden"}>
          <span class="eyebrow">Voge Madrid Sur</span>
          {"<h1>" if i == 0 else "<h2 class=\'h1\'>"}{t}{"</h1>" if i == 0 else "</h2>"}
          <p class="lead">{d}</p>
          <div class="hero__actions"><a class="btn btn--primary" href="/modelo/{sl}/">Más información</a><a class="btn btn--ghost-light" href="/solicitud-de-prueba/?modelo={quote(mm(sl)['name'])}">Solicita una prueba</a></div>
        </div>''' for i, (t, d, sl) in enumerate(hero_txt))
    ld = [DEALER, DEALER_GETAFE, {"@context": "https://schema.org", "@type": "WebSite", "name": "Voge Madrid Sur", "url": SITE + "/", "inLanguage": "es-ES", "publisher": {"@id": DEALER_ID}},
          {"@context": "https://schema.org", "@type": "ItemList", "name": "Gama Voge", "itemListElement": [
              {"@type": "ListItem", "position": i + 1, "url": SITE + model_url(m), "name": full(m)} for i, m in enumerate(M)]}]
    body = f"""
  <section class="hero" aria-label="Voge Madrid Sur">
    <div class="hero__slides">{slides}</div>
    <div class="wrap">
      <div class="hero__inner">{textos}</div>
    </div>
    <div class="wrap" style="position:relative"><div class="hero__dots" role="tablist" aria-label="Modelos destacados">{"".join(f'<button aria-label="{t}"{" class=\"is-active\"" if i == 0 else ""}></button>' for i, (t, d, sl) in enumerate(hero_txt))}</div></div>
  </section>

  <section class="section">
    <div class="wrap">
      <span class="eyebrow" style="display:flex;justify-content:center">Dónde estamos</span>
      <h2>Voge Móstoles y Voge Getafe</h2>
      <p class="sub">Concesionarios oficiales. Prueba tu Voge o contacta con nosotros.</p>
      <div class="hero__actions" style="justify-content:center"><a class="btn btn--dark" href="/solicitud-de-prueba/">Prueba tu Voge</a><a class="btn btn--ghost" href="/contacto/">Contacto</a><a class="btn btn--ghost" href="/concesionario-voge-madrid-sur/">Descubre más</a></div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="wrap">
      <span class="eyebrow" style="display:flex;justify-content:center">Concesionarios oficiales</span>
      <h2>Modelos Voge</h2>
      <div class="catgrid catgrid--3">{tiles}</div>
    </div>
  </section>

  <section class="section" id="gama">
    <div class="wrap">
      <h2>Toda la gama Voge</h2>
      <div class="cat-bar" id="cat-bar" role="group" aria-label="Filtrar por categoría">{bar}</div>
      <div class="grid" id="models-grid">
{cards}
      </div>
      <p class="promo-legal">{PRICE_NOTE}</p>
    </div>
  </section>

  <section class="section section--alt">
    <div class="wrap">
      {visit_block("Tu concesionario Voge en Móstoles y Getafe")}
    </div>
  </section>
"""
    write("/", head("Motos Voge Madrid Sur · Concesionaria de Motos Voge en Madrid Sur",
                    f"Concesionarios oficiales Voge en Móstoles y Getafe. Toda la gama Voge: scooters, naked y adventure, desde {eur(precio_min())}. Solicita tu prueba.",
                    "/", ld=ld, preload="/assets/img/hero/concesionario-voge-madrid-sur-1.webp") + header("inicio") + body + footer())

# ------------------------------------------------------------------ MODELO
def tagline(m):
    t = {"Scooters": "Scooter", "Naked": "Moto naked", "Adventure": "Moto adventure"}[m["cat"]]
    return f"{t} de {m['cc']} cc y {m['cv']} CV · {LIC[m['license']]['label']}"

def related(m, n=3):
    same = [x for x in M if x["cat"] == m["cat"] and x["slug"] != m["slug"]]
    same.sort(key=lambda x: abs(x["price"] - m["price"]))
    if len(same) < n:
        more = [x for x in M if x["license"] == m["license"] and x["slug"] != m["slug"] and x not in same]
        more.sort(key=lambda x: abs(x["price"] - m["price"]))
        same += more
    return same[:n]

def page_model(m):
    c = CAT[m["cat"]]; L = LIC[m["license"]]; fn = full(m)
    url = model_url(m); qmodel = quote(m["name"])
    saving = f'<span class="pricebox__save">Ahorras {eur(m["pvp"] - m["price"])}</span>' if m["pvp"] else ""
    # Colores con su galería
    tabs = "".join(f'<button class="ctab{" active" if i == 0 else ""}" type="button" role="tab" aria-selected="{"true" if i == 0 else "false"}" data-color="{i}">{e(col["name"])}</button>' for i, col in enumerate(m["colors"]))
    panes = ""
    for i, col in enumerate(m["colors"]):
        big = col["imgs"][0]
        thumbs = "".join(f'<button type="button" class="cthumb{" active" if j == 0 else ""}" data-src="/{im["img"]}" aria-label="Foto {j+1} de la {e(fn)} en {e(col["name"].lower())}"><img src="/{im["img"]}" alt="" width="{im["w"]}" height="{im["h"]}" loading="lazy" decoding="async"></button>' for j, im in enumerate(col["imgs"])) if len(col["imgs"]) > 1 else ""
        panes += f"""<div class="cpane{" active" if i == 0 else ""}" data-color="{i}"{"" if i == 0 else " hidden"}>
          <figure class="cpane__big"><img src="/{big["img"]}" alt="{e(fn)} color {e(col["name"].lower())}" width="{big["w"]}" height="{big["h"]}" loading="lazy" decoding="async"></figure>
          {f'<div class="cthumbs">{thumbs}</div>' if thumbs else ''}
        </div>"""
    colores = f"""<section class="section" id="colores">
    <div class="wrap">
      <span class="eyebrow" style="display:flex;justify-content:center">Colores</span>
      <h2>La {e(fn)} en {len(m["colors"])} {"color" if len(m["colors"]) == 1 else "colores"}</h2>
      <p class="sub">{e(", ".join(col["name"] for col in m["colors"]))}.</p>
      <div class="ctabs" role="tablist">{tabs}</div>
      <div class="cpanes">{panes}</div>
    </div>
  </section>"""
    # Bloques de texto del WordPress (alternos)
    bloques = ""
    for i, b in enumerate(m["blocks"]):
        txt = "".join(f"<p>{e(p)}</p>" for p in b["p"])
        img = f'<figure class="story__img"><img src="/{b["img"]}" alt="{e(fn)}: {e(b["h"].lower())}" width="{b["w"]}" height="{b["h_"]}" loading="lazy" decoding="async"></figure>' if b["img"] else ""
        hh = "h2" if i == 0 else "h3"
        bloques += f"""<div class="story{' story--rev' if i % 2 else ''} reveal">
        <div class="story__txt prose">{f'<{hh}>{e(b["h"])}</{hh}>' if b["h"] else ''}{txt}</div>
        {img}
      </div>"""
    equip = "".join(f"""<div class="ecard reveal">{f'<img src="/{q["img"]}" alt="{e(fn)}: {e(q["title"].lower())}" width="900" height="675" loading="lazy" decoding="async">' if q["img"] else ''}<div class="ecard__body"><h3>{e(q["title"])}</h3>{f'<p>{e(q["text"])}</p>' if q["text"] else ''}</div></div>""" for q in m["equip"])
    galeria = "".join(f'<figure><img src="/{g["img"]}" alt="{e(fn)} · foto {i+1}" width="{g["w"]}" height="{g["h"]}" loading="lazy" decoding="async"></figure>' for i, g in enumerate(m["gallery"]))
    rel_cards = "\n".join(card(x) for x in related(m))
    manual = f'<a class="lnk" href="/{m["manual"]}" target="_blank" rel="noopener" download>Descargar</a>' if m["manual"] else f'<a class="lnk" href="/contacto/?modelo={qmodel}#solicita">Pídenoslo</a>'
    precio_txt = (f"{eur(m['price'])} (antes {eur(m['pvp'])})" if m["pvp"] else eur(m["price"]))
    imgs = [SITE + "/" + m["main"]] + [SITE + "/" + col["imgs"][0]["img"] for col in m["colors"]]
    desc_txt = " ".join(p for b in m["blocks"] for p in b["p"])
    product = {"@context": "https://schema.org", "@type": ["Product", "Motorcycle"], "name": fn, "sku": m["slug"],
               "brand": {"@type": "Brand", "name": "Voge"}, "category": f"Motocicletas > {c['plural']}",
               "image": imgs, "description": desc_txt[:480],
               "color": [col["name"] for col in m["colors"]],
               "additionalProperty": [
                   {"@type": "PropertyValue", "name": "Cilindrada", "value": m["cc"], "unitText": "cc"},
                   {"@type": "PropertyValue", "name": "Potencia", "value": m["cv"], "unitText": "CV"},
                   {"@type": "PropertyValue", "name": "Par máximo", "value": m["nm"], "unitText": "Nm"}],
               "offers": {"@type": "Offer", "url": SITE + url, "priceCurrency": "EUR", "price": str(m["price"]),
                          "itemCondition": "https://schema.org/NewCondition", "availability": "https://schema.org/InStoreOnly",
                          "priceValidUntil": f"{datetime.date.today().year}-12-31", "seller": {"@id": DEALER_ID},
                          "areaServed": {"@type": "AdministrativeArea", "name": "Madrid Sur"}}}
    crumbs = [("Inicio", "/"), (c["plural"], cat_url(c)), (fn, url)]
    ld = [product, crumbs_ld(crumbs)]
    title = f"{fn} · Motos Voge Madrid Sur"
    primera = re.split(r"(?<=[.!?])\s", desc_txt.strip())[0] if desc_txt.strip() else ""
    meta = f"{fn} por {eur(m['price'])}. {primera}"
    if len(meta) > 160: meta = meta[:157].rsplit(" ", 1)[0] + "…"
    body = f"""
  {crumbs_html(crumbs)}
  <section class="mhero">
    <div class="wrap mhero__grid">
      <div class="mhero__media">
        <img id="model-photo" class="is-first" src="/{m["main"]}" alt="{e(fn)}" width="{m["mw"]}" height="{m["mh"]}" fetchpriority="high">
      </div>
      <div class="mhero__info">
        <div class="badges"><a class="badge badge--dark" href="{cat_url(c)}">{c["name"]}</a></div>
        <h1><small>Voge</small> {e(m["name"])}</h1>
        <div class="pricebox"><span class="pricebox__now">{eur(m["price"])}</span>{f'<del>{eur(m["pvp"])}</del>' if m["pvp"] else ''}{saving}</div>
        <p class="price-note">{PRICE_NOTE}</p>
        <div class="kpis kpis--3">
          <div class="kpi"><b>{m["cv"]} CV</b><span>Potencia</span></div>
          <div class="kpi"><b>{m["cc"]} cc</b><span>Cilindrada</span></div>
          <div class="kpi"><b>{m["nm"]} Nm</b><span>Par máx.</span></div>
        </div>
        <div class="colors-pick"><div class="colors-pick__label">Colores: <b>{e(", ".join(col["name"] for col in m["colors"]))}</b> · <a href="#colores" class="lnk">Ver fotos</a></div></div>
        <div class="mhero__ctas">
          <a class="btn btn--primary btn--block" href="/contacto/?modelo={qmodel}#solicita">Pedir presupuesto</a>
          <a class="btn btn--ghost btn--block" href="/solicitud-de-prueba/?modelo={qmodel}">Solicita una prueba</a>
        </div>
      </div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="wrap stories">
      {bloques}
    </div>
  </section>

  {colores}

  <section class="section section--alt">
    <div class="wrap">
      <span class="eyebrow" style="display:flex;justify-content:center">Equipamiento</span>
      <h2>{e(m["equipTitle"] or "Equipamiento de la " + fn)}</h2>
      <p class="sub">Lo que trae de serie la {e(fn)}.</p>
      <div class="ecards">{equip}</div>
    </div>
  </section>

  {f'<section class="section"><div class="wrap"><h2>Galería</h2><p class="sub">La {e(fn)} en detalle.</p><div class="mgallery">{galeria}</div></div></section>' if galeria else ''}

  <section class="section{' section--alt' if galeria else ''}">
    <div class="wrap">
      <div class="info-cards" style="margin-top:0">
        <div class="reveal"><h3>Descarga el manual del usuario</h3><p>De tu {e(m["name"])}.</p>{manual}</div>
        <div class="reveal reveal-d1"><h3>Solicita una prueba</h3><p>Prueba la {e(fn)} en Voge Móstoles o Voge Getafe.</p><a class="lnk" href="/solicitud-de-prueba/?modelo={qmodel}">Solicitar prueba</a></div>
        <div class="reveal reveal-d2"><h3>Pide información</h3><p>Precio, disponibilidad y financiación.</p><a class="lnk" href="/contacto/?modelo={qmodel}#solicita">Contactar</a></div>
      </div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="wrap">
      <h2>Otros modelos que te pueden interesar</h2>
      <div class="grid">
{rel_cards}
      </div>
    </div>
  </section>
  {cta_band(f"Prueba la {e(fn)}", "Solicita tu prueba en Voge Móstoles o Voge Getafe.")}
"""
    write(url, head(title, meta, url, og_img="/" + m["og"], ld=ld, preload="/" + m["main"]) + header() + body + footer())

# ------------------------------------------------------------------ CATEGORÍA
def page_cat(c):
    ms = [m for m in M if m["cat"] == c["name"]]
    url = cat_url(c)
    cards = "\n".join(card(m, h="h2") for m in ms)
    pmin = min(m["price"] for m in ms)
    crumbs = [("Inicio", "/"), (c["plural"] + " Voge", url)]
    ld = [crumbs_ld(crumbs), {"@context": "https://schema.org", "@type": "ItemList", "name": c["h1"], "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": SITE + model_url(m), "name": full(m)} for i, m in enumerate(ms)]}]
    others = "".join(f'<a class="btn btn--ghost" href="{cat_url(o)}">{o["plural"]}</a>' for o in CATS if o["slug"] != c["slug"])
    body = f"""
  <section class="hero hero--page">
    <div class="hero__bg"><img src="/assets/img/categorias/{c["img"]}" alt="" width="1200" height="900"></div>
    <div class="wrap"><div class="hero__inner">
      <span class="eyebrow">{len(ms)} modelos · desde {eur(pmin)}</span>
      <h1>{c["h1"]}</h1>
      <p class="lead">{c["corto"]}.</p>
      <div class="hero__actions"><a class="btn btn--primary" href="#modelos">Ver modelos</a><a class="btn btn--ghost-light" href="/solicitud-de-prueba/">Pedir prueba</a></div>
    </div></div>
  </section>
  {crumbs_html(crumbs)}
  <section class="section section--alt" id="modelos">
    <div class="wrap">
      <div class="grid">
{cards}
      </div>
      <p class="promo-legal">{PRICE_NOTE}</p>
    </div>
  </section>
  <section class="section"><div class="wrap"><div class="hero__actions" style="justify-content:center">{others}</div></div></section>
  {cta_band()}
"""
    write(url, head(f"{c['plural']} Voge · Motos Voge Madrid Sur", f"{c['corto']}. {len(ms)} modelos Voge {c['name'].lower()} desde {eur(pmin)} en Voge Móstoles y Voge Getafe.", url, ld=ld) + header("modelos") + body + footer())

# ------------------------------------------------------------------ FORMULARIOS
def model_select():
    out = '<option value="">Selecciona un modelo…</option>'
    for c in CATS:
        out += f'<optgroup label="{c["plural"]}">' + "".join(f'<option>{e(m["name"])}</option>' for m in M if m["cat"] == c["name"]) + "</optgroup>"
    return out + '<option>Aún no lo sé</option>'

def form(tipo):
    prueba = tipo == "prueba"; taller = tipo == "taller"
    subject = {"prueba": "Solicitud de PRUEBA web Voge · Duomo Motor", "taller": "Solicitud TALLER web Voge · Duomo Motor"}.get(tipo, "Nueva solicitud web Voge · Duomo Motor")
    tsol = {"prueba": "Prueba de moto", "taller": "Cita de taller"}.get(tipo, "Información / presupuesto")
    depto = "Taller" if taller else "Ventas"
    tienda = """<div class="field">
              <label for="tienda">¿Qué concesionario te viene mejor?*</label>
              <select id="tienda" name="concesionario" required>
                <option value="">Selecciona…</option>
                <option>Voge Móstoles (Calle Juan de la Cierva, 7-9)</option>
                <option>Voge Getafe (Calle Barberán y Collar, 1)</option>
                <option>Me da igual</option>
              </select>
            </div>"""
    if taller:
        top = """<div class="field">
              <label for="servicio">¿Qué necesitas?*</label>
              <select id="servicio" name="servicio" required>
                <option value="">Selecciona…</option>
                <option>Revisión</option><option>Puesta a punto</option><option>Cambio de aceite</option>
                <option>Revisión de frenos</option><option>Neumáticos</option><option>Instalación de accesorios</option><option>Avería u otra consulta</option>
              </select>
            </div>
            <div class="field">
              <label for="modelo">Modelo de tu moto*</label>
              <input id="modelo" name="modelo" required placeholder="Ej.: Voge 525DSX, 2025">
            </div>"""
    else:
        top = f"""<div class="field">
              <label for="modelo">Modelo de interés{'*' if prueba else ''}</label>
              <select id="modelo" name="modelo"{' required' if prueba else ''}>{model_select()}</select>
            </div>
            {tienda}"""
    extra = """<div class="field">
              <label for="fecha">¿Qué día te viene mejor?</label>
              <input id="fecha" name="dia_preferido" placeholder="Ej.: martes por la tarde">
            </div>""" if (prueba or taller) else ""
    ph = {"prueba": "Cuéntanos si quieres probar más de un modelo o tienes alguna duda.",
          "taller": "Cuéntanos qué le pasa a tu moto o los kilómetros que tiene."}.get(tipo, "Cuéntanos qué necesitas: presupuesto, financiación, valoración de tu moto actual…")
    btn = {"prueba": "Solicitar prueba", "taller": "Pedir cita de taller"}.get(tipo, "Enviar solicitud")
    return f"""<form class="form" id="contact-form" action="https://formsubmit.co/{NEGOCIO["email"]}" method="POST" novalidate>
            <input type="hidden" name="_subject" value="{subject}">
            <input type="hidden" name="_template" value="table">
            <input type="hidden" name="_captcha" value="false">
            <input type="hidden" name="tipo_solicitud" value="{tsol}">
            <input type="hidden" name="departamento" value="{depto}">
            <input type="hidden" name="marca" value="Voge">
            <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off" aria-hidden="true">
            {top}
            <div class="field--row">
              <div class="field"><label for="nombre">Nombre*</label><input id="nombre" name="nombre" required autocomplete="name"></div>
              <div class="field"><label for="tel">Teléfono*</label><input id="tel" name="telefono" type="tel" required autocomplete="tel" inputmode="tel"></div>
            </div>
            <div class="field"><label for="mail">Email*</label><input id="mail" name="email" type="email" required autocomplete="email"></div>
            {extra}
            <div class="field">
              <label for="msg">Mensaje</label>
              <textarea id="msg" name="mensaje" placeholder="{ph}"></textarea>
            </div>
            <label class="check">
              <input type="checkbox" name="acepta_privacidad" value="Sí" required>
              <span>He leído y acepto las <a href="/politicas-de-privacidad/" target="_blank">políticas de privacidad</a>. Usaremos tus datos solo para responder a tu solicitud.*</span>
            </label>
            <button class="btn btn--primary" type="submit">{btn}</button>
            <p class="form__note">* Campos obligatorios. Responsable: {NEGOCIO["razon"]}. Finalidad: atender tu solicitud. Derechos: acceso, rectificación y supresión en {NEGOCIO["email"]}.</p>
            <div class="form-status" id="form-status" role="status" aria-live="polite" hidden></div>
          </form>"""

def info_card(taller=False):
    tel_m = f'<a href="tel:{NEGOCIO["telIntl"]}">910 40 92 76</a>'
    return f"""<div class="info-card reveal">
          <div class="info-item"><div class="info-item__ico">{ICO["pin"]}</div><div><h3>Voge Móstoles</h3><p>{e(DIRECCION)}<br>{tel_m}</p></div></div>
          <div class="info-item"><div class="info-item__ico">{ICO["pin"]}</div><div><h3>Voge Getafe</h3><p>{e(DIR_GETAFE)}<br><a href="tel:{GETAFE["telIntl"]}">{GETAFE["tel"]}</a></p></div></div>
          <div class="info-item"><div class="info-item__ico">{ICO["clock"]}</div><div><h3>Horario (los dos)</h3><p>Lunes a viernes: 10:00 a 14:00 y 16:00 a 19:30<br>Sábados: 10:00 a 14:00 · Domingo: cerrado</p></div></div>
          <div class="info-item"><div class="info-item__ico">{ICO["mail"]}</div><div><h3>Email</h3><a href="mailto:{NEGOCIO["email"]}">{NEGOCIO["email"]}</a></div></div>
          <div class="info-item"><div class="info-item__ico">{ICO["ig"]}</div><div><h3>Instagram</h3><a href="{NEGOCIO["instagram"]}" target="_blank" rel="noopener">{NEGOCIO["instagramUser"]}</a></div></div>
          <iframe class="map-embed" src="{MAPS_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Mapa de Voge Móstoles"></iframe>
          <iframe class="map-embed" src="{GETAFE["embed"]}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Mapa de Voge Getafe" style="margin-top:12px"></iframe>
        </div>"""

def page_form(tipo):
    prueba = tipo == "prueba"
    url = "/solicitud-de-prueba/" if prueba else "/contacto/"
    h1 = "Prueba tu nueva Voge" if prueba else "Contáctanos"
    lead = ("Elige el modelo y el concesionario (Móstoles o Getafe) y te confirmamos día y hora."
            if prueba else "Rellena el formulario y te preparamos presupuesto, financiación y lo que necesites. Te respondemos lo antes posible.")
    crumbs = [("Inicio", "/"), ("Solicitar prueba" if prueba else "Contacto", url)]
    contact_ld = {"@context": "https://schema.org", "@type": "ContactPage", "name": h1, "url": SITE + url, "about": [{"@id": DEALER_ID}, {"@id": GETAFE_ID}]}
    body = f"""
  <section class="hero hero--page">
    <div class="hero__bg"><img src="/assets/img/categorias/{'motos-voge-scooters.webp' if not prueba else 'motos-voge-adventure.webp'}" alt="" width="1200" height="900"></div>
    <div class="wrap"><div class="hero__inner">
      <span class="eyebrow">{'Prueba sin compromiso' if prueba else 'Estamos para ayudarte'}</span>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
    </div></div>
  </section>
  {crumbs_html(crumbs)}
  <section class="section" id="solicita" style="padding-top:36px">
    <div class="wrap">
      <div class="contact-grid">
        <div class="reveal">
          <span class="eyebrow">{'Reserva tu prueba' if prueba else 'Escríbenos'}</span>
          <h2>{'Solicitar prueba' if prueba else 'Solicita información'}</h2>
          {form(tipo)}
        </div>
        {info_card()}
      </div>
    </div>
  </section>
"""
    title = "Solicitud de prueba · Motos Voge Madrid Sur" if prueba else "Contacto · Motos Voge Madrid Sur"
    meta = ("Prueba tu nueva Voge en Voge Móstoles o Voge Getafe. Elige el modelo y te confirmamos día y hora."
            if prueba else f"Contacta con Voge Madrid Sur: Voge Móstoles ({NEGOCIO['tel']}) y Voge Getafe ({GETAFE['tel']}). Formulario, direcciones y horario.")
    write(url, head(title, meta, url, ld=[crumbs_ld(crumbs), contact_ld, DEALER, DEALER_GETAFE]) + header("contacto" if not prueba else "") + body + footer())

# ------------------------------------------------------------------ CONCESIONARIOS (página del WordPress)
def page_concesionarios():
    url = "/concesionario-voge-madrid-sur/"
    crumbs = [("Inicio", "/"), ("Puntos de venta", url)]
    body = f"""
  <section class="hero hero--page">
    <div class="hero__bg"><img src="/assets/img/hero/concesionario-voge-madrid-sur-3.webp" alt="" width="1366" height="911"></div>
    <div class="wrap"><div class="hero__inner">
      <span class="eyebrow">Siempre cerca de ti</span>
      <h1>Voge Madrid Sur: tu concesionario de confianza en Móstoles y Getafe</h1>
      <p class="lead">Disponemos de taller propio, servicio postventa, recambios originales y un equipo humano especializado que garantiza una atención integral y una experiencia completa, cómoda y segura antes, durante y después de tu compra.</p>
      <div class="hero__actions"><a class="btn btn--primary" href="#puntos">Ver puntos de venta</a><a class="btn btn--ghost-light" href="/solicitud-de-prueba/">Prueba la tuya</a></div>
    </div></div>
  </section>
  {crumbs_html(crumbs)}
  <section class="section" style="padding-top:36px">
    <div class="wrap split">
      <div class="prose reveal">
        <span class="eyebrow">Nuestra historia</span>
        <h2>Pasión por el motor desde 1960</h2>
        <p>Nuestra historia nace de una auténtica pasión por el mundo del motor y de una sólida tradición familiar en automoción que se remonta a <b>1960</b>. Hoy, con presencia en <b>Móstoles</b> y <b>Getafe</b>, seguimos construyendo una base de experiencia, compromiso y confianza con cada cliente que confía en nosotros.</p>
        <p>Trabajamos cada día para ofrecer asesoramiento personalizado, el mejor servicio técnico y una atención cercana que convierte cada visita en una experiencia diferencial.</p>
        <figure style="margin:24px 0 0"><img src="/assets/img/empresa/equipo-duomo-motor-bikes.webp" alt="Equipo de Duomo Motor Bikes, concesionario oficial Voge en Móstoles y Getafe" width="1280" height="720" loading="lazy" decoding="async" style="border-radius:var(--radius,8px);width:100%;height:auto"></figure>
      </div>
      <div class="stats reveal reveal-d1" style="grid-template-columns:1fr;text-align:left;gap:20px">
        <div class="stat"><b>+<span data-count="20">20</span></b><span>Profesionales del motor</span></div>
        <div class="stat"><b>+<span data-count="1500">1500</span></b><span>Motos entregadas</span></div>
        <div class="stat"><b>+<span data-count="50">50</span></b><span>Años de experiencia en motos</span></div>
      </div>
    </div>
  </section>
  <section class="section section--alt" id="puntos"><div class="wrap">{visit_block("Puntos de venta")}</div></section>
  {cta_band("Prueba la tuya", "Reserva tu prueba en Voge Móstoles o Voge Getafe y te confirmamos día y hora.")}
"""
    write(url, head("Concesionario Voge Madrid Sur · Motos Voge Madrid Sur",
                    "Voge Madrid Sur, tu concesionario de confianza en Móstoles y Getafe: taller propio, servicio postventa, recambios originales y un equipo humano especializado.",
                    url, ld=[DEALER, DEALER_GETAFE, crumbs_ld(crumbs)]) + header("concesionario") + body + footer())


def bloque_blog(*a, **k): return ""
# ------------------------------------------------------------------ SITEMAP, ROBOTS, LLMS
def seo_files():
    urls = [("/", "1.0", "weekly"), ("/concesionario-voge-madrid-sur/", "0.9", "monthly"),
            ("/solicitud-de-prueba/", "0.7", "monthly"), ("/contacto/", "0.7", "monthly")]
    urls += [(cat_url(c), "0.8", "weekly") for c in CATS]
    urls += [(model_url(m), "0.9", "weekly") for m in M]
    posts = sorted(blog_posts(), key=lambda p: p["fecha"], reverse=True)
    urls += [("/blog/", "0.8", "daily")]
    urls += [(f"/blog/{p['slug']}/", "0.7", "monthly") for p in posts]
    fechas = {f"/blog/{p['slug']}/": p["fecha"] for p in posts}
    if posts: fechas["/blog/"] = posts[0]["fecha"]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for u, p, f in urls:
        imgs = ""
        m = next((x for x in M if model_url(x) == u), None)
        if m:
            imgs = "".join(f"<image:image><image:loc>{SITE}/{c['imgs'][0]['img']}</image:loc></image:image>" for c in m["colors"])
        bp = next((x for x in posts if f"/blog/{x['slug']}/" == u), None)
        if bp: imgs = f"<image:image><image:loc>{SITE}{bp['imagen']}</image:loc></image:image>"
        xml.append(f"  <url><loc>{SITE}{u}</loc><lastmod>{fechas.get(u, TODAY)}</lastmod><changefreq>{f}</changefreq><priority>{p}</priority>{imgs}</url>")
    xml.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(xml) + "\n")
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\nDisallow: /_build/\n\nSitemap: {SITE}/sitemap.xml\n")
    open(os.path.join(ROOT, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8").write(INDEXNOW_KEY)
    gama = "\n".join(f"- [{full(m)}]({SITE}{model_url(m)}): {m['cat'].lower()}, {m['cc']} cc, {m['cv']} CV, {eur(m['price'])}" for m in M)
    blog = "\n".join(f"- [{p['titulo']}]({SITE}/blog/{p['slug']}/)" for p in posts[:20])
    open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8").write(f"""# Voge Madrid Sur · Duomo Motor Bikes

> Concesionarios oficiales Voge en Móstoles y Getafe (Duomo Motor Bikes). Venta de motos Voge nuevas, prueba, taller propio, servicio postventa y recambios originales.

- Voge Móstoles: {DIRECCION} · Tel. 910 40 92 76
- Voge Getafe: {DIR_GETAFE} · Tel. {GETAFE['tel']}
- Email: {NEGOCIO['email']}
- Horario (los dos): {NEGOCIO['horario']}
- WhatsApp: 613 91 55 05

## Páginas principales
- [Inicio]({SITE}/)
- [Puntos de venta: Voge Móstoles y Voge Getafe]({SITE}/concesionario-voge-madrid-sur/)
- [Solicitar prueba]({SITE}/solicitud-de-prueba/)
- [Contacto]({SITE}/contacto/)

## Gama Voge (PVP con IVA)
{gama}

## Blog
{blog}
""")
    open(os.path.join(ROOT, "site.webmanifest"), "w", encoding="utf-8").write(json.dumps({
        "name": "Voge Madrid Sur · Duomo Motor Bikes", "short_name": "Voge Madrid Sur", "start_url": "/", "display": "browser",
        "background_color": "#16171d", "theme_color": "#16171d",
        "icons": [{"src": "/assets/img/logo/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/assets/img/logo/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    page_home()
    for m in M: page_model(m)
    for c in CATS: page_cat(c)
    page_form("contacto"); page_form("prueba"); page_concesionarios()
    for u, (t, s, cnt) in LEGAL.items(): page_legal(u, t, s, cnt)
    page_blog(); page_404(); seo_files()
    print(f"OK · {len(M)} modelos · {len(CATS)} categorías")
