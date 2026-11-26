# CATALOG_MAPPING — 카탈로그 ↔ 홈페이지 데이터 매칭 내역

> 이 문서는 `python tools/make_mapping.py` 로 `data/*.json` 에서 자동 생성됩니다. 직접 수정하지 마세요.

- 원본: `그린원 카탈로그_최종.pdf` (PDF 26쪽 = 인쇄 펼침면 26장, 인쇄 쪽번호 표지~51P)
- 제품군 26개 / 모델 76개 / 설치사례 사진 66장 / 인증서 7종

## 1. 페이지 구성

| 구분 | 인쇄 페이지 | PDF 페이지 | 홈페이지 반영 위치 |
|---|---|---|---|
| 표지 및 기업정보 | 표지 | 1 | 기업정보(`data/company.json`), 메인 비주얼(`assets/img/hero/bridge-night.webp`) |
| 회사소개 및 인증서 | 2~3P | 2 | 인사말·경영이념(`data/ko.json`, `data/en.json`), 인증서 7종, 회사소개 야경(`assets/img/hero/city-night.webp`) |
| 도로표지병 제품 | 4~9P | 3~5 | `ko/road-stud.html`, `ko/products/rs-*.html` (영문 동일) |
| 도로표지병 설치사례 | 10~15P | 6~8 | `ko/applications.html` |
| LED 경관조명 제품 및 설치사례 | 16~51P | 9~26 | `ko/lighting.html`, `ko/products/lt-*.html`, `ko/applications.html` |

## 2. 제품 매칭 (모델 단위)

이미지는 PDF 내장 원본(투명 마스크 포함)을 추출한 것이며 `xref` 는 PDF 내부 이미지 번호입니다. 한 이미지를 여러 모델이 쓰는 경우는 카탈로그 캡션에서 공통 사용이 확인된 범위입니다.

### 도로표지병 (Road Stud)

#### 4P · PDF 3쪽 — Ø138 LED 도로표지병 · 배터리형  (`rs-138-battery`)

- 상세페이지: `ko/products/rs-138-battery.html`, `en/products/rs-138-battery.html`
- 카탈로그 제목: LED 도로표지병 / Road Stud · 제품명: Ф138도로표지병
- 관련 설치사례: `p10-1`, `p10-2`, `p10-3`, `p11-1`, `p11-2`, `p11-3`, `p12-1`, `p12-2`, `p12-3`, `p13-1`, `p13-2`, `p13-3`, `p14-1`, `p14-2`, `p14-3`, `p15-1`, `p15-2`

| 모델명(홈페이지) | 사양표 표기 | 이미지 캡션 표기 | 나라장터 식별번호 | 타입 | 이미지 파일 | xref | 상태 |
|---|---|---|---|---|---|---|---|
| HOR-138WB | HOR-138WB | HOR-138WB | 26146003 | 배터리형 | `rs-138-battery/hor-138wb.webp` | 39 | 확정 |
| HOR-138YB | HOR-138YB | HOR-138YB | 26146004 | 배터리형 | `rs-138-battery/hor-138yb.webp` | 35 | 확정 |

#### 5P · PDF 3쪽 — Ø138 LED 도로표지병 · 하이브리드형  (`rs-138-hybrid`)

- 상세페이지: `ko/products/rs-138-hybrid.html`, `en/products/rs-138-hybrid.html`
- 카탈로그 제목: LED 도로표지병 / Road Stud · 제품명: Ф138도로표지병
- 관련 설치사례: `p10-1`, `p10-2`, `p10-3`, `p11-1`, `p11-2`, `p11-3`, `p12-1`, `p12-2`, `p12-3`, `p13-1`, `p13-2`, `p13-3`, `p14-1`, `p14-2`, `p14-3`, `p15-1`, `p15-2`

| 모델명(홈페이지) | 사양표 표기 | 이미지 캡션 표기 | 나라장터 식별번호 | 타입 | 이미지 파일 | xref | 상태 |
|---|---|---|---|---|---|---|---|
| HOR-138WH | HOR-138WH | HOR-138WH | 26158874 | 하이브리드형 | `rs-138-hybrid/hor-138wh.webp` | 47 | 확정 |
| HOR-138YH | HOR-138YH | HOR-138YH | 26158873 | 하이브리드형 | `rs-138-hybrid/hor-138yh.webp` | 43 | 확정 |

#### 6P · PDF 4쪽 — Ø138 LED 도로표지병 · 태양광형  (`rs-138-solar`)

- 상세페이지: `ko/products/rs-138-solar.html`, `en/products/rs-138-solar.html`
- 카탈로그 제목: LED 도로표지병 / Road Stud · 제품명: Ф138도로표지병
- 관련 설치사례: `p10-1`, `p10-2`, `p10-3`, `p11-1`, `p11-2`, `p11-3`, `p12-1`, `p12-2`, `p12-3`, `p13-1`, `p13-2`, `p13-3`, `p14-1`, `p14-2`, `p14-3`, `p15-1`, `p15-2`

