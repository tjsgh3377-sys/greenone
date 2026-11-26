/* GreenOne — 공통 스크립트 (라이브러리 없음)
   1. 모바일 내비게이션  2. 제품 목록 필터·검색  3. 제품 상세 모델 전환
   4. 이미지 확대(라이트박스)  5. 설치사례 필터  6. 메일 문의 작성  7. 주소 복사 */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var T = (function () { try { return JSON.parse($("#i18n").textContent); } catch (e) { return {}; } })();

  /* 1. 모바일 내비게이션 */
  var burger = $(".burger"), mnav = $("#mnav");
  function setNav(open) {
    if (!burger || !mnav) return;
    mnav.hidden = !open;
    burger.setAttribute("aria-expanded", String(open));
    burger.setAttribute("aria-label", open ? T.close : T.menu);
    document.body.style.overflow = open ? "hidden" : "";
  }
  if (burger) {
    burger.addEventListener("click", function () { setNav(mnav.hidden); });
    window.addEventListener("resize", function () { if (window.innerWidth > 1180 && !mnav.hidden) setNav(false); });
  }

  /* 2. 제품 목록 필터·검색 */
  var plist = $("[data-plist]");
  if (plist) {
    var cards = $$("[data-card]", plist), state = { sub: "", power: "", q: "" };
    var input = $("[data-search]", plist), clear = $("[data-search-clear]", plist);
    var countEl = $("[data-count]", plist), emptyEl = $("[data-empty]", plist);
    var norm = function (s) { return (s || "").toLowerCase().replace(/[\s\-_.·()]/g, ""); };
    var apply = function (push) {
      var n = 0, q = norm(state.q);
      cards.forEach(function (c) {
        var ok = (!state.sub || c.dataset.sub === state.sub) &&
          (!state.power || (" " + c.dataset.power + " ").indexOf(" " + state.power + " ") > -1) &&
          (!q || norm(c.dataset.search).indexOf(q) > -1);
        c.hidden = !ok; if (ok) n++;
      });
      if (countEl) countEl.textContent = n;
      if (emptyEl) emptyEl.hidden = n > 0;
      if (clear) clear.hidden = !state.q;
      $$("[data-filter]", plist).forEach(function (b) { b.setAttribute("aria-pressed", String(state[b.dataset.filter] === b.dataset.value)); });
      if (push && window.history.replaceState && location.protocol !== "file:") {
        var p = new URLSearchParams();
        if (state.sub) p.set("type", state.sub);
        if (state.power) p.set("power", state.power);
        if (state.q) p.set("q", state.q);
        var s = p.toString();
        history.replaceState(null, "", location.pathname + (s ? "?" + s : ""));
      }
    };
    $$("[data-filter]", plist).forEach(function (b) {
      b.addEventListener("click", function () { state[b.dataset.filter] = b.dataset.value; apply(true); });
    });
    if (input) input.addEventListener("input", function () { state.q = input.value.trim(); apply(true); });
    if (clear) clear.addEventListener("click", function () { input.value = ""; state.q = ""; apply(true); input.focus(); });
    var reset = $("[data-reset]", plist);
    if (reset) reset.addEventListener("click", function () { state = { sub: "", power: "", q: "" }; if (input) input.value = ""; apply(true); });
    try {
      var sp = new URLSearchParams(location.search);
      state.sub = sp.get("type") || ""; state.power = sp.get("power") || ""; state.q = sp.get("q") || "";
      if (input && state.q) input.value = state.q;
    } catch (e) { /* noop */ }
    apply(false);
  }

  /* 3. 제품 상세 — 모델 전환 */
  var pd = $("[data-pd]");
  if (pd) {
    var tabs = $$(".model-tab", pd), inquiry = $$("[data-inquiry]", pd);
    var select = function (id, focus) {
      var found = false;
      tabs.forEach(function (t) {
        var on = t.dataset.model === id; if (on) found = true;
        t.setAttribute("aria-selected", String(on)); t.tabIndex = on ? 0 : -1;
        if (on && focus) t.focus();
      });
      if (!found) return false;
      $$("[data-panel]", pd).forEach(function (p) { p.hidden = p.dataset.panel !== id; });
      $$("[data-stage]", pd).forEach(function (s) { s.hidden = s.dataset.stage.split(" ").indexOf(id) < 0; });
      $$("[data-row]").forEach(function (r) { r.classList.toggle("is-active", r.dataset.row === id); });
      var tab = tabs.filter(function (t) { return t.dataset.model === id; })[0];
      inquiry.forEach(function (a) {
        var subject = a.dataset.subject.replace("{model}", tab ? tab.dataset.name : "");
        if (a.dataset.mailto) a.href = "mailto:" + a.dataset.mailto + "?subject=" + encodeURIComponent(subject);
      });
      return true;
    };
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { select(t.dataset.model); setHash(t.dataset.model); });
      t.addEventListener("keydown", function (e) {
        var d = e.key === "ArrowRight" || e.key === "ArrowDown" ? 1 : e.key === "ArrowLeft" || e.key === "ArrowUp" ? -1 : 0;
        if (!d) return; e.preventDefault();
        var nt = tabs[(i + d + tabs.length) % tabs.length]; select(nt.dataset.model, true); setHash(nt.dataset.model);
      });
    });
    $$("[data-pick]").forEach(function (b) {
      b.addEventListener("click", function () {
        select(b.dataset.pick); setHash(b.dataset.pick);
        var top = pd.getBoundingClientRect().top + window.pageYOffset - 100;
        window.scrollTo({ top: top, behavior: "smooth" });
      });
    });
    var setHash = function (id) { if (history.replaceState && location.protocol !== "file:") history.replaceState(null, "", "#" + id); };
    var h = decodeURIComponent(location.hash.replace("#", ""));
    if (!(h && select(h)) && tabs[0]) select(tabs[0].dataset.model);
  }

  /* 4. 라이트박스 */
  var lb, lbImg, lbCap, lbCount, lbItems = [], lbIdx = 0, lbLast = null;
  function buildLb() {
    lb = document.createElement("div");
    lb.className = "lb"; lb.hidden = true; lb.setAttribute("role", "dialog"); lb.setAttribute("aria-modal", "true");
    lb.innerHTML = '<div class="lb-top"><span class="lb-count num" aria-live="polite"></span>' +
      '<button type="button" class="lb-close" aria-label="' + (T.close || "Close") + '">×</button></div>' +
      '<div class="lb-stage"><button type="button" class="lb-nav lb-prev" aria-label="' + (T.prev || "Previous") + '">←</button>' +
      '<img alt=""><button type="button" class="lb-nav lb-next" aria-label="' + (T.next || "Next") + '">→</button></div>' +
      '<div class="lb-cap"></div>';
    document.body.appendChild(lb);
    lbImg = $("img", lb); lbCap = $(".lb-cap", lb); lbCount = $(".lb-count", lb);
    $(".lb-close", lb).addEventListener("click", closeLb);
    $(".lb-prev", lb).addEventListener("click", function () { showLb(lbIdx - 1); });
    $(".lb-next", lb).addEventListener("click", function () { showLb(lbIdx + 1); });
    lb.addEventListener("click", function (e) { if (e.target === lb || e.target.classList.contains("lb-stage")) closeLb(); });
    var x0 = null;
    lb.addEventListener("touchstart", function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    lb.addEventListener("touchend", function (e) {
      if (x0 === null) return; var dx = e.changedTouches[0].clientX - x0; x0 = null;
      if (Math.abs(dx) > 50) showLb(lbIdx + (dx < 0 ? 1 : -1));
    });
    document.addEventListener("keydown", function (e) {
      if (lb.hidden) return;
      if (e.key === "Escape") closeLb();
      else if (e.key === "ArrowLeft") showLb(lbIdx - 1);
      else if (e.key === "ArrowRight") showLb(lbIdx + 1);
      else if (e.key === "Tab") {
        var f = $$("button, a[href]", lb).filter(function (el) { return !el.hidden && el.offsetParent !== null; });
        if (!f.length) return;
        var first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
  }
  function showLb(i) {
    lbIdx = (i + lbItems.length) % lbItems.length;
    var a = lbItems[lbIdx];
    lbImg.src = a.getAttribute("href"); lbImg.alt = a.dataset.alt || "";
    lbCount.textContent = (lbIdx + 1) + " / " + lbItems.length;
    lbCap.textContent = "";
    var s = document.createElement("span"); s.textContent = a.dataset.cap || ""; lbCap.appendChild(s);
    if (a.dataset.link) {
      var l = document.createElement("a"); l.href = a.dataset.link; l.textContent = a.dataset.linkText || ""; lbCap.appendChild(l);
    }
    var single = lbItems.length < 2;
    $(".lb-prev", lb).hidden = single; $(".lb-next", lb).hidden = single;
  }
  function closeLb() {
    lb.hidden = true; document.body.classList.remove("lb-open"); lbImg.removeAttribute("src");
    if (lbLast) lbLast.focus();
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest ? e.target.closest("a[data-lb]") : null;
    if (!a) return;
    e.preventDefault();
    if (!lb) buildLb();
    lbItems = $$('a[data-lb="' + a.dataset.lb + '"]').filter(function (el) { return !el.closest("[hidden]"); });
    lbLast = a; lb.hidden = false; document.body.classList.add("lb-open");
    showLb(Math.max(0, lbItems.indexOf(a)));
    $(".lb-close", lb).focus();
  });

  /* 5. 설치사례 필터 */
  var ap = $("[data-ap]");
  if (ap) {
    var figs = $$("[data-fig]", ap), cat = "", scene = "";
    var apApply = function () {
      var n = 0;
      figs.forEach(function (f) {
        var ok = (!cat || f.dataset.cat === cat) && (!scene || f.dataset.scene === scene);
        f.hidden = !ok; if (ok) n++;
      });
      $$("[data-cat-btn]", ap).forEach(function (b) { b.setAttribute("aria-pressed", String(b.dataset.catBtn === cat)); });
      $$("[data-scene-btn]", ap).forEach(function (b) {
        b.hidden = !!b.dataset.cat && !!cat && b.dataset.cat !== cat;
        if (!cat && b.dataset.sceneBtn) b.hidden = true;
        b.setAttribute("aria-pressed", String(b.dataset.sceneBtn === scene));
      });
      var row = $("[data-scene-row]", ap); if (row) row.hidden = !cat;
      var c = $("[data-ap-count]", ap); if (c) c.textContent = n;
    };
    $$("[data-cat-btn]", ap).forEach(function (b) { b.addEventListener("click", function () { cat = b.dataset.catBtn; scene = ""; apApply(); }); });
    $$("[data-scene-btn]", ap).forEach(function (b) { b.addEventListener("click", function () { scene = b.dataset.sceneBtn; apApply(); }); });
    try {
      var q = new URLSearchParams(location.search);
      if (q.get("category")) cat = q.get("category");
      if (q.get("scene")) { scene = q.get("scene"); var sb = $('[data-scene-btn="' + scene + '"]', ap); if (sb) cat = sb.dataset.cat; }
    } catch (e) { /* noop */ }
    apApply();
  }

  /* 6. 메일 문의 작성 — 서버 전송 없음. 사용자의 메일 프로그램을 연다. */
  var form = $("[data-mailform]");
  if (form) {
    try {
      var pp = new URLSearchParams(location.search).get("product");
      if (pp && form.elements.product) form.elements.product.value = pp;
    } catch (e) { /* noop */ }
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var el = form.elements, lines = [];
      $$("[data-line]", form).forEach(function (f) {
        var v = (f.value || "").trim(); if (v) lines.push(f.dataset.line + ": " + v);
      });
      var body = lines.join("\n") + "\n\n" + (el.message.value || "").trim();
      var type = el.type.options[el.type.selectedIndex].text;
      location.href = "mailto:" + form.dataset.email + "?subject=" + encodeURIComponent(form.dataset.prefix + " " + type) + "&body=" + encodeURIComponent(body);
    });
  }

  /* 7. 주소 복사 */
  $$("[data-copy]").forEach(function (b) {
    b.addEventListener("click", function () {
      var text = b.dataset.copy, done = function () {
        var t = document.createElement("div"); t.className = "toast"; t.setAttribute("role", "status"); t.textContent = b.dataset.done;
        document.body.appendChild(t); requestAnimationFrame(function () { t.classList.add("on"); });
        setTimeout(function () { t.classList.remove("on"); setTimeout(function () { t.remove(); }, 400); }, 1800);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, function () {});
      else { var ta = document.createElement("textarea"); ta.value = text; document.body.appendChild(ta); ta.select(); try { document.execCommand("copy"); done(); } catch (e) { /* noop */ } ta.remove(); }
    });
  });
})();
