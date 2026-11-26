# -*- coding: utf-8 -*-
"""그린원 카탈로그 PDF → 웹용 이미지 추출 스크립트.

사용법:
    python tools/extract_images.py "<카탈로그 PDF>" "<로고 PNG>" "<로고 PDF(벡터)>"

- 제품 이미지 : PDF 내장 이미지(투명 마스크 포함)를 그대로 꺼내 여백만 잘라 WebP 로 저장
- 설치사례    : 카탈로그 지면에서 사진 한 장 단위 영역만 고해상도 렌더링
- 인증서/메인 : 내장 원본 이미지 추출 (지면의 글자·로고가 포함되지 않음)
매핑(어떤 xref/영역이 어떤 모델·사례인지)은 아래 표에 명시되어 있으며 CATALOG_MAPPING.md 와 동일하다.
"""
import io, json, os, sys
import pymupdf
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "assets", "img")

# ── 제품 이미지: (PDF 페이지, 출력 경로, [xref...]) — xref 가 여러 개면 지면 배치대로 합성 ──
PRODUCTS = [
    (3, "products/rs-138-battery/hor-138wb", [39]),
    (3, "products/rs-138-battery/hor-138yb", [35]),
    (3, "products/rs-138-hybrid/hor-138wh", [47]),
    (3, "products/rs-138-hybrid/hor-138yh", [43]),
    (4, "products/rs-138-solar/hor-138ws", [58]),
    (4, "products/rs-138-solar/hor-138ys", [54]),
    (4, "products/rs-113-module/hor-wbi", [64]),
    (4, "products/rs-113-module/hor-ybi", [70]),
    (4, "products/rs-113-module/hor-113whi", [62]),
    (4, "products/rs-113-module/hor-113yhi", [68]),
    (4, "products/rs-113-module/hor-113wsi", [78]),
    (4, "products/rs-113-module/hor-113ysi", [74]),
    (5, "products/rs-125-electric/hor-wc125", [89]),
    (5, "products/rs-125-electric/hor-yc125", [85]),
    (5, "products/rs-196-electric/hor-wc196", [97]),
    (5, "products/rs-196-electric/hor-yc196", [93]),
    (9, "products/lt-line-bar/1000ba-15h", [166]),
    (9, "products/lt-line-bar/1000ba-15b", [170]),
    (9, "products/lt-line-bar/1000fl-10", [174]),
    (10, "products/lt-wall/ll180-s", [181]),
    (10, "products/lt-wall/109wa", [185]),
    (11, "products/lt-curb/hol-19-c-1", [198]),
    (11, "products/lt-curb/hol-155-h", [202]),
    (11, "products/lt-curb/hol-155-b", [206]),
    (12, "products/lt-logo-projector/hol-ll50w-cu", [228]),
    (12, "products/lt-logo-projector/hol-ll80w-cu", [230]),
    (12, "products/lt-logo-projector/hol-ll100w-cu", [226]),
    (13, "products/lt-park/hol-ll80w-butterfly", [241]),
    (13, "products/lt-park/hol-ll80w-seagull", [237]),
    (14, "products/lt-security-50-30/hol-50s", [253]),
    (14, "products/lt-security-50-30/hol-ll30s-3m", [257]),
    (15, "products/lt-security-25/hol-25s", [267]),
    (15, "products/lt-accent/hol-130-b", [271]),
    (15, "products/lt-accent/hol-138s", [275]),
    (15, "products/lt-accent/hol-275-10", [279]),
    (16, "products/lt-floor-square/hol-222-60s", [290, 304, 294, 292, 296]),
    (16, "products/lt-floor-square/hol-118-60s", [286, 306, 308, 310, 312]),
    (17, "products/lt-floor-round/hol-120-60s", [336, 346, 323, 327, 331]),
    (17, "products/lt-floor-round/hol-96-47s", [344, 350, 352, 319, 321]),
    (17, "products/lt-floor-round/hol-67-30s", [340, 348, 325, 329, 333]),
    (18, "products/lt-fence-square/hol-157-s-h", [359]),
    (18, "products/lt-fence-square/hol-157-b", [363]),
    (19, "products/lt-fence-round/hol-110-s", [376]),
    (19, "products/lt-fence-round/hol-110-h", [380]),
    (19, "products/lt-fence-round/hol-110-c", [384]),
    (20, "products/lt-bollard/hol-800bol", [404]),
    (20, "products/lt-bollard/hol-300bol", [408]),
    (20, "products/lt-bollard/hol-110bol", [414]),
    (20, "products/lt-bollard/hol-150bol", [412]),
    (21, "products/lt-linear/hol-1000ba-15", [428]),
    (21, "products/lt-linear/hol-1000ba-7", [430]),
    (22, "products/lt-linear-flood/hol-1000ba-f", [437]),
    (23, "products/lt-flood-125/hol-125c", [452]),
    (24, "products/lt-flood-160-217/hol-160c-36f", [459]),
    (24, "products/lt-flood-160-217/hol-160c-42f", [463]),
    (24, "products/lt-flood-160-217/hol-217c", [467]),
    (25, "products/lt-inground-round/hol-ll100-c12", [477]),
    (25, "products/lt-inground-round/hol-ll140-c18", [481]),
    (25, "products/lt-inground-round/hol-ll180-c36", [485]),
    (25, "products/lt-inground-round/hol-ll220-c54-c72", [489]),
    (26, "products/lt-inground-linear/hol-ll1010-c15", [505]),
    (26, "products/lt-inground-linear/hol-ll1010-c36", [509]),
    (26, "products/lt-inground-linear/hol-ll1010-c72", [513]),
    (26, "products/lt-column/hol-2000-120", [517]),
]