| 모델명(홈페이지) | 사양표 표기 | 이미지 캡션 표기 | 나라장터 식별번호 | 타입 | 이미지 파일 | xref | 상태 |
|---|---|---|---|---|---|---|---|
| HOR-138WS | HOR-138WS | HOR-138WS | 26146001 | 태양광형 | `rs-138-solar/hor-138ws.webp` | 58 | 확정 |
| HOR-138YS | HOR-138YS | HOR-138YS | 26146002 | 태양광형 | `rs-138-solar/hor-138ys.webp` | 54 | 확정 |

#### 7P · PDF 4쪽 — Ø138 도로표지병 모듈교체용  (`rs-113-module`)

- 상세페이지: `ko/products/rs-113-module.html`, `en/products/rs-113-module.html`
- 카탈로그 제목: 모듈교체형 / Module replacement type · 제품명: Ø138 표지병의 모듈교체용
- 관련 설치사례: `p10-1`, `p10-2`, `p10-3`, `p11-1`, `p11-2`, `p11-3`, `p12-1`, `p12-2`, `p12-3`, `p13-1`, `p13-2`, `p13-3`, `p14-1`, `p14-2`, `p14-3`, `p15-1`, `p15-2`

| 모델명(홈페이지) | 사양표 표기 | 이미지 캡션 표기 | 나라장터 식별번호 | 타입 | 이미지 파일 | xref | 상태 |
|---|---|---|---|---|---|---|---|
| HOR-WBI | HOR-WBI | HOR-WBI | 25998110 | 배터리형 | `rs-113-module/hor-wbi.webp` | 64 | 확정 |
| HOR-YBI | HOR-YBI | HOR-YBI | 25998111 | 배터리형 | `rs-113-module/hor-ybi.webp` | 70 | 확정 |
| HOR-113WHI | HOR-113WHI | HOR-113WHI | 26372357 | 하이브리드형 | `rs-113-module/hor-113whi.webp` | 62 | 확정 |
| HOR-113YHI | HOR-113YHI | HOR-113YHI | 26372356 | 하이브리드형 | `rs-113-module/hor-113yhi.webp` | 68 | 확정 |
| HOR-113WSI | HOR-113WSI | HOR-113WSI | 26151423 | 태양광형 | `rs-113-module/hor-113wsi.webp` | 78 | 확정 |
| HOR-113YSI | HOR-113YSI | HOR-113YSI | 26151424 | 태양광형 | `rs-113-module/hor-113ysi.webp` | 74 | 확정 |

#### 8P · PDF 5쪽 — Ø125 LED 도로표지병 · 전기형  (`rs-125-electric`)

- 상세페이지: `ko/products/rs-125-electric.html`, `en/products/rs-125-electric.html`
- 카탈로그 제목: LED 도로표지병 / Road Stud · 제품명: Ø125표지병
- 관련 설치사례: `p10-1`, `p10-2`, `p10-3`, `p11-1`, `p11-2`, `p11-3`, `p12-1`, `p12-2`, `p12-3`, `p13-1`, `p13-2`, `p13-3`, `p14-1`, `p14-2`, `p14-3`, `p15-1`, `p15-2`

| 모델명(홈페이지) | 사양표 표기 | 이미지 캡션 표기 | 나라장터 식별번호 | 타입 | 이미지 파일 | xref | 상태 |
|---|---|---|---|---|---|---|---|
| HOR-WC125 | HOR-WC125 | HOR-WC125 | 25998122 | 전기형 | `rs-125-electric/hor-wc125.webp` | 89 | 확정 |
| HOR-YC125 | HOR-YC125 | HOR-YC125 | 25998123 | 전기형 | `rs-125-electric/hor-yc125.webp` | 85 | 확정 |

#### 9P · PDF 5쪽 — 196 LED 도로표지병 · 전기형  (`rs-196-electric`)

- 상세페이지: `ko/products/rs-196-electric.html`, `en/products/rs-196-electric.html`
- 카탈로그 제목: LED 도로표지병 / Road Stud · 제품명: 196 표지병
- 관련 설치사례: `p10-1`, `p10-2`, `p10-3`, `p11-1`, `p11-2`, `p11-3`, `p12-1`, `p12-2`, `p12-3`, `p13-1`, `p13-2`, `p13-3`, `p14-1`, `p14-2`, `p14-3`, `p15-1`, `p15-2`

| 모델명(홈페이지) | 사양표 표기 | 이미지 캡션 표기 | 나라장터 식별번호 | 타입 | 이미지 파일 | xref | 상태 |
|---|---|---|---|---|---|---|---|
| HOR-WC196 | HOR-WC196 | HOR-WC196 | 25998124 | 전기형 | `rs-196-electric/hor-wc196.webp` | 97 | 확정 |
| HOR-YC196 | HOR-YC196 | HOR-YC196 | 25998125 | 전기형 | `rs-196-electric/hor-yc196.webp` | 93 | 확정 |

### LED 경관조명 (LED Landscape Lighting)

#### 16P · PDF 9쪽 — LED 라인조명 · 플렉시블 조명 (BAR Type)  (`lt-line-bar`)

