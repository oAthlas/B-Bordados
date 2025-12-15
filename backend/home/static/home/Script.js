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