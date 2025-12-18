document.addEventListener('DOMContentLoaded', () => {
    const modal = document.querySelector('.modal-msg');
    if (!modal) return;

    const closeBtns = modal.querySelectorAll('.close');
    closeBtns.forEach(btn => {
        btn.addEventListener('click', () => modal.style.display = 'none');
    });

    // Fecha automaticamente após X milissegundos
    const TEMPO_FECHAR = 1200;
    setTimeout(() => modal.style.display = 'none', TEMPO_FECHAR);
});