- 상세페이지: `ko/products/lt-line-bar.html`, `en/products/lt-line-bar.html`
- 카탈로그 제목: 라인조명 / Line Lighting / BAR Type · 제품명: ➊, ➋ LED라인조명 / ➌ LED플렉시블 조명
- 관련 설치사례: `p17-1`, `p17-2`, `p17-3`

| 모델명(홈페이지) | 사양표 표기 | 이미지 캡션 표기 | 나라장터 식별번호 | 타입 | 이미지 파일 | xref | 상태 |
|---|---|---|---|---|---|---|---|
| HOR-1000BA-15H | HOR-1000BA-15H | HOL-1000BA-15H | 26337936 | 전기형 | `lt-line-bar/1000ba-15h.webp` | 166 | **확인 필요** (I-01) |
| HOR-1000BA-15B | HOR-1000BA-15B | HOL-1000BA-15B | 26337945 | 전기형 | `lt-line-bar/1000ba-15b.webp` | 170 | **확인 필요** (I-01) |
| HOR-1000FL-10 | HOR-1000FL-10 | HOL-1000FL-10 | 26337928 | 전기형 | `lt-line-bar/1000fl-10.webp` | 174 | **확인 필요** (I-01, C-03) |

#### 18P · PDF 10쪽 — LED 벽부등  (`lt-wall`)

- 상세페이지: `ko/products/lt-wall.html`, `en/products/lt-wall.html`
- 카탈로그 제목: LED 벽부등 / Wall Light · 제품명: LED 벽부등
- 관련 설치사례: `p19-1`, `p19-2`, `p19-3`

| 모델명(홈페이지) | 사양표 표기 | 이미지 캡션 표기 | 나라장터 식별번호 | 타입 | 이미지 파일 | xref | 상태 |
|---|---|---|---|---|---|---|---|
| HOR-LL180-SU | HOR-LL180-SU | HOL-LL180-S | 26003286 | 태양광형 | `lt-wall/ll180-s.webp` | 181 | **확인 필요** (I-02) |
| HOR-109WA | HOR-109WA | HOL-109WA | 26084717 | 전기형 | `lt-wall/109wa.webp` | 185 | **확인 필요** (I-02, I-08c) |

#### 20P · PDF 11쪽 — LED 경계석조명  (`lt-curb`)

- 상세페이지: `ko/products/lt-curb.html`, `en/products/lt-curb.html`
- 카탈로그 제목: LED경계석조명 / LED Curb Stone Lighting · 제품명: ➊ 레인보우 / ➋, ➌ 뉴경계석표지병
- 관련 설치사례: `p21-1`, `p21-2`, `p21-3`

| 모델명(홈페이지) | 사양표 표기 | 이미지 캡션 표기 | 나라장터 식별번호 | 타입 | 이미지 파일 | xref | 상태 |
|---|---|---|---|---|---|---|---|
| HOL-19-C-1 | HOL-19-C-1 | HOL-19-C-1 | 25996689 | 전기형 | `lt-curb/hol-19-c-1.webp` | 198 | 확정 |
| HOL-155-H | HOL-155-H | HOL-155-H | 26003291 | 하이브리드형 | `lt-curb/hol-155-h.webp` | 202 | 확정 |
| HOL-155-B | HOL-155-B | HOL-155-B | 26003288 | 배터리형 | `lt-curb/hol-155-b.webp` | 206 | 확정 |

#### 22P · PDF 12쪽 — 로고젝터  (`lt-logo-projector`)

- 상세페이지: `ko/products/lt-logo-projector.html`, `en/products/lt-logo-projector.html`
- 카탈로그 제목: 로고젝터 / Logo Projector · 제품명: LED 경관조명기구
- 관련 설치사례: `p23-1`, `p23-2`, `p23-3`, `p23-4`, `p23-5`

| 모델명(홈페이지) | 사양표 표기 | 이미지 캡션 표기 | 나라장터 식별번호 | 타입 | 이미지 파일 | xref | 상태 |
|---|---|---|---|---|---|---|---|
| HOL-LL50W-CU | HOL-LL50W-CU | HOL-LL50W-CU | 26337946 | 전기형 | `lt-logo-projector/hol-ll50w-cu.webp` | 228 | 확정 |
| HOL-LL80W-CU | HOL-LL80W-CU | HOL-LL80W-CU | 26337955 | 전기형 | `lt-logo-projector/hol-ll80w-cu.webp` | 230 | 확정 |
| HOL-LL100W-CU | HOL-LL100W-CU | HOL-LL100W-CU | 26337956 | 전기형 | `lt-logo-projector/hol-ll100w-cu.webp` | 226 | 확정 |

#### 24P · PDF 13쪽 — LED 공원등  (`lt-park`)

- 상세페이지: `ko/products/lt-park.html`, `en/products/lt-park.html`
- 카탈로그 제목: LED 공원등 / Park Light · 제품명: LED 공원
- 관련 설치사례: `p25-1`, `p25-2`, `p25-3`

