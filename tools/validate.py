# -*- coding: utf-8 -*-
"""빌드 결과 검수 스크립트.  python tools/validate.py

1) 데이터 건수(제품군·모델·설치사례·인증서)와 필수 필드
2) 모든 HTML 의 내부 링크·이미지·다운로드 경로가 실제 파일로 존재하는지
3) 국문/영문 페이지 구성과 모델명·식별번호 노출이 동일한지
4) 타사(기존 참고 사이트) 정보가 남아 있지 않은지
5) 페이지별 title / description / h1 고유성
"""
import html, json, os, re, sys
from urllib.parse import unquote, urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
fail = []


def J(n):
    return json.load(open(os.path.join(ROOT, "data", n), encoding="utf-8"))


PR, INS, CERT, CO = J("products.json"), J("installations.json"), J("certificates.json"), J("company.json")
groups = PR["groups"]
models = [m for g in groups for m in g["models"]]
REQ = ["id", "category", "subcategory", "productGroup", "nameKo", "nameEn", "model", "powerType", "ledColors", "procurementId", "price", "priceBasis",
       "images", "specifications", "sourceCatalogPage", "sourcePdfPage", "verificationStatus"]
for m in models:
    for k in REQ:
        if k not in m:
            fail.append("model %s: missing field %s" % (m["id"], k))
    for im in m["images"]:
        if not os.path.exists(os.path.join(ROOT, im["src"])):
            fail.append("missing product image " + im["src"])
for g in groups:
    for k in ("descriptionKo", "descriptionEn", "installationCaseIds", "sourceCatalogPage", "sourcePdfPage", "verificationStatus"):
        if k not in g:
            fail.append("group %s: missing field %s" % (g["id"], k))
    if len(g["descriptionKo"]) != len(g["descriptionEn"]):
        fail.append("group %s: ko/en description count differs" % g["id"])
iids = {i["id"] for i in INS["items"]}
for i in INS["items"]:
    for k in ("image", "thumb"):
        if not os.path.exists(os.path.join(ROOT, i[k])):
            fail.append("missing installation image " + i[k])
for g in groups:
    for c in g["installationCaseIds"]:
        if c not in iids:
            fail.append("group %s: unknown installation %s" % (g["id"], c))
for c in CERT["items"]:
    if not os.path.exists(os.path.join(ROOT, c["image"])):
        fail.append("missing certificate image " + c["image"])


def cnt(cat):
    gs = [g for g in groups if g["category"] == cat]
    return len(gs), sum(len(g["models"]) for g in gs)


rs, lt = cnt("road-stud"), cnt("lighting")
review = [m for m in models if m["verificationStatus"] != "verified"]
print("도로표지병: 제품군 %d / 모델 %d" % rs)
print("LED 경관조명: 제품군 %d / 모델 %d" % lt)
print("전체 모델 %d (확정 %d / 확인 필요 %d)" % (len(models), len(models) - len(review), len(review)))
print("  확인 필요:", ", ".join(m["model"] for m in review))
print("설치사례 사진 %d (도로표지병 %d / LED 경관조명 %d)" % (len(INS["items"]), sum(i["category"] == "road-stud" for i in INS["items"]),
                                                  sum(i["category"] == "lighting" for i in INS["items"])))
print("인증서 %d" % len(CERT["items"]))
if (rs, lt, len(models), len(INS["items"]), len(CERT["items"])) != ((6, 16), (20, 60), 76, 66, 7):
    fail.append("counts differ from catalog checklist")
if len({m["procurementId"] for m in models}) != len(models):
    fail.append("duplicate procurement id")

# ── HTML 링크 검사 ──
pages = {}
for L in ("ko", "en"):
    for dp, _, fs in os.walk(os.path.join(ROOT, L)):
        for f in fs:
            if f.endswith(".html"):
                p = os.path.join(dp, f)
                pages[os.path.relpath(p, ROOT).replace(os.sep, "/")] = open(p, encoding="utf-8").read()
for extra in ("index.html", "404.html"):
    pages[extra] = open(os.path.join(ROOT, extra), encoding="utf-8").read()
