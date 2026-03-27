from flask_bcrypt import Bcrypt
from flask import flash,request,redirect,jsonify, url_for
from flask_login import UserMixin,login_user,current_user,login_required,logout_user,LoginManager
from datetime import datetime as dt
import psycopg2 
now =dt.now()


try:
    psql= psycopg2.connect(
        database ="cuammunity", 
        user ="postgres",
        password="123", 
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
    
    cur.execute(User_info,(id,))
    
    user = cur.fetchone()
    
    cur.close()
    
    return user;

def Log_in(user_mail):
    try:
        
        cur = psql.cursor()
        mail_query = "SELECT * FROM Usuarios Where correo = %s"
        cur.execute(mail_query,(user_mail,))
        
        password_hash = cur.fetchone()
        cur.close()

        return password_hash 
    except Exception as e:
        return e
    
def Sign_up(name,f_last_name,s_last_name,birth,email,hashed_password,career,user_name,path_pic,code):

    try:
       
        cur = psql.cursor() 
        acceso = cur.execute("INSERT INTO usuarios(nombre,apellido_p,apellido_M,birth,correo,password,carrera,user_name,foto_d_perfil,correo_verificado,code_verification) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,false,%s) RETURNING id",(name,f_last_name,s_last_name,birth,email,hashed_password,career,user_name,path_pic,code))
        
        psql.commit()

        res = cur.fetchone()[0]  
        
        
        general_community = "INSERT INTO cuammunity_users(id_usuario,id_comunidad) VALUES (%s,1) RETURNING id"
        cur.execute(general_community,(res,))
        psql.commit()
        res_cua_user = cur.fetchone()[0]
        
        print(f'El id del insert a la comunidad general es: {res_cua_user}')
        cur.close()
        return res
    
    except Exception as e:
        psql.rollback() 
        ei = str(e)
        print(ei)
        err =""
        if "«correo_unico»" in ei:
            err = "El correo ya existe"
        
        return err


def posts(id_user):
    con = psql.cursor()
    query_cuammunity = "SELECT u.id,u.user_name,u.foto_d_perfil,cu.nombre,cuaji_posts.id, cuaji_posts.fecha, cuaji_posts.titulo, cuaji_posts.contenido_post,cuaji_posts.likes,cuaji_posts.img_post FROM cuammunity_users c join cuaji_posts on c.id_comunidad = cuaji_posts.id_cuammunity JOIN Usuarios u on u.id = cuaji_posts.id_usuario  JOIN cuammunitys cu ON c.id_comunidad = cu.id where c.id_usuario = %s"
    con.execute(query_cuammunity,(id_user,))
    
    
    if (con.rowcount >= 1 ):
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
        cur =psql.cursor()
        if post_img is not None:
            comentar = 'INSERT INTO Cuaji_posts (id_usuario,contenido_post,id_cuammunity,img_post,fecha) VALUES (%s,%s,%s,%s)'
            cur.execute(comentar,(user,new_post_txt,post_community,post_img,now))
        else:
            comentar = 'INSERT INTO Cuaji_posts (id_usuario,contenido_post,id_cuammunity,fecha) VALUES (%s,%s,%s,%s)'
            cur.execute(comentar,(user,new_post_txt,post_community,now))

        psql.commit()
        
        cur.close()
        
        return 1
        
    except Exception as e:
        return e
    
def user_into_communitys(id):
    cur = psql.cursor()
    query = "SELECT c.id, c.nombre, c.usuarios_comunidad, c.logo_comunidad FROM cuammunitys c JOIN cuammunity_users cu ON cu.id_comunidad = c.id AND cu.id_usuario = %s"
    cur.execute(query,(id,))
    
    if cur.rowcount == 1:
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
        
def cuammunity_join(id):
    try:
        cur = psql.cursor()
        query = "INSERT INTO cuammunity_users VALUES (%s,0)"
        cur.execute(query,(id,))
        cur.commit()
        cur.close()
    except Exception as e:
        return e


def erase_post(id):
    try:
        cur = psql.cursor()
        query = "DELETE FROM cuaji_posts where id = %s"
        cur.execute(query,(id,))
        psql.commit()
        cur.close()
        return "success"
    except Exception as e:
        psql.rollback()
        print(e)
        return e
    
def edit_post(id,text):
    try:
        cur = psql.cursor()
        query = "Update cuaji_posts SET contenido_post = %s where id = %s"
        cur.execute(query,(text,id,))
        psql.commit()
        cur.close()
        return "success"
    except Exception as e:
        psql.rollback()
        print(e)
        return e

def update_confirm(id):
    try:
        cur = psql.cursor()
        query = "Update usuarios SET correo_verificado = TRUE where id = %s"
        cur.execute(query,(id,))
        psql.commit()
        cur.close()
        return "success"
    except Exception as e:
        psql.rollback()
        print(e)
        return e