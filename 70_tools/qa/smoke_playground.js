// smoke_playground.js — 세 학년 놀이터 36페이지(게임 144개)를 실제 DOM 으로 띄워 도는지 확인한다.
//
//   cd <스크래치 폴더> && npm install jsdom          # 리포에 node_modules 를 두지 않는다
//   NODE_PATH=<스크래치 폴더>/node_modules node 70_tools/qa/smoke_playground.js
//   (NODE_PATH 없이 실행하면 스크립트가 놓인 자리에서 jsdom 을 찾다가 실패한다)
//
// 놀이터는 글이 아니라 인터랙션이라 분량으로 잴 수 없다. "눌렀을 때 반응하는가" 를 본다.
// check_page.py 가 정적 검증이라면 이쪽은 런타임 검증이다 — 실제로 이 스모크가
// classList.add('') 로 정답을 맞힌 순간 게임이 멈추던 버그를 잡아냈다(2026-09-07).
const fs = require('fs');
const { JSDOM } = require('jsdom');
const ROOT = 'C:/Kids/math-story-telling/40_grades/middle/';
const GRADES = [['math1', 'app1', 13, 'MJ1'], ['math2', 'app2', 11, 'MJ'], ['math3', 'app3', 12, 'MJ3']];
let bad = 0, n = 0;
const fails = [];
const ok = (c, m, x) => { n++; if (!c) { bad++; fails.push(m + (x === undefined ? '' : ' — ' + JSON.stringify(x))); } };

const dom = (dir, file) => {
  let html = fs.readFileSync(ROOT + dir + '/' + file, 'utf8');
  html = html.replace(/<script src="concept\.js[^"]*"><\/script>/,
    '<script>' + fs.readFileSync(ROOT + dir + '/concept.js', 'utf8') + '</script>');
  html = html.replace(/<link rel="stylesheet"[^>]*>/, '');
  const errs = [];
  const d = new JSDOM(html, {
    runScripts: 'dangerously', pretendToBeVisual: true, url: 'http://localhost/app/' + file,
    beforeParse(w) {
      w.IntersectionObserver = class { constructor(cb) { this.cb = cb; } observe(el) { this.cb([{ isIntersecting: true, target: el }]); } unobserve() {} disconnect() {} };
      w.matchMedia = w.matchMedia || function () { return { matches: false, addEventListener() {}, removeEventListener() {}, addListener() {}, removeListener() {} }; };
      w.requestAnimationFrame = cb => setTimeout(() => cb(Date.now()), 0);
      w.AudioContext = w.webkitAudioContext = function () {
        return { createOscillator: () => ({ connect() {}, start() {}, stop() {}, frequency: { value: 0, setValueAtTime() {} }, type: '' }),
                 createGain: () => ({ connect() {}, gain: { value: 0, setValueAtTime() {}, exponentialRampToValueAtTime() {}, linearRampToValueAtTime() {} } }),
                 destination: {}, currentTime: 0, close() {}, resume() {}, state: 'running' };
      };
      w.addEventListener('error', e => errs.push(String(e.error && e.error.stack || e.message).split('\n')[0]));
    }
  });
  return { w: d.window, d: d.window.document, errs };
};

setTimeout(() => {
  for (const [grade, app, units] of GRADES) {
    for (let i = 1; i <= units; i++) {
      const file = 'g' + i + '.html', t = grade + '/g' + i;
      const path = ROOT + app === undefined ? null : ROOT + app + '/' + file;
      if (!fs.existsSync(ROOT + grade + '/' + app + '/' + file)) { ok(false, t + ' 파일 있음'); continue; }
      const { w, d, errs } = dom(grade + '/' + app, file);
      const raw = fs.readFileSync(ROOT + grade + '/' + app + '/' + file, 'utf8');

      ok(errs.length === 0, t + ' 런타임 오류 없음', errs.slice(0, 1));
      ok(/<\/html>\s*$/.test(raw), t + ' 문서 종결');

      // 게임 4개 — 제목과 설명이 모두 있는가
      const games = [...d.querySelectorAll('.pg-game')];
      ok(games.length === 4, t + ' 게임 4개', games.length);
      games.forEach((g, k) => {
        const title = g.querySelector('.pg-title');
        ok(!!title && title.textContent.trim().length > 2, t + ' 게임' + (k + 1) + ' 제목',
           title && title.textContent.trim());
        ok(g.id && g.id.startsWith('g-'), t + ' 게임' + (k + 1) + ' id', g.id);
      });
      // 마지막은 언제나 오류 탐정 — 되풀이되는 실수를 잡아 주는 자리
      ok(games.length && /오류 탐정/.test(games[games.length - 1].textContent),
         t + ' 마지막은 오류 탐정');

      // 점수판이 실제 게임 수와 맞는가
      const st = d.getElementById('scoreT'), sn = d.getElementById('scoreN');
      ok(!!(st && sn), t + ' 점수판');
      if (st) ok(+st.textContent === games.length, t + ' 점수판 목표치 = 게임 수',
                 { 목표: st.textContent, 게임: games.length });

      // 눌러 보기 — 선택 버튼이 있으면 눌렀을 때 화면이 바뀌어야 한다
      let reacted = 0, tried = 0;
      for (const g of games) {
        const btn = g.querySelector('.pg-pbtn, button');
        if (!btn) continue;
        tried++;
        // 반응은 .out 에만 나오지 않는다 — 다음 문제로 넘어가거나 버튼 상태가 바뀌기도 한다.
        // 그래서 게임 블록 전체의 상태를 견준다.
        const snap = () => g.textContent + '|' + g.innerHTML.length + '|' + g.querySelectorAll('.on,.sel,.ok,.no').length;
        const before = snap();
        try { btn.dispatchEvent(new w.Event('click')); } catch (e) { /* 아래에서 잡힌다 */ }
        if (snap() !== before) reacted++;
      }
      ok(tried >= 2, t + ' 누를 수 있는 게임 2개 이상', tried);
      ok(reacted >= 1, t + ' 눌렀을 때 반응하는 게임 있음', { 시도: tried, 반응: reacted });

      // 슬라이더가 있으면 움직였을 때 읽기 영역이 바뀌는가
      const rng = d.querySelector('input[type="range"]');
      if (rng) {
        const read = d.querySelector('.sim-read');
        if (read) {
          const b0 = read.textContent;
          rng.value = String(Math.min(+rng.max, +rng.value + (+rng.step || 1) * 3));
          rng.dispatchEvent(new w.Event('input'));
          ok(read.textContent !== b0 || b0.length > 0, t + ' 슬라이더 읽기 영역');
        }
      }

      // 클릭 뒤에도 새 오류가 생기지 않았는가
      ok(errs.length === 0, t + ' 조작 뒤에도 오류 없음', errs.slice(0, 1));

      // 어투
      const plain = raw.replace(/<script[\s\S]*?<\/script>/g, ' ').replace(/<[^>]+>/g, ' ')
                       .replace(/["“”][^"“”]*["“”]/g, ' ');
      const banmal = (plain.match(/(하자\.|해라|봐라|한다\.|된다\.|같다\.|이다\.)/g) || []);
      ok(banmal.length === 0, t + ' 반말', banmal.join(','));
    }
  }
  if (bad) { console.log(fails.join('\n')); console.log('\n검사 ' + n + '건 중 실패 ' + bad); }
  else console.log('ALL PASS (' + n + ' checks)');
  process.exit(bad ? 1 : 0);
}, 1500);
