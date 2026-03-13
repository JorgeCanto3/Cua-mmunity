
          
const popcard = document.getElementById("PopCard")
const pop_text = document.getElementById("msg")
const pop_btn = document.getElementById("pop_btn")


function mostrarPopCard(mensaje,type){

    if(type === "Error"){
        pop_text.innerHTML = mensaje;
        popcard.style.display = "flex";
        pop_btn.style.backgroundColor = "red";

    }else{
        pop_text.innerHTML = mensaje;
        popcard.style.display = "flex";
        pop_btn.style.backgroundColor = "lightgreen";
    }
}

function ClosePop(){
    popcard.style.display ="none"
}