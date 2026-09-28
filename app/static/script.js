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