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
GETAFE_ID = SITE + "/voge-getafe/#concesionario"
DEALER = {
    "@context": "https://schema.org", "@type": "MotorcycleDealer", "@id": DEALER_ID,
    "name": "Voge Móstoles · Duomo Motor Bikes", "alternateName": "Voge Madrid Sur", "legalName": NEGOCIO["razon"], "url": SITE + "/",
    "image": SITE + "/assets/img/og/voge-madrid-sur.jpg", "logo": SITE + "/assets/img/logo/voge-madrid-sur-negro.png",
    "telephone": NEGOCIO["telIntl"], "email": NEGOCIO["email"], "priceRange": "€€",
    "address": {"@type": "PostalAddress", "streetAddress": NEGOCIO["calle"], "postalCode": NEGOCIO["cp"],
                "addressLocality": NEGOCIO["ciudad"], "addressRegion": "Comunidad de Madrid", "addressCountry": "ES"},
    "openingHoursSpecification": HORAS,
    "areaServed": [{"@type": "City", "name": z} for z in ZONAS if z != "Madrid capital"],
    "brand": {"@type": "Brand", "name": "Voge"},
    "geo": GEO, "hasMap": GMAPS, "sameAs": [NEGOCIO["instagram"], GMAPS],
    "foundingDate": "2020", "currenciesAccepted": "EUR", "paymentAccepted": "Efectivo, tarjeta, transferencia, financiación",
    "slogan": "Tu nueva Voge a 5 minutos del X-Madrid",
    "knowsAbout": ["Motos Voge", "Scooters 125 cc", "Motos para carnet A2", "Motos trail", "Taller de motos", "Financiación de motos"],
    "department": [{"@type": "AutoRepair", "@id": SITE + "/taller-voge/#taller", "name": "Taller Voge Madrid Sur · Duomo Motor Bikes",
                    "telephone": NEGOCIO["telTallerIntl"], "url": SITE + "/taller-voge/", "image": SITE + "/assets/img/og/voge-madrid-sur.jpg",
                    "address": {"@type": "PostalAddress", "streetAddress": NEGOCIO["calle"], "postalCode": NEGOCIO["cp"],
                                "addressLocality": NEGOCIO["ciudad"], "addressRegion": "Comunidad de Madrid", "addressCountry": "ES"}}],
    "parentOrganization": {"@type": "Organization", "name": "Duomo Motor Bikes", "url": "https://duomomotor.com/"},
}
DEALER_GETAFE = {
    "@context": "https://schema.org", "@type": "MotorcycleDealer", "@id": GETAFE_ID,
    "name": GETAFE["nombre"], "legalName": NEGOCIO["razon"], "url": SITE + "/voge-getafe/",
    "image": SITE + "/assets/img/og/voge-madrid-sur.jpg", "logo": SITE + "/assets/img/logo/voge-madrid-sur-negro.png",
    "telephone": GETAFE["telIntl"], "email": NEGOCIO["email"], "priceRange": "€€",
    "address": {"@type": "PostalAddress", "streetAddress": GETAFE["calle"], "postalCode": GETAFE["cp"],
                "addressLocality": GETAFE["ciudad"], "addressRegion": "Comunidad de Madrid", "addressCountry": "ES"},
    "openingHoursSpecification": HORAS, "geo": GETAFE["geo"], "hasMap": GETAFE["gmaps"], "sameAs": [GETAFE["gmaps"]],
    "areaServed": [{"@type": "City", "name": z} for z in ["Getafe", "Leganés", "Parla", "Pinto", "Fuenlabrada", "Madrid capital"]],
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

NAV = [("Modelos", "/#gama", "modelos"), ("Concesionarios", "/concesionario-voge-madrid-sur/", "concesionario"), ("Taller", "/taller-voge/", "taller"),
       ("Blog", "/blog/", "blog"), ("Contacto", "/contacto/", "contacto")]

def header(active=""):
    links = "".join(f'<a href="{u}"{" class=\"active\" aria-current=\"page\"" if k == active else ""}>{n}</a>' for n, u, k in NAV)
    return f"""<body>
  <a class="skip" href="#contenido">Saltar al contenido</a>
  <div class="topbar"><div class="wrap">
    <div class="topbar__info"><span>Concesionarios oficiales en Móstoles y Getafe</span><span>{e(NEGOCIO["horarioCorto"])}</span></div>
    <span class="topbar__tels"><a href="tel:{NEGOCIO["telIntl"]}">Móstoles: {NEGOCIO["tel"]}</a> · <a href="tel:{GETAFE["telIntl"]}">Getafe: {GETAFE["tel"]}</a></span>
  </div></div>
  <header class="site-header">
    <div class="wrap nav">
      <a class="brand" href="/" aria-label="Voge Madrid Sur · Inicio">
        <img src="/assets/img/logo/voge-madrid-sur-negro.png" srcset="/assets/img/logo/voge-madrid-sur-negro@2x.png 2x" alt="Voge Madrid Sur" width="406" height="150">
      </a>
      <nav class="nav__links" id="menu" aria-label="Menú principal">
        {links}
        <a class="btn btn--primary" href="/solicitud-de-prueba/">Pedir prueba</a>
      </nav>
      <button class="nav__toggle" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
    </div>
  </header>
  <main id="contenido">"""

def footer():
    cats = "".join(f'<a href="{cat_url(c)}">{c["plural"]} Voge</a>' for c in CATS)
    return f"""  </main>
  <footer class="site-footer">
    <div class="wrap footer-grid">
      <div>
        <img class="footer-logo" src="/assets/img/logo/voge-madrid-sur-blanco.png" srcset="/assets/img/logo/voge-madrid-sur-blanco@2x.png 2x" alt="Voge Madrid Sur" width="406" height="150" loading="lazy">
        <p style="max-width:38ch">Duomo Motor Bikes · Concesionarios oficiales Voge en Móstoles y Getafe (Madrid Sur). Venta, financiación, taller y recambios originales.</p>
        <p class="disclaimer">Voge y los nombres de sus modelos son marcas registradas de su fabricante. Esta web pertenece a un concesionario oficial, no es la web oficial de la marca. Precios orientativos sujetos a la tarifa y promociones vigentes.</p>
      </div>
      <div>
        <h2>Gama Voge</h2>
        {cats}
        <a href="/motos-voge-a2/">Motos Voge A2</a>
        <a href="/motos-125-carnet-coche/">Motos 125 con carnet de coche</a>
      </div>
      <div>
        <h2>Web</h2>
        <a href="/#gama">Todos los modelos</a>
        <a href="/solicitud-de-prueba/">Solicitar prueba</a>
        <a href="/concesionario-voge-madrid-sur/">Concesionarios Voge</a>
        <a href="/voge-mostoles/">Voge Móstoles</a>
        <a href="/voge-getafe/">Voge Getafe</a>
        <a href="/taller-voge/">Taller Voge</a>
        <a href="/blog/">Blog</a>
        <a href="/contacto/">Contacto</a>
      </div>
      <div>
        <h2>Visítanos</h2>
        <address>
          <a href="{MAPS_DIR}" target="_blank" rel="noopener"><b>Voge Móstoles</b><br>{e(NEGOCIO["calle"])}<br>{NEGOCIO["cp"]} {e(NEGOCIO["ciudad"])} (Madrid)</a>
          <a href="tel:{NEGOCIO["telIntl"]}">{NEGOCIO["tel"]}</a>
          <a href="{GETAFE["dir"]}" target="_blank" rel="noopener" style="margin-top:8px"><b>Voge Getafe</b><br>{e(GETAFE["calle"])}<br>{GETAFE["cp"]} {e(GETAFE["ciudad"])} (Madrid)</a>
          <a href="tel:{GETAFE["telIntl"]}">{GETAFE["tel"]}</a>
          <a href="mailto:{NEGOCIO["email"]}">{NEGOCIO["email"]}</a>
          <a href="{NEGOCIO["instagram"]}" target="_blank" rel="noopener">{NEGOCIO["instagramUser"]}</a>
        </address>
        <p style="font-size:.85rem;margin-top:8px">{e(NEGOCIO["horario"])}</p>
      </div>
    </div>
    <div class="wrap footer-zonas"><span>Concesionario Voge cerca de:</span> <a href="/voge-mostoles/">Móstoles</a> · <a href="/voge-getafe/">Getafe</a> · <a href="/voge-alcorcon/">Alcorcón</a> · <a href="/voge-x-madrid/">X-Madrid</a> · <a href="/voge-fuenlabrada/">Fuenlabrada</a> · <a href="/voge-leganes/">Leganés</a></div>
    <div class="wrap footer-bottom">
      <span>© <span id="year">{datetime.date.today().year}</span> {NEGOCIO["razon"]}. Todos los derechos reservados.</span>
      <span><a href="/aviso-legal/">Aviso legal</a> · <a href="/politicas-de-privacidad/">Privacidad</a> · <a href="/politicas-de-cookies/">Cookies</a></span>
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

def cta_band(title="¿Ya sabes qué Voge quieres?", text="Escríbenos y te preparamos oferta, financiación a medida y una prueba sin compromiso en Voge Móstoles o Voge Getafe."):
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
        <span class="eyebrow">Concesionario oficial Voge</span>
        <h2>{nombre}</h2>
        <div class="info-item"><div class="info-item__ico">{ICO["pin"]}</div><div><h3>Dirección</h3><p>{e(direccion)}</p></div></div>
        <div class="info-item"><div class="info-item__ico">{ICO["clock"]}</div><div><h3>Horario</h3><p>{e(NEGOCIO["horario"])}</p></div></div>
        <div class="info-item"><div class="info-item__ico">{ICO["tel"]}</div><div><h3>Teléfono</h3><a href="tel:{telI}">{tel}</a>{extra}</div></div>
        <div class="hero__actions"><a class="btn btn--primary" href="{dir_}" target="_blank" rel="noopener">Cómo llegar</a><a class="btn btn--ghost-light" href="/solicitud-de-prueba/">Reservar prueba</a></div>
      </div>
      <iframe src="{embed}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Mapa de {e(nombre)}"></iframe>
    </div>"""
    mo = un("Voge Móstoles", DIRECCION, NEGOCIO["tel"], NEGOCIO["telIntl"], MAPS_DIR, MAPS_EMBED, f'<br><small>Taller: <a href="tel:{NEGOCIO["telTallerIntl"]}">{NEGOCIO["telTaller"]}</a></small>')
    ge = un("Voge Getafe", DIR_GETAFE, GETAFE["tel"], GETAFE["telIntl"], GETAFE["dir"], GETAFE["embed"])
    if tienda == "mostoles": return mo
    if tienda == "getafe": return ge
    return f'<h2 style="text-align:center;margin-bottom:28px">{h}</h2>' + mo + '<div style="height:28px"></div>' + ge

def card(m, lazy=True, h="h3"):
    badge = '<span class="card__badge">En promoción</span>' if m["promo"] else ""
    price = (f'<del>{eur(m["pvp"])}</del>' if m["pvp"] else "") + eur(m["price"])
    lic = LIC[m["license"]]["corto"]
    ncol = len(m["colors"])
    return f"""<article class="card reveal" data-cat="{m["cat"]}">
        <div class="card__media"><img src="/{m["main"]}" alt="{e(full(m))} en Móstoles y Getafe" width="{m["mw"]}" height="{m["mh"]}"{' loading="lazy" decoding="async"' if lazy else ''}>{badge}</div>
        <div class="card__body">
          <span class="card__cat">{m["cat"]}</span>
          <{h} class="card__title"><a href="{model_url(m)}">{e(m["name"])}</a></{h}>
          <div class="card__specs">
            <span class="card__spec"><b>{m["cc"]} cc</b>Cilindrada</span>
            <span class="card__spec"><b>{m["cv"]} CV</b>Potencia</span>
            <span class="card__spec"><b>{lic}</b>Carnet</span>
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
      <h1>Blog de motos en <span class="hl">Madrid Sur</span></h1>
      <p class="lead">Novedades del mundo de la moto, rutas desde Alcorcón, Móstoles y Getafe, consejos de carnet y mantenimiento, y todo sobre la gama Voge. Tus concesionarios en Móstoles ({XMADRID}) y Getafe.</p>
    </div></div>
  </section>
  {crumbs_html(crumbs)}
  <section class="section" style="padding-top:36px">
    <div class="wrap">
      <div class="bgrid" id="blog-list">%%LISTADO%%</div>
    </div>
  </section>
  <section class="section section--alt">
    <div class="wrap">
      <h2>Tus concesionarios Voge en Madrid Sur</h2>
      <p class="sub">Estamos en <a href="/voge-mostoles/">Móstoles</a>, {XMADRID}, y en <a href="/voge-getafe/">Getafe</a>. Si vienes desde <a href="/voge-alcorcon/">Alcorcón</a>, <a href="/voge-fuenlabrada/">Fuenlabrada</a> o <a href="/voge-leganes/">Leganés</a>, te pillamos muy cerca.</p>
    </div>
  </section>
  {cta_band("Tu nueva Voge, en Móstoles o Getafe", "Ven a verla y pruébala en Voge Móstoles o Voge Getafe. Toda la gama y taller propio.")}
"""
    return head("Blog de motos en Madrid Sur · Voge Madrid Sur",
                "Novedades de motos, rutas desde Alcorcón, Móstoles y Getafe, consejos de carnet y mantenimiento y la gama Voge. Blog de Voge Madrid Sur (Móstoles y Getafe).",
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
          <p>{e(CREDENCIALES)} Somos los concesionarios oficiales Voge de Duomo Motor Bikes en <a href="/voge-mostoles/">Móstoles</a>, {XMADRID}, y <a href="/voge-getafe/">Getafe</a>, con <a href="/taller-voge/">taller propio</a>.</p></div>
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
          <p class="post__card-t">Cerca de ti</p>
          <a href="/voge-mostoles/">Voge Móstoles</a>
          <a href="/voge-x-madrid/">Voge cerca del X-Madrid</a>
          <a href="/voge-alcorcon/">Voge para Alcorcón</a>
          <a href="/voge-fuenlabrada/">Voge para Fuenlabrada</a>
          <a href="/voge-leganes/">Voge para Leganés</a>
          <a href="/voge-getafe/">Voge Getafe</a>
          <a href="/motos-125-carnet-coche/">Motos 125 con carnet de coche</a>
          <a href="/motos-voge-a2/">Motos Voge para el A2</a>
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
        <span class="cattile__txt"><strong>{c["plural"]}</strong><span>{counts[c["name"]]} modelos · desde {eur(precio_min(cat=c["name"]))}</span></span></a>""" for i, c in enumerate(CATS))
    tiles += f"""<a class="cattile cattile--promo reveal" href="/motos-voge-a2/">
        <span class="cattile__txt"><strong>Carnet A2</strong><span>{sum(1 for m in M if lic_ok_a2(m))} Voge que puedes llevar con el A2</span></span>
        <span class="btn btn--dark">Ver motos A2</span></a>"""
    bar = '<button class="active" data-filter="Todas">Todas <small>' + str(len(M)) + '</small></button>' + "".join(
        f'<button data-filter="{c["name"]}">{c["plural"]} <small>{counts[c["name"]]}</small></button>' for c in CATS)
    cards = "\n".join(card(m) for m in M)
    lic_cards = ""
    for k, t, txt in [("A1", "Carnet de coche o A1", f"Todas las Voge de 125 cc, desde {eur(precio_min('A1'))}: scooters SR16 Air, SR16, SR1 y SR1 ADV y las naked 125R y 125RS. Si tienes el carnet B con más de tres años de antigüedad, puedes llevarlas sin examen."),
                      ("A2", "Carnet A2", f"SR3, SR4 Radar, SR450X, 300 Rally y 525DSX, desde {eur(precio_min('A2'))}, y la 625R en su versión limitada a 35 kW."),
                      ("A", "Carnet A", f"625DSX, DS800 Rally y 900DSX, trail de 64 y 95 CV, desde {eur(precio_min('A'))}, y la naked 625R de 64 CV.")]:
        keys = {"A1": ["A1"], "A2": ["A2", "A-A2"], "A": ["A", "A-A2"]}[k]
        chips = "".join(f'<a href="{model_url(m)}">{e(m["name"])}</a>' for m in M if m["license"] in keys)
        lic_cards += f"""<div class="license reveal"><span class="license__tag">{LIC[k]["tag"]}</span><h3>{t}</h3><p>{txt}</p><div class="license__models">{chips}</div></div>"""
    slides = "".join(f'<div class="hero__slide{" is-active" if i == 0 else ""}"><img src="/assets/img/hero/concesionario-voge-madrid-sur-{i+1}.webp" alt="" width="1366" height="911"></div>' for i in range(3))
    faqs = [
        ("¿Dónde hay un concesionario oficial Voge en Madrid Sur?",
         f"Tienes dos: <b>Voge Móstoles</b>, en {e(DIRECCION)}, y <b>Voge Getafe</b>, en {e(DIR_GETAFE)}. Los dos son de Duomo Motor Bikes, concesionario oficial Voge, con exposición de la gama, financiación y servicio posventa."),
        ("¿Hay un concesionario Voge cerca del X-Madrid?",
         f"Sí. Voge Móstoles está {XMADRID} de Alcorcón: {e(DIRECCION)}. Tienes toda la gama Voge en exposición, prueba y taller."),
        ("¿Qué Voge puedo llevar con el carnet de coche?",
         f"Con el carnet B y más de tres años de antigüedad puedes llevar cualquier Voge de 125 cc: los scooters <a href=\"/modelo/sr16/\">SR16</a>, <a href=\"/modelo/sr16-air/\">SR16 Air</a>, <a href=\"/modelo/sr1/\">SR1</a> y <a href=\"/modelo/sr1-adv/\">SR1 ADV</a> o las naked <a href=\"/modelo/125r/\">125R</a> y <a href=\"/modelo/125rs/\">125RS</a>. Desde {eur(precio_min('A1'))}."),
        ("¿Qué Voge es mejor para el carnet A2?",
         "Depende del uso: para ciudad y viajes, los scooters <a href=\"/modelo/sr3/\">SR3</a>, <a href=\"/modelo/sr4-radar/\">SR4 Radar</a> y <a href=\"/modelo/sr450x/\">SR450X</a>; para trail, la <a href=\"/modelo/300-rally/\">300 Rally</a> y la <a href=\"/modelo/525dsx/\">525DSX</a>; y si buscas una naked, la <a href=\"/modelo/625r/\">625R</a> en versión limitada a 35 kW."),
        ("¿Puedo probar una Voge antes de comprarla?",
         "Sí. Pide tu prueba en <a href=\"/solicitud-de-prueba/\">Solicitar prueba</a> y te confirmamos día, hora y concesionario (Móstoles o Getafe). Recuerda traer tu carnet y tu equipamiento."),
        ("¿Tenéis taller para motos Voge?",
         f"Sí. Tenemos taller propio con servicio posventa y recambios originales. <a href=\"/taller-voge/\">Pide cita en el taller</a> o llama al {NEGOCIO['telTaller']}."),
        ("¿Se puede financiar una Voge?",
         "Sí, te preparamos una financiación a medida. Pídenos las condiciones para el modelo que te interesa y te las enviamos por escrito."),
    ]
    ld = [DEALER, DEALER_GETAFE, {"@context": "https://schema.org", "@type": "WebSite", "name": "Voge Madrid Sur", "url": SITE + "/", "inLanguage": "es-ES", "publisher": {"@id": DEALER_ID}},
          faq_ld(faqs),
          {"@context": "https://schema.org", "@type": "ItemList", "name": "Gama Voge en Madrid Sur", "itemListElement": [
              {"@type": "ListItem", "position": i + 1, "url": SITE + model_url(m), "name": full(m)} for i, m in enumerate(M)]}]
    hero_txt = [("Voge 625 DSX", "Diseñada para ser tu mejor aliada en cualquier terreno, esta motocicleta combina potencia, tecnología avanzada y un diseño robusto.", "625dsx"),
                ("Voge SR4 Radar", "Scooter de vanguardia dotado con tecnología de detección de obstáculos en ángulo muerto y alerta de colisión.", "sr4-radar"),
                ("Voge 900 DSX", "Combina tecnología de punta, un diseño y un precio increíblemente competitivo, que incorpora nuevas características diseñadas para maximizar tu experiencia de conducción.", "900dsx")]
    destacados = "".join(f"""<article class="dest reveal{' reveal-d' + str(i) if i else ''}">
        <a class="dest__media" href="/modelo/{s}/" tabindex="-1" aria-hidden="true"><img src="/{mm(s)['main']}" alt="" width="{mm(s)['mw']}" height="{mm(s)['mh']}" loading="lazy" decoding="async"></a>
        <div class="dest__body"><h3><a href="/modelo/{s}/">{t}</a></h3><p>{d}</p>
        <div class="dest__ctas"><a class="btn btn--dark" href="/modelo/{s}/">Más información</a><a class="btn btn--ghost" href="/solicitud-de-prueba/?modelo={quote(mm(s)['name'])}">Solicita una prueba</a></div></div>
      </article>""" for i, (t, d, s) in enumerate(hero_txt))
    body = f"""
  <section class="hero" aria-label="Voge Madrid Sur">
    <div class="hero__slides">{slides}</div>
    <div class="wrap">
      <div class="hero__inner">
        <span class="eyebrow">Concesionarios oficiales Voge · Móstoles y Getafe</span>
        <h1><span class="hl">Voge Madrid Sur</span>, concesionarios oficiales en Móstoles y Getafe</h1>
        <p class="lead">Toda la gama Voge en Duomo Motor Bikes: scooters, naked y adventure para carnet B, A2 y A. Ven a verlas, pruébalas y llévate la tuya en Voge Móstoles o Voge Getafe.</p>
        <div class="hero__actions">
          <a class="btn btn--primary" href="#gama">Ver la gama Voge</a>
          <a class="btn btn--ghost-light" href="/solicitud-de-prueba/">Solicita una prueba</a>
        </div>
      </div>
    </div>
    <div class="wrap" style="position:relative"><div class="hero__dots" role="tablist" aria-label="Imágenes">{"".join(f'<button aria-label="Imagen {i+1}"{" class=\"is-active\"" if i == 0 else ""}></button>' for i in range(3))}</div></div>
  </section>

  <section class="trust" aria-label="Por qué Duomo">
    <div class="wrap">
      <div class="trust__item"><span class="trust__ico">{ICO["pin"]}</span><span><b>2 concesionarios</b>Móstoles y Getafe</span></div>
      <div class="trust__item"><span class="trust__ico">{ICO["wrench"]}</span><span><b>Taller propio</b>Posventa y recambios originales</span></div>
      <div class="trust__item"><span class="trust__ico">{ICO["bike"]}</span><span><b>+1.500 motos</b>Entregadas</span></div>
      <div class="trust__item"><span class="trust__ico">{ICO["star"]}</span><span><b>Desde 1960</b>Tradición familiar en automoción</span></div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <span class="eyebrow" style="display:flex;justify-content:center">Gama Voge</span>
      <h2>Una Voge para cada estilo</h2>
      <p class="sub">Scooters para el día a día, naked con carácter y adventure para salir del asfalto.</p>
      <div class="catgrid">{tiles}</div>
    </div>
  </section>

  <section class="section section--alt" id="gama">
    <div class="wrap">
      <h2>Toda la gama Voge</h2>
      <p class="sub">Visita toda la gama Voge en Móstoles y Getafe.</p>
      <div class="cat-bar" id="cat-bar" role="group" aria-label="Filtrar por categoría">{bar}</div>
      <div class="grid" id="models-grid">
{cards}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <span class="eyebrow" style="display:flex;justify-content:center">Destacadas</span>
      <h2>Las Voge del momento</h2>
      <div class="dests">{destacados}</div>
    </div>
  </section>

  <section class="section section--alt">
    <div class="wrap">
      <span class="eyebrow" style="display:flex;justify-content:center">Antes de elegir</span>
      <h2>¿Qué Voge puedo llevar con mi carnet?</h2>
      <p class="sub">Es la primera pregunta que nos hacéis. Aquí tienes la respuesta rápida; en el concesionario te lo confirmamos con tu carnet en la mano.</p>
      <div class="licenses">{lic_cards}</div>
    </div>
  </section>

  <section class="section section--dark">
    <div class="wrap">
      <span class="eyebrow" style="display:flex;justify-content:center">Duomo Motor Bikes</span>
      <h2>Siempre cerca de ti: <span class="hl">Móstoles y Getafe</span></h2>
      <p class="sub">Nuestra historia nace de una auténtica pasión por el mundo del motor y de una sólida tradición familiar en automoción que se remonta a 1960.</p>
      <div class="features">
        <div class="feature reveal"><div class="feature__ico">{ICO["wrench"]}</div><h3>Taller propio</h3><p>Servicio posventa con mecánicos especializados para que tu Voge esté siempre a punto.</p></div>
        <div class="feature reveal reveal-d1"><div class="feature__ico">{ICO["box"]}</div><h3>Recambios originales</h3><p>Recambios y accesorios originales Voge, sin esperas.</p></div>
        <div class="feature reveal reveal-d2"><div class="feature__ico">{ICO["euro"]}</div><h3>Financiación a medida</h3><p>Te preparamos la cuota que mejor encaja contigo y te damos las condiciones por escrito.</p></div>
        <div class="feature reveal reveal-d3"><div class="feature__ico">{ICO["key"]}</div><h3>Prueba sin compromiso</h3><p>Siéntate en ella, compárala con otras y pruébala antes de decidir.</p></div>
      </div>
      <div class="stats" style="margin-top:56px">
        <div class="stat reveal"><b>+<span data-count="20">20</span></b><span>Profesionales del motor</span></div>
        <div class="stat reveal reveal-d1"><b>+<span data-count="1500">1500</span></b><span>Motos entregadas</span></div>
        <div class="stat reveal reveal-d2"><b>+<span data-count="50">50</span></b><span>Años de experiencia en motos</span></div>
        <div class="stat reveal reveal-d3"><b>2</b><span>Concesionarios Voge: Móstoles y Getafe</span></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <span class="eyebrow" style="display:flex;justify-content:center">Junto a Alcorcón y en Getafe</span>
      <h2>Tu nueva Voge {XMADRID}</h2>
      <p class="sub">Voge Móstoles está <a href="/voge-x-madrid/" style="border-bottom:2px solid var(--yellow)">{XMADRID}</a> (Alcorcón) y Voge Getafe te pilla cerca si vives en Getafe, Leganés, Parla o Pinto.</p>
      <div class="areas" style="margin-bottom:40px">{"".join(f"<span>{z}</span>" for z in ZONAS)}</div>
      {visit_block("Nuestros concesionarios Voge")}
    </div>
  </section>

  <section class="section section--alt">
    <div class="wrap">
      <h2>Preguntas frecuentes</h2>
      <p class="sub">Lo que más nos preguntáis sobre Voge en el concesionario.</p>
      {faq_html(faqs)}
    </div>
  </section>
  {cta_band()}
"""
    write("/", head("Voge Madrid Sur · Concesionarios oficiales en Móstoles y Getafe",
                    f"Voge Madrid Sur: concesionarios oficiales Voge en Móstoles (junto al X-Madrid) y Getafe. {len(M)} modelos desde {eur(precio_min())}: SR4 Radar, 625DSX, 900DSX…",
                    "/", ld=ld, preload="/assets/img/hero/concesionario-voge-madrid-sur-1.webp") + header("modelos") + body + footer())

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
          <figure class="cpane__big"><img src="/{big["img"]}" alt="{e(fn)} color {e(col["name"].lower())} en Voge Madrid Sur" width="{big["w"]}" height="{big["h"]}" loading="lazy" decoding="async"></figure>
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
    manual = f'<a class="lnk" href="/{m["manual"]}" target="_blank" rel="noopener" download>Descargar el manual del usuario (PDF)</a>' if m["manual"] else f'<a class="lnk" href="/contacto/?modelo={qmodel}#solicita">Pídenos el manual y la ficha completa</a>'
    precio_txt = (f"{eur(m['price'])} (antes {eur(m['pvp'])})" if m["pvp"] else eur(m["price"]))
    faqs = [
        (f"¿Cuánto cuesta la {fn}?", f"La {e(fn)} tiene un precio de {precio_txt}, PVP con IVA incluido. Los gastos de matriculación y transporte y la financiación te los detallamos en el concesionario."),
        (f"¿Qué carnet necesito para la {fn}?", e(L["texto"])),
        (f"¿Dónde puedo ver y probar la {fn} en Madrid?", f"En nuestros concesionarios oficiales Voge: <b>Voge Móstoles</b> ({e(DIRECCION)}), {XMADRID}, y <b>Voge Getafe</b> ({e(DIR_GETAFE)}). Pide tu prueba en <a href=\"/solicitud-de-prueba/?modelo={qmodel}\">Solicitar prueba</a>."),
        (f"¿En qué colores está disponible la {fn}?", f"En {e(', '.join(col['name'] for col in m['colors']))}. Consúltanos la disponibilidad de cada color."),
    ]
    imgs = [SITE + "/" + m["main"]] + [SITE + "/" + col["imgs"][0]["img"] for col in m["colors"]]
    desc_txt = " ".join(p for b in m["blocks"] for p in b["p"])
    product = {"@context": "https://schema.org", "@type": ["Product", "Motorcycle"], "name": fn, "sku": m["slug"],
               "brand": {"@type": "Brand", "name": "Voge"}, "category": f"Motocicletas > {c['plural']}",
               "image": imgs, "description": desc_txt[:480],
               "color": [col["name"] for col in m["colors"]],
               "additionalProperty": [
                   {"@type": "PropertyValue", "name": "Cilindrada", "value": m["cc"], "unitText": "cc"},
                   {"@type": "PropertyValue", "name": "Potencia", "value": m["cv"], "unitText": "CV"},
                   {"@type": "PropertyValue", "name": "Par máximo", "value": m["nm"], "unitText": "Nm"},
                   {"@type": "PropertyValue", "name": "Carnet", "value": L["label"]}],
               "offers": {"@type": "Offer", "url": SITE + url, "priceCurrency": "EUR", "price": str(m["price"]),
                          "itemCondition": "https://schema.org/NewCondition", "availability": "https://schema.org/InStoreOnly",
                          "priceValidUntil": f"{datetime.date.today().year}-12-31", "seller": {"@id": DEALER_ID},
                          "areaServed": {"@type": "AdministrativeArea", "name": "Madrid Sur"}}}
    crumbs = [("Inicio", "/"), (c["plural"], cat_url(c)), (fn, url)]
    ld = [product, crumbs_ld(crumbs), faq_ld(faqs)]
    title = f"{fn}: precio, ficha y prueba en Madrid Sur"
    meta = f"{fn} por {eur(m['price'])} en Voge Madrid Sur: concesionarios oficiales en Móstoles y Getafe. {m['cc']} cc y {m['cv']} CV, {L['label'].replace('Carnet', 'carnet')}. Precio, colores y prueba."
    if len(meta) > 165: meta = f"{fn} por {eur(m['price'])} en Voge Móstoles y Voge Getafe. {m['cc']} cc, {m['cv']} CV, {L['label'].replace('Carnet', 'carnet')}. Precio, colores y prueba."
    body = f"""
  {crumbs_html(crumbs)}
  <section class="mhero">
    <div class="wrap mhero__grid">
      <div class="mhero__media">
        <img id="model-photo" class="is-first" src="/{m["main"]}" alt="{e(fn)} en Voge Madrid Sur (Móstoles y Getafe)" width="{m["mw"]}" height="{m["mh"]}" fetchpriority="high">
      </div>
      <div class="mhero__info">
        <div class="badges"><a class="badge badge--dark" href="{cat_url(c)}">{c["name"]}</a><span class="badge badge--line">{L["label"]}</span></div>
        <h1><small>Voge</small> {e(m["name"])}</h1>
        <p class="mhero__tagline">{e(tagline(m))}. Disponible en Duomo Motor Bikes, concesionarios oficiales Voge en Móstoles y Getafe.</p>
        <div class="pricebox"><span class="pricebox__now">{eur(m["price"])}</span>{f'<del>{eur(m["pvp"])}</del>' if m["pvp"] else ''}{saving}</div>
        <p class="price-note">{PRICE_NOTE}</p>
        <div class="kpis">
          <div class="kpi"><b>{m["cv"]} CV</b><span>Potencia</span></div>
          <div class="kpi"><b>{m["cc"]} cc</b><span>Cilindrada</span></div>
          <div class="kpi"><b>{m["nm"]} Nm</b><span>Par máx.</span></div>
          <div class="kpi"><b>{L["tag"]}</b><span>Carnet</span></div>
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
    <div class="wrap split">
      <div class="note-box reveal" style="margin:0"><b>¿Qué carnet necesito?</b><br>{e(L["texto"])}</div>
      <div class="info-cards reveal reveal-d1" style="grid-template-columns:1fr;margin-top:0">
        <div><h3>Descarga el manual del usuario</h3><p>De tu {e(m["name"])}.</p>{manual}</div>
        <div><h3>Pruébala en Móstoles o Getafe</h3><p>Ven al concesionario, siéntate en ella y sal a probarla. Te confirmamos día y hora.</p><a class="lnk" href="/solicitud-de-prueba/?modelo={qmodel}">Solicitar prueba</a></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <h2>Preguntas sobre la {e(fn)}</h2>
      <p class="sub">Las dudas más habituales antes de comprarla.</p>
      {faq_html(faqs)}
    </div>
  </section>

  <section class="section section--alt">
    <div class="wrap">
      <h2>Otros modelos que te pueden interesar</h2>
      <p class="sub">Compáralos en Voge Móstoles o Voge Getafe.</p>
      <div class="grid">
{rel_cards}
      </div>
    </div>
  </section>
  {cta_band(f"¿Te quedas con la {e(fn)}?", "Pídenos presupuesto con financiación a medida o reserva tu prueba en Móstoles o Getafe. Te respondemos lo antes posible.")}
"""
    write(url, head(title, meta, url, og_img="/" + m["og"], ld=ld, preload="/" + m["main"]) + header() + body + footer())

# ------------------------------------------------------------------ CATEGORÍA
def page_cat(c):
    ms = [m for m in M if m["cat"] == c["name"]]
    url = cat_url(c)
    cards = "\n".join(card(m, h="h2") for m in ms)
    lics = sorted({m["license"] for m in ms}, key=LIC_ORDER.index)
    lic_txt = "".join(f'<li><b>{LIC[k]["label"]}:</b> {", ".join(e(m["name"]) for m in ms if m["license"] == k)}.</li>' for k in lics)
    pmin = min(m["price"] for m in ms)
    nom = c["name"].lower()
    faqs = [
        (f"¿Cuánto cuesta una moto {nom} Voge?", f"En Duomo Motor Bikes tienes {len(ms)} modelos {nom} de Voge desde {eur(pmin)} (PVP con IVA). Consulta financiación en el concesionario."),
        (f"¿Dónde ver motos {nom} Voge en Madrid?", f"En nuestros concesionarios oficiales Voge de Móstoles ({e(DIRECCION)}) y Getafe ({e(DIR_GETAFE)}). Puedes <a href=\"/solicitud-de-prueba/\">pedir una prueba</a>."),
    ]
    crumbs = [("Inicio", "/"), (c["plural"] + " Voge", url)]
    ld = [crumbs_ld(crumbs), faq_ld(faqs), {"@context": "https://schema.org", "@type": "ItemList", "name": c["h1"], "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "url": SITE + model_url(m), "name": full(m)} for i, m in enumerate(ms)]}]
    others = "".join(f'<a class="btn btn--ghost" href="{cat_url(o)}">{o["plural"]}</a>' for o in CATS if o["slug"] != c["slug"])
    body = f"""
  <section class="hero hero--page">
    <div class="hero__bg"><img src="/assets/img/categorias/{c["img"]}" alt="" width="1200" height="900"></div>
    <div class="wrap"><div class="hero__inner">
      <span class="eyebrow">{len(ms)} modelos · desde {eur(pmin)}</span>
      <h1>{c["h1"]}</h1>
      <p class="lead">{c["corto"]}. Precios actualizados, carnet necesario y prueba en Voge Móstoles y Voge Getafe.</p>
      <div class="hero__actions"><a class="btn btn--primary" href="#modelos">Ver modelos</a><a class="btn btn--ghost-light" href="/solicitud-de-prueba/">Pedir prueba</a></div>
    </div></div>
  </section>
  {crumbs_html(crumbs)}
  <section class="section" style="padding-top:36px">
    <div class="wrap split">
      <div class="prose reveal">{"".join(f"<p>{p}</p>" for p in c["intro"])}</div>
      <div class="note-box reveal reveal-d1" style="margin:0"><b>Carnet necesario</b><ul style="margin:8px 0 0 18px">{lic_txt}</ul></div>
    </div>
  </section>
  <section class="section section--alt" id="modelos">
    <div class="wrap">
      <div class="grid">
{cards}
      </div>
      <p class="promo-legal">{PRICE_NOTE}</p>
    </div>
  </section>
  <section class="section">
    <div class="wrap">
      <h2>Preguntas frecuentes</h2>
      <p class="sub">Sobre las motos {nom} de Voge.</p>
      {faq_html(faqs)}
      <div class="hero__actions" style="justify-content:center;margin-top:40px">{others}</div>
    </div>
  </section>
  {cta_band()}
"""
    write(url, head(c["title"], c["meta"], url, ld=ld) + header("modelos") + body + footer())

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
              <label for="carnet">¿Qué carnet tienes?*</label>
              <select id="carnet" name="carnet" required>
                <option value="">Selecciona…</option>
                <option>Carnet B con más de 3 años</option>
                <option>A1</option><option>A2</option><option>A</option>
                <option>Aún no tengo carnet de moto</option>
              </select>
            </div>
            <div class="field">
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
    tel_m = f'<a href="tel:{NEGOCIO["telIntl"]}">{NEGOCIO["tel"]}</a>' + (f' · Taller: <a href="tel:{NEGOCIO["telTallerIntl"]}">{NEGOCIO["telTaller"]}</a>' if taller else "")
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
    if tipo == "taller": return page_taller()
    prueba = tipo == "prueba"
    url = "/solicitud-de-prueba/" if prueba else "/contacto/"
    h1 = "Prueba tu nueva Voge" if prueba else "Contáctanos"
    lead = ("Elige el modelo, dinos qué carnet tienes y en qué concesionario prefieres probarla (Móstoles o Getafe). Te confirmamos día y hora. Recuerda traer tu carnet y tu equipamiento."
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
    title = "Prueba una moto Voge en Móstoles o Getafe · Voge Madrid Sur" if prueba else "Contacto · Voge Madrid Sur (Móstoles y Getafe)"
    meta = ("Reserva una prueba de cualquier moto Voge (SR4 Radar, 525DSX, 625DSX, 900DSX…) en Voge Móstoles o Voge Getafe. Te confirmamos día y hora."
            if prueba else f"Contacta con Voge Madrid Sur: Voge Móstoles ({NEGOCIO['tel']}) y Voge Getafe ({GETAFE['tel']}). Formulario, direcciones y horario.")
    write(url, head(title, meta, url, ld=[crumbs_ld(crumbs), contact_ld, DEALER, DEALER_GETAFE]) + header("contacto" if not prueba else "") + body + footer())

# ------------------------------------------------------------------ TALLER
def page_taller():
    url = "/taller-voge/"
    crumbs = [("Inicio", "/"), ("Taller Voge", url)]
    faqs = [
        ("¿Dónde hay un taller para motos Voge en Madrid Sur?", f"En Voge Madrid Sur (Duomo Motor Bikes), con taller propio en {e(DIRECCION)}. Damos servicio a motoristas de Móstoles, Getafe, Alcorcón, Fuenlabrada, Leganés y el resto del sur de Madrid."),
        ("¿Puedo llevar mi Voge aunque no la comprara en Duomo?", "Sí. Atendemos cualquier Voge, la hayas comprado donde la hayas comprado."),
        ("¿Cómo pido cita en el taller?", f"Rellena el formulario de esta página o llama al taller al <a href=\"tel:{NEGOCIO['telTallerIntl']}\">{NEGOCIO['telTaller']}</a>. Te confirmamos el día."),
        ("¿Usáis recambios originales?", "Sí, trabajamos con recambios originales Voge."),
    ]
    service = {"@context": "https://schema.org", "@type": "AutoRepair", "@id": SITE + "/taller-voge/#taller",
               "name": "Taller Voge Madrid Sur · Duomo Motor Bikes", "url": SITE + url, "telephone": NEGOCIO["telTallerIntl"],
               "address": DEALER["address"], "openingHoursSpecification": HORAS,
               "areaServed": DEALER["areaServed"], "brand": {"@type": "Brand", "name": "Voge"}, "parentOrganization": {"@id": DEALER_ID}}
    servicios = [("Revisiones de mantenimiento", "Siguiendo el plan de mantenimiento que marca Voge para cada modelo."),
                 ("Puesta a punto de temporada", "Antes del verano o del invierno: revisamos niveles, frenos, neumáticos, luces y batería."),
                 ("Cambio de aceite y filtros", "Con los aceites y filtros que marca el fabricante para cada motor."),
                 ("Frenos", "Revisión y cambio de pastillas, discos y líquido de frenos."),
                 ("Neumáticos", "Montaje y equilibrado de neumáticos."),
                 ("Accesorios originales", "Instalamos maletas, baúles, pantallas, protecciones y el resto de accesorios originales.")]
    cards = "".join(f'<div class="equip__item reveal"><div><h3>{t}</h3><p>{d}</p></div></div>' for t, d in servicios)
    body = f"""
  <section class="hero hero--page">
    <div class="hero__bg"><img src="/assets/img/hero/concesionario-voge-madrid-sur-2.webp" alt="" width="1366" height="911"></div>
    <div class="wrap"><div class="hero__inner">
      <span class="eyebrow">Servicio posventa · Móstoles</span>
      <h1>Taller Voge en Madrid Sur</h1>
      <p class="lead">Taller propio, servicio posventa y recambios originales para tu Voge, a un paso de Alcorcón, Fuenlabrada, Getafe y Leganés.</p>
      <div class="hero__actions"><a class="btn btn--primary" href="#cita">Pedir cita</a><a class="btn btn--ghost-light" href="tel:{NEGOCIO["telTallerIntl"]}">Llamar al taller</a></div>
    </div></div>
  </section>
  {crumbs_html(crumbs)}
  <section class="section" style="padding-top:36px">
    <div class="wrap">
      <h2>Qué hacemos en el taller</h2>
      <p class="sub">Un equipo humano especializado y recambios originales. Tu Voge, en manos de quien la conoce.</p>
      <div class="equip">{cards}</div>
    </div>
  </section>
  <section class="section section--alt" id="cita">
    <div class="wrap">
      <div class="contact-grid">
        <div class="reveal">
          <span class="eyebrow">Cita de taller</span>
          <h2>Pide cita para tu Voge</h2>
          {form("taller")}
        </div>
        {info_card(taller=True)}
      </div>
    </div>
  </section>
  <section class="section">
    <div class="wrap">
      <h2>Preguntas frecuentes del taller</h2>
      <p class="sub">Lo que más nos preguntáis antes de traer la moto.</p>
      {faq_html(faqs)}
    </div>
  </section>
"""
    write(url, head("Taller Voge en Madrid Sur · Móstoles",
                    "Taller para motos Voge en Móstoles: mantenimiento, revisiones, neumáticos y recambios originales. Cerca de Alcorcón, Fuenlabrada, Getafe y Leganés.",
                    url, ld=[service, crumbs_ld(crumbs), faq_ld(faqs)]) + header("taller") + body + footer())

# ------------------------------------------------------------------ CONCESIONARIOS (página del WordPress)
def page_concesionarios():
    url = "/concesionario-voge-madrid-sur/"
    crumbs = [("Inicio", "/"), ("Concesionarios Voge", url)]
    faqs = [
        ("¿Dónde están los concesionarios Voge de Duomo?", f"Voge Móstoles: {e(DIRECCION)}, teléfono {NEGOCIO['tel']}. Voge Getafe: {e(DIR_GETAFE)}, teléfono {GETAFE['tel']}."),
        ("¿Qué horario tienen?", "Los dos abren de lunes a viernes de 10:00 a 14:00 y de 16:00 a 19:30, y los sábados de 10:00 a 14:00. Domingos cerrado."),
        ("¿Tenéis las mismas motos en los dos?", "Tenemos toda la gama Voge. Si buscas un modelo o color concreto, escríbenos y te decimos dónde está disponible para verla o probarla."),
    ]
    body = f"""
  <section class="hero hero--page">
    <div class="hero__bg"><img src="/assets/img/hero/concesionario-voge-madrid-sur-3.webp" alt="" width="1366" height="911"></div>
    <div class="wrap"><div class="hero__inner">
      <span class="eyebrow">Siempre cerca de ti</span>
      <h1>Voge Madrid Sur: tu concesionario de confianza en Móstoles y Getafe</h1>
      <p class="lead">Disponemos de taller propio, servicio postventa, recambios originales y un equipo humano especializado que garantiza una atención integral y una experiencia completa, cómoda y segura antes, durante y después de tu compra.</p>
      <div class="hero__actions"><a class="btn btn--primary" href="/voge-mostoles/">Voge Móstoles</a><a class="btn btn--ghost-light" href="/voge-getafe/">Voge Getafe</a></div>
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
  <section class="section section--alt"><div class="wrap">{visit_block("Elige tu concesionario Voge")}</div></section>
  <section class="section">
    <div class="wrap">
      <h2>Preguntas frecuentes</h2>
      <p class="sub">Sobre nuestros concesionarios Voge.</p>
      {faq_html(faqs)}
    </div>
  </section>
  {cta_band("Prueba la tuya", "Reserva tu prueba en Voge Móstoles o Voge Getafe y te confirmamos día y hora.")}
"""
    write(url, head("Concesionarios Voge en Móstoles y Getafe · Voge Madrid Sur",
                    "Voge Madrid Sur: concesionarios oficiales Voge en Móstoles y Getafe con taller propio, posventa y recambios originales. Direcciones, horario y teléfonos.",
                    url, ld=[DEALER, DEALER_GETAFE, crumbs_ld(crumbs), faq_ld(faqs)]) + header("concesionario") + body + footer())

# ------------------------------------------------------------------ TIENDAS
def page_tienda(cual):
    mo = cual == "mostoles"
    url = "/voge-mostoles/" if mo else "/voge-getafe/"
    nombre = "Voge Móstoles" if mo else "Voge Getafe"
    d = DIRECCION if mo else DIR_GETAFE
    tel, telI = (NEGOCIO["tel"], NEGOCIO["telIntl"]) if mo else (GETAFE["tel"], GETAFE["telIntl"])
    dir_ = MAPS_DIR if mo else GETAFE["dir"]
    crumbs = [("Inicio", "/"), ("Concesionarios", "/concesionario-voge-madrid-sur/"), (nombre, url)]
    cerca = "Alcorcón, Fuenlabrada, Villaviciosa de Odón, Arroyomolinos y Navalcarnero" if mo else "Leganés, Parla, Pinto, Fuenlabrada y el sur de Madrid capital"
    tops = [mm(s) for s in (["sr4-radar", "525dsx", "625dsx", "sr1", "300-rally", "900dsx"] if mo else ["sr4-radar", "900dsx", "sr16", "625r", "525dsx", "sr3"])]
    faqs = [
        (f"¿Dónde está {nombre}?", f"En {e(d)}. Es un concesionario oficial Voge de Duomo Motor Bikes. <a href=\"{dir_}\" target=\"_blank\" rel=\"noopener\">Cómo llegar</a>."),
        (f"¿Qué horario tiene {nombre}?", "Lunes a viernes de 10:00 a 14:00 y de 16:00 a 19:30. Sábados de 10:00 a 14:00. Domingo cerrado."),
        (f"¿Cuál es el teléfono de {nombre}?", f"<a href=\"tel:{telI}\">{tel}</a>" + (f". Taller: <a href=\"tel:{NEGOCIO['telTallerIntl']}\">{NEGOCIO['telTaller']}</a>." if mo else ".") + " También puedes escribirnos desde el <a href=\"/contacto/\">formulario de contacto</a>."),
        (f"¿Puedo probar una Voge en {'Móstoles' if mo else 'Getafe'}?", "Sí. Pide tu prueba en <a href=\"/solicitud-de-prueba/\">Solicitar prueba</a>, elige el modelo y el concesionario, y te confirmamos día y hora."),
        ("¿Trabajáis otras marcas?", "Sí. Duomo Motor Bikes trabaja también con otras marcas, como Zontes, Royal Enfield y Suzuki. Pregúntanos qué tenemos disponible en cada concesionario."),
    ]
    if mo: faqs.insert(1, ("¿Está cerca del X-Madrid?", f"Sí, Voge Móstoles está {XMADRID}, el centro comercial de Alcorcón."))
    otra = ("Voge Getafe", "/voge-getafe/", DIR_GETAFE) if mo else ("Voge Móstoles", "/voge-mostoles/", DIRECCION)
    body = f"""
  <section class="hero hero--page">
    <div class="hero__bg"><img src="/assets/img/hero/concesionario-voge-madrid-sur-{1 if mo else 2}.webp" alt="" width="1366" height="911"></div>
    <div class="wrap"><div class="hero__inner">
      <span class="eyebrow">Concesionario oficial Voge · Duomo Motor Bikes</span>
      <h1>Concesionario Voge en {'Móstoles' if mo else 'Getafe'}</h1>
      <p class="lead">Toda la gama Voge, financiación a medida y servicio posventa en {e(d)}.{(' ' + XMADRID[0].upper() + XMADRID[1:] + '.') if mo else ''} Cerca de {cerca}.</p>
      <div class="hero__actions"><a class="btn btn--primary" href="{dir_}" target="_blank" rel="noopener">Cómo llegar</a><a class="btn btn--ghost-light" href="/solicitud-de-prueba/">Pedir prueba</a></div>
    </div></div>
  </section>
  {crumbs_html(crumbs)}
  <section class="section" style="padding-top:36px">
    <div class="wrap">
      <div class="info-cards" style="margin-top:0">
        <div class="reveal"><h3>Dirección</h3><p>{e(d)}</p><a class="lnk" href="{dir_}" target="_blank" rel="noopener">Abrir en Google Maps</a></div>
        <div class="reveal reveal-d1"><h3>Horario</h3><p>{e(NEGOCIO["horario"])}</p><a class="lnk" href="/solicitud-de-prueba/">Reservar prueba</a></div>
        <div class="reveal reveal-d2"><h3>Teléfono</h3><p><a href="tel:{telI}">{tel}</a>{f'<br>Taller: <a href="tel:{NEGOCIO["telTallerIntl"]}">{NEGOCIO["telTaller"]}</a>' if mo else ''}</p><a class="lnk" href="/contacto/">Escribirnos</a></div>
      </div>
    </div>
  </section>
  <section class="section section--alt">
    <div class="wrap">
      <h2>Voge en {'Móstoles' if mo else 'Getafe'}: algunos de los modelos más buscados</h2>
      <p class="sub">Toda la gama está disponible para verla y probarla.</p>
      <div class="grid">{"".join(card(m) for m in tops)}</div>
      <div class="hero__actions" style="justify-content:center;margin-top:30px"><a class="btn btn--dark" href="/#gama">Ver los {len(M)} modelos</a></div>
    </div>
  </section>
  {bloque_confianza()}
  <section class="section"><div class="wrap">{visit_block(nombre, "mostoles" if mo else "getafe")}</div></section>
  <section class="section section--alt">
    <div class="wrap">
      <p class="sub" style="margin-bottom:0">¿Te pilla mejor el otro? <a class="lnk" href="{otra[1]}">{otra[0]}</a> está en {e(otra[2])}.</p>
    </div>
  </section>
  {bloque_blog(["Móstoles", "Alcorcón", "X-Madrid"] if mo else ["Getafe", "Leganés"])}
  <section class="section">
    <div class="wrap">
      <h2>Preguntas frecuentes</h2>
      <p class="sub">Sobre {nombre}.</p>
      {faq_html(faqs)}
    </div>
  </section>
  {cta_band()}
"""
    title = f"{nombre} · Concesionario oficial Voge" + (" junto al X-Madrid" if mo else " en Getafe")
    meta = f"{nombre}: concesionario oficial Voge en {d.split(',')[0]}. Horario, teléfono {tel}, cómo llegar y prueba. Cerca de {cerca.split(',')[0]} y {cerca.split(',')[1].strip()}."
    write(url, head(title, meta, url, ld=[DEALER if mo else DEALER_GETAFE, crumbs_ld(crumbs), faq_ld(faqs)]) + header("concesionario") + body + footer())

# ------------------------------------------------------------------ A2
def page_a2():
    url = "/motos-voge-a2/"
    crumbs = [("Inicio", "/"), ("Motos Voge A2", url)]
    a2 = [m for m in M if m["license"] == "A2"]; lim = [m for m in M if m["license"] == "A-A2"]
    barata = min(a2, key=lambda x: x["price"])
    faqs = [
        ("¿Qué motos Voge puedo llevar con el carnet A2?", f"Sin limitar: {', '.join(e(m['name']) for m in a2)}. Y la naked 625R en su versión limitada a 35 kW."),
        ("¿Cuál es la Voge A2 más barata?", f"La <a href=\"{model_url(barata)}\">Voge {e(barata['name'])}</a>, por {eur(barata['price'])} (PVP con IVA)."),
        ("¿Qué Voge A2 me recomendáis para viajar?", "Si prefieres scooter, la <a href=\"/modelo/sr450x/\">SR450X</a> o la <a href=\"/modelo/sr4-radar/\">SR4 Radar</a>. Si prefieres moto trail, la <a href=\"/modelo/525dsx/\">525DSX</a>, con 47,6 CV, justo en el límite del A2."),
        ("¿Dónde probar una Voge A2 en Madrid Sur?", f"En Voge Móstoles ({e(DIRECCION)}) o en Voge Getafe ({e(DIR_GETAFE)}). <a href=\"/solicitud-de-prueba/\">Pide tu prueba</a>."),
    ]
    body = f"""
  <section class="hero hero--page">
    <div class="hero__bg"><img src="/assets/img/categorias/motos-voge-adventure.webp" alt="" width="1200" height="900"></div>
    <div class="wrap"><div class="hero__inner">
      <span class="eyebrow">{len(a2)} modelos sin limitar · desde {eur(barata["price"])}</span>
      <h1>Motos Voge para carnet A2</h1>
      <p class="lead">Scooters y trail que puedes llevar con el A2 tal cual salen de fábrica, y la 625R en versión de 35 kW. Pruébalas en Voge Móstoles o Voge Getafe.</p>
      <div class="hero__actions"><a class="btn btn--primary" href="#a2">Ver modelos A2</a><a class="btn btn--ghost-light" href="/solicitud-de-prueba/">Pedir prueba</a></div>
    </div></div>
  </section>
  {crumbs_html(crumbs)}
  <section class="section" style="padding-top:36px">
    <div class="wrap split">
      <div class="prose reveal">
        <h2>Las Voge que puedes llevar con el A2</h2>
        <p>El carnet A2 permite motos de hasta <b>35 kW</b> (47,6 CV). En Voge tienes opciones para todos los usos: los scooters <a href="/modelo/sr3/">SR3</a>, <a href="/modelo/sr4-radar/">SR4 Radar</a> y <a href="/modelo/sr450x/">SR450X</a> para moverte a diario y viajar, y las trail <a href="/modelo/300-rally/">300 Rally</a> y <a href="/modelo/525dsx/">525DSX</a> para salir del asfalto.</p>
        <p>Si lo tuyo son las naked, la <a href="/modelo/625r/">625R</a> bicilíndrica de 64 CV también está disponible en versión limitada a 35 kW para el A2.</p>
      </div>
      <div class="note-box reveal reveal-d1" style="margin:0"><b>Con el A2 puedes llevar</b><ul style="margin:8px 0 0 18px"><li>Motos de hasta 35 kW (47,6 CV).</li><li>Relación peso/potencia de hasta 0,2 kW/kg.</li><li>Si la moto está limitada, su potencia original no puede superar el doble (70 kW).</li></ul></div>
    </div>
  </section>
  <section class="section section--alt" id="a2">
    <div class="wrap">
      <h2>Voge A2 sin limitar</h2>
      <p class="sub">Se llevan con el A2 tal cual salen de fábrica.</p>
      <div class="grid">
{chr(10).join(card(m) for m in a2)}
      </div>
    </div>
  </section>
  <section class="section">
    <div class="wrap">
      <h2>Voge en versión A2</h2>
      <p class="sub">Con versión limitada a 35 kW para el carnet A2.</p>
      <div class="grid">
{chr(10).join(card(m) for m in lim)}
      </div>
      <p class="promo-legal">{PRICE_NOTE}</p>
    </div>
  </section>
  <section class="section section--alt">
    <div class="wrap">
      <h2>Preguntas frecuentes</h2>
      <p class="sub">Sobre las Voge para el carnet A2.</p>
      {faq_html(faqs)}
    </div>
  </section>
  {cta_band()}
"""
    write(url, head("Motos Voge para carnet A2 en Madrid Sur",
                    f"Motos Voge para carnet A2 en Móstoles y Getafe: SR3, SR4 Radar, SR450X, 300 Rally y 525DSX desde {eur(barata['price'])}, y la 625R en versión 35 kW. Precios y prueba.",
                    url, ld=[crumbs_ld(crumbs), faq_ld(faqs), {"@context": "https://schema.org", "@type": "ItemList", "name": "Motos Voge para carnet A2", "itemListElement": [
                        {"@type": "ListItem", "position": i + 1, "url": SITE + model_url(m), "name": full(m)} for i, m in enumerate(a2 + lim)]}]) + header("modelos") + body + footer())

# ------------------------------------------------------------------ 125
def page_125():
    url = "/motos-125-carnet-coche/"
    crumbs = [("Inicio", "/"), ("Motos 125 con carnet de coche", url)]
    ms = sorted([m for m in M if m["license"] == "A1"], key=lambda x: x["price"])
    faqs = [
        ("¿Puedo llevar una moto de 125 con el carnet de coche?", "Sí. En España, con el carnet B y más de tres años de antigüedad puedes conducir motos de hasta 125 cc, 11 kW (unos 15 CV) y una relación peso/potencia de 0,1 kW/kg. Ese permiso solo vale para circular por España."),
        ("¿Vale para motos de marchas o solo para scooters?", "Para las dos: con el carnet B de más de tres años puedes llevar tanto scooters automáticos como motos de marchas de 125 cc que cumplan esos límites, como las naked <a href=\"/modelo/125r/\">125R</a> y <a href=\"/modelo/125rs/\">125RS</a>."),
        ("¿Cuál es la Voge 125 más barata?", f"La <a href=\"{model_url(ms[0])}\">Voge {e(ms[0]['name'])}</a>, por {eur(ms[0]['price'])} (PVP con IVA)."),
        ("¿Qué Voge 125 me recomendáis para ir a trabajar a Madrid?", "Un scooter: la <a href=\"/modelo/sr16/\">SR16</a> o la <a href=\"/modelo/sr16-air/\">SR16 Air</a> por ligereza y precio, la <a href=\"/modelo/sr1/\">SR1</a> si buscas más confort, o la <a href=\"/modelo/sr1-adv/\">SR1 ADV</a> si quieres un aire más aventurero."),
        ("¿Dónde probar una Voge 125 en Madrid Sur?", f"En Voge Móstoles ({e(DIRECCION)}), {XMADRID}, o en Voge Getafe ({e(DIR_GETAFE)}). <a href=\"/solicitud-de-prueba/\">Pide tu prueba</a>."),
    ]
    body = f"""
  <section class="hero hero--page">
    <div class="hero__bg"><img src="/assets/img/categorias/motos-voge-scooters.webp" alt="" width="1200" height="900"></div>
    <div class="wrap"><div class="hero__inner">
      <span class="eyebrow">{len(ms)} modelos · desde {eur(ms[0]["price"])}</span>
      <h1>Motos 125 con carnet de coche</h1>
      <p class="lead">Todas las Voge de 125 cc que puedes llevar con el carnet B de más de tres años: scooters y naked. Pruébalas en Voge Móstoles o Voge Getafe.</p>
      <div class="hero__actions"><a class="btn btn--primary" href="#modelos-125">Ver las 125</a><a class="btn btn--ghost-light" href="/solicitud-de-prueba/">Pedir prueba</a></div>
    </div></div>
  </section>
  {crumbs_html(crumbs)}
  <section class="section" style="padding-top:36px">
    <div class="wrap split">
      <div class="prose reveal">
        <h2>Deja el coche: muévete por Madrid en una 125</h2>
        <p>Si vives en Madrid Sur y vas a trabajar a Madrid, una 125 te ahorra atascos y vueltas para aparcar. Con el <b>carnet de coche de más de tres años</b> no necesitas sacarte otro permiso: puedes llevar cualquier moto de 125 cc de hasta 11 kW.</p>
        <p>En Voge tienes cuatro scooters (<a href="/modelo/sr16-air/">SR16 Air</a>, <a href="/modelo/sr16/">SR16</a>, <a href="/modelo/sr1/">SR1</a> y <a href="/modelo/sr1-adv/">SR1 ADV</a>) y dos naked de marchas (<a href="/modelo/125r/">125R</a> y <a href="/modelo/125rs/">125RS</a>).</p>
      </div>
      <div class="note-box reveal reveal-d1" style="margin:0"><b>Con el carnet B (+3 años) puedes llevar</b><ul style="margin:8px 0 0 18px"><li>Motos de hasta 125 cc.</li><li>Potencia máxima de 11 kW (unos 15 CV).</li><li>Relación peso/potencia de hasta 0,1 kW/kg.</li><li>Solo para circular por España.</li></ul></div>
    </div>
  </section>
  <section class="section section--alt" id="modelos-125">
    <div class="wrap">
      <h2>Voge 125 para carnet B</h2>
      <p class="sub">Ordenadas de menor a mayor precio.</p>
      <div class="grid">
{chr(10).join(card(m) for m in ms)}
      </div>
      <p class="promo-legal">{PRICE_NOTE}</p>
    </div>
  </section>
  {bloque_confianza()}
  {bloque_blog(["125", "carnet"])}
  <section class="section">
    <div class="wrap">
      <h2>Preguntas frecuentes</h2>
      <p class="sub">Sobre las 125 y el carnet de coche.</p>
      {faq_html(faqs)}
    </div>
  </section>
  {cta_band()}
"""
    ld = [crumbs_ld(crumbs), faq_ld(faqs), {"@context": "https://schema.org", "@type": "ItemList", "name": "Motos Voge 125 para carnet de coche",
          "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE + model_url(m), "name": full(m)} for i, m in enumerate(ms)]}]
    write(url, head("Motos 125 con carnet de coche · Voge en Madrid Sur",
                    f"Motos de 125 cc que puedes llevar con el carnet B (+3 años): {len(ms)} Voge desde {eur(ms[0]['price'])}. Scooters y naked. Prueba en Voge Móstoles o Voge Getafe.",
                    url, ld=ld) + header("modelos") + body + footer())

# ------------------------------------------------------------------ BLOQUES COMUNES
def posts_relacionados_ciudad(nombres, n=3):
    ps = sorted(blog_posts(), key=lambda p: p["fecha"], reverse=True)
    hit = [p for p in ps if any(x.lower() in (p["titulo"] + " " + p.get("descripcion", "") + " " + p.get("keyword", "")).lower() for x in nombres)]
    resto = [p for p in ps if p not in hit]
    return (hit + resto)[:n]

def bloque_blog(nombres, titulo="Del blog de Voge Madrid Sur"):
    ps = posts_relacionados_ciudad(nombres)
    if not ps: return ""
    return f"""<section class="section section--alt">
    <div class="wrap">
      <h2>{titulo}</h2>
      <p class="sub">Rutas, consejos y novedades para motoristas de la zona.</p>
      <div class="bgrid">{"".join(bcard_html(p) for p in ps)}</div>
      <div class="hero__actions" style="justify-content:center;margin-top:30px"><a class="btn btn--dark" href="/blog/">Ver todos los artículos</a></div>
    </div>
  </section>"""

def bloque_confianza():
    return f"""<section class="section">
    <div class="wrap split">
      <div class="prose reveal">
        <h2>Por qué comprar tu Voge en Duomo Motor Bikes</h2>
        <p>{e(CREDENCIALES)}</p>
        <ul>
          <li><b>Concesionario oficial Voge</b> en Móstoles y en Getafe.</li>
          <li><b>Toda la gama Voge</b>: siéntate en las motos y compáralas una al lado de la otra.</li>
          <li><b>Prueba sin compromiso</b> y financiación a medida.</li>
          <li><b>Taller propio</b>, servicio posventa y recambios originales.</li>
        </ul>
      </div>
      <div class="note-box reveal reveal-d1" style="margin:0">
        <b>Voge Móstoles</b><br>{e(DIRECCION)}<br><a href="tel:{NEGOCIO["telIntl"]}">{NEGOCIO["tel"]}</a> · Taller: <a href="tel:{NEGOCIO["telTallerIntl"]}">{NEGOCIO["telTaller"]}</a><br><br>
        <b>Voge Getafe</b><br>{e(DIR_GETAFE)}<br><a href="tel:{GETAFE["telIntl"]}">{GETAFE["tel"]}</a><br><br>
        <b>Horario:</b> {e(NEGOCIO["horario"])}
      </div>
    </div>
  </section>"""

def note_tienda(t):
    if t == "getafe":
        return f"""<b>Voge Getafe</b><br>{e(DIR_GETAFE)}<br><br><b>Horario:</b> {e(NEGOCIO["horario"])}<br><br><b>Teléfono:</b> <a href="tel:{GETAFE["telIntl"]}">{GETAFE["tel"]}</a>"""
    if t == "mostoles":
        return f"""<b>Voge Móstoles</b><br>{e(DIRECCION)}<br><br><b>Horario:</b> {e(NEGOCIO["horario"])}<br><br><b>Ventas:</b> <a href="tel:{NEGOCIO["telIntl"]}">{NEGOCIO["tel"]}</a> · <b>Taller:</b> <a href="tel:{NEGOCIO["telTallerIntl"]}">{NEGOCIO["telTaller"]}</a>"""
    return f"""<b>Voge Móstoles</b><br>{e(DIRECCION)}<br><a href="tel:{NEGOCIO["telIntl"]}">{NEGOCIO["tel"]}</a><br><br><b>Voge Getafe</b><br>{e(DIR_GETAFE)}<br><a href="tel:{GETAFE["telIntl"]}">{GETAFE["tel"]}</a><br><br><b>Horario:</b> {e(NEGOCIO["horario"])}"""

# ------------------------------------------------------------------ ZONAS
ZONAS_PAG = [
    {"slug": "voge-x-madrid", "ciudad": "el X-Madrid", "corto": "X-Madrid", "tienda": "mostoles", "nombres": ["X-Madrid", "Alcorcón"],
     "title": "Voge X-Madrid · Concesionario a 5 minutos, en Móstoles",
     "meta": f"¿Buscas Voge cerca del X-Madrid? Voge Móstoles está {XMADRID} de Alcorcón: toda la gama Voge, prueba sin compromiso, financiación y taller propio.",
     "eyebrow": "X-Madrid · Alcorcón · Madrid Sur", "h1": f"Tu nueva Voge {XMADRID}",
     "lead": "Voge Móstoles es el concesionario oficial Voge más cercano al X-Madrid de Alcorcón: toda la gama, prueba sin compromiso y taller propio.",
     "hero": "concesionario-voge-madrid-sur-1.webp",
     "intro": [f"Si vives o trabajas cerca del <b>X-Madrid</b>, en Alcorcón, tienes tu concesionario oficial Voge {XMADRID}: <b>Voge Móstoles</b>, de Duomo Motor Bikes. Aquí puedes ver la gama Voge, sentarte en las motos y probar la que te interesa antes de decidir.",
               "Desde los scooters de 125 cc como la <a href=\"/modelo/sr1/\">SR1</a>, que se llevan con el carnet de coche, hasta la <a href=\"/modelo/sr4-radar/\">SR4 Radar</a> para el A2 o las trail <a href=\"/modelo/625dsx/\">625DSX</a> y <a href=\"/modelo/900dsx/\">900DSX</a>."],
     "llegar": "Desde el X-Madrid toma la M-506 en dirección a Móstoles y en unos minutos estás en la Calle Juan de la Cierva.",
     "perfiles": [("Las más buscadas", ["sr4-radar", "sr1", "525dsx", "625dsx", "900dsx", "125r"])],
     "faqs": [("¿Hay un concesionario Voge cerca del X-Madrid?", f"Sí. Voge Móstoles (Duomo Motor Bikes) está {XMADRID} de Alcorcón, en {e(DIRECCION)}. No hay tienda Voge dentro del centro comercial."),
              ("¿Cómo llego desde el X-Madrid?", f"Abre la ruta en <a href=\"{MAPS_DIR}\" target=\"_blank\" rel=\"noopener\">Google Maps</a> y te lleva directo a Calle Juan de la Cierva 7-9, en Móstoles."),
              ("¿Puedo probar una Voge si vengo desde Alcorcón?", "Claro. Pide tu prueba en <a href=\"/solicitud-de-prueba/\">Solicitar prueba</a>, elige el modelo y te confirmamos día y hora."),
              ("¿Qué horario tenéis?", f"{e(NEGOCIO['horario'])}.")]},
    {"slug": "voge-alcorcon", "ciudad": "Alcorcón", "corto": "Alcorcón", "tienda": "mostoles", "nombres": ["Alcorcón", "X-Madrid"],
     "title": "Voge Alcorcón · Concesionario oficial a 5 min, en Móstoles",
     "meta": "¿Buscas Voge en Alcorcón? Voge Móstoles está a 5 minutos del X-Madrid: toda la gama Voge, prueba sin compromiso, financiación y taller propio.",
     "eyebrow": "Alcorcón · X-Madrid · Parque Oeste", "h1": "Concesionario Voge cerca de Alcorcón",
     "lead": "Alcorcón y Móstoles son vecinos: desde el X-Madrid tienes tu concesionario oficial Voge en 5 minutos. Toda la gama, prueba y taller propio.",
     "hero": "concesionario-voge-madrid-sur-2.webp",
     "intro": ["Si vives en <b>Alcorcón</b>, no necesitas cruzar Madrid para ver una Voge. Voge Móstoles está a 5 minutos del <b>X-Madrid</b>, y aquí tienes toda la gama: scooters, naked y adventure.",
               "Si vas a trabajar a Madrid por la A-5, una moto te libra de atascos y de buscar aparcamiento. Con el carnet de coche de más de tres años, los scooters <a href=\"/modelo/sr16/\">SR16</a> y <a href=\"/modelo/sr1/\">SR1</a>; con el A2, la <a href=\"/modelo/sr4-radar/\">SR4 Radar</a>."],
     "llegar": "Desde el centro de Alcorcón o desde el X-Madrid, toma la M-506 en dirección a Móstoles y en unos minutos estás en la Calle Juan de la Cierva.",
     "perfiles": [("Para ir a trabajar a Madrid", ["sr16", "sr1", "sr4-radar"]), ("Para escapadas de fin de semana", ["300-rally", "525dsx", "625dsx"])],
     "faqs": [("¿Hay concesionario Voge en Alcorcón?", f"El concesionario oficial Voge más cercano a Alcorcón es Voge Móstoles (Duomo Motor Bikes), en {e(DIRECCION)}, a 5 minutos del X-Madrid. No tenemos tienda dentro de Alcorcón: estamos en el municipio de al lado."),
              ("¿Qué Voge me recomendáis para ir de Alcorcón a Madrid?", "Con el carnet de coche de más de tres años, un scooter de 125 como la <a href=\"/modelo/sr1/\">SR1</a>. Si tienes el A2 y haces muchos kilómetros por autovía, la <a href=\"/modelo/sr4-radar/\">SR4 Radar</a> o la <a href=\"/modelo/sr450x/\">SR450X</a>."),
              ("¿Puedo llevar mi Voge al taller si vivo en Alcorcón?", "Sí. Nuestro <a href=\"/taller-voge/\">taller</a> está en Móstoles, con servicio posventa y recambios originales."),
              ("¿Qué horario tenéis?", f"{e(NEGOCIO['horario'])}.")]},
    {"slug": "voge-fuenlabrada", "ciudad": "Fuenlabrada", "corto": "Fuenlabrada", "tienda": "ambas", "nombres": ["Fuenlabrada"],
     "title": "Voge Fuenlabrada · Concesionarios oficiales en Móstoles y Getafe",
     "meta": "¿Buscas Voge en Fuenlabrada? Tienes Voge Móstoles y Voge Getafe a pocos minutos: toda la gama Voge, prueba, financiación y taller propio.",
     "eyebrow": "Fuenlabrada · Humanes · Madrid Sur", "h1": "Concesionario Voge cerca de Fuenlabrada",
     "lead": "Fuenlabrada queda entre nuestros dos concesionarios Voge: Móstoles y Getafe. Elige el que te pille mejor.",
     "hero": "concesionario-voge-madrid-sur-3.webp",
     "intro": ["<b>Fuenlabrada</b> está justo entre Móstoles y Getafe, así que tienes dos concesionarios oficiales Voge a pocos minutos. En los dos puedes ver la gama y pedir tu prueba antes de decidir.",
               "Si buscas tu primera moto, las Voge de 125 cc como la <a href=\"/modelo/125r/\">125R</a> o la <a href=\"/modelo/sr16/\">SR16</a> son una buena forma de empezar con el carnet A1 o con el de coche. Si ya tienes el A2, mira las <a href=\"/motos-voge-a2/\">Voge para el carnet A2</a>."],
     "llegar": "Por la M-506 llegas a los dos: hacia el oeste, a Voge Móstoles (Calle Juan de la Cierva, 7-9); hacia el este, a Voge Getafe (Calle Barberán y Collar, 1).",
     "perfiles": [("Primera moto", ["125r", "sr16", "sr1-adv"]), ("Carnet A2", ["sr4-radar", "300-rally", "525dsx"])],
     "faqs": [("¿Dónde comprar una Voge si vivo en Fuenlabrada?", f"En Voge Móstoles ({e(DIRECCION)}) o en Voge Getafe ({e(DIR_GETAFE)}), los dos de Duomo Motor Bikes. No tenemos tienda en Fuenlabrada, pero los dos están muy bien comunicados por la M-506."),
              ("¿Cuál es la Voge más barata?", (lambda m: f"Ahora mismo, la <a href=\"{model_url(m)}\">Voge {e(m['name'])}</a>, por {eur(m['price'])} (PVP con IVA).")(min(M, key=lambda x: x["price"]))),
              ("¿Hacéis revisiones a motos Voge compradas en otro sitio?", "Sí. Nuestro <a href=\"/taller-voge/\">taller</a> atiende cualquier Voge, la hayas comprado aquí o no."),
              ("¿Qué horario tenéis?", f"Los dos concesionarios: {e(NEGOCIO['horario'])}.")]},
    {"slug": "voge-leganes", "ciudad": "Leganés", "corto": "Leganés", "tienda": "getafe", "nombres": ["Leganés"],
     "title": "Voge Leganés · Concesionario oficial al lado, en Getafe",
     "meta": "¿Buscas Voge en Leganés? Voge Getafe es tu concesionario oficial más cercano: toda la gama Voge, prueba sin compromiso y financiación a medida.",
     "eyebrow": "Leganés · Getafe · Madrid Sur", "h1": "Concesionario Voge cerca de Leganés",
     "lead": "Si vives en Leganés, Voge Getafe te pilla al lado: toda la gama Voge, prueba sin compromiso y financiación a medida.",
     "hero": "concesionario-voge-madrid-sur-2.webp",
     "intro": ["Desde <b>Leganés</b> tienes <b>Voge Getafe</b> a un corto trayecto. Allí puedes comparar en persona los scooters, las naked y las adventure de Voge y salir con la moto que de verdad encaja contigo.",
               "Para moverte entre Leganés y Madrid sin atascos ni problemas de aparcamiento, un scooter de 125 con el carnet de coche como la <a href=\"/modelo/sr1/\">SR1</a> es la opción más práctica. Si quieres más motor, la <a href=\"/modelo/sr4-radar/\">SR4 Radar</a> se lleva con el A2."],
     "llegar": "Desde Leganés, ve hacia Getafe por la M-406 o la M-45. Abre la ruta en Google Maps y te lleva directo a la Calle Barberán y Collar, 1.",
     "perfiles": [("Para moverte por Madrid", ["sr16-air", "sr1", "sr3"]), ("Para viajar", ["sr450x", "525dsx", "900dsx"])],
     "faqs": [("¿Hay concesionario Voge en Leganés?", f"El concesionario oficial Voge más cercano a Leganés es Voge Getafe, en {e(DIR_GETAFE)}. No tenemos tienda en Leganés."),
              ("¿Puedo llevar una 125 con el carnet de coche?", "Sí, si tu carnet B tiene más de tres años de antigüedad, en España puedes llevar motos de hasta 125 cc y 11 kW. Mira todas en <a href=\"/motos-125-carnet-coche/\">Voge 125 con carnet de coche</a>."),
              ("¿Me podéis mandar precio sin ir al concesionario?", "Claro. Escríbenos desde el <a href=\"/contacto/\">formulario de contacto</a> y te enviamos precio, financiación y disponibilidad."),
              ("¿Qué horario tenéis?", f"{e(NEGOCIO['horario'])}.")]},
]

def page_zona(z):
    url = f"/{z['slug']}/"
    crumbs = [("Inicio", "/"), (f"Voge cerca de {z['corto']}", url)]
    dir_ = GETAFE["dir"] if z["tienda"] == "getafe" else MAPS_DIR
    perf = ""
    for t, slugs in z["perfiles"]:
        perf += f"""<h3 style="margin:34px 0 14px">{e(t)}</h3><div class="grid">{"".join(card(mm(s)) for s in slugs)}</div>"""
    destino = {"getafe": "Getafe", "mostoles": "Móstoles", "ambas": "Móstoles o Getafe"}[z["tienda"]]
    body = f"""
  <section class="hero hero--page">
    <div class="hero__bg"><img src="/assets/img/hero/{z['hero']}" alt="" width="1366" height="911"></div>
    <div class="wrap"><div class="hero__inner">
      <span class="eyebrow">{e(z['eyebrow'])}</span>
      <h1>{e(z['h1'])}</h1>
      <p class="lead">{z['lead']}</p>
      <div class="hero__actions"><a class="btn btn--primary" href="{dir_}" target="_blank" rel="noopener">Cómo llegar</a><a class="btn btn--ghost-light" href="/solicitud-de-prueba/">Pedir prueba</a></div>
    </div></div>
  </section>
  {crumbs_html(crumbs)}
  <section class="section" style="padding-top:36px">
    <div class="wrap split">
      <div class="prose reveal">
        <h2>Voge para {e(z['ciudad'])}</h2>
        {"".join(f"<p>{p}</p>" for p in z['intro'])}
        <h3>Cómo llegar desde {e(z['ciudad'])}</h3>
        <p>{z['llegar']}</p>
      </div>
      <div class="note-box reveal reveal-d1" style="margin:0">{note_tienda(z["tienda"])}</div>
    </div>
  </section>
  <section class="section section--alt">
    <div class="wrap">
      <h2>Las Voge que más se llevan desde {e(z['corto'])}</h2>
      <p class="sub">Según para qué quieras la moto.</p>
      {perf}
      <div class="hero__actions" style="justify-content:center;margin-top:30px"><a class="btn btn--dark" href="/#gama">Ver los {len(M)} modelos</a></div>
    </div>
  </section>
  {bloque_confianza()}
  <section class="section"><div class="wrap">{visit_block(f"Ven desde {z['corto']} a {destino}", z["tienda"])}</div></section>
  {bloque_blog(z['nombres'])}
  <section class="section">
    <div class="wrap">
      <h2>Preguntas frecuentes</h2>
      <p class="sub">Si vienes desde {e(z['ciudad'])}.</p>
      {faq_html(z['faqs'])}
    </div>
  </section>
  {cta_band()}
"""
    about = {"@id": GETAFE_ID} if z["tienda"] == "getafe" else ({"@id": DEALER_ID} if z["tienda"] == "mostoles" else [{"@id": DEALER_ID}, {"@id": GETAFE_ID}])
    ld = [crumbs_ld(crumbs), faq_ld(z["faqs"]), {"@context": "https://schema.org", "@type": "WebPage", "name": z["h1"], "url": SITE + url,
          "about": about, "spatialCoverage": {"@type": "Place", "name": z["corto"]}}]
    write(url, head(z["title"], z["meta"], url, ld=ld) + header() + body + footer())

# ------------------------------------------------------------------ SITEMAP, ROBOTS, LLMS
def seo_files():
    urls = [("/", "1.0", "weekly"), ("/concesionario-voge-madrid-sur/", "0.9", "monthly"), ("/voge-mostoles/", "0.9", "monthly"), ("/voge-getafe/", "0.9", "monthly"),
            ("/taller-voge/", "0.8", "monthly"), ("/motos-voge-a2/", "0.9", "weekly"), ("/motos-125-carnet-coche/", "0.9", "weekly"),
            ("/solicitud-de-prueba/", "0.7", "monthly"), ("/contacto/", "0.7", "monthly")]
    urls += [(f"/{z['slug']}/", "0.8", "monthly") for z in ZONAS_PAG]
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
    zonas = "\n".join(f"- [Voge cerca de {z['corto']}]({SITE}/{z['slug']}/)" for z in ZONAS_PAG)
    gama = "\n".join(f"- [{full(m)}]({SITE}{model_url(m)}): {m['cat'].lower()}, {m['cc']} cc, {m['cv']} CV, {LIC[m['license']]['label'].lower()}, {eur(m['price'])}" for m in M)
    blog = "\n".join(f"- [{p['titulo']}]({SITE}/blog/{p['slug']}/)" for p in posts[:20])
    open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8").write(f"""# Voge Madrid Sur · Duomo Motor Bikes

> Concesionarios oficiales Voge en Móstoles ({XMADRID} de Alcorcón) y Getafe. Venta de motos Voge nuevas, prueba sin compromiso, financiación, taller propio y recambios originales.

- Voge Móstoles: {DIRECCION} · Tel. {NEGOCIO['tel']} · Taller: {NEGOCIO['telTaller']}
- Voge Getafe: {DIR_GETAFE} · Tel. {GETAFE['tel']}
- Email: {NEGOCIO['email']}
- Horario (los dos): {NEGOCIO['horario']}
- Zona que atendemos: {', '.join(ZONAS)}
- {CREDENCIALES}

## Páginas principales
- [Inicio]({SITE}/)
- [Concesionarios Voge Madrid Sur]({SITE}/concesionario-voge-madrid-sur/)
- [Voge Móstoles]({SITE}/voge-mostoles/)
- [Voge Getafe]({SITE}/voge-getafe/)
{zonas}
- [Taller Voge]({SITE}/taller-voge/)
- [Motos Voge para carnet A2]({SITE}/motos-voge-a2/)
- [Motos 125 con carnet de coche]({SITE}/motos-125-carnet-coche/)
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
    page_form("contacto"); page_form("prueba"); page_taller(); page_concesionarios()
    page_tienda("mostoles"); page_tienda("getafe"); page_a2(); page_125()
    for z in ZONAS_PAG: page_zona(z)
    for u, (t, s, cnt) in LEGAL.items(): page_legal(u, t, s, cnt)
    page_blog(); page_404(); seo_files()
    print(f"OK · {len(M)} modelos · {len(CATS)} categorías")
