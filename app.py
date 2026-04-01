from flask import Flask, render_template,request,redirect,url_for,flash, jsonify
from flask_login import UserMixin,login_user,current_user,login_required,logout_user,LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail,Message
from werkzeug.utils import secure_filename
import os
from datetime import datetime as dt
import model as m
import random as rand

now =dt.now()
app = Flask(__name__)

app.secret_key = 'coloca_contra'

# pa encriptar la contraseña
bcrypt = Bcrypt(app) 

# pa manejar el log
login_manager = LoginManager()
login_manager.init_app(app)

#pa enviar correos


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'jorge.l.santiago@cua.uam.mx'
app.config['MAIL_PASSWORD'] = 'mzku crbg sjgb iuzu'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = ('Cua-Verificator','jorge.l.santiago@cua.uam.mx')

mail = Mail(app)


# Direcciones de las carpetas para almacenar las imagenes
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

COMUMUNITY_UPLOAD = os.path.join(BASE_DIR, 'static', 'Upload','Communitys')
POST_UPLOAD = os.path.join(BASE_DIR, 'static', 'Upload','Post') 
USER_UPLOAD = os.path.join(BASE_DIR, 'static', 'Upload','Profile')
ALLOWED_FILES = {'jpg','png','jpeg'}


app.config['UPLOAD_FOLDER_html'] = '/static/Upload/Profile/'
app.config['UPLOAD_FOLDER_html_Post'] = '/static/Upload/Post/'
app.config['UPLOAD_FOLDER_html_Community'] = '/static/Upload/Communitys/'
app.config['UPLOAD_FOLDER_PY'] = USER_UPLOAD
app.config['UPLOAD_FOLDER_PY_POST'] = POST_UPLOAD
app.config['UPLOAD_FOLDER_PY_COMMUNITY'] = COMUMUNITY_UPLOAD



@login_manager.user_loader
def load_user(user_id):
    data = m.Usuario(user_id)
    
    if data is not None :
        usuario = m.User(id = data[0],email=data[1])
        return usuario
    return None 

  
        
def allow_file(file):
        return '.' in file and \
           file.rsplit('.', 1)[1].lower() in ALLOWED_FILES

def profile_accept(file):
    if file and allow_file(file.filename):
        filename= secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER_PY'],filename))
        return app.config['UPLOAD_FOLDER_html']+filename
    else:
        return '/static/Upload/Img_Borrador.avif'
    
def post_accept(file):
    if file and allow_file(file.filename):
        filename= secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER_PY_POST'],filename))
        return app.config['UPLOAD_FOLDER_html_Post']+filename
    else:
        return 0

def Community_accept(file):
    if file and allow_file(file.filename):
        filename= secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER_PY_COMMUNITY'],filename))
        return app.config['UPLOAD_FOLDER_html_Community']+filename
    else:
        return 0
    
@app.route('/', methods=["GET","POST"])
def index():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('Correo')
        psswrd = data.get('pswd')
        
        user_conf = Log(email,psswrd)
        
        if  type(user_conf) == int:
            return jsonify({"status":"success","details":user_conf})
        else:
            return user_conf     
        
        
      
        
    return render_template('iniciar-sesion.html')

def Log (email,psswrd):
    user_data = m.Log_in(email)
    if( user_data == None):
        return jsonify({"status": "error", "details":"El correo no existe, registrate! "})
    
   
    
    hash_db =user_data[7]
    email_verif = user_data[11]
    ver_contraseña = bcrypt.check_password_hash(hash_db,psswrd)
    
    if  (ver_contraseña and email_verif) is True:
        login_user(m.User(user_data[0],user_data[1]))
        print(f'El id del usuario es {user_data[0]}')
        return user_data[0]
    elif(not ver_contraseña):
        return jsonify({"status":"error","details":"Contraseña erronea"})
    else:
        return jsonify({"status":"error","details":"El correo no ha sido verificado"})
        

@app.route('/registro', methods=["GET"])
def registro():    
    return render_template('registro.html')

