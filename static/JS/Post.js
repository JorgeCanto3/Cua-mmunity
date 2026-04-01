
var looking = document.getElementById("Text-Lp")
var input_id = document.getElementById("id_user")
var templatePost = document.getElementById('template-4-post');
var post_Section= document.getElementById('Users_Posts');
var new_post_text = document.querySelector('#Text_Post')
var popcard = document.getElementById("PopCard")
var pop_text = document.getElementById("msg")
var pop_btn = document.getElementById("pop_btn")
var pop_btn_2 = document.getElementById("pop_btn_2")
var pop_Area = document.getElementById("Pop_Text")
var pop_nText = document.getElementById("Pop_Text_Area")
var containers = document.querySelectorAll(".upload-container");
var file_area_logo =       containers[0]
var file_area_background = containers[1]
var post_id =  document.querySelector("#id_4_data")
var current_user_id =  document.querySelector("#id_current_user")

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
        pop_btn_2.style.backgroundColor = "red";
        pop_btn_2.textContent ="No";
        pop_btn_2.onclick =ClosePop;
        pop_btn.style.display = "flex"
        pop_btn_2.style.display = "flex"
        pop_btn.style.backgroundColor = "lightgreen";
        pop_btn.textContent ="Si";
        pop_btn.style.borderRadius = "50px";
        pop_btn.style.borderRadius = "50px";
        pop_btn.style.width = "6%";
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

        //Community Creation hidden
        file_area_logo.style.display ="none"
        file_area_background.style.display ="none"




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

async function comentar(whatPost){
    const sectionComentarios = whatPost.closest('#Comment_Section');
    
    const Post =  sectionComentarios.previousElementSibling;
    const id_post = Post.querySelector('#Id_post')
    const comment = sectionComentarios.querySelector('#comment_holder')

    if (comment.value.trim() !== ""){

        const send_comment = await fetch('/comentar',{
            method: 'POST',
            headers: {'Content-Type':'application/json'},
            body:JSON.stringify({
                'id_post':id_post.value,
                'text': comment.value
            })

        })


        const res = await send_comment.json()

        if (res.status === "success"){
            mostrarPopCard("Comentario Agregado","success")
            
        }else{
            mostrarPopCard("Ocurrio un error intentalo más tarde","error")

        }
        
    } else{
        return  mostrarPopCard("No puedes mandar cadenas vacias >:(","error")
    }


}


looking.addEventListener('input',() =>{

    var query = looking.value
    
    search_community(query);
    

})




async function notificaciones(){

}



function CloseSuggest(who){
    const user = who.closest('#Suggest')
    user.remove()
}


function EditContent(btn){
    console.log(btn)
    const post_card = btn.closest('#Post');

    const id_post = post_card.querySelector("#Id_post")
    const old_text = post_card.querySelector("#Content-Text")
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
            Posts(ans.update)

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



function Post(dato,dato2) {
    const datos = dato[0]
    const comentarios = dato2
    console.log(comentarios)
        
    post_Section.innerHTML= ''
    const postTemplate = templatePost.content.cloneNode(true);
    var template = postTemplate.getElementById('TemplateComments');
    var comments_Section = postTemplate.getElementById('Comments')
    
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
    console.log(imgUser)
    const imgPost = postTemplate.querySelector('#Post_Img_Content');
    if(datos.imgPost) {
            imgPost.src = `${datos.imgPost}`;
            
        } else {
            imgPost.remove(); 
        }
    
        var edit =  postTemplate.querySelector('#Edit') 
        var erase = postTemplate.querySelector('#Delete') 
    
        if(datos.userID != current_user_id.value){
            edit.style.display = "none"
            erase.style.display = "none"
        }

        if(datos.likes > 0){
            postTemplate.querySelector('#amount-likes').textContent = "Me gusta: " + datos.likes
        }else{
            postTemplate.querySelector('#amount-likes').style.display = "none";
        }
        
        if(datos.like){
            checkbox.checked = true
        }

        post_Section.appendChild(postTemplate);
        
        comentarios.forEach(comentario => {
            const commentTemplate = template.content.cloneNode(true);
            
            commentTemplate.querySelector('#userName_comment').textContent = comentario.name
            commentTemplate.querySelector('#logo_comment').src = comentario.user_pic
            commentTemplate.querySelector('#comment_of_user').textContent = comentario.comentario
    
            comments_Section.appendChild(commentTemplate)
    
        })
}




async function RequestData() {
    const requestFeed = await fetch('/PostData', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                "id":post_id.value
            })
        })

    const dataFeed = await requestFeed.json()
    console.log(dataFeed)

    if(dataFeed.status == "success"){
        Post(dataFeed.posts,dataFeed.comments);
    }

}




document.addEventListener('DOMContentLoaded',() =>{
    console.log(current_user_id)
    console.log(post_id)
    RequestData()

})





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

 