| 모델명(홈페이지) | 사양표 표기 | 이미지 캡션 표기 | 나라장터 식별번호 | 타입 | 이미지 파일 | xref | 상태 |
|---|---|---|---|---|---|---|---|
| HOL-LL80W-Butterfly | HOL-LL80W-Butterfly | HOL-LL80W-Butterfly | 26003285 | 전기형 | `lt-park/hol-ll80w-butterfly.webp` | 241 | 확정 |
| HOL-LL80W-Seagull | HOL-LL80W-Seagull | HOL-LL80W-Seagull | 26003284 | 전기형 | `lt-park/hol-ll80w-seagull.webp` | 237 | 확정 |

#### 26P · PDF 14쪽 — LED 공원보안등 (50W · 30W)  (`lt-security-50-30`)

- 상세페이지: `ko/products/lt-security-50-30.html`, `en/products/lt-security-50-30.html`
- 카탈로그 제목: LED 공원보안등 / Park Security Light · 제품명: LED 공원보안등
- 관련 설치사례: `p27-1`, `p27-2`, `p27-3`

| 모델명(홈페이지) | 사양표 표기 | 이미지 캡션 표기 | 나라장터 식별번호 | 타입 | 이미지 파일 | xref | 상태 |
|---|---|---|---|---|---|---|---|
| HOL-50S | HOL-50S, 50W | HOL-50S, 50W | 25996687 | 태양광형 | `lt-security-50-30/hol-50s.webp` | 253 | 확정 |
| HOL-LL30S-3M | HOL-LL30S-3M | HOL-LL30S-3M | 25996688 | 태양광형 | `lt-security-50-30/hol-ll30s-3m.webp` | 257 | 확정 |

#### 28P · PDF 15쪽 — LED 공원보안등 (25W)  (`lt-security-25`)

- 상세페이지: `ko/products/lt-security-25.html`, `en/products/lt-security-25.html`
- 카탈로그 제목: LED 공원보안등 / Park Security Light · 제품명: LED 공원보안등
- 관련 설치사례: `p27-1`, `p27-2`, `p27-3`

| 모델명(홈페이지) | 사양표 표기 | 이미지 캡션 표기 | 나라장터 식별번호 | 타입 | 이미지 파일 | xref | 상태 |
|---|---|---|---|---|---|---|---|
| HOL-25S | HOL-25S | HOL-25S | 26003282 | 태양광형 | `lt-security-25/hol-25s.webp` | 267 | 확정 |

#### 29P · PDF 15쪽 — LED 포인트 조명  (`lt-accent`)

- 상세페이지: `ko/products/lt-accent.html`, `en/products/lt-accent.html`
- 카탈로그 제목: LED 포인트 조명 / Accent Lighting · 제품명: ➊ 표지병미니 / ➋ 사각표지병 / ➌ LED스탭등

| 모델명(홈페이지) | 사양표 표기 | 이미지 캡션 표기 | 나라장터 식별번호 | 타입 | 이미지 파일 | xref | 상태 |
|---|---|---|---|---|---|---|---|
| HOL-130-B | HOL-50S, 50W | HOL-130-B | 26003287 | 배터리형 | `lt-accent/hol-130-b.webp` | 271 | **확인 필요** (I-03) |
| HOL-138S | HOL-LL30S-3M | HOL-138S | 26337927 | 태양광형 | `lt-accent/hol-138s.webp` | 275 | **확인 필요** (I-03, C-05) |
| HOL-275-10 | HOL-275-10 | HOL-275-10 | 26337934 | 전기형 | `lt-accent/hol-275-10.webp` | 279 | 확정 |

#### 30P · PDF 16쪽 — LED 바닥매립등 · 사각형  (`lt-floor-square`)

- 상세페이지: `ko/products/lt-floor-square.html`, `en/products/lt-floor-square.html`
- 카탈로그 제목: LED 바닥매립등 / Solar-powered type · 제품명: LED경관조명기구
- 관련 설치사례: `p31-1`, `p31-2`, `p31-3`

| 모델명(홈페이지) | 사양표 표기 | 이미지 캡션 표기 | 나라장터 식별번호 | 타입 | 이미지 파일 | xref | 상태 |
|---|---|---|---|---|---|---|---|
| HOL-222-60S | HOL-222-60S | HOL-222-60S | 26337929 | 태양광형 | `lt-floor-square/hol-222-60s.webp` | 290, 304, 294, 292, 296 | 확정 |
| HOL-118-60S | HOL-118-60S | HOL-118-60S | 26337930 | 태양광형 | `lt-floor-square/hol-118-60s.webp` | 286, 306, 308, 310, 312 | 확정 |

#### 32P · PDF 17쪽 — LED 바닥매립등 · 원형  (`lt-floor-round`)

- 상세페이지: `ko/products/lt-floor-round.html`, `en/products/lt-floor-round.html`
- 카탈로그 제목: LED 바닥매립등 / Solar-powered type · 제품명: LED경관조명기구
- 관련 설치사례: `p33-1`, `p33-2`, `p33-3`

