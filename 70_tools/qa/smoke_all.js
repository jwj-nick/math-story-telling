// smoke_all.js — 세 학년 앱의 모든 페이지를 실제 DOM 으로 띄우고 **모든 버튼을 눌러 본다**.
//
//   cd <스크래치 폴더> && npm install jsdom          # 리포에 node_modules 를 두지 않는다
//   NODE_PATH=<스크래치 폴더>/node_modules node 70_tools/qa/smoke_all.js
//   ... node 70_tools/qa/smoke_all.js math1          # 한 학년만
//
// 왜 필요한가 (2026-09-08):
//   놀이터에서 `classList.add('')` 때문에 **정답을 맞힌 순간** 게임이 멈추는 버그가 나왔다.
//   문법은 맞으므로 check_page.py 같은 정적 검증으로는 못 잡고, **눌러 봐야만** 드러난다.
//   이 스모크는 페이지 종류를 가리지 않고 눈에 보이는 버튼을 모두 눌러, 그 뒤에 오류가
//   생기는지만 본다. 종류별 세부 검사는 smoke_pn / smoke_dnp / smoke_playground 가 맡는다.
const fs = require('fs');
const path = require('path');
const { JSDOM, VirtualConsole } = require('jsdom');

const ROOT = 'C:/Kids/math-story-telling/40_grades/middle/';
const APPS = { math1: 'app1', math2: 'app2', math3: 'app3' };
const DEPLOY = {   // 배포 트리 — 소스와 폴더 구조가 달라 링크 확인에 함께 쓴다
  math1: 'C:/Nick/30_Apps/jwj-nick.github.io/mid1/math1/app1',
  math2: 'C:/Nick/30_Apps/jwj-nick.github.io/mid2',
  math3: 'C:/Nick/30_Apps/jwj-nick.github.io/mid3',
};
const only = process.argv.slice(2).filter(a => APPS[a]);
const grades = only.length ? only : Object.keys(APPS);

let bad = 0, n = 0, pages = 0, clicks = 0;
const fails = [];
const ok = (c, m, x) => { n++; if (!c) { bad++; fails.push(m + (x === undefined ? '' : ' — ' + JSON.stringify(x))); } };

function load(dir, file) {
  let html = fs.readFileSync(path.join(dir, file), 'utf8');
  // 같은 폴더의 엔진을 인라인으로 — jsdom 은 상대 경로 스크립트를 가져오지 않는다
  html = html.replace(/<script src="(concept|drills|geo)\.js[^"]*"><\/script>/g, (m0, name) => {
    const p = path.join(dir, name + '.js');
    return fs.existsSync(p) ? '<script>' + fs.readFileSync(p, 'utf8') + '</script>' : '';
  });
  html = html.replace(/<link rel="stylesheet"[^>]*>/g, '');
  const errs = [];
  // 이벤트 리스너가 던진 예외는 window 의 error 이벤트로 오지 않고 jsdomError 로 온다.
  // 둘 다 들어야 "눌렀더니 터진다" 를 놓치지 않는다.
  const vc = new VirtualConsole();
  const firstLine = x => String(x).split(/[\r\n]/)[0];
  vc.on('jsdomError', e => errs.push(firstLine(e && e.message || e)));
  vc.on('error', (...a) => errs.push('console.error: ' + firstLine(a.join(' '))));
  const dom = new JSDOM(html, {
    virtualConsole: vc,
    runScripts: 'dangerously', pretendToBeVisual: true, url: 'http://localhost/app/' + file,
    beforeParse(w) {
      w.IntersectionObserver = class { constructor(cb) { this.cb = cb; } observe(el) { this.cb([{ isIntersecting: true, target: el }]); } unobserve() {} disconnect() {} };
      w.matchMedia = w.matchMedia || (() => ({ matches: false, addEventListener() {}, removeEventListener() {}, addListener() {}, removeListener() {} }));
      w.requestAnimationFrame = cb => setTimeout(() => cb(Date.now()), 0);
      w.scrollTo = () => {};
      w.alert = w.confirm = w.prompt = () => {};      // 대화상자는 검사를 멈춰 세운다
      w.print = () => {};                             // 인쇄 버튼이 jsdom 소음을 낸다
      w.Element.prototype.scrollIntoView = function () {};   // jsdom 미구현
      w.Element.prototype.animate = w.Element.prototype.animate || function () { return { finished: Promise.resolve(), cancel() {} }; };
      w.AudioContext = w.webkitAudioContext = function () {
        return {
          createOscillator: () => ({ connect() {}, start() {}, stop() {}, frequency: { value: 0, setValueAtTime() {} }, type: '' }),
          createGain: () => ({ connect() {}, gain: { value: 0, setValueAtTime() {}, exponentialRampToValueAtTime() {}, linearRampToValueAtTime() {} } }),
          destination: {}, currentTime: 0, close() {}, resume() {}, state: 'running'
        };
      };
      w.addEventListener('error', e => errs.push(String((e.error && e.error.stack) || e.message).split('\n')[0]));
    }
  });
  return { w: dom.window, d: dom.window.document, errs };
}

