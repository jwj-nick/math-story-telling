// smoke_dnp.js — 중2 심화 문제 페이지 11개를 실제 DOM 으로 띄워 확인한다.
// 도전 7 을 새로 넣었으므로 문항 배선이 어긋나지 않았는지가 핵심.
const fs = require('fs');
const { JSDOM } = require('jsdom');
const APP = 'C:/Kids/math-story-telling/40_grades/middle/math2/app2/';
let bad = 0, n = 0;
const ok = (c, m, x) => { n++; if (!c) { bad++; console.log('FAIL', m, x === undefined ? '' : JSON.stringify(x)); } };

// 새로 넣은 도전 7 의 정답
const NEW7 = { 7: 30, 8: 24, 9: 10, 10: 3, 11: 40 };

const dom = file => {
  let html = fs.readFileSync(APP + file, 'utf8');
  html = html.replace(/<script src="concept\.js[^"]*"><\/script>/,
    '<script>' + fs.readFileSync(APP + 'concept.js', 'utf8') + '</script>');
  html = html.replace(/<link rel="stylesheet"[^>]*>/, '');
  const errs = [];
  const d = new JSDOM(html, {
    runScripts: 'dangerously', pretendToBeVisual: true, url: 'http://localhost/app/' + file,
    beforeParse(w) {
      w.IntersectionObserver = class { constructor(cb) { this.cb = cb; } observe(el) { this.cb([{ isIntersecting: true, target: el }]); } unobserve() {} disconnect() {} };
      w.matchMedia = w.matchMedia || function () { return { matches: false, addEventListener() {}, removeEventListener() {}, addListener() {}, removeListener() {} }; };
      w.requestAnimationFrame = cb => setTimeout(() => cb(Date.now()), 0);
      w.addEventListener('error', e => errs.push(String(e.error && e.error.stack || e.message).split('\n')[0]));
    }
  });
  return { w: d.window, d: d.window.document, errs };
};

setTimeout(() => {
  for (let u = 1; u <= 11; u++) {
    const file = 'd' + u + 'p.html', t = 'd' + u + 'p';
    const { w, d, errs } = dom(file);
    const raw = fs.readFileSync(APP + file, 'utf8');
    ok(errs.length === 0, t + ' 런타임 오류 없음', errs.slice(0, 1));
    ok(/<\/html>\s*$/.test(raw), t + ' 문서 종결');
    ok((raw.match(/<section/g) || []).length === (raw.match(/<\/section>/g) || []).length, t + ' section 짝');

    const qs = [...d.querySelectorAll('section.quest')];
    const want = NEW7[u] !== undefined ? 7 : 6;
    ok(qs.length === want, t + ' 도전 ' + want + '개', qs.length);

    // 문항마다 입력·버튼·출력·힌트 둘·풀이가 짝을 이루는지
    for (let i = 1; i <= qs.length; i++) {
      // 답이 둘인 문항은 a1a·a1b 나 a1x·a1y 처럼 id 가 갈린다.
      // 이름 규칙을 강요하지 말고, 그 문항 블록 안에 실제로 있는지를 본다.
      const sec = qs[i - 1];
      const inp = sec.querySelector('input.num');
      const btn = [...sec.querySelectorAll('button')].find(b => /^b/.test(b.id || ''));
      const out = sec.querySelector('.out');
      ok(!!(inp && btn && out), t + ' Q' + i + ' 입력·버튼·출력',
         { inp: inp && inp.id, btn: btn && btn.id, out: out && out.id });
      ok(!!d.getElementById('h' + i + 'a') && !!d.getElementById('h' + i + 'b'), t + ' Q' + i + ' 힌트 2개');
      ok(!!d.getElementById('s' + i), t + ' Q' + i + ' 풀이');
      ok(!!d.getElementById('h' + i + 'btn') && !!d.getElementById('s' + i + 'btn'), t + ' Q' + i + ' 힌트·풀이 버튼');
      const ta = d.getElementById('t' + i);
      ok(!!ta && (ta.getAttribute('placeholder') || '').length > 8, t + ' Q' + i + ' 생각 적는 칸');
      // 오답이면 되묻고 힌트가 열리는지
      if (inp && btn && out) {
        inp.value = '99999'; btn.dispatchEvent(new w.Event('click'));
        ok(out.textContent.length > 0 && !/정답/.test(out.textContent), t + ' Q' + i + ' 오답 반응',
           out.textContent.slice(0, 24));
      }
      const hb = d.getElementById('h' + i + 'btn');
      if (hb) {
        hb.dispatchEvent(new w.Event('click'));
        ok(d.getElementById('h' + i + 'a').classList.contains('show'), t + ' Q' + i + ' 힌트1 열림');
        hb.dispatchEvent(new w.Event('click'));
        ok(d.getElementById('h' + i + 'b').classList.contains('show'), t + ' Q' + i + ' 힌트2 열림');
      }
      const sb = d.getElementById('s' + i + 'btn');
      if (sb) {
        sb.dispatchEvent(new w.Event('click'));
        ok(d.getElementById('s' + i).classList.contains('show'), t + ' Q' + i + ' 풀이 열림');
      }
    }

    // 새로 넣은 도전 7 은 정답을 넣으면 정답이라 말해야 한다
    if (NEW7[u] !== undefined) {
      const inp = d.getElementById('a7'), btn = d.getElementById('b7'), out = d.getElementById('o7');
      inp.value = String(NEW7[u]); btn.dispatchEvent(new w.Event('click'));
      ok(/정답/.test(out.textContent), t + ' 도전7 정답 반응 (답 ' + NEW7[u] + ')', out.textContent.slice(0, 30));
      const sol = d.getElementById('s7');
      ok(sol.querySelectorAll('li').length >= 2, t + ' 도전7 풀이 단계 2개 이상',
         sol.querySelectorAll('li').length);
    }

    ok(errs.length === 0, t + ' 조작 뒤에도 오류 없음', errs.slice(0, 1));

    const plain = raw.replace(/<script[\s\S]*?<\/script>/g, ' ').replace(/<[^>]+>/g, ' ')
                     .replace(/["“”][^"“”]*["“”]/g, ' ');
    const banmal = (plain.match(/(하자\.|해라|봐라|한다\.|된다\.|같다\.|이다\.)/g) || []);
    ok(banmal.length === 0, t + ' 반말', banmal.join(','));
  }
  console.log(bad ? ('\n검사 ' + n + '건 중 실패 ' + bad) : ('ALL PASS (' + n + ' checks)'));
  process.exit(bad ? 1 : 0);
}, 1200);
