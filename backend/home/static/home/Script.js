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
document.querySelectorAll(".remove").forEach(btn => {
  btn.addEventListener("click", (e) => {
    e.preventDefault();

    const itemId = btn.dataset.id;

    fetch(`/remove-from-cart/${itemId}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken"),
      },
    })
    .then(() => {
      // Recarrega só o conteúdo do carrinho
      atualizarCarrinho(); // depois posso te mostrar sem reload
    });
  });
});

function atualizarCarrinho() {
  fetch("/cart/partial/")
    .then(res => res.text())
    .then(html => {
      document.querySelector(".ccompras").innerHTML = html;
    });
}


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