| 모델명(홈페이지) | 사양표 표기 | 이미지 캡션 표기 | 나라장터 식별번호 | 타입 | 이미지 파일 | xref | 상태 |
|---|---|---|---|---|---|---|---|
| HOL-120-60S | HOL-120-60S | HOL-120-60S | 26337933 | 태양광형 | `lt-floor-round/hol-120-60s.webp` | 336, 346, 323, 327, 331 | 확정 |
| HOL-96-47S | HOL-96-47S | HOL-96-47S | 26337932 | 태양광형 | `lt-floor-round/hol-96-47s.webp` | 344, 350, 352, 319, 321 | 확정 |
| HOL-67-30S | HOL-67-30S | HOL-67-30S | 26337931 | 태양광형 | `lt-floor-round/hol-67-30s.webp` | 340, 348, 325, 329, 333 | 확정 |

#### 34P · PDF 18쪽 — 사각 펜스기둥조명  (`lt-fence-square`)

- 상세페이지: `ko/products/lt-fence-square.html`, `en/products/lt-fence-square.html`
- 카탈로그 제목: 사각 펜스기둥조명 / Square Fence Post Light · 제품명: 사각펜스기둥조명
- 관련 설치사례: `p35-1`, `p35-2`, `p35-3`

| 모델명(홈페이지) | 사양표 표기 | 이미지 캡션 표기 | 나라장터 식별번호 | 타입 | 이미지 파일 | xref | 상태 |
|---|---|---|---|---|---|---|---|
| HOL-157-S | HOL-157-S | HOL-157-S | 26003294 | 태양광형 | `lt-fence-square/hol-157-s-h.webp` | 359 | 확정 |
| HOL-157-H | HOL-157-H | HOL-157-H | 26003293 | 하이브리드형 | `lt-fence-square/hol-157-s-h.webp` | 359 | 확정 |
| HOL-157-B | HOL-157-B | HOL-157-B | 26003292 | 확인 필요 | `lt-fence-square/hol-157-b.webp` | 363 | **확인 필요** (I-04) |

#### 36P · PDF 19쪽 — 원형 펜스기둥조명  (`lt-fence-round`)

- 상세페이지: `ko/products/lt-fence-round.html`, `en/products/lt-fence-round.html`
- 카탈로그 제목: 원형 펜스기둥조명 / Round Fence Post Light · 제품명: 원형펜스기둥조명
- 관련 설치사례: `p37-1`, `p37-2`, `p37-3`

| 모델명(홈페이지) | 사양표 표기 | 이미지 캡션 표기 | 나라장터 식별번호 | 타입 | 이미지 파일 | xref | 상태 |
|---|---|---|---|---|---|---|---|
| HOL-110-S | HOL-110-S | HOL-110-S | 26003289 | 태양광형 | `lt-fence-round/hol-110-s.webp` | 376 | 확정 |
| HOL-110-H | HOL-110-H | HOL-110-H | 26003290 | 하이브리드형 | `lt-fence-round/hol-110-h.webp` | 380 | 확정 |
| HOL-110-C | HOL-110-C | HOL-110-C | 26089748 | 전기형 | `lt-fence-round/hol-110-c.webp` | 384 | 확정 |

#### 38P · PDF 20쪽 — LED 볼라드 조명  (`lt-bollard`)

- 상세페이지: `ko/products/lt-bollard.html`, `en/products/lt-bollard.html`
- 카탈로그 제목: LED볼라드 조명 / Bollard Light · 제품명: LED 볼라드 조명
- 관련 설치사례: `p39-1`, `p39-2`, `p39-3`

| 모델명(홈페이지) | 사양표 표기 | 이미지 캡션 표기 | 나라장터 식별번호 | 타입 | 이미지 파일 | xref | 상태 |
|---|---|---|---|---|---|---|---|
| HOL-800BOL | HOL-800BOL | HOL-800BOL | 26084714 | 전기형 | `lt-bollard/hol-800bol.webp` | 404 | 확정 |
| HOL-300BOL | HOL-300BOL | HOL-300BOL | 26084715 | 전기형 | `lt-bollard/hol-300bol.webp` | 408 | 확정 |
| HOL-110BOL | HOL-110BOL | HOL-110BOL | 26122094 | 전기형 | `lt-bollard/hol-110bol.webp` | 414 | 확정 |
| HOL-150BOL | HOL-150BOL | HOL-150BOL | 26122093 | 전기형 | `lt-bollard/hol-150bol.webp` | 412 | 확정 |

#### 40P · PDF 21쪽 — LED 라인조명 (라인바 · 핸드레일바)  (`lt-linear`)

- 상세페이지: `ko/products/lt-linear.html`, `en/products/lt-linear.html`
- 카탈로그 제목: LED 라인조명 / LED Linear Light · 제품명: ➊ LED 라인바 / ➋ LED 핸드레일바 / ➌ LED 바
- 관련 설치사례: `p41-1`, `p41-2`, `p41-3`

