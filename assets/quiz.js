/* VVIS quiz engine: config-driven, client-side only, nothing stored. window.VVIS_QUIZ = {id, questions:[{q,help,opts:[[label,value]],multi?,flag?,flagIf?}], result(answers, ctx) -> {tier,label,text,flags,extraCta?} } */
(function(){
  var cfg=window.VVIS_QUIZ; var root=document.getElementById('vvis-quiz'); if(!cfg||!root) return;
  var PHREESIA='https://phreesia.me/SelfSchedulingVascular', PHONE='901-390-2930', TEL='tel:+19013902930';
  var Q=cfg.questions, answers=[], i=0, body=root.querySelector('.vq-body'), bar=root.querySelector('.vq-bar');
  function el(tag,cls,text){var e=document.createElement(tag); if(cls) e.className=cls; if(text!==undefined) e.textContent=text; return e;}
  function clear(n){while(n.firstChild) n.removeChild(n.firstChild);}
  function render(){
    bar.style.width=Math.round(i/Q.length*100)+'%';
    if(i>=Q.length) return result();
    var q=Q[i]; clear(body);
    body.appendChild(el('div','vq-step','Question '+(i+1)+' of '+Q.length));
    body.appendChild(el('h3','vq-q',q.q));
    if(q.help) body.appendChild(el('p','vq-help',q.help));
    var opts=el('div','vq-opts'); opts.setAttribute('role','group');
    var sel=answers[i]; if(q.multi && !Array.isArray(sel)) sel=[];
    q.opts.forEach(function(o,k){ var b=el('button','vq-opt'+(q.multi&&sel.indexOf(k)>=0?' on':''),o[0]); b.type='button';
      b.addEventListener('click',function(){ if(q.multi){ var p=sel.indexOf(k); if(o[2]==='none'){ sel=[k]; } else { if(p>=0) sel.splice(p,1); else { sel=sel.filter(function(x){return q.opts[x][2]!=='none';}); sel.push(k);} } answers[i]=sel.slice(); render(); } else { answers[i]=k; i++; render(); root.scrollIntoView({behavior:'smooth',block:'start'}); } });
      opts.appendChild(b); });
    body.appendChild(opts);
    var nav=el('div','vq-nav'); var back=el('button','vq-back','← Back'); back.type='button'; if(i===0) back.disabled=true; back.addEventListener('click',function(){ if(i>0){ i--; render(); } }); nav.appendChild(back);
    if(q.multi){ var next=el('button','vq-next','Continue →'); next.type='button'; next.disabled=!(sel&&sel.length); next.addEventListener('click',function(){ answers[i]=sel.slice(); i++; render(); root.scrollIntoView({behavior:'smooth',block:'start'}); }); nav.appendChild(next); }
    else nav.appendChild(el('span','vq-step','No personal information is collected.'));
    body.appendChild(nav);
    var first=body.querySelector('.vq-opt'); if(first&&!q.multi) first.focus({preventScroll:true});
  }
  function value(k){ var q=Q[k], a=answers[k]; if(q.multi){ return (a||[]).reduce(function(s,idx){return s+(q.opts[idx][1]||0);},0); } var o=q.opts[a]; return o?o[1]:0; }
  function chosen(k,label){ var q=Q[k], a=answers[k]; if(q.multi) return (a||[]).some(function(idx){return q.opts[idx][0]===label;}); var o=q.opts[a]; return !!o && o[0]===label; }
  function result(){
    var ctx={value:value, chosen:chosen, PHONE:PHONE};
    var score=0, flags=[]; Q.forEach(function(q,k){ var v=value(k); score+=v; if(q.flag && v>=(q.flagAt||4)) flags.push(q.flag); });
    var r=cfg.result({score:score, flags:flags, value:value, chosen:chosen});
    clear(body); bar.style.width='100%';
    var wrap=el('div','vq-result'); wrap.setAttribute('role','status');
    wrap.appendChild(el('span','vq-tier '+r.tier,r.label)); wrap.appendChild(el('h3',null,'Your result')); wrap.appendChild(el('p',null,r.text));
    var fl=r.flags||flags; if(fl.length){ var ul=el('ul','vq-flags'); fl.forEach(function(f){ul.appendChild(el('li',null,f));}); wrap.appendChild(ul); }
    if(r.urgent){ var up=el('p'); up.appendChild(el('strong',null,r.urgent)); wrap.appendChild(up); }
    var cta=el('div','vq-cta'); var a1=el('a','vq-btn',r.cta1||'Schedule online'); a1.href=r.cta1url||PHREESIA; var a2=el('a','vq-btn alt','Call '+PHONE); a2.href=TEL; cta.appendChild(a1); cta.appendChild(a2); wrap.appendChild(cta);
    wrap.appendChild(el('p','vq-disc',(cfg.disclaimer||'This quiz is an educational screening tool, not a diagnosis. Only an examination can confirm what is going on.')+' If you have sudden severe symptoms, call 911. Your answers stay in your browser and are not sent to us.'));
    var rp=el('p'); var rs=el('button','vq-restart','Start over'); rs.type='button'; rs.addEventListener('click',function(){answers=[];i=0;render();}); rp.appendChild(rs); wrap.appendChild(rp);
    body.appendChild(wrap);
    try{ if(typeof gtag==='function') gtag('event',(cfg.id||'quiz')+'_complete',{risk_tier:r.tier}); }catch(e){}
  }
  render();
})();
