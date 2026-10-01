// Função para abrir/fechar o menu ao clicar
function toggleDropdown(event) {
  event.stopPropagation();
  const menu = document.getElementById('perfilDropdown');
  const trigger = event.currentTarget;
  
  if (menu && trigger) {
    menu.classList.toggle('show');
    trigger.classList.toggle('active');
  }
}

// Fecha o menu automaticamente se o usuário clicar em qualquer outro lugar da tela
document.addEventListener('click', function(event) {
  const menu = document.getElementById('perfilDropdown');
  const trigger = document.querySelector('.dropdown-trigger');
  
  if (menu && menu.classList.contains('show') && !event.target.closest('.user-dropdown')) {
    menu.classList.remove('show');
    trigger.classList.remove('active');
  }
});









document.addEventListener("DOMContentLoaded", () => {
    const card = document.querySelector(".left-info-card");
    const conteudo = document.querySelector(".left-info-card section");
    const logoFundo = document.querySelector(".layer-logo");
    const estrelaGif = document.querySelector(".layer-star");

    // Executa apenas se estiver no PC (telas maiores que 1024px)
    if (window.innerWidth > 1024 && card) {
        
        card.addEventListener("mousemove", (e) => {
            const rect = card.getBoundingClientRect();
            
            // Calcula a posição do mouse de -0.5 a 0.5 em relação ao centro do card
            const x = (e.clientX - rect.left) / rect.width - 0.5;
            const y = (e.clientY - rect.top) / rect.height - 0.5;

            // 1. Inclina o card de vidro principal
            card.style.transform = `perspective(1000px) rotateX(${-y * 15}deg) rotateY(${x * 15}deg)`;

            // 2. Move o Texto levemente para frente
            if(conteudo) conteudo.style.transform = `translateZ(40px) translateX(${x * -15}px) translateY(${y * -15}px)`;

            // 3. Afunda a Logo de fundo (Movimento invertido e profundidade negativa)
            // Mantemos o translate(-50%, -50%) para ela não sair do centro!
            if(logoFundo) logoFundo.style.transform = `translate(-50%, -50%) translateZ(-50px) translateX(${x * 30}px) translateY(${y * 30}px)`;

            // 4. Faz a Estrela pular MUITO para frente (Efeito de sair da tela)
            if(estrelaGif) estrelaGif.style.transform = `translateZ(120px) translateX(${x * -60}px) translateY(${y * -40}px)`;
        });

        // Reseta tudo quando o mouse sai
        card.addEventListener("mouseleave", () => {
            card.style.transform = "perspective(1000px) rotateX(0deg) rotateY(0deg)";
            if(conteudo) conteudo.style.transform = "translateZ(0px) translateX(0px) translateY(0px)";
            if(logoFundo) logoFundo.style.transform = "translate(-50%, -50%) translateZ(0px) translateX(0px) translateY(0px)";
            if(estrelaGif) estrelaGif.style.transform = "translateZ(0px) translateX(0px) translateY(0px)";
        });
    }
});





document.addEventListener('DOMContentLoaded', () => {
    // Pega todos os cards que vão ter o efeito 3D
    const cards = document.querySelectorAll('.left-info-card');
    
    cards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            // Calcula a rotação com base na posição do mouse
            const rotateX = ((y - centerY) / centerY) * -15; // Força do efeito vertical
            const rotateY = ((x - centerX) / centerX) * 15;  // Força do efeito horizontal
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
        });
        
        // Zera a rotação quando o mouse sai do card
        card.addEventListener('mouseleave', () => {
            card.style.transform = `perspective(1000px) rotateX(0deg) rotateY(0deg)`;}
)})})

/* ================= SUBMIT LOCK (UNIVERSAL) ================= */

