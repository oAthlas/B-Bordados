const modal = document.querySelector(".modal-msg");
const closeBtn = document.querySelector(".close");

if (modal && closeBtn) {
    closeBtn.addEventListener("click", () => {
        modal.style.display = "none";
    });
}
setTimeout(() => {
    if (modal) modal.style.display = "none";
}, 4000);
