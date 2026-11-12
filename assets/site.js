
(()=>{
  const root=document.documentElement, body=document.body;
  const btn=document.querySelector('.menu-btn'), mega=document.getElementById('megameny');
  const header=document.querySelector('.masthead'), backdrop=document.querySelector('.mm-backdrop');
  mega.querySelectorAll('.mm-i').forEach((el,i)=>el.style.setProperty('--i',i));
  const setHdr=()=>root.style.setProperty('--hdr',Math.round(header.getBoundingClientRect().bottom)+'px');
  const focusables=()=>[btn,...mega.querySelectorAll('a[href],button:not([disabled]),input')].filter(el=>el.offsetParent!==null||el===btn);
  let open=false;
  function setOpen(v,{focus=true}={}){
    open=v; setHdr();
    root.classList.toggle('menu-open',v); body.classList.toggle('scroll-lock',v);
    btn.setAttribute('aria-expanded',v); btn.setAttribute('aria-label',v?'Lukk meny':'Åpne meny');
    mega.setAttribute('aria-hidden',!v); mega.inert=!v;
    if(v&&focus) setTimeout(()=>mega.querySelector('.mm-main').focus({preventScroll:true}),120);
    if(!v&&focus) btn.focus({preventScroll:true});
  }
  mega.inert=true;
  btn.addEventListener('click',()=>setOpen(!open));
  backdrop.addEventListener('click',()=>setOpen(false));
  document.querySelector('[data-open-search]').addEventListener('click',e=>{e.preventDefault();setOpen(true,{focus:false});setTimeout(()=>mega.querySelector('#mm-q').focus({preventScroll:true}),120)});
  document.addEventListener('keydown',e=>{
    if(!open) return;
    if(e.key==='Escape'){e.preventDefault();setOpen(false);return}
    if(e.key==='Tab'){const f=focusables(),first=f[0],last=f[f.length-1];
      if(e.shiftKey&&document.activeElement===first){e.preventDefault();last.focus()}
      else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus()}}
  });
  // ett rolig bilde som skifter med hovedsiden man peker på
  const figs=[...mega.querySelectorAll('.mm-fig')];
  const show=i=>figs.forEach(f=>f.classList.toggle('is-on',f.dataset.i==i));
  mega.querySelectorAll('.mm-main').forEach(a=>{const i=a.dataset.img;a.addEventListener('mouseenter',()=>show(i));a.addEventListener('focus',()=>show(i))});
  addEventListener('resize',setHdr,{passive:true}); addEventListener('scroll',setHdr,{passive:true}); setHdr();
  window.__menu={setOpen,show};
})();