@app.route('/registrar', methods=["POST"])
def registrar():
    name        = request.form.get('nombre')
    user_name   = request.form.get('usuario_nombre')
    f_last_name = request.form.get('first_lastname')
    s_last_name = request.form.get('second_lastname')
    birth       = request.form.get('birth')
    email       = request.form.get('correo')
    psswrd      = request.form.get('contraseña')
    career      = request.form.get('carrer')
    profile_pic = request.files.get('Profile_pic')
    profile_bg = request.files.get('Profile_bg')
    


    code = "".join([str(rand.randint(0, 9)) for _ in range(6)])

    

    hashed_password = bcrypt.generate_password_hash (psswrd).decode('utf-8')
    path_pic = profile_accept(profile_pic)
    path_bg  = profile_accept(profile_bg)

    print(f'{name},{f_last_name},{s_last_name},{birth},{email},{hashed_password},{career},{user_name},{path_pic},{path_bg},{code}')    
    insert_db = m.Sign_up(name,f_last_name,s_last_name,birth,email,hashed_password,career,user_name,path_pic,path_bg,code)   
    id_sign = insert_db
    if (type(insert_db) == int):    
        verify_mail(email,code)
        return jsonify({"status":"success","id":id_sign})
    else: 
        print(f'Se envia el error:{insert_db}')
        return jsonify({"status":"error", "details": insert_db})


@app.route('/feed/<int:id>')
@login_required
def main(id):
    if(current_user.id!=id):
        
        flash("Error no puedes cambiar de usuario","Error")
        return redirect(url_for('index'))
    else:
        
        data_user = m.Usuario(id)
         
    return render_template('index.html',profile_data = data_user)
    
@app.route('/Cuammunity/<int:id_com>')
@login_required
def community(id_com):
    community_data = m.Community(id_com)
    data_user = m.Usuario(current_user.id)
    return render_template('community.html',community_data =community_data,profile_data = data_user)

@app.route('/comentar', methods=["GET", "POST"])
def comentar():
    user = current_user.id
    data = request.get_json()
    user_post = data.get('id_post')
    text =data.get('text')
    
    img = None
    
    comentario = m.add_comment(user,user_post,text, img)
    
    if (type(comentario) == int):
        return jsonify({"status":"success"})
    else:
        return jsonify({"status":"fail"})

@app.route('/post', methods=["POST","GET"])
@login_required
def post():
    user = current_user.id

    new_post_txt =      request.form.get('text')   
    post_community =    request.form.get('community')  
    post_img =          request.files.get('img')  
    if(post_img is not None ):
        post_url = post_accept(post_img)
        
        if(type(post_url) != int):
        
            posted = m.create_post(user,new_post_txt,post_community,post_url)
        

            if posted:
                data = post_4_user()
                return jsonify({"status":"success", "mensaje":"Post Creado 🦐🦐","data":data})
            else:
                return jsonify({"status":"fail", "mensaje":"No se pudo crear el post 😭😭"})
        else:
            return jsonify({"status":"error","details":"Formato de Imagen no aceptado"})
    else:
        posted = m.create_post(user,new_post_txt,post_community,None)
        if posted:
            data = post_4_user()
            return jsonify({"status":"success", "mensaje":"Post Creado 🦐🦐","data":data})
        else:
            return jsonify({"status":"fail", "mensaje":"No se pudo crear el post 😭😭"})
        

@login_manager.unauthorized_handler
def unauthorized():
    flash("No puedes acceder","error")
    return  redirect(url_for('index'))


@app.route('/search_cuammunity',methods=["GET"])
def search_cuammunity():
    data = request.get_json()
    text_query = data.get('search')
    query = m.community_search(text_query) 
    
    cuammunitys = []
    
    for cua in query:
        cuammunitys.append({"id":cua[0],"cuammunity":cua[1]})
    
    return cuammunitys

@app.route('/cuammunity_tpost',methods=["POST"])
@login_required
def cuamminitys_to_post():
    data = request.get_json()
    id_4_post = data.get('id')
    query = m.user_into_communitys(id_4_post) 

    cuammunitys = []
    
    for cua in query:
        cuammunitys.append({"id":cua[0],"nombre":cua[1],"logo":cua[3]})
    
    
    return jsonify({"status":"success","comunidades":cuammunitys})

@login_required
def post_4_user():
    
    query = m.posts(current_user.id)
    if(query != 0):
        posts = []
        for c in query:
            like_user = m.DoUserlikes(current_user.id,c[4])
            posts.append({"id":c[0],"usuario":c[1],"imgPerfil":c[2],"comunidad":c[3],"idPost":c[4],"fecha":[5],"titulo":c[6],"texto":c[7],"likes":c[8],"imgPost":c[9],"like":like_user})
        return posts
    else:
        return None
    


