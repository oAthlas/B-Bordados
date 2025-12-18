window.addEventListener("load", () => {
    const modal = document.querySelector(".modal-msg");

    // Se não existir modal, sai
    if (!modal) return;

    const closeBtns = modal.querySelectorAll(".close");

    // Fecha ao clicar no botão
    closeBtns.forEach(btn => {
        btn.addEventListener("click", () => {
            modal.style.display = "none";
        });
    });

    // Fecha automaticamente após X segundos
    setTimeout(() => {
        modal.style.display = "none";
    }, 1000); // X segundos
});