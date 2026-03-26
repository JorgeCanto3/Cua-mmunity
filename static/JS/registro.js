
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
const emailSec = document.getElementById("email-input-holder");
var validEmail = true;
const progressBar = document.getElementById("progress_bar");
const progresstext = document.getElementById("security_text");
const securityFrame = document.getElementById("security_Section");



console.log(passwordSec);

emailSec.addEventListener('input', () => {
    
    const mail= emailSec.value;
    let cua = 'cua.uam.mx';
    validEmail = mail.includes(cua);

    emailSec.style.borderColor = validEmail ? "#219644" : "#a71606";


});

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
    let btn = true;
    const hue = percent * 1.2; 
    progressBar.style.backgroundColor = `hsl(${hue-30}, 100%, 40%)`;
   
  if (percent === 0) {
        text = "";
        securityFrame.style.display = "none";
    } else if (percent <= 30 ) {
        text = "Debil";
        btn = true;
        
    } else if (percent <= 60) {
        text = "Aceptable";
        btn = false;
    } else if (percent <= 90) {
        text = "Fuerte";
        btn = false;

    } else {
        text = "Muy Fuerte";
        btn = false;

    }



    btncheck =  btn || !validEmail ? true: false;
    button.disabled = btncheck;
    progresstext.innerHTML = text;
    progresstext.style.borderRadius =`${25}px`; 
    progresstext.style.color = `hsl(${hue-30}, 100%, 30%)`;

}

const popcard = document.getElementById("PopCard")
const PopCard_Content = document.getElementById("PopCard_Content")
const pop_text = document.getElementById("msg")
const pop_btn = document.getElementById("pop_btn")
const code_form = document.getElementById("code")
const code_btn = document.getElementById("code_btn")





function mostrarPopCard(mensaje,type){

    if(type === "error"){
        pop_text.innerHTML = mensaje;
        popcard.style.display = "flex";
        code_form.style.display = "none"
        pop_btn.style.backgroundColor = "red";

    }else if(type === "success"){
        pop_text.innerHTML = mensaje;
        popcard.style.display = "flex";
        pop_btn.style.display ="flex"
        code_form.style.display = "none"
        pop_btn.style.backgroundColor = "lightgreen";
    }else if(type === "code"){
        pop_text.innerHTML = mensaje;
        pop_btn.style.display ="none"
        PopCard_Content.style.width ="100%"
        PopCard_Content.style.height ="100%"
        PopCard_Content.style.gap ="10%"
        pop_btn.style.width= "20%";
        pop_btn.style.height= "30%";
        popcard.style.display = "flex";
        code_form.style.display = "flex"
        code_btn.style.backgroundColor = "lightgreen";

    }
}

function ClosePop(){
    popcard.style.display ="none"
}
const name_user         =  document.getElementById("user-input-holder")
const first_lastname    =  document.getElementById("first_lastname-input-holder")
const second_lastname   =  document.getElementById("second_lastname-input-holder")
const email             =  document.getElementById("email-input-holder")
const user_name         =  document.getElementById("user_name-input-holder")
const carrer            =  document.getElementById("carreer-input-holder")
const birth             =  document.getElementById("birth-input-holder")
const profile_p         =  document.getElementById("profile_p-input-holder")
const pswd              =  document.getElementById("pswd-input-holder")


async function Registro() {
    if (button.disabled || !validEmail) {
        console.log("Intento de envío bloqueado");
        return; 
    }

    const formData = new FormData();
    formData.append("correo", email.value);
    formData.append("contraseña", pswd.value);
    formData.append("nombre", name_user.value);
    formData.append("usuario_nombre", user_name.value);
    formData.append("first_lastname", first_lastname.value);
    formData.append("second_lastname", second_lastname.value);
    formData.append("carrer", carrer.value);
    formData.append("birth", birth.value);

    formData.append('Profile_pic', profile_p.files[0]);
    
        const respuesta = await fetch('/registrar', {
            method: 'POST',
            body: formData
        });

        const flask_res = await respuesta.json();

        if (flask_res.status === "success") { 
            document.getElementById("Form-R").reset();
            document.getElementById("Form-R").style.display = "none";
            document.querySelector('#Id_new_user').value = flask_res.id
            mostrarPopCard("Ingresa el Codigo recibido","code");
        
        
        } else {
            mostrarPopCard("Ocurrió un error: " + flask_res.details, "error");
        }


}

async function ConfirmaCorreo() 
{
    digs = [];
    id = document.querySelector('#Id_new_user')
    dig = document.querySelectorAll('.code_input')
    
    dig.forEach(e => {
        console.log(e.value)
        digs.push(e.value);
    });

   const query = await fetch('/confirm',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({"code_inputs":digs,"id": id.value})
    })

    const answer = await query.json()

    if(answer.status === "success"){
        document.getElementById("PopBotton").href = '/'
        mostrarPopCard("Confirmación Exitosa, puedes pasar", "success");
    }else{
        mostrarPopCard("Intentalo de Nuevo", "code");

    }

console.log(datos);
}


const inputsCodigo = document.querySelectorAll('.code_input');

inputsCodigo.forEach((input, index) => {
    
    input.addEventListener('input', () => {
        if (input.value.length === 1 && index < inputsCodigo.length - 1) {
            inputsCodigo[index + 1].focus();
        }
    });

    input.addEventListener('keydown', (e) => {
        if (e.key === "Backspace" && input.value === "" && index > 0) {
            inputsCodigo[index - 1].focus();
        }
    });
});