| 모델명(홈페이지) | 사양표 표기 | 이미지 캡션 표기 | 나라장터 식별번호 | 타입 | 이미지 파일 | xref | 상태 |
|---|---|---|---|---|---|---|---|
| HOL-1000BA-15 | HOL-1000BA-15 | HOL-1000BA-15 | 26337935 | 전기형 | `lt-linear/hol-1000ba-15.webp` | 428 | 확정 |
| HOL-1000BA-B15 | HOL-1000BA-B15 | HOL-1000BA-B15 | 26396633 | 전기형 | `lt-linear/hol-1000ba-15.webp` | 428 | 확정 |
| HOL-1000BA-7A | HOL-1000BA-7A | HOL-1000BA-7A | 26396635 | 전기형 | `lt-linear/hol-1000ba-7.webp` | 430 | 확정 |
| HOL-1000BA-7B | HOL-1000BA-7B | HOL-1000BA-7B | 26396634 | 전기형 | `lt-linear/hol-1000ba-7.webp` | 430 | 확정 |

#### 42P · PDF 22쪽 — LED 라인투광조명  (`lt-linear-flood`)

- 상세페이지: `ko/products/lt-linear-flood.html`, `en/products/lt-linear-flood.html`
- 카탈로그 제목: LED 라인투광조명 / LED Linear Floodlight · 제품명: LED 바 투광등
- 관련 설치사례: `p43-1`, `p43-2`, `p43-3`

| 모델명(홈페이지) | 사양표 표기 | 이미지 캡션 표기 | 나라장터 식별번호 | 타입 | 이미지 파일 | xref | 상태 |
|---|---|---|---|---|---|---|---|
| HOL-1000BA-18F | HOL-1000BA-18F | HOL-1000BA-18F | 26337937 | 전기형 | `lt-linear-flood/hol-1000ba-f.webp` | 437 | 확정 |
| HOL-1000BA-24F | HOL-1000BA-24F | HOL-1000BA-24F | 26337938 | 전기형 | `lt-linear-flood/hol-1000ba-f.webp` | 437 | 확정 |
| HOL-1000BA-36F | HOL-1000BA-36F | HOL-1000BA-36F | 26337947 | 전기형 | `lt-linear-flood/hol-1000ba-f.webp` | 437 | 확정 |
| HOL-1000BA-54F | HOL-1000BA-54F | HOL-1000BA-54F | 26337948 | 전기형 | `lt-linear-flood/hol-1000ba-f.webp` | 437 | 확정 |

#### 44P · PDF 23쪽 — LED 원형 투광등 (125C)  (`lt-flood-125`)

- 상세페이지: `ko/products/lt-flood-125.html`, `en/products/lt-flood-125.html`
- 카탈로그 제목: LED투광조명 / LED Floodlight · 제품명: LED 원형 투광등
- 관련 설치사례: `p45-1`, `p45-2`

| 모델명(홈페이지) | 사양표 표기 | 이미지 캡션 표기 | 나라장터 식별번호 | 타입 | 이미지 파일 | xref | 상태 |
|---|---|---|---|---|---|---|---|
| HOL-125C-12F | HOL-125C-12F | HOL-125C-12F | 26337939 | 전기형 | `lt-flood-125/hol-125c.webp` | 452 | 확정 |
| HOL-125C-18F | HOL-125C-18F | HOL-125C-18F | 26337940 | 전기형 | `lt-flood-125/hol-125c.webp` | 452 | 확정 |
| HOL-125C-24F | HOL-125C-24F | HOL-125C-24F | 26337941 | 전기형 | `lt-flood-125/hol-125c.webp` | 452 | 확정 |

#### 46P · PDF 24쪽 — LED 원형 투광등 (160C · 217C)  (`lt-flood-160-217`)

- 상세페이지: `ko/products/lt-flood-160-217.html`, `en/products/lt-flood-160-217.html`
- 카탈로그 제목: LED투광조명 / LED Floodlight · 제품명: LED 원형 투광등
- 관련 설치사례: `p47-1`, `p47-2`, `p47-3`

| 모델명(홈페이지) | 사양표 표기 | 이미지 캡션 표기 | 나라장터 식별번호 | 타입 | 이미지 파일 | xref | 상태 |
|---|---|---|---|---|---|---|---|
| HOL-160C-36F | HOL-160C-36F | HOL-160C-36F | 26337949 | 전기형 | `lt-flood-160-217/hol-160c-36f.webp` | 459 | 확정 |
| HOL-160C-42F | HOL-160C-42F | HOL-160C-42F | 26337950 | 전기형 | `lt-flood-160-217/hol-160c-42f.webp` | 463 | 확정 |
| HOL-217C-54F | HOL-217C-54F | HOL-217C-54F | 26337951 | 전기형 | `lt-flood-160-217/hol-217c.webp` | 467 | 확정 |
| HOL-217C-72F | HOL-217C-72F | HOL-217C-72F | 26337957 | 전기형 | `lt-flood-160-217/hol-217c.webp` | 467 | 확정 |
| HOL-217C-108F | HOL-217C-108F | HOL-217C-108F | 26337960 | 전기형 | `lt-flood-160-217/hol-217c.webp` | 467 | 확정 |
| HOL-217C-108FB | HOL-217C-108FB | HOL-217C-108FB | 26396632 | 전기형 | `lt-flood-160-217/hol-217c.webp` | 467 | 확정 |

