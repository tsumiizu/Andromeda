/* ════════════════════════════════════════════════════════════════
   ANDROMEDA — SCRIPT UNIFICADO
   Cobre: index (home) + services (serviços)
   Módulos:
     1. Cursor galáxia
     2. Canvas de estrelas
     3. Ticker (home)
     4. Carrossel de depoimentos (home)
     5. Fade-in ao scroll
     6. Filtro de serviços (services)
     7. FAQ accordion (services)
     8. Modal de login
     9. Formulário de contato (home)
    10. Contador animado (home)
   ════════════════════════════════════════════════════════════════ */


/* ══════════════════════════════════════════════════════════════
   1. CURSOR GALÁXIA
   — cGal segue o mouse em tempo real
   — cRing segue com inércia (lerp 10%)
   — Elementos interativos expandem o cursor ao hover
══════════════════════════════════════════════════════════════ */
const cGal  = document.getElementById('cursorGalaxy');
const cRing = document.getElementById('cursorRing');
let mx = -200, my = -200; // posição do mouse
let rx = -200, ry = -200; // posição suavizada do anel

document.addEventListener('mousemove', e => {
  mx = e.clientX; my = e.clientY;
  cGal.style.left = mx + 'px';
  cGal.style.top  = my + 'px';
});

(function ringLoop() {
  rx += (mx - rx) * 0.1;
  ry += (my - ry) * 0.1;
  cRing.style.left = rx + 'px';
  cRing.style.top  = ry + 'px';
  requestAnimationFrame(ringLoop);
})();

// Seletores compartilhados entre as duas páginas
const interactiveSelectors = [
  'a', 'button',
  '.service-card', '.service-card-v2', '.featured-service', // cards de serviço
  '.stat-card', '.step-card', '.step-item',                  // cards home / services
  '.review-card', '.contact-item',                           // depoimentos e contato
  '.faq-question',                                           // FAQ
].join(',');

document.querySelectorAll(interactiveSelectors).forEach(el => {
  el.addEventListener('mouseenter', () => { cGal.classList.add('expand'); cRing.classList.add('expand'); });
  el.addEventListener('mouseleave', () => { cGal.classList.remove('expand'); cRing.classList.remove('expand'); });
});


/* ══════════════════════════════════════════════════════════════
   2. CANVAS DE ESTRELAS CINTILANTES
   — Cada estrela tem fase, frequência e opacidade próprias
   — Usa o timestamp do rAF: efeito completamente orgânico
══════════════════════════════════════════════════════════════ */
const canvas = document.getElementById('stars-canvas');
const ctx    = canvas.getContext('2d');
let stars    = [];

function resizeCanvas() {
  canvas.width  = window.innerWidth;
  canvas.height = window.innerHeight;
}

function makeStars() {
  stars = [];
  // ~1 estrela por 7 000 px² — ajuste a divisão para mais/menos estrelas
  const n = Math.min(500, Math.floor(canvas.width * canvas.height / 7000));
  for (let i = 0; i < n; i++) {
    stars.push({
      x:     Math.random() * canvas.width,
      y:     Math.random() * canvas.height,
      r:     Math.random() * 1.6 + 0.15,
      phase: Math.random() * Math.PI * 2,
      freq:  0.25 + Math.random() * 1.5,  // rad/s — grande variedade de velocidades
      lo:    0.04 + Math.random() * 0.1,   // opacidade mínima
      hi:    0.45 + Math.random() * 0.55,  // opacidade máxima
    });
  }
}

