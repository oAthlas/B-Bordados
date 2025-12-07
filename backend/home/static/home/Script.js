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
    modal.style.display = "flex";
}

closeBtn.onclick = () => {
    modal.style.display = "none";
}

window.onclick = (e) => {
    if (e.target === modal) modal.style.display = "none";
}
