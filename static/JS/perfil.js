var looking = document.getElementById("Text-Lp")
var input_id = document.getElementById("user-id")
var template = document.getElementById('template-4-post');
var template_Nfriends = document.getElementById('Suggestions');
var post_Section= document.getElementById('Users_Posts');
var suggestion_Section = document.getElementById('New_Friends')
var new_post_text = document.querySelector('#Text_Post')
var templateCommunity = document.getElementById('template-4-communitys');
var into_communitys = document.getElementById('Communitys')
var popcard = document.getElementById("PopCard")
var pop_text = document.getElementById("msg")
var pop_btn = document.getElementById("pop_btn")
var pop_btn_2 = document.getElementById("pop_btn_2")
var pop_Area = document.getElementById("Pop_Text")
var pop_nText = document.getElementById("Pop_Text_Area")
var file_area_logo =       document.querySelector(".upload-container" )
var file_area_background = document.querySelector(".upload-container" )
var title_community = document.querySelector("#CommunityN_Title")
var btnreal = document.getElementById('community_logo_input')
var btnrealbg = document.getElementById('community_background_input')
var btnfake = document.getElementById('btnfake')
var btnfake_bg = document.getElementById('btnfake_bg')
var btntxt = document.getElementById('fakefile')
var btntxt_bg = document.getElementById('fakefile_background')
var imgPost_fake = document.querySelector('#btnfake_post')
var imgPost_Real = document.querySelector('#input-pic')
var Home_link = document.querySelector('#Home')


function mostrarPopCard(mensaje,type,text){

    if(type === "error"){
        pop_text.innerHTML = mensaje;
        popcard.style.display = "flex";
        pop_btn_2.style.display = "none"
        pop_Area.style.display = "none"
        file_area_background.style.display ="none"
        file_area_logo.style.display ="none"

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
        pop_Area.style.height="auto"
        pop_Area.style.gap="none"


    }else if(type === "Crear-Comunidad"){
        title_community.textContent = "Nombre de tu comunidad"
        pop_text.innerHTML = mensaje;
        pop_Area.style.width="max-content"
        popcard.style.display = "flex"
        pop_Area.style.flexDirection = "column"
        pop_Area.style.alignItems ="center"
        pop_Area.style.justifyContent ="center"
        pop_nText.placeholder = "Cuammunity!"
        pop_Area.style.gap="6%"
        pop_Area.style.height="40%"
        pop_btn.style.fontSize = "1.5em"
        pop_Area.style.display = "flex";
        file_area_logo.style.display ="flex"
        file_area_background.style.display ="flex"
        pop_btn.textContent = text;
        pop_btn_2.style.display = "none";
        pop_btn.style.backgroundColor = "orange"

        pop_btn.addEventListener('click',()=>{
            CreaComunidad()
        },{ once: true })

    }
}

function ClosePop(){
    popcard.style.display ="none"
}



looking.addEventListener('input',() =>{

    var query = looking.value
    
    search_community(query);
    

})