document.addEventListener("DOMContentLoaded", () => {
    // Universal: pega TODOS os forms da página
    document.querySelectorAll("form").forEach(form => {
        form.addEventListener("submit", event => {
            if (form.dataset.locked === "true") {
                event.preventDefault();
                return;
            }
            form.dataset.locked = "true";
            // Pega o botão de submit OU qualquer botão clicado dentro do form
            const button =
                form.querySelector("[data-submit-button]") ||
                form.querySelector("button[type='submit']") ||
                form.querySelector("button:not([type='button'])");
            if (!button) return;
            // Aplica o estado de loading (só animação, sem texto)
            button.classList.add("is-locked");
            button.disabled = true;
            button.setAttribute("aria-disabled", "true");
            button.setAttribute("aria-busy", "true");
        });
    });
});


/* ================= MOSTRAR SENHA ================= */
document.addEventListener("DOMContentLoaded",()=>{
    const toggle=document.getElementById("passwordToggle");
    const input=document.getElementById("loginSenha");
    if(!toggle||!input)return;
    toggle.addEventListener("click",()=>{
        const visible=input.type==="text";
        input.type=visible?"password":"text";
        toggle.textContent=visible?"☀️":"🌑";
        toggle.setAttribute(
            "aria-label",
            visible?"Mostrar senha":"Ocultar senha"
        );
    });
});

/* ================= SERVIÇO: EXPANDIR DETALHE ================= */
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".servico-toggle").forEach(btn => {
        btn.addEventListener("click", () => {
            const container = btn.closest(".servico-card, .servico-destaque");
            const target = document.getElementById(btn.dataset.target);
            if (!target || !container) return;

            const isOpen = container.classList.contains("is-expanded");

            document.querySelectorAll(".servico-card.is-expanded, .servico-destaque.is-expanded").forEach(el => {
                if (el !== container) {
                    el.classList.remove("is-expanded");
                    const t = el.querySelector(".servico-detalhe");
                    if (t) t.classList.remove("is-open");
                    const b = el.querySelector(".servico-toggle");
                    if (b) {
                        const hasDestaque = el.classList.contains("servico-destaque");
                        b.textContent = hasDestaque ? "SAIBA MAIS ✦" : "SAIBA MAIS →";
                    }
                }
            });

            container.classList.toggle("is-expanded", !isOpen);
            target.classList.toggle("is-open", !isOpen);

            const hasDestaque = container.classList.contains("servico-destaque");
            btn.textContent = isOpen
                ? (hasDestaque ? "SAIBA MAIS ✦" : "SAIBA MAIS →")
                : "FECHAR ✕";
        });
    });
});