function drawStars(ts) {
  const t = ts * 0.003;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (const s of stars) {
    const norm = (Math.sin(s.phase + t * s.freq) + 1) * 0.5; // normaliza 0..1
    const a    = s.lo + (s.hi - s.lo) * norm;
    ctx.beginPath();
    ctx.arc(s.x, s.y, s.r, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(215,238,255,${a.toFixed(3)})`;
    ctx.fill();
  }
  requestAnimationFrame(drawStars);
}

resizeCanvas();
makeStars();
requestAnimationFrame(drawStars);
window.addEventListener('resize', () => { resizeCanvas(); makeStars(); });


/* ══════════════════════════════════════════════════════════════
   3. TICKER (home)
   — Gerado via JS para manter o HTML DRY
   — Duplicado para o loop CSS ser contínuo
══════════════════════════════════════════════════════════════ */
const tickerTrack = document.getElementById('tickerTrack');

if (tickerTrack) {
  const tickerItems = [
    'Sites Profissionais', 'Lojas Virtuais', 'Sistemas de Gestão',
    'Landing Pages', 'Portfólios Digitais', 'Automação de Processos',
    'Identidade Visual', 'SEO & Performance',
  ];

  // SVG de estrela separadora — alterna entre cyan e azul
  const starSVG = (color) =>
    `<span class="ticker-sep"><svg viewBox="0 0 14 14" fill="none">
      <path d="M7 0.5C7.4 4.5,7.5 6,7 7C6.5 6,6.6 4.5,7 0.5Z" fill="${color}"/>
      <path d="M7 13.5C6.6 9.5,6.5 8,7 7C7.5 8,7.4 9.5,7 13.5Z" fill="${color}"/>
      <path d="M0.5 7C4.5 7.4,6 7.5,7 7C6 6.5,4.5 6.6,0.5 7Z" fill="${color}"/>
      <path d="M13.5 7C9.5 6.6,8 6.5,7 7C8 7.5,9.5 7.4,13.5 7Z" fill="${color}"/>
    </svg></span>`;

  // Duplica os itens para scroll infinito
  const tickerHTML = [...tickerItems, ...tickerItems]
    .map((text, i) =>
      `<div class="ticker-item">${text}${starSVG(i % 2 === 0 ? '#00d4ff' : '#3b9eff')}</div>`
    ).join('');

  tickerTrack.innerHTML = tickerHTML;
}


/* ══════════════════════════════════════════════════════════════
   4. CARROSSEL DE DEPOIMENTOS (home)
   — Gerado via JS para manter o HTML DRY
   — Duplicado para o loop CSS ser contínuo
══════════════════════════════════════════════════════════════ */
const reviewsTrack = document.getElementById('reviewsTrack');

if (reviewsTrack) {
  const reviews = [
    {
      initials: 'MR', name: 'Marcos Rocha', role: 'Dono — Ótica Rocha & Filhos', badge: 'Loja Virtual',
      text: 'A Andromeda transformou minha loja física em um e-commerce completo em menos de 3 semanas. Hoje atendo clientes de todo o Brasil. Resultado surpreendente e profissionalismo total.',
    },
    {
      initials: 'PS', name: 'Dra. Patrícia Silva', role: 'Médica — Clínica Bem-Estar', badge: 'Site Profissional',
      text: 'Desenvolveram o site do meu consultório com agendamento online integrado. Meus pacientes adoraram a facilidade. Reduzi em 80% as ligações para marcação de consultas.',
    },
    {
      initials: 'CF', name: 'Carlos Ferreira', role: 'Sócio — Distribuidora FerTech', badge: 'Sistema de Gestão',
      text: 'O sistema de gestão que a Andromeda criou economiza horas de trabalho toda semana. Controle total de pedidos, estoque e clientes em um só lugar. Valeu cada centavo.',
    },
    {
      initials: 'AL', name: 'Amanda Lima', role: 'Diretora — Studio AL Moda', badge: 'Landing Page',
      text: 'Precisávamos de uma landing page de alta conversão. A Andromeda entregou em 5 dias um trabalho que superou todas as nossas expectativas. Taxa de conversão triplicou.',
    },
    {
      initials: 'JM', name: 'João Mendes', role: 'Fotógrafo Profissional', badge: 'Portfólio Digital',
      text: 'Meu portfólio fotográfico ficou incrível. A equipe entendeu exatamente o que eu queria e entregou uma identidade visual única. Recomendo de olhos fechados.',
    },
    {
      initials: 'RP', name: 'Ricardo Pinheiro', role: 'CEO — Construtora Pinheiro', badge: 'SEO & Performance',
      text: 'Site novo + SEO bem feito = dobrei as visitas orgânicas em 2 meses. A Andromeda não só criou o site, mas garantiu que ele apareça no Google. Isso faz toda a diferença.',
    },
  ];

  const reviewCard = (r) => `
    <div class="review-card">
      <div class="review-stars">★★★★★ <span>5.0</span></div>
      <span class="review-quote-mark">"</span>
      <p class="review-text">${r.text}</p>
      <div class="review-author">
        <div class="review-avatar">${r.initials}</div>
        <div>
          <div class="review-name">${r.name}</div>
          <div class="review-role">${r.role}</div>
        </div>
        <div class="review-service-badge">${r.badge}</div>
      </div>
    </div>`;

  // Duplica para scroll infinito
  reviewsTrack.innerHTML = [...reviews, ...reviews].map(reviewCard).join('');
}


/* ══════════════════════════════════════════════════════════════
   5. FADE-IN AO SCROLL
   — IntersectionObserver adiciona .visible quando o elemento
     entra na viewport (threshold: 10%)
══════════════════════════════════════════════════════════════ */
const fadeObs = new IntersectionObserver(entries => {
  entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); });
}, { threshold: 0.1 });

document.querySelectorAll('.fade-in').forEach(el => fadeObs.observe(el));


/* ══════════════════════════════════════════════════════════════
   6. FILTRO DE SERVIÇOS (services)
   — Clique em .filter-btn filtra cards por data-category
   — Oculta cards não correspondentes reduzindo opacidade
══════════════════════════════════════════════════════════════ */
document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    // Marca apenas o botão clicado como ativo
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');

    const filter = btn.dataset.filter;

    document.querySelectorAll('[data-category]').forEach(card => {
      const show = filter === 'all' || card.dataset.category === filter;
      card.style.opacity       = show ? '1' : '.25';
      card.style.pointerEvents = show ? '' : 'none';
      card.style.transition    = 'opacity .4s';
    });
  });
});


/* ══════════════════════════════════════════════════════════════
   7. FAQ ACCORDION (services)
   — Abre/fecha .faq-item com a classe .open
   — Fecha os demais ao abrir um novo
══════════════════════════════════════════════════════════════ */
document.querySelectorAll('.faq-item').forEach(item => {
  item.querySelector('.faq-question')?.addEventListener('click', () => {
    const isOpen = item.classList.contains('open');
    document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
    if (!isOpen) item.classList.add('open');
  });
});


/* ══════════════════════════════════════════════════════════════
   8. MODAL DE LOGIN
   — openModal / closeModal controlam a classe .active
   — Fecha ao clicar no overlay ou pressionar Escape
   — handleLogin valida email + senha (≥ 6 chars) com delay fake
══════════════════════════════════════════════════════════════ */
const loginModal = document.getElementById('loginModal');

function openModal() {
  loginModal.classList.add('active');
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  loginModal.classList.remove('active');
  document.body.style.overflow = '';
}

// Fecha ao clicar fora do modal-box
loginModal?.addEventListener('click', function (e) {
  if (e.target === this) closeModal();
});

// Fecha com Escape
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

// Garante que .modal-overlay.active sempre exibe o modal
// (sobrepõe qualquer CSS inline residual)
const modalStyle = document.createElement('style');
modalStyle.textContent = '.modal-overlay.active { opacity: 1 !important; visibility: visible !important; } .modal-overlay.active > div { transform: translateY(0) scale(1) !important; }';
document.head.appendChild(modalStyle);

function handleLogin(e) {
  e.preventDefault();
  const email = document.getElementById('loginEmail').value;
  const pass  = document.getElementById('loginPass').value;
  const errEl = document.getElementById('loginError');
  const btn   = e.target.querySelector('button[type=submit]');

  btn.textContent = 'Verificando...';
  btn.disabled    = true;

  setTimeout(() => {
    if (email && pass.length >= 6) {
      btn.textContent = 'Acesso Autorizado ✓';
      btn.style.background = 'linear-gradient(135deg, #0d5e3f, #1a9e6f)';
      errEl.style.display  = 'none';
      setTimeout(() => {
        closeModal();
        btn.textContent      = 'Acessar Painel ✦';
        btn.style.background = '';
        btn.disabled         = false;
      }, 1500);
    } else {
      errEl.style.display = 'block';
      btn.textContent     = 'Acessar Painel ✦';
      btn.disabled        = false;
    }
  }, 900);
}


/* ══════════════════════════════════════════════════════════════
   9. FORMULÁRIO DE CONTATO (home)
   — Feedback visual no botão ao submeter
   — Reseta o formulário após 3,5 s
══════════════════════════════════════════════════════════════ */
function handleSubmit(e) {
  e.preventDefault();
  const btn = e.target.querySelector('.btn-send');

  btn.textContent        = 'Mensagem Enviada ✓';
  btn.style.background   = 'linear-gradient(135deg, #0d5e3f, #1a9e6f)';
  btn.style.borderColor  = '#1a9e6f';

  setTimeout(() => {
    btn.textContent       = 'Enviar Mensagem ✦';
    btn.style.background  = '';
    btn.style.borderColor = '';
    e.target.reset();
  }, 3500);
}


/* ══════════════════════════════════════════════════════════════
   10. CONTADOR ANIMADO (home)
   — Usa IntersectionObserver: anima apenas quando visível
   — Lê o valor alvo pelo texto atual do elemento .stat-num
══════════════════════════════════════════════════════════════ */
function animateCounter(el, target, suffix) {
  let v = 0;
  const step = target / 60;
  const ti = setInterval(() => {
    v += step;
    if (v >= target) {
      el.textContent = target + suffix;
      clearInterval(ti);
    } else {
      el.textContent = Math.floor(v) + suffix;
    }
  }, 16);
}

const statObs = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    const card  = entry.target;
    const numEl = card.querySelector('.stat-num');
    if (!numEl || card.dataset.animated) return;

    card.dataset.animated = '1'; // evita re-animação

    const txt = numEl.textContent;
    if      (txt.includes('200')) animateCounter(numEl, 200, '+');
    else if (txt.includes('98'))  animateCounter(numEl,  98, '%');
    else if (txt.includes('4+'))  animateCounter(numEl,   4, '+');
  });
}, { threshold: 0.5 });

document.querySelectorAll('.stat-card').forEach(c => statObs.observe(c));

document.getElementById('contactForm').addEventListener('submit', function(e) {
  e.preventDefault(); 

  const form = e.target;
  const formData = new FormData(form);
  const toast = document.getElementById('toastNotification');

  // Envia os dados em segundo plano
  fetch('https://api.web3forms.com/submit', {
    method: 'POST',
    body: formData
  })
  .then(async (response) => {
    if (response.status === 200) {
      // Exibe a notificação
      toast.classList.add('show');
      form.reset(); 
      
      // Fecha automaticamente após 5 segundos
      setTimeout(() => {
        closeToast();
      }, 5000);
      
    } else {
      const json = await response.json();
      alert("Erro ao enviar: " + (json.message || "Tente novamente."));
    }
  })
  .catch(error => {
    console.error("Erro na requisição:", error);
    alert("Ocorreu um erro de conexão ao enviar o formulário.");
  });
});

// Função para fechar manualmente no "X"
function closeToast() {
  document.getElementById('toastNotification').classList.remove('show');
}

/* ══════════════════════════════════════════════════════════════
   11. CADASTRO DE CLIENTE
   — Máscaras de CPF, telefone e CEP
   — Busca automática de endereço via CEP (ViaCEP)
   — Mostrar/ocultar senha
══════════════════════════════════════════════════════════════ */

// — Máscara de CPF: 000.000.000-00 —
const cpfInput = document.getElementById('clienteCpf');
cpfInput?.addEventListener('input', e => {
  let v = e.target.value.replace(/\D/g, '').slice(0, 11);
  v = v.replace(/(\d{3})(\d)/, '$1.$2');
  v = v.replace(/(\d{3})(\d)/, '$1.$2');
  v = v.replace(/(\d{3})(\d{1,2})$/, '$1-$2');
  e.target.value = v;
});

// — Máscara de telefone: (00) 00000-0000 ou (00) 0000-0000 —
const telInput = document.getElementById('clienteTelefone');
telInput?.addEventListener('input', e => {
  let v = e.target.value.replace(/\D/g, '').slice(0, 11);
  if (v.length > 10) {
    v = v.replace(/(\d{2})(\d{5})(\d{0,4})/, '($1) $2-$3');
  } else if (v.length > 5) {
    v = v.replace(/(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3');
  } else if (v.length > 2) {
    v = v.replace(/(\d{2})(\d{0,5})/, '($1) $2');
  } else if (v.length > 0) {
    v = v.replace(/(\d{0,2})/, '($1');
  }
  e.target.value = v.replace(/-$/, '').replace(/\)\s$/, ')');
});

// — Máscara de CEP + busca automática de endereço (ViaCEP) —
const cepInput   = document.getElementById('clienteCep');
const cepStatus  = document.getElementById('cepStatus');
const enderecoInput = document.getElementById('clienteEndereco');
const bairroInput   = document.getElementById('clienteBairro');

cepInput?.addEventListener('input', e => {
  let v = e.target.value.replace(/\D/g, '').slice(0, 8);
  v = v.replace(/(\d{5})(\d{1,3})/, '$1-$2');
  e.target.value = v;

  cepStatus.classList.remove('show', 'error');

  const digits = v.replace(/\D/g, '');
  if (digits.length === 8) {
    cepStatus.textContent = 'Buscando...';
    cepStatus.classList.add('show');

    fetch(`https://viacep.com.br/ws/${digits}/json/`)
      .then(res => res.json())
      .then(data => {
        if (data.erro) {
          cepStatus.textContent = 'CEP não encontrado';
          cepStatus.classList.add('error');
          return;
        }
        if (enderecoInput) enderecoInput.value = data.logradouro || enderecoInput.value;
        if (bairroInput)   bairroInput.value   = data.bairro || bairroInput.value;
        cepStatus.textContent = 'Endereço encontrado ✓';
        setTimeout(() => cepStatus.classList.remove('show'), 2500);
      })
      .catch(() => {
        cepStatus.textContent = 'Erro ao buscar CEP';
        cepStatus.classList.add('error');
      });
  }
});

// — Mostrar / ocultar senha —
document.querySelectorAll('.password-toggle').forEach(btn => {
  btn.addEventListener('click', () => {
    const input = document.getElementById(btn.dataset.target);
    if (!input) return;
    const isHidden = input.type === 'password';
    input.type = isHidden ? 'text' : 'password';
    btn.textContent = isHidden ? '🙈' : '👁️';
  });
});
