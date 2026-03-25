from flask import Flask, render_template,request,redirect,url_for,flash, jsonify
from flask_bcrypt import Bcrypt
from flask_login import UserMixin,login_user,current_user,login_required,logout_user,LoginManager
from werkzeug.utils import secure_filename
import os
from datetime import datetime as dt
import model as m

now =dt.now()
app = Flask(__name__)

app.secret_key = 'coloca_contra'

# pa encriptar la contraseña
bcrypt = Bcrypt(app) 

# pa manejar el log
login_manager = LoginManager()
login_manager.init_app(app)


# Direcciones de las carpetas para almacenar las imagenes
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

COMUMUNITY_UPLOAD = os.path.join(BASE_DIR, 'static', 'Upload','Community')
POST_UPLOAD = os.path.join(BASE_DIR, 'static', 'Upload','Post') 
USER_UPLOAD = os.path.join(BASE_DIR, 'static', 'Upload','Profile')
ALLOWED_FILES = {'jpg','png','jpeg'}


app.config['UPLOAD_FOLDER_html'] = '/static/Upload/Profile/'
app.config['UPLOAD_FOLDER_html_Post'] = '/static/Upload/Post/'
app.config['UPLOAD_FOLDER_html_Community'] = '/static/Upload/Community/'
app.config['UPLOAD_FOLDER_PY'] = USER_UPLOAD


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
        
@app.route('/', methods=["GET","POST"])
def index():
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('Correo')
        psswrd = data.get('pswd')
        user_conf = Log(email,psswrd)
            
        if  user_conf != 0:
            return jsonify({"status":"success","details":user_conf})
        else:
            return jsonify({"status":"error", "details": user_conf})     
        
        
      
        
    return render_template('iniciar-sesion.html')

@app.route('/iniciar', methods=["POST"])
def Log (email,psswrd):
    user_data = m.Log_in(email)
    
    hash_db =user_data[7]
    ver_contraseña = bcrypt.check_password_hash(hash_db,psswrd)
    
    if  ver_contraseña is True:
        login_user(m.User(user_data[0],user_data[1]))
        return user_data[0]
    else:
        return 0

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

    hashed_password = bcrypt.generate_password_hash (psswrd).decode('utf-8')
    path_pic=profile_accept(profile_pic)
            
    insert_db = m.Sign_up(name,f_last_name,s_last_name,birth,email,hashed_password,career,user_name,path_pic)   
    if (insert_db == 1):
        return jsonify({"status":"success"})
    else:
        return jsonify({"status":"error", "details": str(insert_db)})


@app.route('/feed/<int:id>')
@login_required
def main(id):
    if(current_user.id!=id):
        print(current_user.id)
        print(current_user.email)
        
        flash("Error no puedes cambiar de usuario","Error")
        return redirect(url_for('index'))
    else:
        
        data_user = m.Usuario(id)
        #amigos = cur.execute("select * from amigos where id = %s",(current_user.id,))
        #feed = cur.execute("SELECT * From Cuajiposts Where id =%s join on id from cuammunitys ")
         
    return render_template('index.html',profile_data = data_user)
    
@app.route('/Community')
def community():
    return render_template('community.html')

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
    
@app.route('/post', methods=["POST"])
def post():
    user = current_user.id

    
    new_post_txt =      request.form.get('text')   
    post_community =    request.form.get('community')  
    post_img =          request.files.get('img')  
    
    posted = m.create_post(user,new_post_txt,post_community,post_img)

    if posted:
            return jsonify({"status":"success", "mensaje":"Post Creado 🦐🦐"})
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
def cuamminitys_to_post():
    data = request.get_json()
    id_4_post = data.get('id')
    query = m.user_into_communitys(id_4_post) 

    cuammunitys = []
    
    for cua in query:
        cuammunitys.append({"id":cua[0],"nombre":cua[1],"logo":cua[3]})
    
    
    return jsonify({"status":"success","comunidades":cuammunitys})

@app.route('/posts',methods = ["GET"])
def post_4_user():
    
    query = m.posts(current_user.id)
    
    if(query != 0):
        posts = []
        for c in query:
            posts.append({"usuario":c[0],"imgPerfil":c[1],"comunidad":c[2],"idPost":c[3],"fecha":[4],"titulo":c[5],"texto":c[6],"likes":c[7],"imgPost":c[8]})
        
        return jsonify({"status":"success" ,"post":posts})
    else:
        return jsonify({"status":"error"})

@app.route('/Communitys')
def Community_card():
    id_4_post =current_user.id
    query = m.user_into_communitys(id_4_post) 

    cuammunity = []
    
    for cua in query:
        cuammunity.append({"id":cua[0],"nombre":cua[1],"usuarios":cua[2],"logo":cua[3]})
    
    
    return jsonify({"status":"success","comunidad":cuammunity})

@app.route('/delete', methods=["POST"])
def Delete_post():
    data = request.get_json()
    id_post = data.get('id')
    
    print(id_post)
    query = m.erase_post(id_post) 
    if query:
        return jsonify({"status":"success"})
    else:
        print(query)
        return jsonify({"status":"error", "details": query})


@app.route('/edit', methods=["POST"])
def Update_post():
    data = request.get_json()
    id_post = data.get('id')
    text = data.get('text')
    
    
    print(id_post)
    print(text)
    query = m.edit_post(id_post,text) 
    if query:
        return jsonify({"status":"success"})
    else:
        print(query)
        return jsonify({"status":"error", "details": query})



if __name__ == '__main__':
    app.run(debug=True,port=8000)
    