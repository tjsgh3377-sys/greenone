# -*- coding: utf-8 -*-
"""그린원 홈페이지 정적 빌드 스크립트 (Python 표준 라이브러리만 사용).

    python tools/build.py                      # data/*.json → ko/, en/ HTML 생성
    python tools/build.py --site-url https://계정.github.io/저장소/

- 제품·설치사례·인증·기업정보는 data/*.json 한 곳에서 관리하고 국문·영문 페이지에 함께 반영된다.
- 생성된 HTML 은 서버 없이(GitHub Pages, file://) 그대로 열린다. 모든 경로는 상대경로.
"""
import datetime, html, json, os, sys
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
try:  # 한글 Windows 콘솔(cp949)에서도 출력이 깨지지 않도록
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def load(name):
    with open(os.path.join(ROOT, "data", name), encoding="utf-8") as f:
        return json.load(f)


CO, PR, INS, CERT = load("company.json"), load("products.json"), load("installations.json"), load("certificates.json")
TXT = {"ko": load("ko.json"), "en": load("en.json")}
SITE_URL = CO["site"].get("siteUrl", "")
if "--site-url" in sys.argv:
    SITE_URL = sys.argv[sys.argv.index("--site-url") + 1]
if SITE_URL and not SITE_URL.endswith("/"):
    SITE_URL += "/"
SHOW_NOTES = bool(CO["site"].get("showVerificationNotes", True))
YEAR = datetime.date.today().year
# CSS/JS 수정 시 브라우저 캐시가 남지 않도록 파일 수정시각을 버전 값으로 붙인다.
ASSET_VER = datetime.datetime.fromtimestamp(max(os.path.getmtime(os.path.join(ROOT, "assets", d, f)) for d, f in (("css", "site.css"), ("js", "site.js")))).strftime("%y%m%d%H%M")
GROUPS = PR["groups"]
GMAP = {g["id"]: g for g in GROUPS}
SUB = {s["id"] + "@" + s["category"]: s for s in PR["subcategories"]}
CAT = {c["id"]: c for c in PR["categories"]}
IMAP = {i["id"]: i for i in INS["items"]}
SCENE = {s["id"]: s for s in INS["scenes"]}
POWER_SHORT = {"battery": ("배터리형", "Battery"), "hybrid": ("하이브리드형", "Hybrid"), "solar": ("태양광형", "Solar"),
               "electric": ("전기형", "Mains-powered")}
OUT = []  # (경로, lang) — sitemap 용

e = lambda s: html.escape(str(s), quote=True)


def t(L, path, **kw):
    v = TXT[L]
    for k in path.split("."):
        v = v[k]
    if kw and isinstance(v, str):
        for k, val in kw.items():
            v = v.replace("{" + k + "}", str(val))
    return v


def ln(obj, key, L):
    """nameKo/nameEn 형태 필드 선택."""
    return obj[key + ("Ko" if L == "ko" else "En")]


class P:
    """현재 페이지 컨텍스트 — 언어와 깊이에 따라 상대경로를 계산."""

    def __init__(self, L, path):
        self.L, self.path = L, path
        self.depth = path.count("/")

    def a(self, asset):  # 사이트 루트 기준 자산 경로
        return "../" * (self.depth + 1) + asset

    def u(self, page):  # 같은 언어 안의 페이지 경로
        return "../" * self.depth + page

    def other(self):
        return "../" * (self.depth + 1) + ("en" if self.L == "ko" else "ko") + "/" + self.path

    def t(self, path, **kw):
        return t(self.L, path, **kw)

    def abs(self, L=None, path=None):
        return SITE_URL + (L or self.L) + "/" + (self.path if path is None else path).replace("index.html", "")


def img(src, alt, w=None, h=None, cls="", lazy=True, extra=""):
    return '<img src="%s" alt="%s"%s%s%s%s decoding="async"%s>' % (
        e(src), e(alt), ' width="%s"' % w if w else "", ' height="%s"' % h if h else "",
        ' class="%s"' % cls if cls else "", ' loading="lazy"' if lazy else ' fetchpriority="high"', " " + extra if extra else "")


def inst_img(p, iid, alt=None, thumb=False, lazy=True):
    it = IMAP[iid]
    return img(p.a(it["thumb"] if thumb else it["image"]), alt or ln(it, "alt", p.L), it["w"], it["h"], lazy=lazy)


NAV = [("about", "about.html", [("overview", "about.html"), ("greeting", "greeting.html"), ("philosophy", "philosophy.html"),
                                 ("certificates", "certificates.html"), ("location", "location.html")]),
       ("products", "road-stud.html", [("roadStud", "road-stud.html"), ("lighting", "lighting.html")]),
       ("applications", "applications.html", []), ("resources", "resources.html", []), ("contact", "contact.html", [])]


def jsonld(obj):
    return '<script type="application/ld+json">%s</script>' % json.dumps(obj, ensure_ascii=False).replace("</", "<\\/")


def org_ld(L):
    d = {"@context": "https://schema.org", "@type": "Organization", "name": ln(CO, "name", L), "alternateName": [CO["nameKo"], CO["nameEn"], "GreenOne", "그린원"],
         "description": ln(CO, "business", L), "slogan": ln(CO, "slogan", L), "telephone": CO["telIntl"], "faxNumber": CO["faxIntl"], "email": CO["email"],
         "address": {"@type": "PostalAddress", "streetAddress": "율마로 27, 나동 2층" if L == "ko" else "2F, Building Na, 27 Yulma-ro, Daegot-myeon",
                     "addressLocality": "김포시" if L == "ko" else "Gimpo-si", "addressRegion": "경기도" if L == "ko" else "Gyeonggi-do",
                     "postalCode": CO["postalCode"], "addressCountry": "KR"},
         "founder": {"@type": "Person", "name": ln(CO, "ceo", L), "jobTitle": "CEO"}}
    if SITE_URL:
        d["url"] = SITE_URL + L + "/"; d["logo"] = SITE_URL + "assets/img/brand/logo.png"
    return d


def crumb_ld(p, trail):
    if not SITE_URL:
        return ""
    items = [{"@type": "ListItem", "position": i + 1, "name": n, "item": p.abs(path=h)} for i, (n, h) in enumerate(trail)]
    return jsonld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items})