@login_required
def post_of(user):
    
    query = m.posts_of(user)
    if(query != 0):
        posts = []
        for c in query:
            like_user = m.DoUserlikes(current_user.id,c[4])
            posts.append({"id":c[0],"usuario":c[1],"imgPerfil":c[2],"comunidad":c[3],"idPost":c[4],"fecha":c[5],"titulo":c[6],"texto":c[7],"likes":c[8],"imgPost":c[9],"like":like_user})
        return posts
    else:
        return None



@login_required
def Community_card():
    id_4_post =current_user.id
    query = m.user_into_communitys(id_4_post) 

    cuammunity = []
    
    for cua in query:
        cuammunity.append({"id":cua[0],"nombre":cua[1],"usuarios":cua[2],"logo":cua[3]})
    
    
    return cuammunity

@login_required
def Community_card_user(user_id):
    
    query = m.user_into_communitys(user_id) 

    cuammunity = []
    
    for cua in query:
        cuammunity.append({"id":cua[0],"nombre":cua[1],"usuarios":cua[2],"logo":cua[3]})
    
    
    return cuammunity


@app.route('/delete', methods=["POST"])
@login_required
def Delete_post():
    data = request.get_json()
    id_post = data.get('id')
    
    query = m.erase_post(id_post) 
    if query:
        data = post_4_user()
        return jsonify({"status":"success","details": data})
    else:
        print(query)
        return jsonify({"status":"error", "details": query})


@app.route('/edit', methods=["POST"])
@login_required
def Update_post():
    data = request.get_json()
    id_post = data.get('id')
    text = data.get('text')
    
    
    query = m.edit_post(id_post,text) 
    if query:
        data = post_4_user()
        return jsonify({"status":"success","update": data})
    else:
        print(query)
        return jsonify({"status":"error", "details": query})


def verify_mail(email,code):
    subject = "Verifica tu Correo!"
    
    try:
        msg = Message(
            subject = subject,
            recipients = [email],
            body = "Tu codigo de verificación es: " + code
        )
        
        mail.send(msg)  
        
        return 
        
    except Exception as e:
        print(e)
        return None

@app.route('/confirm',methods=['POST'])
def confirm():
    data= request.get_json()
    list_code = data.get('code_inputs',[])
    input_code = "".join(list_code)
    id_to_verify =data.get('id')
    
    
    data_user = m.Usuario(id_to_verify)
    
    ver_code = data_user[12]
    
    if(input_code == ver_code):
        m.update_confirm(id_to_verify)
        return jsonify({"status":"success"})
    else:
        return jsonify({"status":"error", "details":"The code doesn't match"})
        
@app.route('/Like', methods=['POST'])
@login_required
def like():
    data = request.get_json()
    id_post = data.get('id')
    status = data.get('status')
    
    if(status):
        likes = m.UpdateLikes(status,id_post,current_user.id)
        if(type(likes) == int):
            return jsonify({"status":"add","amount":likes} )
        else:
            return jsonify({"status":"error","details":likes} )

    else:
        likes = m.UpdateLikes(status,id_post,current_user.id)
        if(type(likes) == int):
            return jsonify({"status":"delete","amount":likes} )
        else:
            str(likes)
            return jsonify({"status":"error","details":likes} )

@app.route('/NewCuammunity', methods=['POST'])
@login_required
def NewCuammunity():
    newLogo=request.files.get('Logo')
    newBG=request.files.get('BackGround')
    newName=request.form.get('Name')
    
    print(f'The data colected is {newLogo},{newBG},{newName}')
    imgCommunty_URL =Community_accept(newLogo)
    imgBGCommunty_URL =Community_accept(newBG)
    
    print(f'The url for the imgs gotten are {imgBGCommunty_URL},{imgCommunty_URL}')
    if((imgCommunty_URL and imgBGCommunty_URL) != int):
    
        cuammunity = m.CreateCuammunity(newName,imgCommunty_URL,imgBGCommunty_URL)
        if(type(cuammunity) == int):
            m.join_a_cuammunity(current_user.id,cuammunity,'Admin')
            return jsonify({"status":"success","id": cuammunity})
        else:
            return jsonify({"status":"error","details": cuammunity})
    else:
            return jsonify({"status":"error","details": "El formato de las imagenes no es valido, intenta nuevamente"})
        
@login_required
def amount_into():
    communitys = m.amount_communitys(current_user.id)
    friends = m.amount_friends(current_user.id)
    
    print(communitys,friends)
    
    ammount = []
    ammount.append({"friends":friends,"communitys":communitys})

    return ammount

@login_required
def amount_into_profile(user):
    communitys = m.amount_communitys(user)
    friends = m.amount_friends(user)
    
    print(communitys,friends)
    
    ammount = []
    ammount.append({"friends":friends,"communitys":communitys})

    return ammount


