# 그린원 주식회사 (GreenOne Co., Ltd.) 기업 홈페이지

도로표지병 · LED 경관조명 전문 제조기업 그린원의 국문/영문 홈페이지입니다.
서버 없이 동작하는 정적 사이트이며 GitHub Pages 에 그대로 배포할 수 있습니다.

- 국문: `ko/index.html` · 영문: `en/index.html` (루트 `index.html` 은 브라우저 언어에 따라 자동 이동)
- 제품군 26개 / 모델 76개 / 설치사례 사진 66장 / 인증서 7종 — 모두 `그린원 카탈로그_최종.pdf` 기준

## 폴더 구조

```
├── index.html, 404.html, robots.txt, favicon.ico, .nojekyll
├── ko/                     국문 페이지 (자동 생성 — 직접 수정하지 않음)
│   ├── index.html          메인
│   ├── about.html, greeting.html, philosophy.html, certificates.html, location.html
│   ├── road-stud.html, lighting.html      제품 목록(필터·검색)
│   ├── products/<제품군ID>.html           제품 상세 26쪽
│   └── applications.html, resources.html, contact.html
├── en/                     영문 페이지 (국문과 동일 구성)
├── data/                   ★ 콘텐츠 원본 — 여기만 수정
│   ├── company.json        기업정보, 사이트 설정(배포 주소, 확인 안내 노출 여부)
│   ├── products.json       제품군·모델·사양·나라장터 식별번호·가격(비노출)·검증 상태
│   ├── installations.json  설치사례 사진
│   ├── certificates.json   인증서
│   └── ko.json, en.json    메뉴·문구·페이지별 제목/설명
├── assets/
│   ├── css/site.css        디자인 시스템 (DESIGN_SYSTEM.md 참고)
│   ├── js/site.js          필터·검색·모델 전환·확대 보기·문의 작성
│   ├── img/                brand / hero / products / installations / certificates
│   └── docs/GreenOne_Catalog.pdf
├── tools/
│   ├── build.py            data → ko/, en/ HTML 생성
│   ├── validate.py         데이터·링크·국영문 일치·타사 정보 잔존 검사
│   ├── extract_images.py   카탈로그 PDF → 웹용 이미지 추출
│   ├── make_mapping.py     CATALOG_MAPPING.md 생성
│   ├── preview.html        (개발용) 지정한 화면 폭으로 미리보기
│   └── sweep.html          (개발용) 전체 페이지 가로 넘침·깨진 이미지·스크립트 오류 점검
├── CATALOG_MAPPING.md      카탈로그 페이지별 제품·설치사례 매칭
├── CATALOG_ISSUES.md       카탈로그 표기 불일치·확인 필요 항목
├── DESIGN_SYSTEM.md        컬러·타이포·컴포넌트
└── DEVELOPMENT_REPORT.md   개발 결과 및 테스트 보고
```

## 내용 수정 방법

Python 3.9 이상만 있으면 됩니다(추가 설치 없음).

1. `data/` 의 JSON 을 수정합니다. 제품 정보는 `products.json` 한 곳만 고치면 국문·영문 페이지에 함께 반영됩니다.
2. 빌드와 검수를 실행합니다.

```bash
python tools/build.py
```

```bash
python tools/validate.py
```

3. 로컬에서 확인합니다. (`ko/index.html` 을 더블클릭해도 열립니다.)

```bash
python -m http.server 8765
```

### 자주 하는 작업

| 작업 | 방법 |
|---|---|
| 제품·모델 추가 | `products.json` 의 `groups[].models` 에 추가, 이미지는 `assets/img/products/<제품군ID>/` 에 투명 배경 WebP 로 저장 |
| 설치사례 추가 | `assets/img/installations/` 와 `thumb/` 에 이미지 저장 후 `installations.json` 의 `items` 에 추가 |
| 카탈로그 교체 | `assets/docs/GreenOne_Catalog.pdf` 를 같은 이름으로 덮어쓰기 (자료실의 용량 표기는 빌드 시 자동 갱신) |
| 문구·메뉴 수정 | `ko.json`, `en.json` |
| 확인 필요 항목 확정 | `products.json` 에서 값 수정 → `verificationStatus: "verified"` → 전부 끝나면 `company.json` 의 `site.showVerificationNotes: false` |
| 카탈로그가 바뀐 경우 이미지 재추출 | `python tools/extract_images.py "<카탈로그.pdf>" "<로고.png>" "<로고.pdf>"` (PyMuPDF, Pillow 필요. 지면 배치가 바뀌면 스크립트 안의 매핑 표를 수정) |

## 배포 (GitHub Pages)

기존 다른 사이트의 저장소와 분리된 **새 저장소**에 배포합니다.

1. GitHub 에서 새 저장소를 만듭니다. (예: `greenone`)
2. `data/company.json` 의 `site.siteUrl` 에 배포 주소를 입력합니다. 끝에 `/` 포함. (예: `https://<계정>.github.io/greenone/`)
3. `python tools/build.py` → canonical, hreflang(절대경로), `sitemap.xml`, `robots.txt` 의 Sitemap 항목이 생성됩니다.
4. 이 폴더 전체를 저장소에 올리고 Settings → Pages 에서 `main` 브랜치 `/ (root)` 를 선택합니다.

모든 경로가 상대경로이므로 `https://계정.github.io/저장소/` 같은 하위 디렉터리에서도 그대로 동작합니다.
`tools/` 는 배포에 필요하지 않습니다(같이 올려도 검색엔진에는 노출되지 않도록 `noindex` 처리).

## 문의 기능

별도 서버나 폼 처리 서비스가 없으므로 전화(`tel:`)와 이메일(`mailto:`) 연결 방식입니다.
문의하기 페이지의 양식은 입력 내용을 사용자의 메일 프로그램에 채워 여는 기능이며, 서버로 전송하지 않고 "전송 완료" 표시도 하지 않습니다.

## 관리자 기능

현재 포함되어 있지 않습니다. 정적 호스팅(GitHub Pages)에서는 저장 기능을 가진 관리자를 만들 수 없고,
별도의 백엔드(예: GitHub 토큰을 보관하는 서버리스 프록시)와 전용 인증 정보가 필요합니다.
자세한 내용은 `DEVELOPMENT_REPORT.md` 의 "관리자 기능" 항목을 참고하세요.