def layout(p, title, desc, body, group="", current="", ld="", og_image="assets/img/brand/og.jpg"):
    L = p.L
    nav_d, nav_m = [], []
    for key, href, subs in NAV:
        cur = ' class="is-current"' if key == group else ""
        if subs:
            sub = "".join('<li><a href="%s"%s>%s</a></li>' % (p.u(h), ' aria-current="page"' if k == current else "", e(t(L, "nav." + k))) for k, h in subs)
            nav_d.append('<li%s><a href="%s">%s</a><ul class="sub">%s</ul></li>' % (cur, p.u(href), e(t(L, "nav." + key)), sub))
            nav_m.append('<li><a href="%s">%s</a><div class="mnav-sub">%s</div></li>' % (
                p.u(href), e(t(L, "nav." + key)), "".join('<a href="%s">%s</a>' % (p.u(h), e(t(L, "nav." + k))) for k, h in subs)))
        else:
            nav_d.append('<li%s><a href="%s">%s</a></li>' % (cur, p.u(href), e(t(L, "nav." + key))))
            nav_m.append('<li><a href="%s">%s</a></li>' % (p.u(href), e(t(L, "nav." + key))))
    logo_alt = "GreenOne " + CO["nameKo"]
    logo = img(p.a("assets/img/brand/logo.png"), logo_alt, 750, 140, lazy=False)
    ko_href = os.path.basename(p.path) if L == "ko" else p.other()
    en_href = os.path.basename(p.path) if L == "en" else p.other()
    lang = ('<div class="lang" role="group" aria-label="%s"><a href="%s" lang="ko" hreflang="ko"%s>KR</a><a href="%s" lang="en" hreflang="en"%s>EN</a></div>'
            % (e(t(L, "nav.langSwitch")), ko_href, ' class="on" aria-current="true"' if L == "ko" else "", en_href, ' class="on" aria-current="true"' if L == "en" else ""))
    seo = []
    if SITE_URL:
        seo.append('<link rel="canonical" href="%s">' % e(p.abs()))
        seo.append('<link rel="alternate" hreflang="ko" href="%s">' % e(p.abs("ko")))
        seo.append('<link rel="alternate" hreflang="en" href="%s">' % e(p.abs("en")))
        seo.append('<link rel="alternate" hreflang="x-default" href="%s">' % e(p.abs("ko")))
        seo.append('<meta property="og:url" content="%s">' % e(p.abs()))
        og = SITE_URL + og_image
    else:
        seo.append('<link rel="alternate" hreflang="ko" href="%s">' % ko_href)
        seo.append('<link rel="alternate" hreflang="en" href="%s">' % en_href)
        og = p.a(og_image)
    i18n = json.dumps({k: t(L, "common." + k) for k in ("close", "prev", "next")} | {"menu": t(L, "nav.menu")}, ensure_ascii=False)
    tel = CO["tel"] if L == "ko" else CO["telIntl"]
    fax = CO["fax"] if L == "ko" else CO["faxIntl"]
    addr = "(%s) %s" % (CO["postalCode"], CO["addressKo"]) if L == "ko" else "%s (%s)" % (CO["addressEn"], CO["postalCode"])
    ft_menu = "".join('<a href="%s">%s</a>' % (p.u(h), e(t(L, "nav." + k))) for k, h in
                      [("overview", "about.html"), ("roadStud", "road-stud.html"), ("greeting", "greeting.html"), ("lighting", "lighting.html"),
                       ("certificates", "certificates.html"), ("applications", "applications.html"), ("location", "location.html"), ("resources", "resources.html"),
                       ("contact", "contact.html")])
    return """<!DOCTYPE html>
<html lang="{L}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{seo}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{site}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{og}">
<meta property="og:locale" content="{locale}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0C361C">
<meta name="format-detection" content="telephone=no">
<link rel="icon" href="{fav}" sizes="any">
<link rel="icon" type="image/png" sizes="48x48" href="{fav48}">
<link rel="apple-touch-icon" href="{touch}">
<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/variable/pretendardvariable-dynamic-subset.min.css">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;500;600;700&display=swap">
<link rel="stylesheet" href="{css}">
{ld}
</head>
<body>
<a class="skip" href="#main">{skip}</a>
<header class="hd">
<div class="hd-in">
<a class="hd-logo" href="{home}" aria-label="{site} {homeLabel}">{logo}</a>
<nav class="gnb" aria-label="{menu}"><ul>{nav_d}</ul></nav>
<div class="hd-util">{lang}<a class="btn btn-solid btn-sm hd-cta" href="{contact}">{cta}</a>
<button type="button" class="burger" aria-controls="mnav" aria-expanded="false" aria-label="{menu}"><span></span><span></span></button></div>
</div>
</header>
<div class="mnav" id="mnav" hidden>
<nav aria-label="{menu}"><ul class="mnav-list">{nav_m}</ul></nav>
<div class="mnav-foot"><a class="btn btn-solid" href="{contact}">{inq}</a>
<p class="mnav-contact">{telL} <a href="tel:{telHref}">{tel}</a><br>{mailL} <a href="mailto:{mail}">{mail}</a></p></div>
</div>
<main id="main">
{body}
</main>
<footer class="ft">
<div class="wrap">
<div class="ft-top">
<div class="ft-brand"><a class="ft-logo" href="{home}">{logo_lazy}</a><p class="ft-tag">{tag}</p></div>
<dl class="ft-info">
<div><dt>{cL}</dt><dd>{cname}</dd></div>
<div><dt>{ceoL}</dt><dd>{ceo}</dd></div>
<div><dt>{addrL}</dt><dd>{addr}</dd></div>
<div><dt>{telL}</dt><dd><a href="tel:{telHref}">{tel}</a></dd></div>
<div><dt>{faxL}</dt><dd>{fax}</dd></div>
<div><dt>{mailL}</dt><dd><a href="mailto:{mail}">{mail}</a></dd></div>
</dl>
<div><p class="ft-title">{menuT}</p><nav class="ft-menu" aria-label="{menuT}">{ft_menu}</nav>
<p class="ft-dl"><a class="arrow-link" href="{cat}" download>{catL}</a></p></div>
</div>
<div class="ft-bottom"><span>{copy}</span><span>{biz} · {reg}</span></div>
</div>
</footer>
<script type="application/json" id="i18n">{i18n}</script>
<script src="{js}" defer></script>
</body>
</html>
""".format(L=L, title=e(title), desc=e(desc), seo="\n".join(seo), site=e(t(L, "siteName")), og=e(og), locale="ko_KR" if L == "ko" else "en_US",
           fav=p.a("favicon.ico"), fav48=p.a("assets/img/brand/favicon-48.png"), touch=p.a("assets/img/brand/apple-touch-icon.png"),
           css=p.a("assets/css/site.css") + "?v=" + ASSET_VER, js=p.a("assets/js/site.js") + "?v=" + ASSET_VER, ld=ld, skip=e(t(L, "nav.skip")), home=p.u("index.html"),
           homeLabel=e(t(L, "common.home")), logo=logo, logo_lazy=img(p.a("assets/img/brand/logo.png"), logo_alt, 750, 140),
           menu=e(t(L, "nav.menu")), nav_d="".join(nav_d), nav_m="".join(nav_m), lang=lang, contact=p.u("contact.html"), cta=e(t(L, "nav.cta")),
           inq=e(t(L, "common.inquiry")), telL=e(t(L, "common.tel")), faxL=e(t(L, "common.fax")), mailL=e(t(L, "common.email")),
           tel=e(tel), telHref=CO["telIntl"].replace("-", ""), fax=e(fax), mail=e(CO["email"]), body=body, tag=e(t(L, "footer.tagline")),
           cL=e(t(L, "common.company")), cname=e(ln(CO, "name", L)), ceoL=e(t(L, "common.ceo")), ceo=e(ln(CO, "ceo", L)),
           addrL=e(t(L, "common.address")), addr=e(addr), menuT=e(t(L, "footer.menu")), ft_menu=ft_menu, cat=p.a(CO["catalogFile"]),
           catL=e(t(L, "common.catalog")), copy=e(t(L, "footer.copyright", year=YEAR)), biz=e(ln(CO, "business", L)), reg=e(ln(CO, "registration", L)), i18n=i18n)


def write(p, htmltext):
    path = os.path.join(ROOT, p.L, p.path.replace("/", os.sep))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(htmltext)
    OUT.append((p.L, p.path))


def page_hero(p, eyebrow, h1, lead, trail, media=None):
    crumbs = "".join('<li>%s</li>' % ('<a href="%s">%s</a>' % (p.u(h), e(n)) if h and i < len(trail) - 1 else '<span aria-current="page">%s</span>' % e(n))
                     for i, (n, h) in enumerate(trail))
    media = None  # 서브페이지 상단에는 사진을 쓰지 않는다(연두 배경만). 사진을 다시 쓰려면 이 줄을 지운다.
    m = '<div class="ph-media">%s</div>' % media if media else ""
    return ('<section class="ph%s"><div class="ph-in"><div class="ph-text"><nav aria-label="breadcrumb"><ol class="crumb">%s</ol></nav>'
            '<p class="eyebrow">%s</p><h1>%s</h1>%s</div>%s</div></section>'
            % (" has-media" if media else "", crumbs, e(eyebrow), e(h1), '<p class="lead">%s</p>' % e(lead) if lead else "", m))


def about_tabs(p, current):
    items = [("overview", "about.html"), ("greeting", "greeting.html"), ("philosophy", "philosophy.html"), ("certificates", "certificates.html"), ("location", "location.html")]
    return '<nav class="tabs" aria-label="%s"><div class="wrap"><ul>%s</ul></div></nav>' % (
        e(p.t("nav.about")), "".join('<li><a href="%s"%s>%s</a></li>' % (p.u(h), ' aria-current="page"' if k == current else "", e(p.t("nav." + k))) for k, h in items))


def cta_band(p):
    L = p.L
    tel = CO["tel"] if L == "ko" else CO["telIntl"]
    return """<section class="sec cta"><div class="wrap"><div class="cta-grid">
<div><p class="eyebrow">{eb}</p><h2>{title}</h2></div>
<div><div class="btn-row"><a class="btn btn-light btn-dl" href="{cat}" download>{c1}</a><a class="btn btn-line-light" href="{contact}">{c2}</a></div>
<dl class="cta-contact"><div><dt>{telL}</dt><dd><a href="tel:{telHref}">{tel}</a></dd></div><div><dt>{mailL}</dt><dd><a href="mailto:{mail}">{mail}</a></dd></div></dl></div>
</div></div></section>""".format(eb=e(p.t("home.contact.eyebrow")), title=e(p.t("home.contact.title")), cat=p.a(CO["catalogFile"]), c1=e(p.t("home.contact.cta1")),
                                 c2=e(p.t("home.contact.cta2")), contact=p.u("contact.html"), telL=e(p.t("common.tel")), tel=e(tel),
                                 telHref=CO["telIntl"].replace("-", ""), mailL=e(p.t("common.email")), mail=e(CO["email"]))


