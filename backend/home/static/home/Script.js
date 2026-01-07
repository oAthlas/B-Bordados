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


function openProfileModal() {
    document.getElementById('profileModal').classList.add('active');
}

function closeProfileModal() {
    document.getElementById('profileModal').classList.remove('active');
}

function selectAvatar(img) {

    // remove seleção anterior
    document.querySelectorAll('.profile-suggestions img')
        .forEach(el => el.classList.remove('active'));

    // marca o atual
    img.classList.add('active');

    // joga no preview
    document.getElementById('profilePreview').src = img.src;
}
