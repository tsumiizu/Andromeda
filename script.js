/* ══════════════════════════════════════
   CURSOR
══════════════════════════════════════ */
const cGal = document.getElementById('cursorGalaxy');
const cRing = document.getElementById('cursorRing');
let mx=-200,my=-200,rx=-200,ry=-200;

document.addEventListener('mousemove', e => {
  mx=e.clientX; my=e.clientY;
  cGal.style.left=mx+'px'; cGal.style.top=my+'px';
});
(function ringLoop(){
  rx+=(mx-rx)*0.1; ry+=(my-ry)*0.1;
  cRing.style.left=rx+'px'; cRing.style.top=ry+'px';
  requestAnimationFrame(ringLoop);
})();

document.querySelectorAll('a,button,.stat-card,.service-card,.step-card,.review-card,.contact-item').forEach(el=>{
  el.addEventListener('mouseenter',()=>{cGal.classList.add('expand');cRing.classList.add('expand')});
  el.addEventListener('mouseleave',()=>{cGal.classList.remove('expand');cRing.classList.remove('expand')});
});

/* ══════════════════════════════════════
   STARS — TWINKLING REAL
   Usa o timestamp do requestAnimationFrame
   para que cada estrela pisce em frequência
   e fase próprias → efeito completamente vivo
══════════════════════════════════════ */
const canvas = document.getElementById('stars-canvas');
const ctx    = canvas.getContext('2d');
let stars    = [];

function resizeCanvas(){
  canvas.width  = window.innerWidth;
  canvas.height = window.innerHeight;
}

function makeStars(){
  stars=[];
  // ~1 estrela por 7000px² — ajuste conforme quiser
  const n = Math.min(500, Math.floor(canvas.width*canvas.height/7000));
  for(let i=0;i<n;i++){
    stars.push({
      x:   Math.random()*canvas.width,
      y:   Math.random()*canvas.height,
      r:   Math.random()*1.6+0.15,
      phase: Math.random()*Math.PI*2,
      freq:  0.25+Math.random()*1.5,  // rad/s — variedade grande
      lo:    0.04+Math.random()*0.1,
      hi:    0.45+Math.random()*0.55,
    });
  }
}

function drawStars(ts){
  const t = ts*0.003;
  ctx.clearRect(0,0,canvas.width,canvas.height);
  for(const s of stars){
    const norm = (Math.sin(s.phase + t*s.freq)+1)*0.5; // 0..1
    const a    = s.lo+(s.hi-s.lo)*norm;
    ctx.beginPath();
    ctx.arc(s.x,s.y,s.r,0,Math.PI*2);
    ctx.fillStyle=`rgba(215,238,255,${a.toFixed(3)})`;
    ctx.fill();
  }
  requestAnimationFrame(drawStars);
}

resizeCanvas(); makeStars(); requestAnimationFrame(drawStars);
window.addEventListener('resize',()=>{ resizeCanvas(); makeStars(); });

/* ══════════════════════════════════════
   TICKER — gera via JS para manter DRY
══════════════════════════════════════ */
const tickerItems=[
  'Sites Profissionais','Lojas Virtuais','Sistemas de Gestão',
  'Landing Pages','Portfólios Digitais','Automação de Processos',
  'Identidade Visual','SEO & Performance'
];
const starSVG=(c)=>`<span class="ticker-sep"><svg viewBox="0 0 14 14" fill="none"><path d="M7 0.5C7.4 4.5,7.5 6,7 7C6.5 6,6.6 4.5,7 0.5Z" fill="${c}"/><path d="M7 13.5C6.6 9.5,6.5 8,7 7C7.5 8,7.4 9.5,7 13.5Z" fill="${c}"/><path d="M0.5 7C4.5 7.4,6 7.5,7 7C6 6.5,4.5 6.6,0.5 7Z" fill="${c}"/><path d="M13.5 7C9.5 6.6,8 6.5,7 7C8 7.5,9.5 7.4,13.5 7Z" fill="${c}"/></svg></span>`;
const tickerHTML=[...tickerItems,...tickerItems].map((t,i)=>
  `<div class="ticker-item">${t}${starSVG(i%2===0?'#00d4ff':'#3b9eff')}</div>`
).join('');
document.getElementById('tickerTrack').innerHTML=tickerHTML;