def cert_items(p, lb="cert"):
    out = []
    for c in CERT["items"]:
        name = ln(c, "name", p.L)
        sub = '<span class="cert-en" lang="en">%s</span>' % e(c["nameEn"]) if p.L == "ko" else ""
        out.append('<a class="cert" href="%s" data-lb="%s" data-cap="%s" data-alt="%s"><span class="cert-img">%s</span><span class="cert-name">%s</span>%s</a>'
                   % (p.a(c["image"]), lb, e(name), e(name), img(p.a(c["image"]), name, c["w"], c["h"]), e(name), sub))
    return "".join(out)


def sub_name(g, L):
    return ln(SUB[g["subcategory"] + "@" + g["category"]], "name", L)


def power_label(g, L):
    return " · ".join(POWER_SHORT[x][0 if L == "ko" else 1] for x in g["powerTypes"] if x in POWER_SHORT)


def group_image(g):
    return g["models"][0]["images"][0]


def pcard(p, g, label=None, href=None, show_cat=True):
    L = p.L
    im = group_image(g)
    models = [m["model"] for m in g["models"]]
    shown = " · ".join(models[:3]) + (" +%d" % (len(models) - 3) if len(models) > 3 else "")
    search = " ".join([g["nameKo"], g["nameEn"]] + [" ".join([m["model"], m["procurementId"], m["nameKo"], m["nameEn"], m["modelSource"]["specTable"], m["modelSource"]["imageCaption"]]) for m in g["models"]])
    power = " ".join(x for x in g["powerTypes"] if x in POWER_SHORT)
    return ('<a class="pcard" href="%s" data-card data-sub="%s" data-power="%s" data-search="%s"><div class="pcard-img">%s</div><div class="pcard-body">%s<h3>%s</h3>'
            '<p class="pcard-models">%s</p><p class="pcard-foot"><span>%s</span></p></div></a>'
            % (href or p.u("products/%s.html" % g["id"]), g["subcategory"], power, e(search), img(p.a(im["src"]), label or ln(g, "name", L), im["w"], im["h"]),
               '<span class="pcard-cat">%s</span>' % e(sub_name(g, L) if g["category"] == "lighting" else ln(CAT[g["category"]], "name", L)) if show_cat else "",
               e(label or ln(g, "name", L)), e(shown), e(power_label(g, L))))


# ───────────────────────── HOME ─────────────────────────
def build_home(L):
    p = P(L, "index.html")
    H = TXT[L]["home"]
    hero_img = ('<img src="{a}" srcset="{b} 900w, {a} 2000w" sizes="100vw" alt="{alt}" width="2000" height="1773" fetchpriority="high" decoding="async">'
                .format(a=p.a("assets/img/hero/bridge-night.webp"), b=p.a("assets/img/hero/bridge-night-900.webp"), alt=e(H["hero"]["imageAlt"])))
    body = """<section class="hero">
<div class="hero-text">
<p class="eyebrow">{eb}</p>
<h1>{h1}</h1>
<p class="hero-desc">{desc}</p>
<div class="btn-row"><a class="btn btn-light" href="{u1}">{c1}</a><a class="btn btn-line-light" href="{u2}">{c2}</a></div>
<p class="hero-foot"><b>{tag}</b><span>{sub}</span></p>
</div>
<div class="hero-media">{img}
</div>
</section>""".format(eb=e(H["hero"]["eyebrow"]), h1="".join("<span>%s</span>" % e(x) for x in H["hero"]["title"]), desc=e(H["hero"]["desc"]),
                     u1=p.u("road-stud.html"), u2=p.u("applications.html"), u3=p.u("lighting.html"), c1=e(H["hero"]["cta1"]), c2=e(H["hero"]["cta2"]),
                     tag=e(H["hero"]["tag"]), sub=e(H["hero"]["sub"]), img=hero_img, n1=e(p.t("nav.roadStud")), n2=e(p.t("nav.lighting")))

    def duo(no, key, href, iid, rev):
        d = H["products"][key]
        return ('<article class="duo-item%s"><a class="duo-media" href="%s" tabindex="-1" aria-hidden="true">%s</a><div class="duo-body"><p class="duo-no" aria-hidden="true">%s</p>'
                '<p class="duo-en">%s</p><h3>%s</h3><p>%s</p><ul class="duo-types">%s</ul><a class="arrow-link" href="%s">%s</a></div></article>'
                % (" rev" if rev else "", p.u(href), inst_img(p, iid, d["alt"]), no, e(d["en"]), e(d["name"]), e(d["desc"]),
                   "".join("<li>%s</li>" % e(x) for x in d["types"]), p.u(href), e(p.t("common.viewProducts"))))
    body += """<section class="sec"><div class="wrap">
<div class="sec-head"><div><p class="eyebrow">{eb}</p><h2 class="h2">{title}</h2></div></div>
<div class="duo">{a}{b}</div></div></section>""".format(eb=e(H["products"]["eyebrow"]), title=e(H["products"]["title"]),
                                                       a=duo("01", "roadStud", "road-stud.html", "p12-3", False), b=duo("02", "lighting", "lighting.html", "p17-2", True))

    items = "".join('<li><span class="num">%02d</span><div><h3>%s</h3><p>%s</p><p class="tech-scope"><b>%s</b><span>%s</span></p></div></li>'
                    % (i + 1, e(x["title"]), e(x["desc"]), e(H["tech"]["scopeLabel"]), e(x["scope"])) for i, x in enumerate(H["tech"]["items"]))
    body += """<section class="sec tech"><div class="wrap"><div class="tech-grid">
<div class="tech-head"><p class="eyebrow">{eb}</p><h2 class="h2">{title}</h2><p class="lead">{lead}</p></div>
<ol class="tech-list">{items}</ol></div></div></section>""".format(eb=e(H["tech"]["eyebrow"]), title=e(H["tech"]["title"]), lead=e(H["tech"]["lead"]), items=items)

    cards = ""
    for it in H["collection"]["items"]:
        g = GMAP[it["group"]]
        im = group_image(g)
        href = p.u(it.get("href") or "products/%s.html" % g["id"])
        cards += ('<a class="pcard" href="%s"><div class="pcard-img">%s</div><div class="pcard-body"><span class="pcard-cat">%s</span><h3>%s</h3>'
                  '<p class="pcard-models">%s · %s</p><p class="pcard-foot"><span>%s</span></p></div></a>'
                  % (href, img(p.a(im["src"]), it["label"], im["w"], im["h"]), e(ln(CAT[g["category"]], "name", L)), e(it["label"]),
                     e(H["collection"]["repModel"]), e(g["models"][0]["model"]), e(p.t("common.more"))))
    body += """<section class="sec"><div class="wrap">
<div class="sec-head"><div><p class="eyebrow">{eb}</p><h2 class="h2">{title}</h2></div></div>
<div class="pgrid">{cards}</div></div></section>""".format(eb=e(H["collection"]["eyebrow"]), title=e(H["collection"]["title"]), cards=cards)

    pos = ["m1", "m2", "m4", "m5", "m3", "m6"]
    mos = "".join('<a class="mo %s" href="%s">%s<span class="mo-label">%s</span></a>'
                  % (pos[i], p.u("applications.html"), inst_img(p, it["id"], it["label"], thumb=pos[i] not in ("m1", "m6")), e(it["label"]))
                  for i, it in enumerate(H["gallery"]["items"]))
    body += """<section class="sec sec-ivory"><div class="wrap">
<div class="sec-head"><div><p class="eyebrow">{eb}</p><h2 class="h2">{title}</h2></div><p class="lead">{lead}</p></div>
<div class="mosaic">{mos}</div><div class="sec-foot"><a class="arrow-link" href="{u}">{cta}</a></div></div></section>""".format(
        eb=e(H["gallery"]["eyebrow"]), title=e(H["gallery"]["title"]), lead=e(H["gallery"]["lead"]), mos=mos, u=p.u("applications.html"), cta=e(H["gallery"]["cta"]))

    facts = "".join("<div><dt>%s</dt><dd>%s</dd></div>" % (e(a), e(b)) for a, b in [
        (p.t("common.business"), ln(CO, "business", L)), (p.t("common.ceo"), ln(CO, "ceo", L)), (p.t("common.registration"), ln(CO, "registration", L))])
    body += """<section class="sec"><div class="wrap"><div class="split">
<div class="split-media">{im}</div>
<div class="split-body"><p class="eyebrow">{eb}</p><h2 class="h2">{title}</h2>{ps}<dl class="facts">{facts}</dl><a class="arrow-link" href="{u}">{cta}</a></div>
</div></div></section>""".format(im=img(p.a("assets/img/hero/city-night-900.webp"), H["about"]["imageAlt"], 807, 900), eb=e(H["about"]["eyebrow"]),
                                 title=e(H["about"]["title"]), ps="".join("<p>%s</p>" % e(x) for x in H["about"]["body"]), facts=facts, u=p.u("about.html"), cta=e(H["about"]["cta"]))

    body += """<section class="sec sec-ivory"><div class="wrap">
<div class="sec-head"><div><p class="eyebrow">{eb}</p><h2 class="h2">{title}</h2></div><p class="lead">{lead}</p></div>
<div class="cert-strip">{certs}</div><div class="sec-foot"><a class="arrow-link" href="{u}">{cta}</a></div></div></section>""".format(
        eb=e(H["certs"]["eyebrow"]), title=e(H["certs"]["title"]), lead=e(H["certs"]["lead"]), certs=cert_items(p), u=p.u("certificates.html"), cta=e(H["certs"]["cta"]))
    body += cta_band(p)
    ld = jsonld(org_ld(L))
    if SITE_URL:
        ld += jsonld({"@context": "https://schema.org", "@type": "WebSite", "name": t(L, "siteName"), "url": SITE_URL + L + "/", "inLanguage": L})
    write(p, layout(p, H["title"], H["description"], body, ld=ld))