# ── 설치사례: PDF 페이지 → (인쇄 페이지, [사진 영역(pt)...]) ──
L3 = [(44, 152, 291, 471), (293, 152, 540, 471), (44, 476, 540, 797)]
ROWS = [(652, 151, 1145, 365), (652, 367, 1145, 581), (652, 583, 1145, 798)]
T2B1 = [(652, 152, 897, 472), (900, 152, 1145, 472), (652, 476, 1145, 797)]
T1B2 = [(652, 152, 1145, 472), (652, 476, 897, 797), (900, 476, 1145, 797)]
INSTALL = [
    (6, 10, L3),
    (6, 11, [(651, 152, 933, 797), (935, 152, 1146, 471), (935, 476, 1146, 797)]),
    (7, 12, L3),
    (7, 13, T1B2),
    (8, 14, L3),
    (8, 15, [(652, 151, 1145, 472), (652, 476, 1145, 798)]),
    (9, 17, ROWS),
    (10, 19, T1B2),
    (11, 21, T2B1),
    (12, 23, [(652, 151, 1145, 365), (652, 368, 897, 580), (901, 368, 1145, 580),
              (652, 584, 897, 796), (901, 584, 1145, 796)]),
    (13, 25, ROWS),
    (14, 27, T2B1),
    (16, 31, T2B1),
    (17, 33, T1B2),
    (18, 35, T2B1),
    (19, 37, ROWS),
    (20, 39, T1B2),
    (21, 41, ROWS),
    (22, 43, T2B1),
    (23, 45, [(652, 152, 1145, 472), (652, 476, 1145, 797)]),
    (24, 47, T1B2),
    (25, 49, ROWS),
]

CERTS = [  # (xref, id) — 카탈로그 3P 배치 순서
    (16, "factory-registration"), (20, "direct-production-road-stud"),
    (26, "direct-production-led-lighting"), (28, "construction-business"),
    (22, "women-owned-business"), (24, "sme"), (18, "rnd-department"),
]


def save_webp(im, rel, quality=82, max_side=None, lossless=False):
    path = os.path.join(IMG, rel + ".webp")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if max_side and max(im.size) > max_side:
        r = max_side / max(im.size)
        im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
    im.save(path, "WEBP", quality=quality, method=6, lossless=lossless)
    return im.size


def xref_rgba(doc, xref):
    """내장 이미지를 (소프트마스크 포함) RGBA 로 꺼낸다."""
    info = doc.extract_image(xref)
    pix = pymupdf.Pixmap(doc, xref)
    if pix.colorspace and pix.colorspace.n != 3:
        pix = pymupdf.Pixmap(pymupdf.csRGB, pix)
    if pix.alpha:
        pix = pymupdf.Pixmap(pix, 0)
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    sm = info.get("smask", 0)
    if sm:
        m = pymupdf.Pixmap(doc, sm)
        mask = Image.frombytes("L", (m.width, m.height), m.samples)
        if mask.size != im.size:
            mask = mask.resize(im.size, Image.LANCZOS)
        im = im.convert("RGBA"); im.putalpha(mask)
    else:
        im = im.convert("RGBA")
    return im


