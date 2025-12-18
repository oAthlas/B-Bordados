document.addEventListener("DOMContentLoaded", () => {
    const modal = document.querySelector(".modal-msg");

    // Se não existir mensagem, não faz nada
    if (!modal) return;

    const closeBtns = modal.querySelectorAll('.close');

    // Anexa handler a todos os botões de fechar
    closeBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            modal.style.display = 'none';
        });
    });

    // Fecha automaticamente após X milissegundos
    const TEMPO_FECHAR = 2000; // segundos

    setTimeout(() => {
        modal.style.display = 'none';
    }, TEMPO_FECHAR);
});