setTimeout(() => {
  for (const g of grades) {
    const dir = path.join(ROOT, g, APPS[g]);
    const files = fs.readdirSync(dir).filter(f => f.endsWith('.html')).sort();
    for (const file of files) {
      const t = g + '/' + file.replace('.html', '');
      let ctx;
      try { ctx = load(dir, file); } catch (e) { ok(false, t + ' 열림', String(e).slice(0, 90)); continue; }
      const { w, d, errs } = ctx;
      const raw = fs.readFileSync(path.join(dir, file), 'utf8');
      pages++;

      ok(errs.length === 0, t + ' 첫 로딩에 오류 없음', errs.slice(0, 1));
      ok(/<\/html>\s*$/.test(raw), t + ' 문서 종결');
      ok((raw.match(/<section/g) || []).length === (raw.match(/<\/section>/g) || []).length, t + ' section 짝');

      // 중복 id — 런타임에서 실제로 겹치는지
      const ids = [...d.querySelectorAll('[id]')].map(e => e.id);
      const dup = ids.filter((x, i) => ids.indexOf(x) !== i);
      ok(dup.length === 0, t + ' 중복 id 없음', [...new Set(dup)].slice(0, 3));

      // 링크가 실재하는지 — 소스와 배포는 폴더 구조가 다르다.
      // 프린트는 소스에서 앱 폴더 밖(40_grades/<학년>/print)에 있고 배포에서는 앱 옆(mid2/print)에 있다.
      // 그래서 양쪽 다 없을 때만 오류로 본다.
      for (const href of new Set([...d.querySelectorAll('a[href]')].map(a => a.getAttribute('href')))) {
        if (!href || /^(https?:|#|mailto:|\.\.\/)/.test(href)) continue;
        const f = href.split(/[?#]/)[0];
        if (!f || f.endsWith('/')) continue;
        const here = fs.existsSync(path.join(dir, f));
        const deployed = DEPLOY[g] && fs.existsSync(path.join(DEPLOY[g], f));
        ok(here || deployed, t + ' 링크한 파일 실재(소스 또는 배포)', href);
      }

      // ★ 모든 버튼을 여러 바퀴 눌러 본다.
      // 한 바퀴로는 모자란다 — 선택형 게임은 한 번 답하면 잠기고, "다음 문제" 를 눌러야
      // 다른 갈래를 탄다. 정답일 때만 터지는 버그(classList.add(''))는 여러 바퀴를 돌아야 걸린다.
      const before = errs.length;
      const btns = [...d.querySelectorAll('button')];
      for (let round = 0; round < 3; round++)
      for (const b of btns) {
        // 입력이 비어 있으면 지나가는 버튼이 많아, 숫자를 하나 채우고 누른다
        const box = b.closest('.row, .pq, .check, .card, section') || d.body;
        box.querySelectorAll('input.num, input.blank, input[type="text"], input[inputmode]').forEach(i => {
          if (!i.value) i.value = '1';
        });
        try { b.dispatchEvent(new w.Event('click', { bubbles: true })); clicks++; } catch (e) { errs.push('click: ' + String(e).slice(0, 80)); }
      }
      // 슬라이더도 끝까지 밀어 본다
      for (const r of d.querySelectorAll('input[type="range"]')) {
        for (const v of [r.min, r.max]) {
          r.value = v;
          try { r.dispatchEvent(new w.Event('input', { bubbles: true })); } catch (e) { errs.push('range: ' + String(e).slice(0, 80)); }
        }
      }
      ok(errs.length === before, t + ' 버튼 ' + btns.length + '개를 세 바퀴 눌러도 오류 없음',
         errs.slice(before, before + 1));

      // 어투 — 인용문은 원문을 그대로 두므로 뺀다
      // 어투 검사에서 빼는 두 가지 — 문제 발문("…라 하자", "…이다")은 수학 문제의 표준 문체이고,
      // 인용문은 원문을 그대로 옮겨야 한다.
      const plain = raw.replace(/<script[\s\S]*?<\/script>/g, ' ')
                       .replace(/<p class="ask"[\s\S]*?<\/p>/g, ' ')
                       .replace(/<div class="given"[\s\S]*?<\/div>/g, ' ')
                       .replace(/<[^>]+>/g, ' ')
                       .replace(/["“”][^"“”]*["“”]/g, ' ');
      const banmal = (plain.match(/(하자\.|해라[\s.!?]|봐라[\s.!?]|한다\.|된다\.|같다\.|이다\.)/g) || []);
      ok(banmal.length === 0, t + ' 반말', banmal.slice(0, 3).join(','));

      // 아이에게 직접 말하는 안내 문구(요령·머리말·목표)는 더 좁게 본다.
      // 발문과 달리 이 자리는 언제나 해요체여야 한다.
      const guides = [...d.querySelectorAll('.tip, .lede, .aim, .pg-desc, .m-title + *, .intro')]
        .map(e => e.textContent.trim()).filter(Boolean);
      const rough = guides.filter(x => /(다|자|라)\.\s*$/.test(x) && !/(에요|예요|어요|아요|해요)\.?\s*$/.test(x));
      ok(rough.length === 0, t + ' 안내 문구가 해요체', rough.slice(0, 2));
    }
  }
  if (bad) { console.log(fails.join('\n')); console.log('\n페이지 ' + pages + ' · 클릭 ' + clicks + ' · 검사 ' + n + '건 중 실패 ' + bad); }
  else console.log('ALL PASS — 페이지 ' + pages + ' · 클릭 ' + clicks + ' · ' + n + ' checks');
  process.exit(bad ? 1 : 0);
}, 2000);