# ───────────────────────── ABOUT ─────────────────────────
def company_facts(p):
    L = p.L
    tel = CO["tel"] if L == "ko" else CO["telIntl"]
    addr = "(%s) %s" % (CO["postalCode"], CO["addressKo"]) if L == "ko" else "%s (%s)" % (CO["addressEn"], CO["postalCode"])
    rows = [(p.t("common.company"), e(CO["nameKo"] + " / " + CO["nameEn"])), (p.t("common.ceo"), e(ln(CO, "ceo", L))),
            (p.t("common.business"), e(ln(CO, "business", L))), (p.t("common.registration"), e(ln(CO, "registration", L))),
            (p.t("common.address"), e(addr)), (p.t("common.tel"), '<a href="tel:%s">%s</a>' % (CO["telIntl"].replace("-", ""), e(tel))),
            (p.t("common.fax"), e(CO["fax"] if L == "ko" else CO["faxIntl"])), (p.t("common.email"), '<a href="mailto:%s">%s</a>' % (CO["email"], CO["email"]))]
    return '<dl class="facts">%s</dl>' % "".join("<div><dt>%s</dt><dd>%s</dd></div>" % (e(a), b) for a, b in rows)


def build_about(L):
    # 기업소개
    p = P(L, "about.html"); A = TXT[L]["overview"]
    trail = [(p.t("common.home"), "index.html"), (p.t("nav.about"), "about.html"), (A["h1"], "about.html")]
    biz = "".join('<a href="%s"><span class="en">%s</span><strong>%s</strong><span class="d">%s</span></a>'
                  % (p.u(h), e(TXT[L]["home"]["products"][k]["en"]), e(TXT[L]["home"]["products"][k]["name"]), e(TXT[L]["home"]["products"][k]["desc"]))
                  for k, h in (("roadStud", "road-stud.html"), ("lighting", "lighting.html")))
    certs = " · ".join(ln(c, "name", L) for c in CERT["items"])
    body = page_hero(p, A["eyebrow"], A["h1"], A["lead"], trail) + about_tabs(p, "overview") + """
<section class="sec"><div class="wrap">
<p class="statement">{st}</p>
<div class="ov-photo">{im}</div>
</div></section>
<section class="sec sec-ivory"><div class="wrap"><div class="ov-grid">
<div><p class="eyebrow">ABOUT GREENONE</p><h2 class="h2">{slogan}</h2></div>
<div class="prose">{ps}</div>
</div></div></section>
<section class="sec"><div class="wrap"><div class="ov-grid">
<div><h2 class="block-title">{bt}</h2></div><div class="biz">{biz}</div></div>
<div class="ov-grid" style="margin-top:clamp(56px,6vw,96px)"><div><h2 class="block-title">{ft}</h2></div><div>{facts}
<p class="fine" style="margin-top:20px"><b>{ct}</b> — {certs}. <a class="arrow-link" href="{cu}" style="margin-left:8px">{cl}</a></p></div></div>
</div></section>""".format(st=e(A["statement"]), im=img(p.a("assets/img/hero/city-night.webp"), A["imageAlt"], 1613, 1800), slogan=e(ln(CO, "slogan", L)),
                           ps="".join("<p>%s</p>" % e(x) for x in A["body"]), bt=e(A["businessTitle"]), biz=biz, ft=e(A["factsTitle"]), facts=company_facts(p),
                           ct=e(A["certTitle"]), certs=e(certs), cu=p.u("certificates.html"), cl=e(p.t("nav.certificates"))) + cta_band(p)
    write(p, layout(p, A["title"], A["description"], body, "about", "overview", jsonld(org_ld(L)) + crumb_ld(p, trail)))

    # 인사말
    p = P(L, "greeting.html"); G = TXT[L]["greeting"]
    trail = [(p.t("common.home"), "index.html"), (p.t("nav.about"), "about.html"), (G["h1"], "greeting.html")]
    body = page_hero(p, G["eyebrow"], G["h1"], "", trail) + about_tabs(p, "greeting") + """
<section class="sec"><div class="wrap"><div class="greet">
<div class="greet-head"><p class="eyebrow">{eb}</p><h2 class="h2">{hl}</h2></div>
<div><div class="prose">{ps}</div><p class="greet-sign"><span>{c} {tt}</span><strong>{n}</strong></p></div>
</div></div></section>""".format(eb=e(G["eyebrow"]), hl=e(G["headline"]), ps="".join("<p>%s</p>" % e(x) for x in G["paragraphs"]),
                                 c=e(G["signCompany"]), tt=e(G["signTitle"]), n=e(G["signName"])) + cta_band(p)
    write(p, layout(p, G["title"], G["description"], body, "about", "greeting", crumb_ld(p, trail)))

    # 경영이념
    p = P(L, "philosophy.html"); F = TXT[L]["philosophy"]
    trail = [(p.t("common.home"), "index.html"), (p.t("nav.about"), "about.html"), (F["h1"], "philosophy.html")]
    a, b = ("ko", "en") if L == "ko" else ("en", "ko")
    lis = "".join('<li><span class="num">%02d</span><strong>%s</strong><em lang="%s">%s</em></li>' % (i + 1, e(x[a]), b, e(x[b])) for i, x in enumerate(F["items"]))
    body = page_hero(p, F["eyebrow"], F["h1"], F["lead"], trail) + about_tabs(p, "philosophy") + """
<section class="sec"><div class="wrap"><p class="statement">{st}</p>
<ol class="phil-list" style="margin-top:clamp(48px,6vw,96px)">{lis}</ol></div></section>""".format(st=e(F["statement"]), lis=lis) + cta_band(p)
    write(p, layout(p, F["title"], F["description"], body, "about", "philosophy", crumb_ld(p, trail)))

    # 인증현황
    p = P(L, "certificates.html"); C = TXT[L]["certificates"]
    trail = [(p.t("common.home"), "index.html"), (p.t("nav.about"), "about.html"), (C["h1"], "certificates.html")]
    body = page_hero(p, C["eyebrow"], C["h1"], C["lead"], trail) + about_tabs(p, "certificates") + """
<section class="sec"><div class="wrap"><div class="cert-grid">{certs}</div>
<p class="fine" style="margin-top:clamp(40px,5vw,72px);max-width:60em">{note}</p></div></section>""".format(certs=cert_items(p), note=e(C["note"])) + cta_band(p)
    write(p, layout(p, C["title"], C["description"], body, "about", "certificates", crumb_ld(p, trail)))

    # 오시는 길
    p = P(L, "location.html"); O = TXT[L]["location"]
    trail = [(p.t("common.home"), "index.html"), (p.t("nav.about"), "about.html"), (O["h1"], "location.html")]
    q = quote(CO["addressKo"].split(",")[0])
    addr_main = CO["addressKo"] if L == "ko" else CO["addressEn"]
    addr_sub = "(%s) %s" % (CO["postalCode"], CO["nameKo"]) if L == "ko" else "%s · %s" % (CO["postalCode"], CO["addressKo"])
    body = page_hero(p, O["eyebrow"], O["h1"], O["lead"], trail) + about_tabs(p, "location") + """
<section class="sec"><div class="wrap"><div class="loc-grid">
<div><p class="eyebrow">{eb}</p><p class="loc-addr" style="margin-top:24px">{am}<small>{asub}</small></p>
<div style="margin-top:40px">{facts}</div></div>
<aside class="loc-map"><h2 class="h3">{mt}</h2><p class="fine">{mn}</p>
<a class="btn btn-solid" href="https://map.naver.com/p/search/{q}" target="_blank" rel="noopener">{nv}</a>
<a class="btn btn-line" href="https://map.kakao.com/?q={q}" target="_blank" rel="noopener">{kk}</a>
<a class="btn btn-line" href="https://www.google.com/maps/search/?api=1&amp;query={q}" target="_blank" rel="noopener">{gg}</a>
<button type="button" class="btn btn-line btn-plain" data-copy="{copy}" data-done="{done}">{cp}</button></aside>
</div></div></section>""".format(eb=e(p.t("common.address")), am=e(addr_main), asub=e(addr_sub), facts=company_facts(p), mt=e(O["mapTitle"]), mn=e(O["mapNote"]),
                                 q=q, nv=e(O["naver"]), kk=e(O["kakao"]), gg=e(O["google"]), copy=e(CO["addressKo"] if L == "ko" else CO["addressEn"]),
                                 done=e(O["copied"]), cp=e(O["copy"])) + cta_band(p)
    write(p, layout(p, O["title"], O["description"], body, "about", "location", jsonld(org_ld(L)) + crumb_ld(p, trail)))


