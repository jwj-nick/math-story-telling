// H 문항 정답 독립 재계산: spec.expr(수식) vs p 페이지 P('bN4',...) ans / spec.ans
const fs=require('fs');
const spec=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const html=fs.readFileSync(process.argv[3],'utf8');
const page={}; for(const m of html.matchAll(/P\('b(\d)4','a\d4',(.+?),'o\d4','([^']*)'\)/g)) page[m[1]]={ans:m[2].trim(),disp:m[3]};
let bad=0;
for(const p of spec.problems){
  const pg=page[String(p.type)]; if(!pg){console.log('MISSING type',p.type);bad++;continue;}
  const exp=Function('return ('+p.expr+')')();
  const got=Function('return ('+pg.ans+')')();
  const ok=Math.abs(exp-got)<1e-9 && String(pg.disp)===String(p.disp);
  if(!ok){bad++;console.log('MISMATCH type',p.type,'expr=',exp,'page=',got,'disp',pg.disp,'/',p.disp);} else console.log('ok',p.type,pg.disp);
}
// TOTAL / TYPES
if(!/TOTAL=28;/.test(html)||!/c7:4\}/.test(html)){bad++;console.log('TOTAL/TYPES not updated');}
console.log('unit',spec.unit,'bad',bad); process.exit(bad?1:0);
