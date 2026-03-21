from flask_bcrypt import bcrypt
from flask import flash,request,redirect,jsonify, url_for
from flask_login import UserMixin,login_user,current_user,login_required,logout_user,LoginManager
from datetime import datetime as dt
import psycopg2 
now =dt.now()


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

class User(UserMixin):
    def __init__(self, id, email):
        self.id = id
        self.email = email
    

    
def Users():
        con = psql.cursor()
        query = "Select * FROM Usuarios"
        con.execute(query,)
        users_data = con.fetchall()
        con.close()
        
        return users_data
    

def Usuario(id):
    cur = psql.cursor()
    
    User_info = "SELECT * FROM Usuarios where id =%s"
    
    cur.execute(User_info,id)
    
    user = cur.fetchone()
    
    cur.close()
    
    return user;

def Log_in(user_mail,password):
    cur = psql.cursor()
    mail_query = "SELECT * FROM Usuarios Where correo = %s"
    cur.execture(mail_query,user_mail)
    password_hash = cur.fetchone()
    hash_db = password_hash[7]
    ver_contraseña = bcrypt.check_password_hash(hash_db,password)

    cur.close()

    if ver_contraseña:
        user = User(password_hash[0],password_hash[5])
        login_user(user)
             
        return redirect(url_for('main', id=password_hash[0])) 
    else:
        flash( "Usuario o contraseña incorrectos")
        return redirect(url_for('index'))
    
def Sign_up(name,f_last_name,s_last_name,birth,email,hashed_password,career,user_name,path_pic):

    try:
       
        cur = psql.cursor() 
        acceso = cur.execute("INSERT INTO usuarios(nombre,apellido_p,apellido_M,birth,correo,password,carrera,user_name,foto_d_perfil) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(name,f_last_name,s_last_name,birth,email,hashed_password,career,user_name,path_pic))
            
        psql.commit()
        cur.close()
        print("se logro")
        return 1
    
    except Exception as e:
        psql.rollback() 
        print(e)
        return jsonify({"status": "error", "mensaje": str(e)}), 500


def posts(id):
    con = psql.cursor()
    query_cuammunity = " SELECT * FROM cuammunity_users c join cuaji_posts on c.id_comunidad = cuaji_posts.id_cuammunity and cuaji_posts.id_usuario = %s"
    con.execute(query_cuammunity,(id,))
    
    if (con.rowcount() > 1 ):
        posts = con.fetchall()
        return posts
    else: 
        return 0
    
    
def add_comment(user,user_post,text,route):

    if route:
        try:
            cur = psql.cursor

            comentar = 'INSERT INTO Comentarios(id_post,id_usuario,comentario,img,date)'

            cur.execute(comentar,(user_post,user,text,route,now))

            cur.commit()
            
            cur.close()
            
            flash("Comentario Agregado","success")
            return redirect(url_for('main'))
            
        except Exception as e:
            flash("Error no se pudo agregar tu comentario, intentalo más tarde","error")
            return redirect(url_for('main'))  
    else: 
        try:
            cur = psql.cursor

            comentar = 'INSERT INTO Comentarios(id_post,id_usuario,comentario,date)'

            cur.execute(comentar,(user_post,user,text,now))

            cur.commit()
            
            cur.close()
            
            return 1
            
        except Exception as e:
            return 0
        
def create_post(user,new_post_txt,post_community,post_img):
    try:
        cur =psql.cursor
        if post_img is not None:
            comentar = 'INSERT INTO Cuajipost (id_user,text,community,img,date)'
            cur.execute(comentar,(user,new_post_txt,post_community,post_img,now))
        else:
            comentar = 'INSERT INTO Cuajipost (id_user,text,community,date)'
            cur.execute(comentar,(user,new_post_txt,post_community,now))

        cur.commit()
        
        cur.close()
        
        return 1
        
    except Exception as e:
        return 0
    
def user_into_communitys(id):
    cur = psql.cursor()
    query = "SELECT c.nombre c.usuarios_comunidad c.logo FROM cuammunitys c JOIN cuammunity_users cu ON c.id_comunidad = cu.id AND c.id_usuario = %s"
    cur.execute(query,(id,))
    
    if cur.rowcount > 1:
        communidades = cur.fetchall()
        cur.close()
        return communidades
    else: 
        cur.close()
        return 0
    
def amount_friends(id):
    cur = psql.cursor()
    query = "SELECT COUNT(id_usuario) FROM amigos WHERE id_usuario = %s"
    cur.execute(query,(id,))
    
    if cur.rowcount():
        friends_count = cur.fetchone()
        cur.close()
        return friends_count
    else:
        cur.close()
        return 0
    
def community_search(text):
        cur = psql.cursor()
        query = "SELECT * FROM cuammunitys WHERE nombre LIKE  %s"
        cur.execute(query,(text,))
        
        if cur.rowcount > 1:
            communitys = cur.fetchall()
            cur.close()
            return communitys
        else:
            cur.close()
            return 0