# ───────────────────────── PRODUCTS ─────────────────────────
def build_list(L, cat, page, hero_inst, nav_key):
    p = P(L, page); X = TXT[L]["productList"]; S = X[cat]
    gs = [g for g in GROUPS if g["category"] == cat]
    trail = [(p.t("common.home"), "index.html"), (p.t("nav.products"), "road-stud.html"), (S["h1"], page)]
    subs = [s for s in PR["subcategories"] if s["category"] == cat]
    chips = '<button type="button" class="chip" data-filter="sub" data-value="" aria-pressed="true">%s</button>' % e(p.t("common.all"))
    chips += "".join('<button type="button" class="chip" data-filter="sub" data-value="%s" aria-pressed="false">%s</button>' % (s["id"], e(ln(s, "name", L))) for s in subs)
    rows = '<div class="tb-row"><span class="tb-label" id="f-type">%s</span><div class="chips" role="group" aria-labelledby="f-type">%s</div></div>' % (e(X["filterType"]), chips)
    if cat == "lighting":
        pc = '<button type="button" class="chip" data-filter="power" data-value="" aria-pressed="true">%s</button>' % e(p.t("common.all"))
        pc += "".join('<button type="button" class="chip" data-filter="power" data-value="%s" aria-pressed="false">%s</button>' % (k, e(POWER_SHORT[k][0 if L == "ko" else 1]))
                      for k in ("electric", "solar", "hybrid", "battery"))
        rows += '<div class="tb-row"><span class="tb-label" id="f-power">%s</span><div class="chips" role="group" aria-labelledby="f-power">%s</div></div>' % (e(X["filterPower"]), pc)
    n_models = sum(len(g["models"]) for g in gs)
    count = p.t("common.count", n='<b data-count>%d</b>' % len(gs))
    body = page_hero(p, S["eyebrow"], S["h1"], S["lead"], trail, inst_img(p, hero_inst, S["imageAlt"], lazy=False)) + """
<section class="sec sec-tight"><div class="wrap" data-plist>
<div class="toolbar">{rows}
<div class="tb-search"><div class="search"><label class="vh" for="q">{sl}</label><input id="q" type="search" data-search placeholder="{sp}" autocomplete="off" spellcheck="false">
<button type="button" class="search-clear" data-search-clear aria-label="{reset}" hidden>×</button></div>
<p class="tb-count">{count} · {mc}</p></div></div>
<div class="pgrid{cols}">{cards}</div>
<p class="empty" data-empty hidden>{nores} <button type="button" class="arrow-link" data-reset style="margin-left:12px">{reset}</button></p>
</div></section>""".format(rows=rows, sl=e(X["searchLabel"]), sp=e(X["searchPlaceholder"]), reset=e(X["reset"]), count=count,
                           mc=e(t(L, "productList.modelsCount", n=n_models)), cols=" cols4" if cat == "lighting" else "",
                           cards="".join(pcard(p, g) for g in gs), nores=e(p.t("common.noResult"))) + cta_band(p)
    ld = crumb_ld(p, trail)
    if SITE_URL:
        ld += jsonld({"@context": "https://schema.org", "@type": "ItemList", "name": S["h1"],
                      "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": ln(g, "name", L), "url": p.abs(path="products/%s.html" % g["id"])} for i, g in enumerate(gs)]})
    write(p, layout(p, S["title"], S["description"], body, "products", nav_key, ld))


def color_text(m, g, L):
    names = PR["ledColorNames"]
    if m["ledColors"]:
        return " / ".join(names[c][L] for c in m["ledColors"])
    return " / ".join(g["ledColorsCatalog"]) if g["ledColorsCatalog"] else ""


def power_text(m, L):
    if m["powerType"] == "unconfirmed":
        return PR["powerTypes"]["unconfirmed"][L]
    return PR["powerTypes"][m["powerType"]][L]


