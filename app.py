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


    code = "".join([str(rand.randint(0, 9)) for _ in range(6)])

    

    hashed_password = bcrypt.generate_password_hash (psswrd).decode('utf-8')
    path_pic=profile_accept(profile_pic)
    insert_db = m.Sign_up(name,f_last_name,s_last_name,birth,email,hashed_password,career,user_name,path_pic,code)   
    id_sign = insert_db
    if (type(insert_db) == int):    
        verify_mail(email,code)
        return jsonify({"status":"success","id":id_sign})
    else: 
        print(f'Se envia el erro:{insert_db}')
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
    user_post = request.form['user_post']

    text = request.form['comment']
    
    comentario = m.add_comment(user,user_post,text)
    
    if comentario:
        return jsonify({"status":"success"})
    else:
        return jsonify({"status":"fail"})

@app.route('/post', methods=["POST","GET"])
@login_required
def post():
    user = current_user.id

    print(f'El usuario{current_user.id} va a postiar')
    new_post_txt =      request.form.get('text')   
    post_community =    request.form.get('community')  
    post_img =          request.files.get('img')  
    print(f'Verficando imagen: {post_img}')
    post_url = post_accept(post_img)
    
    print(f'La imagen es: {post_url}')
    
    if(type(post_url) != int):
    
        posted = m.create_post(user,new_post_txt,post_community,post_url)
    

        if posted:
                return jsonify({"status":"success", "mensaje":"Post Creado 🦐🦐"})
        else:
            return jsonify({"status":"fail", "mensaje":"No se pudo crear el post 😭😭"})
    else:
        return jsonify({"status":"error","details":"Formato de Imagen no aceptado"})

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

@app.route('/posts',methods = ["GET"])
@login_required
def post_4_user():
    
    query = m.posts(current_user.id)
    if(query != 0):
        posts = []
        for c in query:
            like_user = m.DoUserlikes(current_user.id,c[4])
            posts.append({"id":c[0],"usuario":c[1],"imgPerfil":c[2],"comunidad":c[3],"idPost":c[4],"fecha":[5],"titulo":c[6],"texto":c[7],"likes":c[8],"imgPost":c[9],"like":like_user})
        return jsonify({"status":"success" ,"post":posts})
    else:
        return jsonify({"status":"error"})

@app.route('/Communitys')
@login_required
def Community_card():
    id_4_post =current_user.id
    query = m.user_into_communitys(id_4_post) 

    cuammunity = []
    
    for cua in query:
        cuammunity.append({"id":cua[0],"nombre":cua[1],"usuarios":cua[2],"logo":cua[3]})
    
    
    return jsonify({"status":"success","comunidad":cuammunity})

@app.route('/delete', methods=["POST"])
@login_required
def Delete_post():
    data = request.get_json()
    id_post = data.get('id')
    
    query = m.erase_post(id_post) 
    if query:
        return jsonify({"status":"success"})
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
        return jsonify({"status":"success"})
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
        
@app.route('/amount_user', methods=['POST','GET'])
@login_required
def amount_into():
    communitys = m.amount_communitys(current_user.id)
    friends = m.amount_friends(current_user.id)
    
    print(communitys,friends)
    
    return jsonify({"status":"success","friends":friends,"community":communitys})

@app.route('/profile/<int:id_p>', methods=['POST','GET'])
@login_required
def profile_user(id_p):
    data_user = m.Usuario(current_user.id)
    return render_template('perfil.html',profile_data = data_user)

@app.route('/suggestions',methods=['POST','GET'])
@login_required
def friends_suggestions():
    data = m.not_friends()
    newfriends =[]
    
    for f in data:
        newfriends.append({"id":f[0],"usuario":f[1],"imgPerfil":f[2]})

    return jsonify({"status":"success","friends": newfriends})

if __name__ == '__main__':
    app.run(debug=True,port=8000)

