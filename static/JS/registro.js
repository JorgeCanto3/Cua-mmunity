
var button = document.getElementById("Sign_Up");
function passwordCheck() {
    var pass = document.getElementById("pswd-input-holder").value;
    var passCheck = document.getElementById("pswd-input-holder-verification").value;
    var mensaje = document.getElementById("match");



    if (pass === "" || passCheck === "") {
        mensaje.innerHTML = "";
        mensaje.style.display = "none"; 
        button.disabled = true;
        return;
    }

    if (pass === passCheck) {   
        mensaje.style.display = "flex"; 
        mensaje.innerHTML = "Coinciden";
        mensaje.style.textAlign="center"
        mensaje.style.borderRadius = `${25}px`;
        mensaje.style.color = "#219644"; 
        mensaje.style.width = `${100}%`;
        mensaje.style.paddingLeft = `${1}%`;
        button.disabled = false;
    } else {
        mensaje.style.display = "flex" ;
        mensaje.innerHTML = "No coinciden";
        mensaje.style.textAlign="center"
        mensaje.style.borderRadius = `${25}px`;
        mensaje.style.color = "#a71606"; 
        button.disabled = true;

    }
}

const passwordSec = document.getElementById("pswd-input-holder");
const progressBar = document.getElementById("progress_bar");
const progresstext = document.getElementById("security_text");
const securityFrame = document.getElementById("security_Section");

console.log(passwordSec);

passwordSec.addEventListener('input', () => {
    securityFrame.style.display = "flex";
    
    const pass = passwordSec.value;
    let score = 0;

    if (!pass) {
        updateBar(0);
        return;
    }

    
    score += Math.min(pass.length * 4, 40); 

     
    if (/[A-Z]/.test(pass)) score += 15; 
    if (/[a-z]/.test(pass)) score += 15; 
    if (/[0-9]/.test(pass)) score += 15; 
    if (/[^A-Za-z0-9]/.test(pass)) score += 15;

    updateBar(score);
});

function updateBar(percent) {
    progressBar.style.width = `${percent}%`;
    let text ="";
    let btn = false;
    const hue = percent * 1.2; 
    progressBar.style.backgroundColor = `hsl(${hue-30}, 100%, 40%)`;
   
  if (percent === 0) {
        text = "";
        securityFrame.style.display = "none";
    } else if (percent <= 30) {
        text = "Debil";
        btn = false;
    } else if (percent <= 60) {
        text = "Aceptable";
        btn = true;
    } else if (percent <= 90) {
        text = "Fuerte";
        btn = true;

    } else {
        text = "Muy Fuerte";
        btn = true;

    }

    button.disabled = btn;
    progresstext.innerHTML = text;
    progresstext.style.borderRadius =`${25}px`; 
    progresstext.style.color = `hsl(${hue-30}, 100%, 30%)`;

}

const popcard = document.getElementById("PopCard")
const pop_text = document.getElementById("msg")
const pop_btn = document.getElementById("pop_btn")


function mostrarPopCard(mensaje,type){

    if(type === "error"){
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