/* ══════════════════════════════════════
   REVIEWS — gera via JS
══════════════════════════════════════ */
const reviews=[
  {initials:'MR',name:'Marcos Rocha',role:'Dono — Ótica Rocha & Filhos',badge:'Loja Virtual',
   text:'A Andromeda transformou minha loja física em um e-commerce completo em menos de 3 semanas. Hoje atendo clientes de todo o Brasil. Resultado surpreendente e profissionalismo total.'},
  {initials:'PS',name:'Dra. Patrícia Silva',role:'Médica — Clínica Bem-Estar',badge:'Site Profissional',
   text:'Desenvolveram o site do meu consultório com agendamento online integrado. Meus pacientes adoraram a facilidade. Reduzi em 80% as ligações para marcação de consultas.'},
  {initials:'CF',name:'Carlos Ferreira',role:'Sócio — Distribuidora FerTech',badge:'Sistema de Gestão',
   text:'O sistema de gestão que a Andromeda criou economiza horas de trabalho toda semana. Controle total de pedidos, estoque e clientes em um só lugar. Valeu cada centavo.'},
  {initials:'AL',name:'Amanda Lima',role:'Diretora — Studio AL Moda',badge:'Landing Page',
   text:'Precisávamos de uma landing page de alta conversão. A Andromeda entregou em 5 dias um trabalho que superou todas as nossas expectativas. Taxa de conversão triplicou.'},
  {initials:'JM',name:'João Mendes',role:'Fotógrafo Profissional',badge:'Portfólio Digital',
   text:'Meu portfólio fotográfico ficou incrível. A equipe entendeu exatamente o que eu queria e entregou uma identidade visual única. Recomendo de olhos fechados.'},
  {initials:'RP',name:'Ricardo Pinheiro',role:'CEO — Construtora Pinheiro',badge:'SEO & Performance',
   text:'Site novo + SEO bem feito = dobrei as visitas orgânicas em 2 meses. A Andromeda não só criou o site, mas garantiu que ele apareça no Google. Isso faz toda a diferença.'},
];
const reviewCard=r=>`
<div class="review-card">
  <div class="review-stars">★★★★★ <span>5.0</span></div>
  <span class="review-quote-mark">"</span>
  <p class="review-text">${r.text}</p>
  <div class="review-author">
    <div class="review-avatar">${r.initials}</div>
    <div><div class="review-name">${r.name}</div><div class="review-role">${r.role}</div></div>
    <div class="review-service-badge">${r.badge}</div>
  </div>
</div>`;
document.getElementById('reviewsTrack').innerHTML=[...reviews,...reviews].map(reviewCard).join('');

/* ══════════════════════════════════════
   FADE-IN ON SCROLL
══════════════════════════════════════ */
const fadeObs=new IntersectionObserver(entries=>{
  entries.forEach(e=>{ if(e.isIntersecting) e.target.classList.add('visible'); });
},{threshold:0.1});
document.querySelectorAll('.fade-in').forEach(el=>fadeObs.observe(el));

/* ══════════════════════════════════════
   MODAL
══════════════════════════════════════ */
function openModal(){document.getElementById('loginModal').classList.add('active');document.body.style.overflow='hidden'}
function closeModal(){document.getElementById('loginModal').classList.remove('active');document.body.style.overflow=''}
document.getElementById('loginModal').addEventListener('click',function(e){if(e.target===this)closeModal()});
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeModal()});

function handleLogin(e){
  e.preventDefault();
  const email=document.getElementById('loginEmail').value;
  const pass=document.getElementById('loginPass').value;
  const errEl=document.getElementById('loginError');
  const btn=e.target.querySelector('button[type=submit]');
  btn.textContent='Verificando...'; btn.disabled=true;
  setTimeout(()=>{
    if(email&&pass.length>=6){
      btn.textContent='Acesso Autorizado ✓';
      btn.style.background='linear-gradient(135deg,#0d5e3f,#1a9e6f)';
      errEl.style.display='none';
      setTimeout(()=>{closeModal();btn.textContent='Acessar Painel ✦';btn.style.background='';btn.disabled=false},1500);
    }else{errEl.style.display='block';btn.textContent='Acessar Painel ✦';btn.disabled=false}
  },900);
}

/* ══════════════════════════════════════
   CONTACT FORM
══════════════════════════════════════ */
function handleSubmit(e){
  e.preventDefault();
  const btn=e.target.querySelector('.btn-send');
  btn.textContent='Mensagem Enviada ✓';
  btn.style.background='linear-gradient(135deg,#0d5e3f,#1a9e6f)';
  btn.style.borderColor='#1a9e6f';
  setTimeout(()=>{btn.textContent='Enviar Mensagem ✦';btn.style.background='';btn.style.borderColor='';e.target.reset()},3500);
}

/* ══════════════════════════════════════
   COUNTER ANIMATION
══════════════════════════════════════ */
function animateCounter(el,target,suffix){
  let v=0; const step=target/60;
  const ti=setInterval(()=>{
    v+=step;
    if(v>=target){el.textContent=target+suffix;clearInterval(ti)}
    else{el.textContent=Math.floor(v)+suffix}
  },16);
}
const statObs=new IntersectionObserver(entries=>{
  entries.forEach(entry=>{
    if(!entry.isIntersecting)return;
    const card=entry.target; const numEl=card.querySelector('.stat-num');
    if(!numEl||card.dataset.animated)return;
    card.dataset.animated='1';
    const txt=numEl.textContent;
    if(txt.includes('200'))animateCounter(numEl,200,'+');
    else if(txt.includes('98'))animateCounter(numEl,98,'%');
    else if(txt.includes('4+'))animateCounter(numEl,4,'+');
  });
},{threshold:.5});
document.querySelectorAll('.stat-card').forEach(c=>statObs.observe(c));