document.addEventListener('DOMContentLoaded', () => {
    const track = document.getElementById('servicesTrack');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const dots = document.querySelectorAll('.carousel-dot');
    const mainContainer = document.querySelector('.services-carousel-container');
    
    // FUNÇÃO QUE FECHA QUALQUER CARD ABERTO
    const closeAllExpandedCards = () => {
        document.querySelectorAll('.servico-detalhe.is-open').forEach(el => el.classList.remove('is-open'));
        document.querySelectorAll('.servico-card-inner.card-expanded').forEach(el => el.classList.remove('card-expanded'));
        document.querySelectorAll('.servico-toggle').forEach(btn => btn.textContent = 'SAIBA MAIS ✦');
        if (mainContainer) mainContainer.classList.remove('carousel-expanded');
    };

    if (track && prevBtn && nextBtn) {
        const cards = Array.from(track.children);
        let currentIndex = 0;

        const updateCarousel = () => {
            const cardWidth = track.clientWidth;
            track.style.transform = `translateX(-${currentIndex * cardWidth}px)`;
            
            // Atualiza as bolotas ativas
            dots.forEach((dot, index) => {
                if (index === currentIndex) {
                    dot.classList.add('active');
                } else {
                    dot.classList.remove('active');
                }
            });
        };

        // Avançar
        nextBtn.addEventListener('click', () => {
            closeAllExpandedCards(); // <--- CORREÇÃO DO BUG: Fecha aba ao mudar de lado
            if (currentIndex >= cards.length - 1) {
                currentIndex = 0; 
            } else {
                currentIndex++;
            }
            updateCarousel();
        });

        // Voltar
        prevBtn.addEventListener('click', () => {
            closeAllExpandedCards(); // <--- CORREÇÃO DO BUG: Fecha aba ao mudar de lado
            if (currentIndex <= 0) {
                currentIndex = cards.length - 1; 
            } else {
                currentIndex--;
            }
            updateCarousel();
        });

        // Clicar nas bolotas para trocar
        dots.forEach((dot, index) => {
            dot.addEventListener('click', () => {
                closeAllExpandedCards(); // <--- CORREÇÃO DO BUG
                currentIndex = index;
                updateCarousel();
            });
        });

        window.addEventListener('resize', updateCarousel);
    }

    // Abertura do "Saiba Mais" interno e Expansão
    const toggles = document.querySelectorAll('.servico-toggle');
    toggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const targetEl = document.getElementById(targetId);
            const cardInner = this.closest('.servico-card-inner');

            if (targetEl.classList.contains('is-open')) {
                // Se já tá aberto, fecha
                targetEl.classList.remove('is-open');
                this.textContent = 'SAIBA MAIS ✦';
                if(cardInner) cardInner.classList.remove('card-expanded');
                if (mainContainer) mainContainer.classList.remove('carousel-expanded');
            } else {
                // Se está fechado, garante que tudo tá fechado e abre o clicado
                closeAllExpandedCards(); 
                
                targetEl.classList.add('is-open');
                this.textContent = 'FECHAR ✕';
                if(cardInner) cardInner.classList.add('card-expanded');
                if (mainContainer) mainContainer.classList.add('carousel-expanded');
            }
        });
    });

    // Geração randômica de estrelas cadentes em toda a largura da tela
    const starsContainer = document.getElementById('shootingStars');
    if (starsContainer) {
        const starCount = 12; 
        for (let i = 0; i < starCount; i++) {
            const star = document.createElement('span');
            star.classList.add('shooting-star');
            
            const starTip = document.createElement('span');
            starTip.classList.add('star-tip');
            starTip.textContent = '✦';
            star.appendChild(starTip);
            
            star.style.left = Math.random() * 100 + '%';
            
            const duration = Math.random() * 3 + 2.5;
            star.style.animationDuration = duration + 's';
            
            const delay = Math.random() * 6;
            star.style.animationDelay = delay + 's';
            
            starsContainer.appendChild(star);
        }
    }
});








// Geração randômica de estrelas cadentes com ponta brilhante
const starsContainer = document.getElementById('shootingStars');
if (starsContainer) {
    const starCount = 8; // Podes ajustar a quantidade de estrelas se achares necessário
    for (let i = 0; i < starCount; i++) {
        const star = document.createElement('span');
        star.classList.add('shooting-star');
        
        // Cria a ponta de estrela na frente
        const starTip = document.createElement('span');
        starTip.classList.add('star-tip');
        starTip.textContent = '✦';
        star.appendChild(starTip);
        
        // Posição horizontal em toda a largura da tela (0% a 100%)
        star.style.left = Math.random() * 120 + '%';
        
        // Velocidade/Duração aleatória (entre 2.5s e 5.5s)
        const duration = Math.random() * 3 + 2.5;
        star.style.animationDuration = duration + 's';
        
        // Atraso de queda aleatório
        const delay = Math.random() * 6;
        star.style.animationDelay = delay + 's';
        
        starsContainer.appendChild(star);
    }
}








// Abertura do "Saiba Mais" interno com Expansão do Card
    const toggles = document.querySelectorAll('.servico-toggle');
    toggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const targetEl = document.getElementById(targetId);
            
            // Pega o container do card e da logo para aplicar o efeito de expansão
            const cardInner = this.closest('.servico-card-inner');

            if (targetEl.classList.contains('is-open')) {
                targetEl.classList.remove('is-open');
                this.textContent = 'SAIBA MAIS ✦';
                // Remove a classe de expansão
                if(cardInner) cardInner.classList.remove('card-expanded');
            } else {
                targetEl.classList.add('is-open');
                this.textContent = 'FECHAR ✕';
                // Adiciona a classe de expansão
                if(cardInner) cardInner.classList.add('card-expanded');
            }
        });
    });