#### 48P · PDF 25쪽 — LED 원형 지중등  (`lt-inground-round`)

- 상세페이지: `ko/products/lt-inground-round.html`, `en/products/lt-inground-round.html`
- 카탈로그 제목: LED지중등 / LED In-ground Light · 제품명: LED 원형 지중등
- 관련 설치사례: `p49-1`, `p49-2`, `p49-3`

| 모델명(홈페이지) | 사양표 표기 | 이미지 캡션 표기 | 나라장터 식별번호 | 타입 | 이미지 파일 | xref | 상태 |
|---|---|---|---|---|---|---|---|
| HOL-LL100-C12 | HOL-LL100-C12 | HOL-LL100-C12 | 26337942 | 전기형 | `lt-inground-round/hol-ll100-c12.webp` | 477 | 확정 |
| HOL-LL140-C18 | HOL-LL140-C18 | HOL-LL140-C18 | 26337943 | 전기형 | `lt-inground-round/hol-ll140-c18.webp` | 481 | 확정 |
| HOL-LL180-C36 | HOL-LL180-C36 | HOL-LL180-C36 | 26337952 | 전기형 | `lt-inground-round/hol-ll180-c36.webp` | 485 | 확정 |
| HOL-LL220-C54 | HOL-LL220-C54 | HOL-LL220-C54 | 26337953 | 전기형 | `lt-inground-round/hol-ll220-c54-c72.webp` | 489 | 확정 |
| HOL-LL220-C72 | HOL-LL220-C72 | HOL-LL220-C72 | 26337958 | 전기형 | `lt-inground-round/hol-ll220-c54-c72.webp` | 489 | 확정 |

#### 50P · PDF 26쪽 — LED 라인지중등  (`lt-inground-linear`)

- 상세페이지: `ko/products/lt-inground-linear.html`, `en/products/lt-inground-linear.html`
- 카탈로그 제목: LED 라인지중등 / LED Linear In-ground Light · 제품명: LED바 지중등

| 모델명(홈페이지) | 사양표 표기 | 이미지 캡션 표기 | 나라장터 식별번호 | 타입 | 이미지 파일 | xref | 상태 |
|---|---|---|---|---|---|---|---|
| HOL-LL1010-C15 | HOL-LL1010-C15 | HOL-LL1010-C15 | 26337944 | 전기형 | `lt-inground-linear/hol-ll1010-c15.webp` | 505 | 확정 |
| HOL-LL1010-C36 | HOL-LL1010-C36 | HOL-LL1010-C36 | 26337954 | 전기형 | `lt-inground-linear/hol-ll1010-c36.webp` | 509 | 확정 |
| HOL-LL1010-C72 | ECO-LL1010-C72 | HOL-LL1010-C72 | 26337959 | 전기형 | `lt-inground-linear/hol-ll1010-c72.webp` | 513 | **확인 필요** (I-07) |

#### 51P · PDF 26쪽 — LED 열주등  (`lt-column`)

- 상세페이지: `ko/products/lt-column.html`, `en/products/lt-column.html`
- 카탈로그 제목: LED열주등 / LED Bollard Light · 제품명: LED 열주등

| 모델명(홈페이지) | 사양표 표기 | 이미지 캡션 표기 | 나라장터 식별번호 | 타입 | 이미지 파일 | xref | 상태 |
|---|---|---|---|---|---|---|---|
| HOL-2000-120 | HOL-2000-120 | HOL-2000-120 | 26337961 | 전기형 | `lt-column/hol-2000-120.webp` | 517 | 확정 |

## 3. 설치사례 매칭 (사진 1장 = 1건)

지면에서 사진 한 장의 영역만 렌더링하여 추출했습니다. 파일: `assets/img/installations/<id>.webp` (목록용 축소본은 `thumb/`).