@app.route('/Profile/<int:id_p>', methods=['POST','GET'])
@login_required
def profile_user(id_p):
    data_user = m.Usuario(id_p)
    return render_template('perfil.html',profile_data = data_user)


def friends_suggestions():
    data,pending = m.not_friends(current_user.id)
    newfriends =[]
    for f in data:
        if len(pending) > 0:
            if f[11] is True and f[0] not in pending[0]:
                newfriends.append({"id":f[0],"usuario":f[8],"imgPerfil":f[9]})
        else:
            if f[11] is True :
                newfriends.append({"id":f[0],"usuario":f[8],"imgPerfil":f[9]})
    return newfriends

def notificaciones_4_user():
    notifications = m.notificaciones(current_user.id)
    
    if isinstance(notifications, tuple):
        notifications = [notifications]
    
    if(notifications is not None):
        data = []
        for n in notifications: 
            data.append({'name':n[0],'idNotification':n[1]})
        return data
    else:
        return None

@app.route('/mainData',methods=['GET'])
@login_required
def main_data():
    try:
        
        amount_user = amount_into()
        suggestions = friends_suggestions()
        communitys_user = Community_card()
        posts = post_4_user()
        notificaciones = notificaciones_4_user()
        print(notificaciones)
        
        return jsonify({"status":"success", "ammount":amount_user,"suggestions":suggestions,"CommunityCards":communitys_user,"Posts": posts,"Notifications":notificaciones })
    except Exception as e:
        err = str(e)
        print(err)
        return jsonify({"status":"error","details":err})


 
@app.route('/profileData',methods=['GET','POST'])
@login_required
def profile_data():
    try:
        data = request.get_json()
        id_profile = data.get('id')
        amount_user = amount_into_profile(id_profile)
        suggestions = friends_suggestions()
        communitys_user = Community_card_user(id_profile)
        posts = post_of(id_profile)
        return jsonify({"status":"success", "ammount":amount_user,"suggestions":suggestions,"CommunityCards":communitys_user,"Posts": posts,"WhoRequest":current_user.id})
    except Exception as e:
        err = str(e)
        print(err)
        return jsonify({"status":"error","details":err})


@app.route('/FriendRequest',methods=['GET','POST'])
@login_required
def FriendRequest():
    datos = request.get_json()
    requested = datos.get('id_to')
    who_request = current_user.id
    
    try:
        m.addFRequest(requested,who_request)
        return jsonify({"status":"success"})
    except Exception as e:
        err = str(e)
        print(err)
        return jsonify({"status":"error","details":err })

@app.route('/Post/<int:id_p>', methods=['GET','POST'])
@login_required
def PostCompleto(id_p):
    data_user = m.Usuario(current_user.id)
    return render_template('Post.html', profile_data = data_user, post_id = id_p)


@app.route('/PostData', methods=['POST'])
@login_required
def PostData():
    data = request.get_json()
    post_id =data.get('id')
    print(post_id)
    comment_raw = m.comentarios(post_id)
    
    post_raw = m.post(post_id)
    
    post_data = []
    like_user = m.DoUserlikes(current_user.id,post_raw[0])
    post_data.append({"idPost":post_raw[0],"idCuammunity":post_raw[1],"texto":post_raw[2],"likes":post_raw[3],"imgPost":post_raw[4],"usuario":post_raw[5],"imgPerfil":post_raw[6],"comunidad":post_raw[7],"userID":post_raw[8],"like":like_user})
    comments =[]
    print(post_data)
    
    
    for c in comment_raw:
        comments.append({"id_user":c[0],"name":c[1],"user_pic":c[2],"comentario":c[3]})
    
    print(comments)
    return jsonify({"status": "success", "posts":post_data,"comments":comments})



@app.route('/acceptFriend', methods =[ 'POST','GET'])
@login_required
def acceptrequest():
    data = request.get_json()
    id_not = data.get('id')
    
    try:
        m.acceptrq(id_not)
        return jsonify({"status":"success"})
    except Exception as e:
        err = str(e)
        print (err)
        return err
    
@app.route('/rejectFriend', methods =[ 'POST','GET'])
@login_required
def declinerequest():
    data = request.get_json()
    id_not = data.get('id')
    
    try:
        m.rejectrq(id_not)
        return jsonify({"status":"success"})
    except Exception as e:
        err = str(e)
        print (err)
        return err

if __name__ == '__main__':
    app.run(debug=True,port=8000)

