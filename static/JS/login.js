
          
const popcard = document.getElementById("PopCard")
const pop_text = document.getElementById("msg")
const pop_btn = document.getElementById("pop_btn")

const mail = document.getElementById("user-input-holder")
const password = document.getElementById("pswd-input-holder")




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

async function log_in(){

    const respuesta = await  fetch('/',{
        method:'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            "Correo" : mail.value,
            "pswd": password.value

        })
    })

    const flask_res = await respuesta.json();
    if (flask_res.status === "success") { 
        document.getElementById("Form-R").reset();
        mostrarPopCard("Bienvenido", "success");


        document.getElementById("PopBotton").href = `/feed/${flask_res.details}`;
    
    } else {
        mostrarPopCard("Ocurrió un error: " + flask_res.details, "error");
    }
}