def build_detail(L, g, prev_g, next_g):
    p = P(L, "products/%s.html" % g["id"]); D = TXT[L]["detail"]
    cat = CAT[g["category"]]
    name = ln(g, "name", L)
    list_page = cat["page"]
    trail = [(p.t("common.home"), "index.html"), (p.t("nav.products"), "road-stud.html"), (ln(cat, "name", L), list_page), (name, p.path)]
    models = g["models"]
    # 이미지 스테이지 (공통 이미지는 한 번만 출력)
    stages, seen = [], {}
    for m in models:
        src = m["images"][0]["src"]
        seen.setdefault(src, {"im": m["images"][0], "models": []})["models"].append(m)
    for i, (src, s) in enumerate(seen.items()):
        mnames = ", ".join(x["model"] for x in s["models"])
        note = '<span>%s</span>' % e(D["sharedImage"]) if len(s["models"]) > 1 else "<span></span>"
        stages.append('<figure data-stage="%s"%s><div class="stage">%s</div><figcaption class="stage-cap"><span class="num">%s</span>%s</figcaption></figure>'
                      % (" ".join(x["id"] for x in s["models"]), "" if i == 0 else " hidden",
                         img(p.a(src), "%s %s" % (name, mnames), s["im"]["w"], s["im"]["h"], lazy=i > 0), e(mnames), note))
    tabs = ""
    if len(models) > 1:
        tabs = '<div class="pd-block"><p class="block-title" id="mt">%s</p><div class="model-tabs" role="tablist" aria-labelledby="mt">%s</div></div>' % (
            e(D["selectModel"]), "".join(
                '<button type="button" class="model-tab" role="tab" id="tab-%s" aria-controls="panel-%s" aria-selected="%s" data-model="%s" data-name="%s"%s>%s<small>%s</small></button>'
                % (m["id"], m["id"], "true" if i == 0 else "false", m["id"], e(m["model"]), "" if i == 0 else ' tabindex="-1"', e(m["model"]),
                   e(variant_label(m, g, L))) for i, m in enumerate(models)))
    panels = ""
    for i, m in enumerate(models):
        review = m["verificationStatus"] != "verified" and SHOW_NOTES
        badge = ' <span class="badge-review">%s</span>' % e(p.t("common.review")) if review else ""
        keys = [(p.t("common.model"), '<span class="big">%s</span>%s' % (e(m["model"]), badge)), (p.t("common.productName"), e(ln(m, "name", L))),
                (p.t("common.procurementId"), '<span class="pid num">%s</span>' % e(m["procurementId"])), (p.t("common.type"), e(power_text(m, L)))]
        ct = color_text(m, g, L)
        if ct:
            keys.append((p.t("common.ledColor"), e(ct)))
        spec = "".join("<tr><th scope=\"row\">%s</th><td>%s</td></tr>" % (e(p.t("spec." + s["key"])), e(s[L]).replace(" / ", "<br>")) for s in m["specifications"])
        note = ""
        if review:
            lis = []
            ms = m["modelSource"]
            if ms["specTable"] != ms["imageCaption"]:
                lis.append(D["reviewModel"].replace("{a}", ms["specTable"]).replace("{b}", ms["imageCaption"]))
            if m.get("powerTypeCatalog"):
                lis.append(D["reviewPower"].replace("{a}", m["powerTypeCatalog"]["typeField"][L]).replace("{b}", m["powerTypeCatalog"]["powerSupplyRow"][L]))
            if not lis:
                lis.append(D["reviewGeneric"])
            note = '<div class="note pd-block"><h3>%s</h3><ul>%s</ul></div>' % (e(D["reviewTitle"]), "".join("<li>%s</li>" % e(x) for x in lis))
        panels += ('<div class="pd-panel" id="panel-%s" data-panel="%s"%s%s><dl class="keys pd-block">%s</dl>'
                   '<table class="spec pd-block"><caption>%s — %s</caption><tbody>%s</tbody></table>%s</div>'
                   % (m["id"], m["id"], ' role="tabpanel" aria-labelledby="tab-%s"' % m["id"] if len(models) > 1 else "", "" if i == 0 else " hidden",
                      "".join("<div><dt>%s</dt><dd>%s</dd></div>" % (e(a), b) for a, b in keys), e(D["specTitle"]), e(m["model"]), spec, note))
    subject = D["mailSubject"].replace("{name}", name)
    first_subject = subject.replace("{model}", models[0]["model"])
    sub_line = '<p class="pd-sub en" lang="en">%s</p>' % e(g["nameEn"]) if L == "ko" else ""
    catline = ln(cat, "name", L) + (" · " + sub_name(g, L) if g["category"] == "lighting" else "")
    crumbs = "".join('<li>%s</li>' % ('<a href="%s">%s</a>' % (p.u(h), e(n)) if i < len(trail) - 1 else '<span aria-current="page">%s</span>' % e(n))
                     for i, (n, h) in enumerate(trail))
    body = '<div class="pd-top"><div class="wrap"><nav aria-label="breadcrumb"><ol class="crumb">%s</ol></nav></div></div>' % crumbs
    body += """<section class="sec sec-tight"><div class="wrap"><div class="pd" data-pd>
<div class="pd-stage">{stages}</div>
<div class="pd-info"><p class="pd-cat">{src}</p><h1>{name}</h1>{sub}{tabs}{panels}
<div class="pd-cta"><div class="btn-row"><a class="btn btn-solid" data-inquiry data-mailto="{mail}" data-subject="{subj}" href="mailto:{mail}?subject={fs}">{inq}</a>
<a class="btn btn-line btn-plain" href="tel:{telHref}">{call} {tel}</a></div><p class="fine">{pn}</p></div>
</div></div></div></section>""".format(stages="".join(stages), src=e(catline + " · " + p.t("common.catalogPage", p=g["sourceCatalogPage"])), name=e(name), sub=sub_line,
                                       tabs=tabs, panels=panels, mail=CO["email"], subj=e(subject), fs=quote(first_subject), inq=e(D["inquiry"]),
                                       telHref=CO["telIntl"].replace("-", ""), call=e(D["call"]), tel=e(CO["tel"] if L == "ko" else CO["telIntl"]), pn=e(D["priceNote"]))
    # 제품 특징
    desc = ln(g, "description", L)
    notes = ""
    if g.get("pendingDescription") and SHOW_NOTES:
        notes += '<div class="note" style="margin-top:24px"><h3>%s</h3><p class="fine">%s</p></div>' % (e(D["pendingTitle"]), e(D["pendingBody"]))
    if "I-05" in g["issueRefs"] and SHOW_NOTES:
        notes += '<div class="note" style="margin-top:24px"><h3>%s</h3><p class="fine">%s</p></div>' % (e(D["reviewTitle"]), e(D["reviewGroup40"]))
    if desc or notes:
        body += """<section class="sec sec-tight sec-ivory"><div class="wrap"><div class="feat"><div><p class="eyebrow">FEATURES</p><h2 class="h2">{ft}</h2></div>
<div>{ul}{notes}</div></div></div></section>""".format(ft=e(D["featuresTitle"]), ul='<ul class="feat-list">%s</ul>' % "".join("<li>%s</li>" % e(x) for x in desc) if desc else "",
                                                     notes=notes.replace('class="note"', 'class="note" style="background:#fff"') if not desc else notes)
    # 모델 비교
    if len(models) > 1:
        keys = [k for k in ("powerSupply", "materials", "size", "powerConsumption") if len({next((s[L] for s in m["specifications"] if s["key"] == k), "") for m in models}) > 1]
        if not keys:
            keys = ["size"]
        head = "".join("<th scope=\"col\">%s</th>" % e(x) for x in [p.t("common.model"), p.t("common.procurementId"), p.t("common.type"), p.t("common.ledColor")] + [p.t("spec." + k) for k in keys])
        trs = ""
        for m in models:
            vals = "".join("<td>%s</td>" % e(next((s[L] for s in m["specifications"] if s["key"] == k), "–")) for k in keys)
            trs += ('<tr data-row="%s"><th scope="row"><button type="button" data-pick="%s">%s</button></th><td class="num">%s</td><td>%s</td><td>%s</td>%s</tr>'
                    % (m["id"], m["id"], e(m["model"]), e(m["procurementId"]), e(power_text(m, L)), e(color_text(m, g, L) or "–"), vals))
        body += """<section class="sec sec-tight"><div class="wrap" data-pd-cmp><div class="sec-head sec-head-stack"><p class="eyebrow">MODELS</p><h2 class="h2">{ct}</h2></div>
<div class="cmp-wrap" tabindex="0" role="region" aria-label="{ct}"><table class="cmp"><thead><tr>{head}</tr></thead><tbody>{trs}</tbody></table></div></div></section>""".format(
            ct=e(D["compareTitle"]), head=head, trs=trs)
    # 관련 설치사례
    if g["installationCaseIds"]:
        ids = g["installationCaseIds"]
        show = ids[:8]
        rel = "".join('<a href="%s" data-lb="rel" data-cap="%s" data-alt="%s">%s</a>'
                      % (p.a(IMAP[i]["image"]), e("%s · %s" % (ln(SCENE[IMAP[i]["scene"]], "name", L), p.t("common.catalogPage", p=IMAP[i]["sourceCatalogPage"]))),
                         e(ln(IMAP[i], "alt", L)), inst_img(p, i, thumb=True)) for i in show)
        q = "?category=road-stud" if g["category"] == "road-stud" else "?scene=" + IMAP[ids[0]]["scene"]
        body += """<section class="sec sec-tight"><div class="wrap"><div class="sec-head"><div><p class="eyebrow">APPLICATIONS</p><h2 class="h2">{rt}</h2></div><p class="lead" style="font-size:.9375rem">{rn}</p></div>
<div class="rel-grid">{rel}</div><div class="sec-foot"><a class="arrow-link" href="{u}">{va} ({n})</a></div></div></section>""".format(
            rt=e(D["relatedTitle"]), rn=e(D["relatedNoteRoad"] if g["category"] == "road-stud" else D["relatedNoteLighting"]), rel=rel,
            u=p.u("applications.html" + q), va=e(p.t("common.viewAll")), n=e(p.t("common.countPhotos", n=len(ids))))
    # 이전/다음
    nav = '<a class="prev" href="%s"><small>← %s</small><strong>%s</strong></a>' % (p.u("products/%s.html" % prev_g["id"]), e(D["prevProduct"]), e(ln(prev_g, "name", L))) if prev_g else "<span></span>"
    nav += '<a class="list" href="%s">%s</a>' % (p.u(list_page), e(D["backToList"]))
    nav += '<a class="next" href="%s"><small>%s →</small><strong>%s</strong></a>' % (p.u("products/%s.html" % next_g["id"]), e(D["nextProduct"]), e(ln(next_g, "name", L))) if next_g else "<span></span>"
    body += '<section class="sec-tight" style="padding-top:0"><div class="wrap"><nav class="pd-nav" aria-label="%s">%s</nav></div></section>' % (e(p.t("nav.products")), nav)
    body += cta_band(p)
    # 구조화 데이터 (가격·리뷰·재고 없음)
    def abs_img(src):
        return (SITE_URL + src) if SITE_URL else p.a(src)
    variants = [{"@type": "Product", "name": "%s %s" % (ln(m, "name", L), m["model"]), "model": m["model"], "sku": m["model"], "image": abs_img(m["images"][0]["src"]),
                 "identifier": {"@type": "PropertyValue", "propertyID": "KONEPS", "name": t(L, "common.procurementId"), "value": m["procurementId"]},
                 "additionalProperty": [{"@type": "PropertyValue", "name": t(L, "spec." + s["key"]), "value": s[L]} for s in m["specifications"]]} for m in models]
    pld = {"@context": "https://schema.org", "@type": "ProductGroup", "name": name, "productGroupID": g["id"], "category": ln(cat, "name", L),
           "brand": {"@type": "Brand", "name": "GreenOne"}, "manufacturer": {"@type": "Organization", "name": ln(CO, "name", L)},
           "image": abs_img(group_image(g)["src"]), "hasVariant": variants}
    if desc:
        pld["description"] = " ".join(x.rstrip(".") + "." for x in desc)
    title = "%s | %s | %s" % (name, " · ".join(m["model"] for m in models[:3]), D["titleSuffix"])
    mdesc = ("%s — %s. %s %s." % (name, ", ".join(m["model"] for m in models), p.t("common.procurementId"), ", ".join(m["procurementId"] for m in models)))[:300]
    write(p, layout(p, title, mdesc, body, "products", "roadStud" if g["category"] == "road-stud" else "lighting", jsonld(pld) + crumb_ld(p, trail), og_image="assets/img/brand/og.jpg"))