function Communitys_cards(community) {
    
    console.log(community)
    into_communitys.innerHTML=''
    community.forEach(community =>{
        const community_template = templateCommunity.content.cloneNode(true);
        community_template.querySelector('#Community_Name').textContent = community.nombre;
        community_template.querySelector('#linkCommunity').href = '/Cuammunity/'+community.id;
        if(community.usuarios == "1"){
            community_template.querySelector('#Community_Users').textContent = community.usuarios + ' Usuario';
        }else{
            community_template.querySelector('#Community_Users').textContent = community.usuarios + ' Usuarios';
        }
        community_template.querySelector('#Community_pic').src = `${community.logo}`;
     
        into_communitys.appendChild(community_template);
    });

    
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
    const img = document.querySelector("#input-pic");

    data_post.append("text", new_post_text.value);
    data_post.append("community", Cuammunity.getAttribute('community-id'));
    data_post.append('img',img.files[0]);

    console.log(img)

    const new_post = await fetch('/post',{
        method:'POST',
        body:data_post
    });

    const response = await new_post.json();

    if (response.status === "success"){
        mostrarPopCard(response.mensaje, response.status)
        Posts()

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



function Posts(posts_db,Whorequest) {
        
    
    if (posts_db.length >  0){
        post_Section.innerHTML= ''
        posts_db.forEach(datos => {
            const postTemplate = template.content.cloneNode(true);
            
            const uniqueId = "toggle-heart-" + datos.idPost;
            const checkbox = postTemplate.querySelector('#toggle-heart');
            const label = postTemplate.querySelector('label[for="toggle-heart"]');
            
            checkbox.id = uniqueId;
            label.setAttribute('for', uniqueId);
            
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


            var edit =  postTemplate.querySelector('#Edit') 
            var erase = postTemplate.querySelector('#Delete') 

            if(datos.id != Whorequest){
                edit.style.display = "none"
                erase.style.display = "none"
            }

            if(datos.likes > 0){
                postTemplate.querySelector('#amount-likes').textContent = "Me gusta: " + datos.likes
            }else{
                postTemplate.querySelector('#amount-likes').style.display = "none";

            }
            console.log(datos.like)

            if(datos.like){
                checkbox.checked = true
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

async function CreaComunidad() {
    const imgCommunity = document.querySelector("#community_logo_input")
    const imgCommunityBG = document.querySelector("#community_background_input")
    const Name = document.querySelector("#Pop_Text_Area")

    const request = new FormData();

    console.log(Name.value,imgCommunityBG.files[0],imgCommunity.files[0])
    request.append('Logo',imgCommunity.files[0])
    request.append('BackGround',imgCommunityBG.files[0])
    request.append("Name",Name.value)

    const create = await fetch('/NewCuammunity',{
        method:'POST',
        body: request
    })
    

    const newcom = await create.json()

    if(newcom.status === "success"){
        mostrarPopCard("Comunidad Creada!","success")
        const pop_btn = document.getElementById("pop_btn")
        pop_btn.addEventListener("click",()=>{

            pop_btn.href = '/Cuammunity/'+newcom.id

         },{ once: true })
        

    }else if(newcom.status === "error"){
        mostrarPopCard("Ocurrio un error","error")
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
            options.innerHTML = '<div class="Cuammunity-option">No hay Comunidades a las que este unido</div>';
        }
}

async function RequestData() {
    
    console.log(input_id.value)
    const requestFeed = await fetch('/profileData', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'},
            body: JSON.stringify({"id":input_id.value})
            
            
        })

    const dataFeed = await requestFeed.json()
    console.log(dataFeed)

    if(dataFeed.status == "success"){
        Communitys_cards(dataFeed.CommunityCards)
        Posts(dataFeed.Posts,dataFeed.WhoRequest)
        Home_link.href  = '/feed/'+dataFeed.WhoRequest
    }


}



function CommunityForm(){
    console.log("Prueba")
    mostrarPopCard("Ingresa los datos para crear tu comunidad!", "Crear-Comunidad","Crear!")
}


 function Amount_CF(res){
    const friends_u   = document.querySelector('#Amount_Friends')
    const community_u = document.querySelector('#Amount_Community')

    
        friends_u.textContent = res.friends;
        community_u.textContent = res.community;
}

function Suggestions(sugg_db) {
    sugg_db.forEach(datos => {
        const userTemplate = template_Nfriends.content.cloneNode(true);
        const url = userTemplate.querySelector('#Suggestion-User').href='/Profile/'+datos.id
        console.log(url)
        userTemplate.querySelector('#Suggest_Name').textContent =  datos.usuario;
        const imgUser = userTemplate.querySelector('#suggestion_Img');
        imgUser.src = `${datos.imgPerfil}`;
        
        suggestion_Section.appendChild(userTemplate);
    });

}


document.addEventListener('DOMContentLoaded',() =>{

    RequestData()

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



btnfake.addEventListener("click", function() {
  btnreal.click();
});

btnreal.addEventListener("change", function() {
  if (btnreal.value) {
    btntxt.innerHTML = btnreal.value.match(/[\/\\]([\w\d\s\.\-\(\)]+)$/)[1];
  } else {
    btntxt.innerHTML = "No file chosen, yet.";
  }
});

btnfake_bg.addEventListener("click", function() {
  btnrealbg.click();
});

btnrealbg.addEventListener("change", function() {
  if (btnrealbg.value) {
    btntxt_bg.innerHTML = btnrealbg.value.match(/[\/\\]([\w\d\s\.\-\(\)]+)$/)[1];
  } else {
    btntxt_bg.innerHTML = "No file chosen, yet.";
  }
});

imgPost_fake.addEventListener("click", function() {
  imgPost_Real.click();
});

imgPost_Real.addEventListener("change", function() {
  if (imgPost_Real.value) {
    imgPost_fake.innerHTML = " <i class='fas fa-cloud-upload-alt'></i> Foto Seleccionada";
  } else {
    imgPost_fake.innerHTML = " <i class='fas fa-cloud-upload-alt'></i> Seleccionar Foto";
  }
});



document.addEventListener('change', (e) => {
    if (e.target.id && e.target.id.startsWith('toggle-heart')) {
        const isLiked = e.target.checked;
        const postPrincipal = e.target.closest('.glass-card'); 
        const idPost = postPrincipal.querySelector('#Id_post').value;
        const ammount = postPrincipal.querySelector('#amount-likes');
        LikeUpdate(isLiked,idPost,ammount)
    }
});



async function LikeUpdate(isLiked,idPost,amount) {
    if(isLiked){
        const like = await fetch('/Like',{
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({
            'id': idPost,
            'status': isLiked
        })
        })

        const update = await like.json()
        if(update.status === "add"){
            amount.style.display = "flex"
            amount.textContent = "Me gusta: "+ update.amount;
        }

    }else{
        const unlike = await fetch('/Like',{
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body: JSON.stringify({
                'id': idPost,
                'status': isLiked
            })
        })

        
        const update = await unlike.json()
        if(update.status === "delete"){
            if(update.amount == "0"){
                amount.textContent = "";
                amount.style.display="none";
            }
        }

    }
    
}

 


