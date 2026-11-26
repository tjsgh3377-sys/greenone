# -*- coding: utf-8 -*-
"""data/*.json 과 tools/image_manifest.json 으로 CATALOG_MAPPING.md 를 생성한다.  python tools/make_mapping.py"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = lambda *p: json.load(open(os.path.join(ROOT, *p), encoding="utf-8"))
PR, INS, CERT, MAN = J("data", "products.json"), J("data", "installations.json"), J("data", "certificates.json"), J("tools", "image_manifest.json")
PT = {"battery": "배터리형", "hybrid": "하이브리드형", "solar": "태양광형", "electric": "전기형", "unconfirmed": "확인 필요"}
out = []
w = out.append
models = [m for g in PR["groups"] for m in g["models"]]
w("# CATALOG_MAPPING — 카탈로그 ↔ 홈페이지 데이터 매칭 내역\n")
w("> 이 문서는 `python tools/make_mapping.py` 로 `data/*.json` 에서 자동 생성됩니다. 직접 수정하지 마세요.\n")
w("- 원본: `그린원 카탈로그_최종.pdf` (PDF 26쪽 = 인쇄 펼침면 26장, 인쇄 쪽번호 표지~51P)")
w("- 제품군 %d개 / 모델 %d개 / 설치사례 사진 %d장 / 인증서 %d종\n" % (len(PR["groups"]), len(models), len(INS["items"]), len(CERT["items"])))
w("## 1. 페이지 구성\n")
w("| 구분 | 인쇄 페이지 | PDF 페이지 | 홈페이지 반영 위치 |\n|---|---|---|---|")
w("| 표지 및 기업정보 | 표지 | 1 | 기업정보(`data/company.json`), 메인 비주얼(`assets/img/hero/bridge-night.webp`) |")
w("| 회사소개 및 인증서 | 2~3P | 2 | 인사말·경영이념(`data/ko.json`, `data/en.json`), 인증서 7종, 회사소개 야경(`assets/img/hero/city-night.webp`) |")
w("| 도로표지병 제품 | 4~9P | 3~5 | `ko/road-stud.html`, `ko/products/rs-*.html` (영문 동일) |")
w("| 도로표지병 설치사례 | 10~15P | 6~8 | `ko/applications.html` |")
w("| LED 경관조명 제품 및 설치사례 | 16~51P | 9~26 | `ko/lighting.html`, `ko/products/lt-*.html`, `ko/applications.html` |\n")

w("## 2. 제품 매칭 (모델 단위)\n")
w("이미지는 PDF 내장 원본(투명 마스크 포함)을 추출한 것이며 `xref` 는 PDF 내부 이미지 번호입니다. "
  "한 이미지를 여러 모델이 쓰는 경우는 카탈로그 캡션에서 공통 사용이 확인된 범위입니다.\n")
for cat in PR["categories"]:
    w("### %s (%s)\n" % (cat["nameKo"], cat["nameEn"]))
    for g in [g for g in PR["groups"] if g["category"] == cat["id"]]:
        w("#### %sP · PDF %d쪽 — %s  (`%s`)\n" % (g["sourceCatalogPage"], g["sourcePdfPage"], g["nameKo"], g["id"]))
        w("- 상세페이지: `ko/products/%s.html`, `en/products/%s.html`" % (g["id"], g["id"]))
        w("- 카탈로그 제목: %s / %s · 제품명: %s" % (g["catalogTitle"]["ko"], g["catalogTitle"]["en"], g["catalogProductName"]["ko"]))
        if g["installationCaseIds"]:
            w("- 관련 설치사례: %s" % ", ".join("`%s`" % i for i in g["installationCaseIds"]))
        w("")
        w("| 모델명(홈페이지) | 사양표 표기 | 이미지 캡션 표기 | 나라장터 식별번호 | 타입 | 이미지 파일 | xref | 상태 |\n|---|---|---|---|---|---|---|---|")
        for m in g["models"]:
            src = m["images"][0]["src"]
            key = src.replace("assets/img/", "").replace(".webp", "")
            xr = ", ".join(str(x) for x in MAN["products"][key]["xrefs"])
            w("| %s | %s | %s | %s | %s | `%s` | %s | %s |" % (m["model"], m["modelSource"]["specTable"], m["modelSource"]["imageCaption"], m["procurementId"],
                                                              PT[m["powerType"]], src.replace("assets/img/products/", ""), xr,
                                                              "확정" if m["verificationStatus"] == "verified" else "**확인 필요** (%s)" % ", ".join(m["issueRefs"])))
        w("")

w("## 3. 설치사례 매칭 (사진 1장 = 1건)\n")
w("지면에서 사진 한 장의 영역만 렌더링하여 추출했습니다. 파일: `assets/img/installations/<id>.webp` (목록용 축소본은 `thumb/`).\n")
w("| 인쇄 페이지 | PDF 페이지 | 카탈로그 구분 | 사진 수 | 사진 ID | 연결 제품군 |\n|---|---|---|---|---|---|")
pages = {}
for it in INS["items"]:
    pages.setdefault(it["sourceCatalogPage"], []).append(it)
scene = {s["id"]: s for s in INS["scenes"]}
tot = 0
for pg, items in pages.items():
    s = scene[items[0]["scene"]]
    rel = "도로표지병 전 제품군" if items[0]["category"] == "road-stud" else ", ".join("`%s`" % x for x in items[0]["relatedGroupIds"])
    w("| %sP | %d | %s | %d | %s | %s |" % (pg, items[0]["sourcePdfPage"], s["nameKo"], len(items), ", ".join("`%s`" % i["id"] for i in items), rel))
    tot += len(items)
rs = sum(1 for i in INS["items"] if i["category"] == "road-stud")
w("| **합계** | | | **%d** | 도로표지병 %d장 · LED 경관조명 %d장 | |\n" % (tot, rs, tot - rs))
w("설치사례가 수록되지 않은 제품군: " + ", ".join("%s(%sP)" % (g["nameKo"], g["sourceCatalogPage"]) for g in PR["groups"] if not g["installationCaseIds"]) + "\n")

w("## 4. 인증서 매칭 (3P · PDF 2쪽)\n")
w("| 인증서 | 영문 | 파일 | 원본 크기 |\n|---|---|---|---|")
for c in CERT["items"]:
    w("| %s | %s | `%s` | %d×%dpx |" % (c["nameKo"], c["nameEn"], c["image"].replace("assets/img/", ""), c["w"], c["h"]))
w("")
w("## 5. 기타 이미지\n")
w("| 용도 | 원본 | 파일 |\n|---|---|---|")
w("| 메인 비주얼 | 표지(PDF 1쪽) 내장 야경 사진 원본 — 지면의 글자·로고 미포함 | `assets/img/hero/bridge-night.webp`, `bridge-night-900.webp` |")
w("| 회사소개 배경 | 3P(PDF 2쪽) 내장 야경 사진 원본 — 지면의 글자·인증서 미포함 | `assets/img/hero/city-night.webp`, `city-night-900.webp` |")
w("| 로고 | `그린원_로고_최종.png` 의 투명 여백만 제거 | `assets/img/brand/logo.png` |")
w("| 파비콘·앱 아이콘 | `그린원_로고_최종.pdf`(벡터) 가로형 로고의 심볼 영역 | `favicon.ico`, `assets/img/brand/symbol.png`, `icon-512.png`, `apple-touch-icon.png` |")
w("| 공유 이미지(OG) | 메인 야경 + 원본 로고 합성 | `assets/img/brand/og.jpg` |")
w("| 카탈로그 원본 | `그린원 카탈로그_최종.pdf` | `assets/docs/GreenOne_Catalog.pdf` |")
open(os.path.join(ROOT, "CATALOG_MAPPING.md"), "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
print("CATALOG_MAPPING.md written:", len(out), "lines")