/* Undersider: filtre, skuff og galleri (kun demo, filtrerer ikke data) */
(()=>{
  const dds=[...document.querySelectorAll('.f-dd')];
  const closeAll=except=>dds.forEach(d=>{if(d!==except){d.classList.remove('is-open');d.querySelector('.f-btn').setAttribute('aria-expanded','false')}});
  dds.forEach(d=>{
    const b=d.querySelector('.f-btn');
    b.addEventListener('click',e=>{e.stopPropagation();const o=!d.classList.contains('is-open');closeAll(d);d.classList.toggle('is-open',o);b.setAttribute('aria-expanded',o);if(o)setTimeout(()=>d.querySelector('input')?.focus(),60)});
    d.querySelector('.f-pop').addEventListener('click',e=>e.stopPropagation());
  });
  document.addEventListener('click',()=>closeAll());
  document.addEventListener('keydown',e=>{if(e.key==='Escape'){const o=dds.find(d=>d.classList.contains('is-open'));if(o){closeAll();o.querySelector('.f-btn').focus()}}});
  // aktive valg som brikker
  const status=document.querySelector('.f-active');
  const sync=()=>{
    if(!status) return;
    status.innerHTML='';
    const seen=new Set();document.querySelectorAll('.filters-scope input[type=checkbox]:checked').forEach(cb=>{if(seen.has(cb.dataset.v))return;seen.add(cb.dataset.v);
      const c=document.createElement('button');c.type='button';c.className='chip';c.innerHTML=cb.dataset.v+' <i aria-hidden="true">×</i>';c.setAttribute('aria-label','Fjern '+cb.dataset.v);
      c.onclick=()=>{document.querySelectorAll('.filters-scope input[data-v="'+CSS.escape(cb.dataset.v)+'"]').forEach(x=>x.checked=false);sync()};status.appendChild(c);
    });
    dds.forEach(d=>{const n=d.querySelectorAll('input:checked').length,s=d.querySelector('.n');if(s){s.textContent=n;s.hidden=!n}});
    document.querySelectorAll('.f-status .f-reset').forEach(r=>r.hidden=!status.children.length);
  };
  document.querySelectorAll('.filters-scope input[type=checkbox]').forEach(cb=>cb.addEventListener('change',()=>{document.querySelectorAll('.filters-scope input[data-v="'+CSS.escape(cb.dataset.v)+'"]').forEach(x=>x.checked=cb.checked);sync()}));
  document.querySelectorAll('.f-reset').forEach(r=>r.addEventListener('click',()=>{document.querySelectorAll('.filters-scope input:checked').forEach(x=>x.checked=false);sync()}));
  sync();
  // skuff
  const dr=document.querySelector('.drawer'),open=document.querySelectorAll('[data-drawer]');
  if(dr){
    const root=document.documentElement;let last=null;
    const set=v=>{root.classList.toggle('drawer-open',v);document.body.classList.toggle('scroll-lock',v);dr.inert=!v;dr.setAttribute('aria-hidden',!v);open.forEach(b=>b.setAttribute('aria-expanded',v));
      if(v){last=document.activeElement;setTimeout(()=>dr.querySelector('.drawer__close').focus(),80)}else if(last)last.focus()};
    dr.inert=true;
    open.forEach(b=>b.addEventListener('click',e=>{e.stopPropagation();closeAll();set(true)}));
    document.querySelectorAll('[data-drawer-close]').forEach(b=>b.addEventListener('click',()=>set(false)));
    document.addEventListener('keydown',e=>{if(!root.classList.contains('drawer-open'))return;
      if(e.key==='Escape'){set(false);return}
      if(e.key==='Tab'){const f=[...dr.querySelectorAll('button,summary,input,a[href],select')].filter(x=>x.offsetParent!==null);const a=f[0],z=f[f.length-1];
        if(e.shiftKey&&document.activeElement===a){e.preventDefault();z.focus()}else if(!e.shiftKey&&document.activeElement===z){e.preventDefault();a.focus()}}});
    window.__drawer=set;
  }
  // galleri
  document.querySelectorAll('.thumbs button').forEach(b=>b.addEventListener('click',()=>{
    const g=b.closest('.gallery'),m=g.querySelector('.gallery__main img');
    m.style.opacity=0;setTimeout(()=>{m.src=b.dataset.src;m.alt=b.dataset.alt||'';m.style.opacity=1},180);
    g.querySelectorAll('.thumbs button').forEach(x=>x.setAttribute('aria-pressed',x===b));
  }));
})();
/* Artikkelkategorier (demo: filtrerer kortene på siden) */
(()=>{const tabs=document.querySelectorAll('.cat-tabs button');if(!tabs.length)return;
tabs.forEach(t=>t.addEventListener('click',()=>{const c=t.dataset.cat;tabs.forEach(x=>x.setAttribute('aria-pressed',x===t));
let any=0;document.querySelectorAll('.lead[data-cat],.acard[data-cat]').forEach(el=>{const on=!c||el.dataset.cat===c;el.hidden=!on;if(on)any++});
document.querySelectorAll('section[data-year]').forEach(g=>{const vis=[...g.children].some(x=>!x.hidden);g.hidden=!vis;const h=document.querySelector('.year[data-year="'+g.dataset.year+'"]');if(h){h.hidden=!vis;const n=[...g.children].filter(x=>!x.hidden).length;h.querySelector('span').textContent=n+(n===1?' artikkel':' artikler')}});
document.querySelector('.cat-empty').hidden=!!any;}));})();
/* Søk og filter: venstre kolonne på desktop, panel fra venstre på mobil */
(()=>{const sf=document.querySelector('.sf');if(!sf)return;const root=document.documentElement,btn=document.querySelector('.sf-open'),mq=matchMedia('(max-width:900px)');let last=null;
const isOpen=()=>root.classList.contains('sf-open-state');
const sync=()=>{sf.inert=mq.matches&&!isOpen();if(mq.matches){sf.setAttribute('role','dialog');sf.setAttribute('aria-modal','true')}else{sf.removeAttribute('role');sf.removeAttribute('aria-modal');if(isOpen())set(false)}};
const set=v=>{root.classList.toggle('sf-open-state',v);document.body.classList.toggle('scroll-lock',v);btn&&btn.setAttribute('aria-expanded',v);sync();
 if(v){last=document.activeElement;setTimeout(()=>sf.querySelector('.sf__close').focus(),80)}else if(last){last.focus();last=null}};
btn&&btn.addEventListener('click',()=>set(true));
document.querySelectorAll('[data-sf-close]').forEach(b=>b.addEventListener('click',()=>set(false)));
document.addEventListener('keydown',e=>{if(!isOpen())return;if(e.key==='Escape'){set(false);return}
 if(e.key==='Tab'){const f=[...sf.querySelectorAll('button,summary,input,select,a[href]')].filter(x=>x.offsetParent!==null);const a=f[0],z=f[f.length-1];
 if(e.shiftKey&&document.activeElement===a){e.preventDefault();z.focus()}else if(!e.shiftKey&&document.activeElement===z){e.preventDefault();a.focus()}}});
mq.addEventListener('change',sync);sync();window.__sf=set;})();