def variant_label(m, g, L):
    """모델 선택 버튼의 보조 라벨 — 타입 또는 색상/전력 등 모델 간 차이를 짧게 표시."""
    parts = []
    if len(g["powerTypes"]) > 1:
        parts.append(POWER_SHORT.get(m["powerType"], (PR["powerTypes"]["unconfirmed"]["ko"], PR["powerTypes"]["unconfirmed"]["en"]))[0 if L == "ko" else 1])
    if m["ledColors"] and len({tuple(x["ledColors"]) for x in g["models"]}) > 1:
        parts.append(" / ".join(PR["ledColorNames"][c][L] for c in m["ledColors"]))
    pc = next((s[L] for s in m["specifications"] if s["key"] == "powerConsumption"), "")
    if pc and len({next((s[L] for s in x["specifications"] if s["key"] == "powerConsumption"), "") for x in g["models"]}) > 1:
        parts.append(pc)
    if not parts:
        parts.append(ln(m, "name", L))
    return " · ".join(parts)


# ───────────────────────── APPLICATIONS / RESOURCES / CONTACT ─────────────────────────
def build_applications(L):
    p = P(L, "applications.html"); A = TXT[L]["applications"]
    n = len(INS["items"])
    trail = [(p.t("common.home"), "index.html"), (A["h1"], "applications.html")]
    cats = '<button type="button" class="ap-cat" data-cat-btn="" aria-pressed="true">%s<span class="num">%d</span></button>' % (e(p.t("common.all")), n)
    for c in PR["categories"]:
        cats += '<button type="button" class="ap-cat" data-cat-btn="%s" aria-pressed="false">%s<span class="num">%d</span></button>' % (
            c["id"], e(ln(c, "name", L)), sum(1 for i in INS["items"] if i["category"] == c["id"]))
    scenes = '<button type="button" class="chip" data-scene-btn="" aria-pressed="true">%s</button>' % e(p.t("common.all"))
    scenes += "".join('<button type="button" class="chip" data-scene-btn="%s" data-cat="%s" aria-pressed="false" hidden>%s</button>'
                      % (s["id"], s["category"], e(ln(s, "name", L).split(" (")[0] if s["id"] == "others" else ln(s, "name", L))) for s in INS["scenes"])
    figs = ""
    for it in INS["items"]:
        s = SCENE[it["scene"]]
        sname = ln(s, "name", L)
        if it["category"] == "road-stud":
            link = p.u("road-stud.html")
        else:
            link = p.u("products/%s.html" % it["relatedGroupIds"][0])
        cap = "%s · %s" % (sname, p.t("common.catalogPage", p=it["sourceCatalogPage"]))
        figs += ('<figure class="ap" data-fig data-cat="%s" data-scene="%s"><a href="%s" data-lb="ap" data-cap="%s" data-alt="%s" data-link="%s" data-link-text="%s">%s</a>'
                 '<figcaption><b>%s</b><span>%s</span></figcaption></figure>'
                 % (it["category"], it["scene"], p.a(it["image"]), e(cap), e(ln(it, "alt", L)), link, e(A["viewProduct"]),
                    inst_img(p, it["id"], thumb=True), e(sname.split(" (")[0] if it["scene"] == "others" else sname), e(p.t("common.catalogPage", p=it["sourceCatalogPage"]))))
    body = page_hero(p, A["eyebrow"], A["h1"], A["lead"], trail, inst_img(p, "p47-1", lazy=False)) + """
<section class="sec sec-tight"><div class="wrap" data-ap>
<div class="ap-bar"><div class="ap-cats" role="group" aria-label="{h1}">{cats}</div>
<div class="tb-row" data-scene-row hidden><span class="tb-label">{sc}</span><div class="chips">{scenes}</div></div></div>
<div class="masonry">{figs}</div>
<p class="fine" style="margin-top:32px">{note}</p>
</div></section>""".format(h1=e(A["h1"]), cats=cats, sc=e(A["scene"]), scenes=scenes, figs=figs, note=e(A["note"])) + cta_band(p)
    write(p, layout(p, A["title"], A["description"].replace("{n}", str(n)), body, "applications", "", crumb_ld(p, trail)))


def build_resources(L):
    p = P(L, "resources.html"); R = TXT[L]["resources"]
    trail = [(p.t("common.home"), "index.html"), (R["h1"], "resources.html")]
    size = os.path.getsize(os.path.join(ROOT, CO["catalogFile"].replace("/", os.sep))) / 1048576
    body = page_hero(p, R["eyebrow"], R["h1"], R["lead"], trail) + """
<section class="sec sec-tight"><div class="wrap">
<article class="res-card"><div class="res-cover">{cover}<div class="res-cover-logo">{logo}</div></div>
<div class="res-body"><p class="eyebrow">PRODUCT CATALOG</p><h2>{ct}</h2><p>{cd}</p><p class="res-meta">{cm}</p>
<a class="btn btn-solid btn-dl" href="{cat}" download>{dl}</a></div></article>
<div class="res-rows">
<div class="res-row"><h2 class="h3">{t1}</h2><p>{d1}</p><a class="btn btn-line btn-sm" href="{u1}">{c1}</a></div>
<div class="res-row"><h2 class="h3">{t2}</h2><p>{d2}</p><a class="btn btn-line btn-sm" href="{u2}">{c2}</a></div>
</div></div></section>""".format(cover=img(p.a("assets/img/hero/bridge-night-900.webp"), TXT[L]["home"]["hero"]["imageAlt"], 900, 798),
                                 logo=img(p.a("assets/img/brand/logo.png"), "GreenOne", 750, 140), ct=e(R["catalogTitle"]), cd=e(R["catalogDesc"]),
                                 cm=e(R["catalogMeta"].replace("{size}", "%.1f MB" % size)), cat=p.a(CO["catalogFile"]), dl=e(R["download"]),
                                 t1=e(R["certTitle"]), d1=e(R["certDesc"]), u1=p.u("certificates.html"), c1=e(R["certCta"]),
                                 t2=e(R["requestTitle"]), d2=e(R["requestDesc"]), u2=p.u("contact.html"), c2=e(p.t("nav.contact"))) + cta_band(p)
    write(p, layout(p, R["title"], R["description"], body, "resources", "", crumb_ld(p, trail)))


