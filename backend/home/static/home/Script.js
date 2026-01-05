// ===== SLIDER =====
let count = 1;
const radio1 = document.getElementById("radio1");

if (radio1) {
    radio1.checked = true;

    setInterval(() => {
        nextImage();
    }, 10000);
}

function nextImage() {
    count++;
    if (count > 4) {
        count = 1;
    }

    const radio = document.getElementById("radio" + count);
    if (radio) {
        radio.checked = true;
    }
}

// ===== MODAL =====
const modal = document.getElementById("modal");
const openBtn = document.getElementById("openmodal");
const closeBtn = document.getElementById("closeModal");

if (modal && openBtn && closeBtn) {
    openBtn.onclick = () => {
        modal.classList.add("ativo");
    };

    closeBtn.onclick = () => {
        modal.classList.remove("ativo");
    };

    modal.onclick = (e) => {
        if (e.target === modal) {
            modal.classList.remove("ativo");
        }
    };
}

document.getElementById('open_btn').addEventListener('click', function () {
    document.getElementById('sidebar').classList.toggle('open-sidebar');
});

