var looking = document.getElementById("Text-Lp")
var input_id = document.getElementById("id_user")
var template = document.getElementById('template-4-post');
var post_Section= document.getElementById('Users_Posts');
var new_post_text = document.querySelector('#Text_Post')
var templateCommunity = document.getElementById('template-4-communitys');
var into_communitys = document.getElementById('Communitys')



looking.addEventListener('input',() =>{

    var query = looking.value
    
    search_community(query);
    

})




async function Communitys_cards() {

    const data = await fetch('/Communitys')

    const data_community = await data.json()

    
    console.log(data_community)
    if(data_community.status === "success"){
        into_communitys.innerHTML=''
        data_community.comunidad.forEach(community =>{
            const community_template = templateCommunity.content.cloneNode(true);
            community_template.querySelector('#Community_Name').textContent = community.nombre;
            if(community.usuarios == "1"){
                community_template.querySelector('#Community_Users').textContent = community.usuarios + ' Usuario';
            }else{
                community_template.querySelector('#Community_Users').textContent = community.usuarios + ' Usuarios';
            }
            community_template.querySelector('#Community_pic').src = `${community.logo}`;
         

            into_communitys.appendChild(community_template);
        });




    }

    
}

async function notificaciones(){

}

async function usuarios_agregar(){
    
}

function EditContent(){
    const id_post = document.querySelector("#Id_post")
    const old_text = document.querySelector("#Content-Text")
    mostrarPopCard("Ingresa el nuevo texto!","edit",old_text.textContent)

    const confirm = document.querySelector("#pop_btn")
    
    confirm.addEventListener("click",()=>{
        const new_text = document.getElementById("Pop_Text_Area").value
        console.log(new_text)
        
        Edit(id_post, new_text)

    },{ once: true })

    

}

async function Edit(id_post,new_text){

    console.log(id_post,new_text)

    const query = await fetch('/edit',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({
           'id' : id_post.value ,
            "text":new_text
        })
    })

    const ans = await query.json()

    if (ans.status === "success"){
        mostrarPopCard("Se actualizo la publicación con Exito!","success")
        const confirm = document.querySelector("#pop_btn")
        confirm.addEventListener("click",()=>{
        
        ClosePop()
        Posts()
        },{ once: true })

    }else{
        mostrarPopCard("No se pudo actualizar la publicación, intentalo más tarde","error")
    }
}


function Preventive (){
    
    const id_post = document.querySelector("#Id_post")
    mostrarPopCard("Estas seguro de eliminar la publicación?","options",)
    
    const confirm = document.querySelector("#pop_btn_2")


    confirm.addEventListener("click",()=>{
        ClosePop();
        erase(id_post.value);
    },{ once: true })
}

async function erase(id_post){



    const query = await fetch('/delete',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({
           'id' : id_post }
        )
    })

    const ans = await query.json()

    if (ans.status === "success"){
        mostrarPopCard("Se elimino la publicación con Exito!","success")
        Posts()
    }else{
        mostrarPopCard("No se pudo eliminar la publicación, intentalo más tarde","error")
    }
}


async function Add_Post() {
    const data_post = new FormData();
    const Cuammunity = document.querySelector('#Cuammunity-btn');
    const img = null;

    data_post.append("text", new_post_text.value);
    data_post.append("community", Cuammunity.getAttribute('community-id'));
    data_post.append("img",img);

    const new_post = await fetch('/post',{
        method:'POST',
        body:data_post
    });

    const response = await new_post.json();

    if (response.status === "success"){
        mostrarPopCard(response.mensaje, response.status)
    }else{
        mostrarPopCard(response.mensaje, response.status)
    }


    
}

