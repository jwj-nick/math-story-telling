// smoke_b5.js — B5 로 낱말·왜 상자를 더한 세 페이지를 실제 DOM 으로 확인한다.
const fs = require('fs');
const { JSDOM } = require('jsdom');
const ROOT = 'C:/Kids/math-story-telling/40_grades/middle/';
let bad = 0, n = 0;
const ok = (c, m, x) => { n++; if (!c) { bad++; console.log('FAIL', m, x === undefined ? '' : JSON.stringify(x)); } };

for (const [dir] of [['math2/app2'], ['math3/app3']]) {
  const css = fs.readFileSync(ROOT + dir + '/concept.css', 'utf8');
  ok(/\.wordbox\{/.test(css), dir + ' concept.css 에 .wordbox');
  ok(/\.whybox\{/.test(css), dir + ' concept.css 에 .whybox');
  ok(/@media \(max-width:480px\)[\s\S]{0,140}wordbox dl/.test(css), dir + ' 좁은 폰 배치');
}

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
      w.addEventListener('error', e => errs.push(String(e.error && e.error.stack || e.message).split('\n')[0]));
    }
  });
  return { w: d.window, d: d.window.document, errs };
};

// 단원마다 반드시 들어가야 하는 한자와 "왜" 문구
const WANT = [
  ['math2/app2', 'u7.html', ['外心', '內心', '垂心', '二等邊三角形'], ['왜 외심은 삼각형 밖으로'], 1],
  ['math3/app3', 'u11.html', ['散布度', '偏差', '分散', '標準偏差', '最頻値'], ['왜 편차를 그냥 더하지 않고'], 1],
  ['math3/app3', 'u12.html', ['四分位數', '四分位範圍', '散點圖', '相關關係'], ['왜 상자 그림은 극단값에', '상관관계가 있으면 원인과 결과'], 2],
];

setTimeout(() => {
  for (const [dir, file, chars, whys, nWhy] of WANT) {
    const t = dir.split('/')[0] + '/' + file.replace('.html', '');
    const { w, d, errs } = dom(dir, file);
    const raw = fs.readFileSync(ROOT + dir + '/' + file, 'utf8');

    ok(errs.length === 0, t + ' 런타임 오류 없음', errs.slice(0, 1));
    ok(/<\/html>\s*$/.test(raw), t + ' 문서 종결');
    ok((raw.match(/<section/g) || []).length === (raw.match(/<\/section>/g) || []).length, t + ' section 짝');

    const wb = d.querySelectorAll('.wordbox'), why = d.querySelectorAll('.whybox');
    ok(wb.length === 1, t + ' 낱말 상자 1개', wb.length);
    ok(why.length === nWhy, t + ' 왜 상자 ' + nWhy + '개', why.length);

    const body = d.body.textContent;
    for (const c of chars) ok(body.includes(c), t + ' 한자 ' + c);
    for (const q of whys) ok(body.includes(q), t + ' 왜 문구', q);

    wb.forEach(b => {
      const dt = b.querySelectorAll('dt'), dd = b.querySelectorAll('dd');
      ok(dt.length === dd.length && dt.length >= 5, t + ' dt/dd 짝과 개수', { dt: dt.length, dd: dd.length });
      dt.forEach((e, k) => ok(!!e.querySelector('i') && e.querySelector('i').textContent.trim().length > 0,
                              t + ' 낱말 ' + (k + 1) + ' 원어 표기'));
      dd.forEach((e, k) => ok(e.textContent.trim().length > 20, t + ' 낱말 뜻 ' + (k + 1) + ' 내용',
                              e.textContent.trim().length));
    });
    why.forEach((e, k) => {
      ok(!!e.querySelector('.why-h'), t + ' 왜 상자 ' + (k + 1) + ' 머리말');
      ok(e.textContent.trim().length > 100, t + ' 왜 상자 ' + (k + 1) + ' 내용', e.textContent.trim().length);
    });

    // 기존 진행바·채점이 그대로 도는지
    ok(!!d.getElementById('prog'), t + ' 진행바 살아 있음');
    const btn = d.getElementById('c1b'), inp = d.getElementById('c1'), out = d.getElementById('c1o');
    if (btn && inp && out) {
      inp.value = '__틀린답__'; btn.dispatchEvent(new w.Event('click'));
      ok(out.textContent.length > 0, t + ' 채점 반응');
    }

    const plain = raw.replace(/<script[\s\S]*?<\/script>/g, ' ').replace(/<[^>]+>/g, ' ')
                     .replace(/["“”][^"“”]*["“”]/g, ' ');
    const banmal = (plain.match(/(하자\.|해라|봐라|한다\.|된다\.|같다\.|이다\.)/g) || []);
    ok(banmal.length === 0, t + ' 반말', banmal.join(','));
  }
  console.log(bad ? ('\n검사 ' + n + '건 중 실패 ' + bad) : ('ALL PASS (' + n + ' checks)'));
  process.exit(bad ? 1 : 0);
}, 1000);
