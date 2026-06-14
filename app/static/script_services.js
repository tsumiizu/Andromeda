/* ── CURSOR ── */
const cGal=document.getElementById('cursorGalaxy');
const cRing=document.getElementById('cursorRing');
let mx=-200,my=-200,rx=-200,ry=-200;
document.addEventListener('mousemove',e=>{mx=e.clientX;my=e.clientY;cGal.style.left=mx+'px';cGal.style.top=my+'px'});
(function ringLoop(){rx+=(mx-rx)*.1;ry+=(my-ry)*.1;cRing.style.left=rx+'px';cRing.style.top=ry+'px';requestAnimationFrame(ringLoop)})();
document.querySelectorAll('a,button,.service-card-v2,.featured-service,.step-item,.faq-question').forEach(el=>{
  el.addEventListener('mouseenter',()=>{cGal.classList.add('expand');cRing.classList.add('expand')});
  el.addEventListener('mouseleave',()=>{cGal.classList.remove('expand');cRing.classList.remove('expand')});
});

/* ── STARS ── */
const canvas=document.getElementById('stars-canvas');
const ctx=canvas.getContext('2d');
let stars=[];
function resizeCanvas(){canvas.width=window.innerWidth;canvas.height=window.innerHeight}
function makeStars(){stars=[];const n=Math.min(500,Math.floor(canvas.width*canvas.height/7000));for(let i=0;i<n;i++){stars.push({x:Math.random()*canvas.width,y:Math.random()*canvas.height,r:Math.random()*1.6+.15,phase:Math.random()*Math.PI*2,freq:.25+Math.random()*1.5,lo:.04+Math.random()*.1,hi:.45+Math.random()*.55})}}
function drawStars(ts){const t=ts*.003;ctx.clearRect(0,0,canvas.width,canvas.height);for(const s of stars){const norm=(Math.sin(s.phase+t*s.freq)+1)*.5;const a=s.lo+(s.hi-s.lo)*norm;ctx.beginPath();ctx.arc(s.x,s.y,s.r,0,Math.PI*2);ctx.fillStyle=`rgba(215,238,255,${a.toFixed(3)})`;ctx.fill()}requestAnimationFrame(drawStars)}
resizeCanvas();makeStars();requestAnimationFrame(drawStars);
window.addEventListener('resize',()=>{resizeCanvas();makeStars()});

/* ── FADE-IN ── */
const fadeObs=new IntersectionObserver(entries=>{entries.forEach(e=>{if(e.isIntersecting)e.target.classList.add('visible')})},{threshold:.1});
document.querySelectorAll('.fade-in').forEach(el=>fadeObs.observe(el));

/* ── FILTER ── */
document.querySelectorAll('.filter-btn').forEach(btn=>{
  btn.addEventListener('click',()=>{
    document.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    const f=btn.dataset.filter;
    document.querySelectorAll('[data-category]').forEach(card=>{
      const show=f==='all'||card.dataset.category===f;
      card.style.opacity=show?'1':'.25';
      card.style.pointerEvents=show?'':'none';
      card.style.transition='opacity .4s';
    });
  });
});

/* ── FAQ ── */
document.querySelectorAll('.faq-item').forEach(item=>{
  item.querySelector('.faq-question').addEventListener('click',()=>{
    const isOpen=item.classList.contains('open');
    document.querySelectorAll('.faq-item').forEach(i=>i.classList.remove('open'));
    if(!isOpen)item.classList.add('open');
  });
});

/* ── MODAL ── */
function openModal(){document.getElementById('loginModal').classList.add('active');document.body.style.overflow='hidden'}
function closeModal(){document.getElementById('loginModal').classList.remove('active');document.body.style.overflow=''}
document.getElementById('loginModal').addEventListener('click',function(e){if(e.target===this)closeModal()});
document.getElementById('loginModal').style.cssText+='';
// override active state
const style=document.createElement('style');
style.textContent='.modal-overlay.active{opacity:1!important;visibility:visible!important}.modal-overlay.active>div{transform:translateY(0) scale(1)!important}';
document.head.appendChild(style);
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeModal()});

function handleLogin(e){
  e.preventDefault();
  const email=document.getElementById('loginEmail').value;
  const pass=document.getElementById('loginPass').value;
  const errEl=document.getElementById('loginError');
  const btn=e.target.querySelector('button[type=submit]');
  btn.textContent='Verificando...';btn.disabled=true;
  setTimeout(()=>{
    if(email&&pass.length>=6){btn.textContent='Acesso Autorizado ✓';errEl.style.display='none';setTimeout(()=>{closeModal();btn.textContent='Acessar Painel ✦';btn.disabled=false},1500)}
    else{errEl.style.display='block';btn.textContent='Acessar Painel ✦';btn.disabled=false}
  },900);
}