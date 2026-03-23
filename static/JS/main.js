var looking = document.getElementById("Text-Lp")

looking.addEventListener('input',() =>{

    var query = looking.value
    
    search_community(query);
    

})



async function cuammunitys(){

    const respuesta = await  fetch('/cuammunity_tpost',{
        method:'GET',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            "id" : mail.value,

        })
    })

    const flask_res = await respuesta.json();
    console.log(flask_res.details);
    if (flask_res.status === "success") { 
        flask_res.forEach(comunidad => {
                const option = document.createElement('option');
                option.value = comunidad.id;
                option.textContent = comunidad.nombre;
                selectComunidades.appendChild(option);
            });    
    } else {
        
        mostrarPopCard("Ocurrió un error: " + flask_res.mensaje, "error");
    }
}

async function posts(params) {
        
    const res = await  fetch('/posts',{
        method:'POST',
        headers:{'Content-Type': 'application/json'},
        body: JSON.stringify({
            'search': looking.value
        })

    })


    const res_db = await res.json()

    if (res_db.status == 'success')
        res_db.forEach(comunidad => {
                const option = document.createElement('option');
                option.value = comunidad.id;
                option.textContent = comunidad.nombre;
                selectComunidades.appendChild(option);
            });

    
}

async function community_data(params) {
    
}

async function notificaciones(){

}

async function usuarios_agregar(){

}

async function search_community(lp) {
    
    const res = await  fetch('/search_cuammunity',{
        method:'POST',
        headers:{'Content-Type': 'application/json'},
        body: JSON.stringify({
            'search': looking.value
        })

    })


    const res_db = await res.json()

    if (res_db.status == 'success')
        res_db.forEach(comunidad => {
                const option = document.createElement('option');
                option.value = comunidad.id;
                option.textContent = comunidad.nombre;
                selectComunidades.appendChild(option);
            });

}


