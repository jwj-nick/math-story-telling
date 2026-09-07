// smoke_d.js — 중1 심화 13개 보강본을 실제 DOM 으로 띄워 확인한다.
// 새로 넣은 유도 절과 도전 문제가 도는지, 기존 실험실이 상하지 않았는지.
const fs=require('fs');
const {JSDOM}=require('jsdom');
const APP='C:/Kids/math-story-telling/40_grades/middle/math1/app1/';
let bad=0,n=0;
const ok=(c,m,x)=>{n++; if(!c){bad++; console.log('FAIL',m,x===undefined?'':JSON.stringify(x));} };

const ANS={1:'13',2:'23',3:'22',4:'10',5:'-7',6:'15',7:'83',8:'3',9:'4',10:'15',11:'30',12:'36',13:'18'};
const NEXT={1:'u2.html',2:'u3.html',3:'u4.html',4:'u5.html',5:'u6.html',6:'u7.html',7:'u8.html',
            8:'u9.html',9:'u10.html',10:'u11.html',11:'u12.html',12:'u13.html',13:'data-mastery.html'};

const CSS=fs.readFileSync(APP+'concept.css','utf8');
ok(/\.derive\.narr\{/.test(CSS),'concept.css 에 .derive.narr');

const dom=file=>{
  let html=fs.readFileSync(APP+file,'utf8');
  html=html.replace(/<script src="concept\.js[^"]*"><\/script>/,'<script>'+fs.readFileSync(APP+'concept.js','utf8')+'</script>');
  html=html.replace(/<link rel="stylesheet"[^>]*>/,'');
  const errs=[];
  const d=new JSDOM(html,{runScripts:'dangerously',pretendToBeVisual:true,url:'http://localhost/app/'+file,
    beforeParse(w){
      w.IntersectionObserver=class{constructor(cb){this.cb=cb;}observe(el){this.cb([{isIntersecting:true,target:el}]);}unobserve(){}disconnect(){}};
      w.matchMedia=w.matchMedia||function(){return{matches:false,addEventListener(){},removeEventListener(){},addListener(){},removeListener(){}};};
      w.requestAnimationFrame=cb=>setTimeout(()=>cb(Date.now()),0);
      w.addEventListener('error',e=>errs.push(String(e.error&&e.error.stack||e.message)));
    }});
  return {w:d.window,d:d.window.document,errs};
};

setTimeout(()=>{
  for(let i=1;i<=13;i++){
    const file='d'+i+'.html', t='d'+i;
    const {w,d,errs}=dom(file);
    ok(errs.length===0,t+' 런타임 오류 없음',errs.slice(0,1));

    const raw=fs.readFileSync(APP+file,'utf8');
    ok(/<\/html>\s*$/.test(raw),t+' 문서 종결');
    ok((raw.match(/<section/g)||[]).length===(raw.match(/<\/section>/g)||[]).length,t+' section 짝');
    ok((raw.match(/<div class="card">/g)||[]).length>=2,t+' card 2개 이상');

    // 절 번호 1~4 가 모두 있는지
    const nums=[...d.querySelectorAll('.eyebrow .n')].map(e=>e.textContent);
    ok(nums.join(',')==='1,2,3,4',t+' 절 번호 1~4',nums);

    // 유도 절 — 단계 4개, 처음엔 전부 감춰져 있고 버튼을 4번 누르면 다 열린다
    const st=d.querySelectorAll('.derive.narr .step');
    ok(st.length===4,t+' 유도 단계 4개',st.length);
    ok([...st].every(e=>!e.classList.contains('on')),t+' 처음엔 단계가 감춰짐');
    ok([...st].every(e=>e.textContent.trim().length>10),t+' 단계마다 내용 있음');
    const db=d.getElementById('dstep');
    ok(!!db,t+' 다음 단계 버튼');
    if(db){
      for(let k=0;k<4;k++) db.dispatchEvent(new w.Event('click'));
      ok([...st].every(e=>e.classList.contains('on')),t+' 네 번 누르면 다 열림');
      ok(db.disabled===true,t+' 다 열면 버튼 잠김');
    }

    // 도전 — 오답이면 되묻고, 정답이면 정답이라 말한다
    const inp=d.getElementById('ch1'), btn=d.getElementById('ch1b'), out=d.getElementById('ch1o');
    ok(!!(inp&&btn&&out),t+' 도전 입력·버튼·출력');
    if(inp&&btn&&out){
      btn.dispatchEvent(new w.Event('click'));
      ok(/답을 넣어|숫자를 넣어/.test(out.textContent),t+' 빈칸이면 안내',out.textContent.slice(0,30));
      inp.value='99999'; btn.dispatchEvent(new w.Event('click'));
      const wrong=out.textContent;
      ok(wrong.length>0&&!/정답/.test(wrong),t+' 오답 반응',wrong.slice(0,30));
      inp.value=ANS[i]; btn.dispatchEvent(new w.Event('click'));
      ok(/정답/.test(out.textContent),t+' 정답 반응 (답 '+ANS[i]+')',out.textContent.slice(0,40));
    }

    // 힌트 3단
    const hb=d.getElementById('hbtn');
    ok(!!hb,t+' 힌트 버튼');
    if(hb){
      const hs=[1,2,3].map(k=>d.getElementById('h'+k));
      ok(hs.every(e=>e&&!e.classList.contains('show')),t+' 힌트는 처음엔 닫힘');
      ok(hs.every(e=>e&&/💡/.test(e.textContent)&&e.textContent.length>12),t+' 힌트마다 내용 있음');
      for(let k=0;k<3;k++) hb.dispatchEvent(new w.Event('click'));
      ok(hs.every(e=>e.classList.contains('show')),t+' 세 번 누르면 힌트 셋 다 열림');
      ok(hb.disabled===true,t+' 힌트 다 쓰면 버튼 잠김');
    }

    // 다음 링크가 실재하는 파일을 가리키는지
    const link=d.querySelector('.nextlink a.golink');
    ok(!!link,t+' 다음 링크');
    if(link){
      const href=link.getAttribute('href');
      ok(href===NEXT[i],t+' 링크 대상',href);
      ok(fs.existsSync(APP+href),t+' 링크한 파일이 실재',href);
      ok(link.textContent.trim().length>6,t+' 링크 문구');
    }

    // 기존 실험실이 살아 있는지 + 안내 문구
    ok(!!d.querySelector('.sim, #gsim, .derive'),t+' 실험실/카드 살아 있음');
    ok(/도전 문제.*하나가 있어요/.test(d.querySelector('.intro').textContent),t+' 안내 문구 갱신');

    // 어투
    const plain=raw.replace(/<script[\s\S]*?<\/script>/g,' ').replace(/<[^>]+>/g,' ');
    const spoken=plain.replace(/["“”][^"“”]*["“”]/g,' ');   // 인용문은 원문 그대로 두므로 어투 검사에서 뺀다
    const banmal=(spoken.match(/(하자\.|해라|봐라|한다\.|된다\.|같다\.|이다\.)/g)||[]);
    ok(banmal.length===0,t+' 반말',banmal.join(','));
  }
  console.log(bad? ('\n검사 '+n+'건 중 실패 '+bad) : ('ALL PASS ('+n+' checks)'));
  process.exit(bad?1:0);
},1200);
