// smoke_pn.js — 중2 연습 페이지 11개를 실제 DOM 으로 띄워 확인한다.
// 뒷단원에 미션 7 을 새로 넣었으므로, 진행바·도장 조건·채점 배선이 어긋나지 않았는지가 핵심.
const fs = require('fs');
const { JSDOM } = require('jsdom');
const APP = 'C:/Kids/math-story-telling/40_grades/middle/math2/app2/';
let bad = 0, n = 0;
const ok = (c, m, x) => { n++; if (!c) { bad++; console.log('FAIL', m, x === undefined ? '' : JSON.stringify(x)); } };

// 새로 넣은 미션 7 의 정답
const NEW = { 7: [42, 9, 5], 8: [15, 18, 20], 9: [9, 14, 8], 10: [7, 3, 9], 11: [16, 10, 4] };

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
    const file = 'p' + u + '.html', t = 'p' + u;
    const { w, d, errs } = dom(file);
    const raw = fs.readFileSync(APP + file, 'utf8');
    ok(errs.length === 0, t + ' 런타임 오류 없음', errs.slice(0, 1));
    ok(/<\/html>\s*$/.test(raw), t + ' 문서 종결');
    ok((raw.match(/<section/g) || []).length === (raw.match(/<\/section>/g) || []).length, t + ' section 짝');

    // 미션 수와 배선 상수가 서로 맞는가 — 새 미션을 넣으면 여기가 가장 먼저 어긋난다
    const miss = [...d.querySelectorAll('section.mission')];
    const pq = d.querySelectorAll('.pq').length;
    const mTypes = raw.match(/var TYPES=\{([^}]*)\}, TOTAL=(\d+)/);
    ok(!!mTypes, t + ' TYPES·TOTAL 선언');
    if (mTypes) {
      const keys = mTypes[1].split(',').filter(Boolean).length;
      ok(keys === miss.length, t + ' TYPES 개수 = 미션 수', { TYPES: keys, 미션: miss.length });
      ok(+mTypes[2] === pq, t + ' TOTAL = 문항 수', { TOTAL: +mTypes[2], 문항: pq });
    }
    const mProg = raw.match(/makeProgress\('prog',\s*(\d+)\)/);
    ok(!!mProg && +mProg[1] === miss.length, t + ' 진행바 칸 = 미션 수',
       { 진행바: mProg && +mProg[1], 미션: miss.length });

    // 미션마다 제목·요령·문항이 있는가
    miss.forEach((s, k) => {
      ok(!!s.querySelector('.m-title') && s.querySelector('.m-title').textContent.trim().length > 1,
         t + ' 미션' + (k + 1) + ' 제목');
      ok(!!s.querySelector('.tip'), t + ' 미션' + (k + 1) + ' 요령');
      ok(s.querySelectorAll('.pq').length >= 2, t + ' 미션' + (k + 1) + ' 문항 2개 이상',
         s.querySelectorAll('.pq').length);
    });

    // 도장 문구가 미션 수와 맞는가
    const seal = d.querySelector('.seal-t');
    if (seal) {
      const m = seal.textContent.match(/(\d+)가지/);
      ok(!!m && +m[1] === miss.length, t + ' 도장 문구의 유형 수', { 문구: seal.textContent, 미션: miss.length });
    }

    // 새 미션 7 — 오답이면 되묻고, 정답이면 정답이라 말하고 "왜?" 가 열리는가
    if (NEW[u]) {
      const s7 = d.getElementById('c7');
      ok(!!s7, t + ' 미션 7');
      NEW[u].forEach((ans, k) => {
        const i = k + 1;
        const inp = d.getElementById('a7' + i), btn = d.getElementById('b7' + i), out = d.getElementById('o7' + i);
        ok(!!(inp && btn && out), t + ' 미션7 (' + i + ') 입력·버튼·출력');
        if (!(inp && btn && out)) return;
        inp.value = '99999'; btn.dispatchEvent(new w.Event('click'));
        ok(out.textContent.length > 0 && !/정답/.test(out.textContent), t + ' 미션7 (' + i + ') 오답 반응',
           out.textContent.slice(0, 22));
        inp.value = String(ans); btn.dispatchEvent(new w.Event('click'));
        ok(/정답/.test(out.textContent), t + ' 미션7 (' + i + ') 정답 반응 (답 ' + ans + ')',
           out.textContent.slice(0, 30));
        const why = d.getElementById('w7' + i);
        ok(!!why && why.style.display === 'block', t + ' 미션7 (' + i + ') 왜? 열림');
      });
      // 세 문항을 다 맞히면 그 미션이 끝난 것으로 표시되는가
      ok(s7.classList.contains('solved'), t + ' 미션7 완료 표시');
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