| 인쇄 페이지 | PDF 페이지 | 카탈로그 구분 | 사진 수 | 사진 ID | 연결 제품군 |
|---|---|---|---|---|---|
| 10P | 6 | 횡단보도 | 3 | `p10-1`, `p10-2`, `p10-3` | 도로표지병 전 제품군 |
| 11P | 6 | 중앙차선 | 3 | `p11-1`, `p11-2`, `p11-3` | 도로표지병 전 제품군 |
| 12P | 7 | 좌우차선 | 3 | `p12-1`, `p12-2`, `p12-3` | 도로표지병 전 제품군 |
| 13P | 7 | 안심귀갓길 · 골목길 | 3 | `p13-1`, `p13-2`, `p13-3` | 도로표지병 전 제품군 |
| 14P | 8 | 기타 (공원, 수변공원, 수변도로, 회전교차로, 산책로, 자전거도로) | 3 | `p14-1`, `p14-2`, `p14-3` | 도로표지병 전 제품군 |
| 15P | 8 | 기타 (공원, 수변공원, 수변도로, 회전교차로, 산책로, 자전거도로) | 2 | `p15-1`, `p15-2` | 도로표지병 전 제품군 |
| 17P | 9 | 라인조명 | 3 | `p17-1`, `p17-2`, `p17-3` | `lt-line-bar` |
| 19P | 10 | LED 벽부등 | 3 | `p19-1`, `p19-2`, `p19-3` | `lt-wall` |
| 21P | 11 | LED 경계석조명 | 3 | `p21-1`, `p21-2`, `p21-3` | `lt-curb` |
| 23P | 12 | 로고젝터 | 5 | `p23-1`, `p23-2`, `p23-3`, `p23-4`, `p23-5` | `lt-logo-projector` |
| 25P | 13 | LED 공원등 | 3 | `p25-1`, `p25-2`, `p25-3` | `lt-park` |
| 27P | 14 | LED 공원보안등 | 3 | `p27-1`, `p27-2`, `p27-3` | `lt-security-50-30`, `lt-security-25` |
| 31P | 16 | LED 바닥매립등 (사각형) | 3 | `p31-1`, `p31-2`, `p31-3` | `lt-floor-square` |
| 33P | 17 | LED 바닥매립등 (원형) | 3 | `p33-1`, `p33-2`, `p33-3` | `lt-floor-round` |
| 35P | 18 | 사각 펜스기둥조명 | 3 | `p35-1`, `p35-2`, `p35-3` | `lt-fence-square` |
| 37P | 19 | 원형 펜스기둥조명 | 3 | `p37-1`, `p37-2`, `p37-3` | `lt-fence-round` |
| 39P | 20 | LED 볼라드 조명 | 3 | `p39-1`, `p39-2`, `p39-3` | `lt-bollard` |
| 41P | 21 | LED 라인조명 | 3 | `p41-1`, `p41-2`, `p41-3` | `lt-linear` |
| 43P | 22 | LED 라인투광조명 | 3 | `p43-1`, `p43-2`, `p43-3` | `lt-linear-flood` |
| 45P | 23 | LED 원형 투광등 (125C) | 2 | `p45-1`, `p45-2` | `lt-flood-125` |
| 47P | 24 | LED 원형 투광등 (160C · 217C) | 3 | `p47-1`, `p47-2`, `p47-3` | `lt-flood-160-217` |
| 49P | 25 | LED 원형 지중등 | 3 | `p49-1`, `p49-2`, `p49-3` | `lt-inground-round` |
| **합계** | | | **66** | 도로표지병 17장 · LED 경관조명 49장 | |

설치사례가 수록되지 않은 제품군: LED 포인트 조명(29P), LED 라인지중등(50P), LED 열주등(51P)

## 4. 인증서 매칭 (3P · PDF 2쪽)

| 인증서 | 영문 | 파일 | 원본 크기 |
|---|---|---|---|
| 공장등록증 | Factory Registration Certificate | `certificates/factory-registration.webp` | 397×561px |
| 직접생산증명서 (도로표지병) | Direct Production Certificate (Road Studs) | `certificates/direct-production-road-stud.webp` | 397×561px |
| 직접생산증명서 (LED 경관조명기구) | Direct Production Certificate (LED Landscape Lighting Fixtures) | `certificates/direct-production-led-lighting.webp` | 397×561px |
| 건설업 등록증 | Construction Business Registration Certificate | `certificates/construction-business.webp` | 397×561px |
| 여성기업 확인서 | Women-Owned Business Certificate | `certificates/women-owned-business.webp` | 397×561px |
| 중소기업 확인서 | Small and Medium-Sized Enterprise Certificate | `certificates/sme.webp` | 397×561px |
| 연구개발전담부서 인정서 | R&D Department Recognition Certificate | `certificates/rnd-department.webp` | 397×561px |

## 5. 기타 이미지

| 용도 | 원본 | 파일 |
|---|---|---|
| 메인 비주얼 | 표지(PDF 1쪽) 내장 야경 사진 원본 — 지면의 글자·로고 미포함 | `assets/img/hero/bridge-night.webp`, `bridge-night-900.webp` |
| 회사소개 배경 | 3P(PDF 2쪽) 내장 야경 사진 원본 — 지면의 글자·인증서 미포함 | `assets/img/hero/city-night.webp`, `city-night-900.webp` |
| 로고 | `그린원_로고_최종.png` 의 투명 여백만 제거 | `assets/img/brand/logo.png` |
| 파비콘·앱 아이콘 | `그린원_로고_최종.pdf`(벡터) 가로형 로고의 심볼 영역 | `favicon.ico`, `assets/img/brand/symbol.png`, `icon-512.png`, `apple-touch-icon.png` |
| 공유 이미지(OG) | 메인 야경 + 원본 로고 합성 | `assets/img/brand/og.jpg` |
| 카탈로그 원본 | `그린원 카탈로그_최종.pdf` | `assets/docs/GreenOne_Catalog.pdf` |
