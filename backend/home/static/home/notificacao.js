document.addEventListener("DOMContentLoaded", function () {

    var modal = document.querySelector(".modal-msg");
    if (!modal) {
        return;
    }

    var box = modal.querySelector(".modal-box");
    if (!box) {
        return;
    }

    // força repaint antes de animar
    setTimeout(function () {
        box.className += " show";
    }, 10);

    var TEMPO_FECHAR = 3000;

    setTimeout(function () {

        box.className = box.className.replace(" show", "") + " hide";

        setTimeout(function () {
            if (modal.parentNode) {
                modal.parentNode.removeChild(modal);
            }
        }, 400);

    }, TEMPO_FECHAR);

});