n_links = 0
for rel, src in pages.items():
    base = os.path.dirname(os.path.join(ROOT, rel))
    for attr, url in re.findall(r'\b(href|src)="([^"]+)"', src):
        url = html.unescape(url)
        if re.match(r"^(https?:|mailto:|tel:|#|data:)", url):
            continue
        parts = urlsplit(url)
        path = unquote(parts.path)
        if not path:
            continue
        target = os.path.normpath(os.path.join(base, path))
        if os.path.isdir(target):
            target = os.path.join(target, "index.html")
        n_links += 1
        if not os.path.exists(target):
            fail.append("%s: broken %s -> %s" % (rel, attr, url))
    for srcset in re.findall(r'srcset="([^"]+)"', src):
        for part in srcset.split(","):
            u = part.strip().split(" ")[0]
            if not os.path.exists(os.path.normpath(os.path.join(base, u))):
                fail.append("%s: broken srcset -> %s" % (rel, u))
print("HTML %d개, 내부 링크·리소스 %d건 검사" % (len(pages), n_links))

# ── 국문/영문 일치 ──
ko = sorted(k[3:] for k in pages if k.startswith("ko/"))
en = sorted(k[3:] for k in pages if k.startswith("en/"))
if ko != en:
    fail.append("ko/en page sets differ: %s" % (set(ko) ^ set(en)))
for g in groups:
    for L in ("ko", "en"):
        src = pages["%s/products/%s.html" % (L, g["id"])]
        for m in g["models"]:
            if m["model"] not in src or m["procurementId"] not in src:
                fail.append("%s/products/%s.html: model %s or id missing" % (L, g["id"], m["model"]))
        if re.search(r"\d{1,3}(,\d{3})+\s*원", src) or "납품하차도" in src:
            fail.append("%s/products/%s.html: price exposed" % (L, g["id"]))
for L in ("ko", "en"):
    ap = pages[L + "/applications.html"]
    if ap.count("data-fig") != len(INS["items"]):
        fail.append(L + "/applications.html: figure count %d" % ap.count("data-fig"))
print("국문 %d쪽 / 영문 %d쪽, 제품 상세 %d쪽 × 2개 언어 모델·식별번호 노출 확인" % (len(ko), len(en), len(groups)))

# ── title / description / h1 ──
for L in ("ko", "en"):
    seen_t, seen_d = {}, {}
    for rel, src in pages.items():
        if not rel.startswith(L + "/"):
            continue
        tt = re.search(r"<title>(.*?)</title>", src).group(1)
        dd = re.search(r'<meta name="description" content="(.*?)">', src).group(1)
        h1 = re.findall(r"<h1[ >]", src)
        if len(h1) != 1:
            fail.append("%s: h1 count %d" % (rel, len(h1)))
        if tt in seen_t:
            fail.append("duplicate title: %s / %s" % (rel, seen_t[tt]))
        if dd in seen_d:
            fail.append("duplicate description: %s / %s" % (rel, seen_d[dd]))
        seen_t[tt] = rel; seen_d[dd] = rel
        for im in re.findall(r"<img\b[^>]*>", src):
            if 'alt="' not in im:
                fail.append("%s: img without alt" % rel)

# ── 타사 정보 잔존 검사 (자기 자신·문서는 제외) ──
BAN = ["ecoday", "에코데이", "김정기", "574-1770", "574-1772", "ecoday-road", "거북로", "테크피아", "ecoday-en", "haodesign", "EDBL-", "영북로", "음봉"]
hits = 0
for dp, dn, fs in os.walk(ROOT):
    dn[:] = [d for d in dn if d not in (".git", ".claude", "__pycache__")]
    for f in fs:
        if not f.lower().endswith((".html", ".css", ".js", ".json", ".xml", ".txt", ".py")):
            continue
        p = os.path.join(dp, f)
        if os.path.abspath(p) == os.path.abspath(__file__):
            continue
        s = open(p, encoding="utf-8", errors="replace").read().lower()
        for b in BAN:
            if b.lower() in s:
                hits += 1
                fail.append("타사 정보 문자열 '%s' in %s" % (b, os.path.relpath(p, ROOT)))
print("타사 정보 문자열 검사: %d건" % hits)
print("배포 URL:", CO["site"].get("siteUrl") or "미설정")

if fail:
    print("\nFAIL %d" % len(fail))
    for f in fail[:60]:
        print(" -", f)
    sys.exit(1)
print("\nALL CHECKS PASSED")