async function Search_community(lp) {
    
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



async function Posts() {
        
    const res = await  fetch('/posts')


    const res_db = await res.json()

    if (res_db.status === "success"){
        
        post_Section.innerHTML= ''
        res_db.post.forEach(datos => {
            const postTemplate = template.content.cloneNode(true);
            
            postTemplate.querySelector('#Post_Name').textContent = datos.usuario;
            postTemplate.querySelector('#Id_post').value = datos.idPost;
            postTemplate.querySelector('#Content-Text').textContent = datos.texto;
            postTemplate.querySelector('#Community_Name').textContent = datos.comunidad
            const imgUser = postTemplate.querySelector('#Post_Img_User');
            imgUser.src = `${datos.imgPerfil}`;
            
            const imgPost = postTemplate.querySelector('#Post_Img_Content');
            if(datos.imgPost) {
                imgPost.src = `${datos.imgPost}`;
            } else {
                imgPost.remove(); 
            }

            post_Section.appendChild(postTemplate);
        });
        

    }
    else{
  
        post_Section.innerHTML = '<h2>Todavia no hay posts</h2>'
        post_Section.style.alignContent = "center";
        post_Section.style.alignItems = "center";
        post_Section.style.justifyContent = "center";
        post_Section.style.justifyItems = "center";


        
    }

    
}

function UpdateCuammunity(cuammunity, id, logo_url){

    const Cuammunity_text = document.querySelector('#Cuammunity-btn');
    const Cuammunity_logo = document.querySelector('#Community_Img');
    const menu = document.querySelector('#Cuammunity-menu');

    Cuammunity_text.textContent = cuammunity;
    Cuammunity_text.setAttribute('community-id',id);
    menu.classList.remove('show');

    if(logo_url){
        Cuammunity_logo.src =`${logo_url}`;
    }
    else{
        Cuammunity_logo.src =`/static/img/Logo-Cuammunity.avif`;

    }
}



async function Cuammunitys(options){
    try {
        const respuesta = await  fetch('/cuammunity_tpost',{
            method:'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                "id" : input_id.value,

            })
        })

        const flask_res = await respuesta.json();
        options.innerHTML = ' ';
        if (flask_res.status === "success") { 
            console.log(flask_res.comunidades)
            flask_res.comunidades.forEach(comunidad => {
                    const option = document.createElement('div');
                    option.className = 'Cuammunity-option';
                    option.setAttribute('community-id',comunidad.id);
                    option.textContent = comunidad.nombre;
                
                option.addEventListener('click',(e)=>{
                    e.preventDefault()
                    UpdateCuammunity(comunidad.nombre,comunidad.id,comunidad.logo);

                })
                
                
                    options.appendChild(option);
                });    
        }}catch (error) {
            optionsElement.innerHTML = '<div class="Cuammunity-option">No hay Comunidades a las que este unido</div>';
        }
}

const popcard = document.getElementById("PopCard")
const pop_text = document.getElementById("msg")
const pop_btn = document.getElementById("pop_btn")
const pop_btn_2 = document.getElementById("pop_btn_2")
const pop_Area = document.getElementById("Pop_Text")
const pop_nText = document.getElementById("Pop_Text_Area")





function mostrarPopCard(mensaje,type,text){

    if(type === "error"){
        pop_text.innerHTML = mensaje;
        popcard.style.display = "flex";
        pop_btn_2.style.display = "none"
        pop_Area.style.display = "none"

        pop_btn.textContent = "Entendido"
        pop_btn.style.backgroundColor = "red";

    }else if (type ==="success" ){
        pop_text.innerHTML = mensaje;
        popcard.style.display = "flex";
        pop_btn_2.style.display = "none"
        pop_Area.style.display = "none"

        pop_btn.textContent = "Entendido"
        pop_btn.style.backgroundColor = "lightgreen";
    }else if( type === "options"){
        console.log("entre")
        pop_text.innerHTML = mensaje;
        popcard.style.display = "flex";
        pop_btn.style.backgroundColor = "red";
        pop_btn.textContent ="No";
        pop_btn.onclick =ClosePop;
        pop_btn_2.style.display = "flex"
        pop_btn_2.style.backgroundColor = "lightgreen";
        pop_btn_2.textContent ="Si";
        pop_btn.style.borderRadius = "50px";
        pop_btn_2.style.borderRadius = "50px";
        pop_btn_2.style.width = "6%";
        pop_Area.style.display = "none"




    }else if(type ==="edit"){
        pop_text.innerHTML = mensaje;
        pop_Area.style.display = "flex"
        pop_nText.placeholder = text
        popcard.style.display = "flex";
        pop_btn.textContent = "Aceptar"
        pop_btn_2.textContent = "Cancelar"
        pop_btn_2.style.display ="flex"
        pop_btn_2.onclick = ClosePop;
        pop_btn_2.style.backgroundColor = "red";
        pop_btn.style.backgroundColor = "lightgreen";
    }
}

function ClosePop(){
    popcard.style.display ="none"
}






document.addEventListener('DOMContentLoaded',() =>{

    Posts()

    Communitys_cards()

    const dropdown = document.querySelector('#Community-options');

    if(dropdown){
        const dropdown_btn = dropdown.querySelector('#Cuammunity-btn')
        const menu = dropdown.querySelector('#Cuammunity-menu');
    

        dropdown_btn.addEventListener('click',(e)=>{
            e.stopPropagation(); 
            const options = dropdown.querySelector('#Cuammunity-menu');
           if(options.classList.contains('show')){
                options.classList.remove('show')
            }else{
                options.classList.add('show')
            }

            if(options.children.length === 0){
                Cuammunitys(options)
            }

        })

    }

    document.addEventListener('click', (e) => {
        const menu = document.querySelector('#Cuammunity-menu');
        const dropdown = document.querySelector('#Community-options');

        if(menu && dropdown && !dropdown.contains(e.target)){
            menu.classList.remove('show');
        }
    });

   



})