def build_contact(L):
    p = P(L, "contact.html"); C = TXT[L]["contact"]
    trail = [(p.t("common.home"), "index.html"), (C["h1"], "contact.html")]
    tel = CO["tel"] if L == "ko" else CO["telIntl"]
    addr = "(%s) %s" % (CO["postalCode"], CO["addressKo"]) if L == "ko" else "%s (%s)" % (CO["addressEn"], CO["postalCode"])
    body = page_hero(p, C["eyebrow"], C["h1"], C["lead"], trail) + """
<section class="sec sec-tight"><div class="wrap"><div class="ct-grid">
<div>
<div class="ct-block"><h2 class="block-title">{dt}</h2><a class="ct-big" href="tel:{telHref}">{tel}</a><p>{dd}</p></div>
<div class="ct-block"><h2 class="block-title">{et}</h2><a class="ct-mail" href="mailto:{mail}">{mail}</a><p>{ed}</p></div>
<div class="ct-block"><h2 class="block-title">{it}</h2><dl class="facts"><div><dt>{faxL}</dt><dd>{fax}</dd></div><div><dt>{addrL}</dt><dd>{addr}</dd></div></dl>
<p style="margin-top:22px"><a class="arrow-link" href="{lu}">{lc}</a></p></div>
</div>
<form class="form" data-mailform data-email="{mail}" data-prefix="{prefix}" novalidate>
<h2>{ft}</h2><p class="fine">{fn}</p>
<div class="form-grid">
<div class="field full"><label for="f-type2">{fType}</label><select id="f-type2" name="type"><option>{o1}</option><option>{o2}</option><option>{o3}</option></select></div>
<div class="field"><label for="f-name">{fName}</label><input id="f-name" name="name" data-line="{fName}" autocomplete="name"></div>
<div class="field"><label for="f-company">{fCompany}</label><input id="f-company" name="company" data-line="{fCompany}" autocomplete="organization"></div>
<div class="field"><label for="f-phone">{fPhone}</label><input id="f-phone" name="phone" data-line="{fPhone}" type="tel" autocomplete="tel"></div>
<div class="field"><label for="f-product">{fProduct}</label><input id="f-product" name="product" data-line="{fProduct}"></div>
<div class="field full"><label for="f-message">{fMessage}</label><textarea id="f-message" name="message" required></textarea></div>
</div>
<button type="submit" class="btn btn-solid">{fs}</button>
<p class="fine form-fallback">{fb}</p>
</form>
</div></div></section>""".format(dt=e(C["domesticTitle"]), telHref=CO["telIntl"].replace("-", ""), tel=e(tel), dd=e(C["domesticDesc"]), et=e(C["exportTitle"]), mail=CO["email"],
                                 ed=e(C["exportDesc"]), it=e(C["infoTitle"]), faxL=e(p.t("common.fax")), fax=e(CO["fax"] if L == "ko" else CO["faxIntl"]),
                                 addrL=e(p.t("common.address")), addr=e(addr), lu=p.u("location.html"), lc=e(C["locationCta"]), prefix=e(C["subjectPrefix"]),
                                 ft=e(C["formTitle"]), fn=e(C["formNote"]), fType=e(C["fType"]), o1=e(C["fTypeQuote"]), o2=e(C["fTypeExport"]), o3=e(C["fTypeEtc"]),
                                 fName=e(C["fName"]), fCompany=e(C["fCompany"]), fPhone=e(C["fPhone"]), fProduct=e(C["fProduct"]), fMessage=e(C["fMessage"]),
                                 fs=e(C["fSubmit"]), fb=e(C["fFallback"].replace("{email}", CO["email"])))
    write(p, layout(p, C["title"], C["description"], body, "contact", "", jsonld(org_ld(L)) + crumb_ld(p, trail)))


def build_root():
    canon = '<link rel="canonical" href="%sko/">' % SITE_URL if SITE_URL else ""
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write("""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>그린원 주식회사 | GreenOne Co., Ltd.</title>
<meta name="description" content="그린원 주식회사 — 도로표지병 · LED 경관조명 전문 제조기업 / GreenOne Co., Ltd. — LED road stud and LED landscape lighting manufacturer.">
%s
<link rel="icon" href="favicon.ico" sizes="any">
<script>(function(){var l=(navigator.language||"ko").toLowerCase();location.replace(l.indexOf("ko")===0?"ko/":"en/");})();</script>
<noscript><meta http-equiv="refresh" content="0; url=ko/"></noscript>
<style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#F6F5EF;color:#202824;font-family:-apple-system,"Malgun Gothic",sans-serif}main{text-align:center;padding:24px}img{width:220px;max-width:70vw;height:auto}a{display:inline-block;margin:28px 8px 0;padding:14px 26px;border:1px solid #0C361C;color:#0C361C;text-decoration:none;font-weight:600}</style>
</head>
<body><main><img src="assets/img/brand/logo.png" alt="GreenOne 그린원 주식회사" width="750" height="140"><p><a href="ko/" lang="ko">한국어</a><a href="en/" lang="en">English</a></p></main></body>
</html>
""" % canon)
    with open(os.path.join(ROOT, "404.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write("""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>페이지를 찾을 수 없습니다 | Page not found — GreenOne</title>
<style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#F6F5EF;color:#202824;font-family:-apple-system,"Malgun Gothic",sans-serif}main{text-align:center;padding:24px}h1{font-size:28px;margin:0 0 8px}p{color:#5C655F;margin:0}a{display:inline-block;margin:28px 8px 0;padding:14px 26px;border:1px solid #0C361C;color:#0C361C;text-decoration:none;font-weight:600}.n{font-size:88px;font-weight:300;color:#D9D7CB;line-height:1}</style>
</head>
<body><main><div class="n">404</div><h1>페이지를 찾을 수 없습니다</h1><p>Page not found — the page may have been moved or deleted.</p>
<p><a id="ko" href="ko/">홈으로 이동</a><a id="en" href="en/">Go to home</a></p></main>
<script>(function(){var b=/github\\.io$/.test(location.hostname)?"/"+location.pathname.split("/")[1]+"/":"/";document.getElementById("ko").href=b+"ko/";document.getElementById("en").href=b+"en/";})();</script>
</body>
</html>
""")
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write("User-agent: *\nAllow: /\n" + ("Sitemap: %ssitemap.xml\n" % SITE_URL if SITE_URL else ""))
    sm = os.path.join(ROOT, "sitemap.xml")
    if SITE_URL:
        today = datetime.date.today().isoformat()
        urls = []
        for L, path in OUT:
            loc = SITE_URL + L + "/" + path.replace("index.html", "")
            alt = "".join('<xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (x, SITE_URL + x + "/" + path.replace("index.html", "")) for x in ("ko", "en"))
            urls.append("<url><loc>%s</loc><lastmod>%s</lastmod>%s</url>" % (loc, today, alt))
        with open(sm, "w", encoding="utf-8", newline="\n") as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")
    elif os.path.exists(sm):
        os.remove(sm)
    open(os.path.join(ROOT, ".nojekyll"), "w").close()


def main():
    for L in ("ko", "en"):
        build_home(L)
        build_about(L)
        build_list(L, "road-stud", "road-stud.html", "p14-3", "roadStud")
        build_list(L, "lighting", "lighting.html", "p43-3", "lighting")
        for c in ("road-stud", "lighting"):
            gs = [g for g in GROUPS if g["category"] == c]
            for i, g in enumerate(gs):
                build_detail(L, g, gs[i - 1] if i else None, gs[i + 1] if i + 1 < len(gs) else None)
        build_applications(L)
        build_resources(L)
        build_contact(L)
    build_root()
    with open(os.path.join(ROOT, "tools", "pages.json"), "w", encoding="utf-8") as f:  # tools/sweep.html 점검 대상 목록
        json.dump(["%s/%s" % o for o in OUT], f, indent=0)
    n_models = sum(len(g["models"]) for g in GROUPS)
    print("pages: %d (ko %d / en %d) | groups %d | models %d | installations %d | certificates %d | site url: %s"
          % (len(OUT), sum(1 for o in OUT if o[0] == "ko"), sum(1 for o in OUT if o[0] == "en"), len(GROUPS), n_models, len(INS["items"]), len(CERT["items"]),
             SITE_URL or "(not set: canonical/sitemap skipped)"))


if __name__ == "__main__":
    main()