def main(pdf, logo_png, logo_pdf):
    doc = pymupdf.open(pdf)
    manifest = {"products": {}, "installations": [], "certificates": {}}

    # 제품
    for pn, rel, xrefs in PRODUCTS:
        page = doc[pn - 1]
        boxes = {i["xref"]: i["bbox"] for i in page.get_image_info(xrefs=True)}
        if len(xrefs) == 1:
            im = xref_rgba(doc, xrefs[0])
        else:
            main_im = xref_rgba(doc, xrefs[0])
            b0 = boxes[xrefs[0]]
            s = main_im.width / (b0[2] - b0[0])  # px per pt (대표 이미지 원본 해상도 기준)
            x0 = min(boxes[x][0] for x in xrefs); y0 = min(boxes[x][1] for x in xrefs)
            x1 = max(boxes[x][2] for x in xrefs); y1 = max(boxes[x][3] for x in xrefs)
            canvas = Image.new("RGBA", (round((x1 - x0) * s), round((y1 - y0) * s)), (0, 0, 0, 0))
            for x in xrefs:
                b = boxes[x]
                part = xref_rgba(doc, x).resize((round((b[2] - b[0]) * s), round((b[3] - b[1]) * s)), Image.LANCZOS)
                canvas.alpha_composite(part, (round((b[0] - x0) * s), round((b[1] - y0) * s)))
            im = canvas
        bb = im.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
        if bb:
            im = im.crop(bb)
        size = save_webp(im, rel, quality=90)
        manifest["products"][rel] = {"w": size[0], "h": size[1], "pdfPage": pn, "xrefs": xrefs}

    # 설치사례
    for pn, cp, rects in INSTALL:
        page = doc[pn - 1]
        for n, r in enumerate(rects, 1):
            clip = pymupdf.Rect(r[0] + 0.6, r[1] + 0.6, r[2] - 0.6, r[3] - 0.6)
            pix = page.get_pixmap(matrix=pymupdf.Matrix(3.2, 3.2), clip=clip, alpha=False)
            im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
            iid = "p%02d-%d" % (cp, n)
            size = save_webp(im, "installations/" + iid, quality=80, max_side=1600)
            save_webp(im, "installations/thumb/" + iid, quality=74, max_side=760)
            manifest["installations"].append({"id": iid, "catalogPage": cp, "pdfPage": pn, "w": size[0], "h": size[1]})

    # 인증서 (원본 397×561px — 확대 없이 저장)
    for xref, cid in CERTS:
        im = xref_rgba(doc, xref).convert("RGB")
        size = save_webp(im, "certificates/" + cid, quality=92)
        manifest["certificates"][cid] = {"w": size[0], "h": size[1]}

    # 메인 비주얼(표지 야경 원본, 글자 없음) / 회사소개 배경(3P 야경 원본)
    hero = xref_rgba(doc, 636).convert("RGB")
    save_webp(hero, "hero/bridge-night", quality=82, max_side=2000)
    save_webp(hero, "hero/bridge-night-900", quality=78, max_side=900)
    about = xref_rgba(doc, 14).convert("RGB")
    save_webp(about, "hero/city-night", quality=80, max_side=1800)
    save_webp(about, "hero/city-night-900", quality=76, max_side=900)

    # 로고: 원본 PNG 의 투명 여백만 제거
    lg = Image.open(logo_png).convert("RGBA")
    lg = lg.crop(lg.getchannel("A").getbbox())
    os.makedirs(os.path.join(IMG, "brand"), exist_ok=True)
    lg.save(os.path.join(IMG, "brand", "logo.png"), optimize=True)
    # 파비콘: 벡터 로고 PDF 의 가로형 로고에서 심볼 영역만 렌더링
    lp = pymupdf.open(logo_pdf)[0]
    pix = lp.get_pixmap(matrix=pymupdf.Matrix(12, 12), clip=pymupdf.Rect(140, 215, 222, 282), alpha=True)
    sym = Image.frombytes("RGBA", (pix.width, pix.height), pix.samples)
    sym = sym.crop(sym.getchannel("A").getbbox())
    sym.save(os.path.join(IMG, "brand", "symbol.png"), optimize=True)
    for sz, name in ((512, "icon-512.png"), (180, "apple-touch-icon.png"), (48, "favicon-48.png")):
        pad = round(sz * 0.14)
        c = Image.new("RGBA", (sz, sz), (255, 255, 255, 255))
        s2 = sym.copy(); s2.thumbnail((sz - 2 * pad, sz - 2 * pad), Image.LANCZOS)
        c.alpha_composite(s2, ((sz - s2.width) // 2, (sz - s2.height) // 2))
        c.convert("RGB").save(os.path.join(IMG, "brand", name), optimize=True)
    Image.open(os.path.join(IMG, "brand", "favicon-48.png")).save(os.path.join(ROOT, "favicon.ico"), sizes=[(16, 16), (32, 32), (48, 48)])
    # 공유 이미지(OG): 메인 야경 + 원본 로고
    og = Image.new("RGB", (1200, 630), (246, 245, 239))
    h2 = hero.copy(); r = 630 / h2.height
    h2 = h2.resize((round(h2.width * r), 630), Image.LANCZOS)
    og.paste(h2.crop((h2.width - 700, 0, h2.width, 630)), (500, 0))
    l2 = lg.copy(); l2.thumbnail((360, 200), Image.LANCZOS)
    og.paste(l2, (70, (630 - l2.height) // 2), l2)
    og.save(os.path.join(IMG, "brand", "og.jpg"), quality=88)

    with open(os.path.join(ROOT, "tools", "image_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    print("products", len(manifest["products"]), "installations", len(manifest["installations"]),
          "certificates", len(manifest["certificates"]))


if __name__ == "__main__":
    main(*sys.argv[1:4])
