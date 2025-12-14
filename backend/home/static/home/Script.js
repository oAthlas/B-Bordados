let count = 1;
document.getElementById("radio1").checked = true;

setInterval( function(){
        nextImage();
}, 10000)


function nextImage(){
  count++;
   if(count>4){
      count = 1;
    }

    document.getElementById("radio"+count).checked = true;
}


const modal = document.getElementById("modal");
const openBtn = document.getElementById("openmodal");
const closeBtn = document.getElementById("closeModal");

    if (!openBtn || !modal || !closeBtn) return;

        openBtn.addEventListener("click", () => {
        modal.classList.add("ativo");
        });

    closeBtn.addEventListener("click", () => {
        modal.classList.remove("ativo");
        });
