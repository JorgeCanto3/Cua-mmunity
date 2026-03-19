from flask import Flask, render_template,request,redirect,url_for,flash, jsonify
from flask_bcrypt import Bcrypt
from flask_login import UserMixin,login_user,current_user,login_required,logout_user,LoginManager
from werkzeug.utils import secure_filename
import psycopg2 
import os
from datetime import datetime as dt
from model import *

now =dt.now()
app = Flask(__name__)
app.secret_key = 'coloca_contra'
bcrypt = Bcrypt(app) 
login_manager = LoginManager()
login_manager.init_app(app)

try:
    psql= psycopg2.connect(
        database ="cuammunity", 
        user ="postgres",
        password="123", # 
        host="localhost",
        port="5432"
    )
except Exception as e:
    flash(e,"error")

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


class User(UserMixin):
    def __init__(self, id, email):
        self.id = id
        self.email = email
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
        

@login_manager.user_loader
def load_user(user_id):

    cur = psql.cursor()
  
    cur.execute("SELECT id, nombre, correo FROM usuarios WHERE id = %s", (user_id,))
    data = cur.fetchone()
    cur.close()

    if data:
        return User(id=data[0], email=data[2])
    
    return flash("El usuario no exisite en la base de datos","Error")

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
            user_mail = request.form['user']
            psswrd = request.form['pswd']
            
            cur = psql.cursor() # <--- sirve para hacer acciones dentro de la bd
            
            acceso = cur.execute("SELECT * FROM usuarios WHERE correo = %s ",(user_mail,))
            
            usuario = cur.fetchone()

            hash_db = usuario[7]
            sec_contraseña = bcrypt.check_password_hash(hash_db,psswrd)

            cur.close()

            if sec_contraseña:
                user = User(usuario[0],usuario[5])
                login_user(user)
                
                return redirect(url_for('main', id=usuario[0])) 
            else:

                flash( "Usuario o contraseña incorrectos")
                return redirect(url_for('index'))

    return render_template('iniciar-sesion.html')

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
            
    insert_db = Sign_up(name,f_last_name,s_last_name,birth,email,hashed_password,career,user_name,path_pic)   
    if (insert_db == 1):
        return jsonify({"status":"success"})
    else:
        return jsonify({"status":"error", "details": str(insert_db)})


@app.route('/feed/<int:id>')
@login_required
def main(id):
    if(current_user.id!=id):
         
        flash("Error no puedes cambiar de usuario","Error")
        return redirect(url_for('index'))
    else:
        cur = psql.cursor()
        usuario = cur.execute("select * from usuarios where id = %s",(current_user.id,))
        #amigos = cur.execute("select * from amigos where id = %s",(current_user.id,))
        #feed = cur.execute("SELECT * From Cuajiposts Where id =%s join on id from cuammunitys ")
        
        

        data_user = cur.fetchone()

        cur.close()
         
    return render_template('index.html',profile_data = data_user)
    
@app.route('/Community')
def community():
    return render_template('community.html')

@app.route('/comentar', methods=["GET", "POST"])
def comentar():
    user = current_user.id
    user_post = request.form['user_post']

    text = request.form['comment']
    
    try:
        cur =psql.cursor
        comentar = 'INSERT INTO Comentarios(id_post,id_usuario,comentario,date)'
        cur.execute(comentar,(user_post,user,text,now))

        
        cur.commit()
        
        cur.close()
        
        flash("Comentario Agregado","success")
        return redirect(url_for('main'))
        
    except Exception as e:
        flash("Error no se pudo agregar tu comentario, intentalo más tarde","error")
        return redirect(url_for('main'))

@app.route('/post', methods=["GET","POST"])
def post():
    user = current_user.id
    new_post_txt =  request.form['new_txt_post']   
    post_community = request.form['selected_community']  
    post_img = request.form['img_upload']  
    
    try:
        cur =psql.cursor
        comentar = 'INSERT INTO Cuajipost (id_user,text,community,img,date)'
        cur.execute(comentar,(user,new_post_txt,post_community,post_img,now))

        
        cur.commit()
        
        cur.close()
        
        flash("Post Creado 🦐🦐","success")
        return redirect(url_for('main'))
        
    except Exception as e:
        flash("Error no se pudo crear tu cuajipost :(, intentalo más tarde","error")
        return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(debug=True,port=8000)