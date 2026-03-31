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
    

def Usuario(id_usr):
    cur = psql.cursor()
    
    User_info = "SELECT * FROM Usuarios where id =%s"
    
    cur.execute(User_info,(id_usr,))
    
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
        psql.rollback()
        return e
    
def Sign_up(name,f_last_name,s_last_name,birth,email,hashed_password,career,user_name,path_pic,path_bg,code):

    try:
       
        cur = psql.cursor() 
        acceso = cur.execute("INSERT INTO usuarios(nombre,apellido_p,apellido_M,birth,correo,password,carrera,user_name,foto_d_perfil,correo_verificado,code_verification,fondo_perfil) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,false,%s,%s) RETURNING id",(name,f_last_name,s_last_name,birth,email,hashed_password,career,user_name,path_pic,code,path_bg))
        
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
        
        return ei


def posts(id_user):
    
    con = psql.cursor()
    query_cuammunity = "SELECT u.id,u.user_name,u.foto_d_perfil,cu.nombre,cuaji_posts.id, cuaji_posts.fecha, cuaji_posts.titulo, cuaji_posts.contenido_post,cuaji_posts.likes,cuaji_posts.img_post FROM cuammunity_users c join cuaji_posts on c.id_comunidad = cuaji_posts.id_cuammunity JOIN Usuarios u on u.id = cuaji_posts.id_usuario  JOIN cuammunitys cu ON c.id_comunidad = cu.id where c.id_usuario = %s ORDER BY  cuaji_posts.id DESC"
    con.execute(query_cuammunity,(id_user,))
    
    
    if (con.rowcount >= 1 ):
        posts = con.fetchall()
        return posts
    else: 
        return 0
    
def posts_of(id_user):
    con = psql.cursor()
    query_cuammunity = "SELECT u.id,u.user_name,u.foto_d_perfil,cu.nombre,cuaji_posts.id, cuaji_posts.fecha, cuaji_posts.titulo, cuaji_posts.contenido_post,cuaji_posts.likes,cuaji_posts.img_post FROM cuammunity_users c join cuaji_posts on c.id_comunidad = cuaji_posts.id_cuammunity JOIN Usuarios u on u.id = %s JOIN cuammunitys cu ON c.id_comunidad = cu.id WHERE c.id_usuario =%s  AND cuaji_posts.id_usuario = %s ORDER BY cuaji_posts.id DESC;"
    con.execute(query_cuammunity,(id_user,id_user,id_user,))
    
    
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
            psql.rollback()
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
        print(f'La imagen recibida es {post_img}')
        print(f'La comunidad recibida es {post_community}')
        
        if post_img is not None:
            print('Insertando Poooost')
            comentar = 'INSERT INTO Cuaji_posts (id_usuario,contenido_post,id_cuammunity,img_post,fecha) VALUES (%s,%s,%s,%s,%s)'
            cur.execute(comentar,(user,new_post_txt,post_community,post_img,now))
            print(f'Se postio')
        else:
            comentar = 'INSERT INTO Cuaji_posts (id_usuario,contenido_post,id_cuammunity,fecha) VALUES (%s,%s,%s,%s)'
            cur.execute(comentar,(user,new_post_txt,post_community,now))

        psql.commit()
        
        cur.close()
        
        return 1
        
    except Exception as e:
        psql.rollback()
        
        print(e)
        return e
    
def user_into_communitys(id_user):
    try:
        cur = psql.cursor()
        query = "SELECT c.id, c.nombre, c.usuarios_comunidad, c.logo_comunidad FROM cuammunitys c JOIN cuammunity_users cu ON cu.id_comunidad = c.id AND cu.id_usuario = %s"
        cur.execute(query,(id_user,))
        
        if cur.rowcount >= 1:
            communidades = cur.fetchall()
            print(communidades)
            cur.close()
            return communidades
        else: 
            cur.close()
            return 0
    except Exception as e:
        print(e)
        err = str(e)
        psql.rollback()
        return err
    
def amount_friends(id):
    try:
        cur = psql.cursor()
        query = "SELECT COUNT(*) FROM amigos WHERE id_usuario = %s"
        cur.execute(query,(id,))
        
        if cur.rowcount >= 1:
            friends_count = cur.fetchone()[0]
            cur.close()
            return friends_count
        else:
            cur.close()
            return 0
    except Exception as e:
        err = str(e)
        print(e)
        psql.rollback()
        return err
    
def amount_communitys(id):
    try:
        cur = psql.cursor()
        query = "SELECT COUNT(*) FROM cuammunity_users WHERE id_usuario = %s"
        cur.execute(query,(id,))
        
        if cur.rowcount >= 1:
            friends_count = cur.fetchone()[0]
            cur.close()
            return friends_count
        else:
            cur.close()
            return 0
    except Exception as e:
        err = str(e)
        print(e)
        psql.rollback()
        return err
    
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
        print(e)
        err = str(e)
        psql.rollback()
        return err


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
    
def UpdateLikes(status,id_post,id_user):
    try:
        cur = psql.cursor()
        if status :
            
            query = "INSERT INTO PostUsers_likes (id_usuarios,id_post) values (%s,%s)"
            cur.execute(query,(id_user,id_post,))
        else:
            query = "DELETE FROM PostUsers_likes WHERE id_usuarios = %s RETURNING (SELECT likes FROM cuaji_posts WHERE id = %s)"     
            cur.execute(query,(id_user,id_post))
        
        query_count = "SELECT likes FROM cuaji_posts WHERE id = %s"
        cur.execute(query_count,(id_post,))
        likes = cur.fetchone()[0]
        psql.commit()
        cur.close()
        return likes
    except Exception as e:
        psql.rollback()
        print(e)
        return e
    
def DoUserlikes(id_user,id_post):
    try:
        cur = psql.cursor()
        query = "Select * FROM PostUsers_likes where id_usuarios = %s and id_post = %s"
        cur.execute(query,(id_user,id_post,))
        user_like = cur.rowcount
        cur.close()
        if user_like:  
            return True
        else:
            return False
                
    except Exception as e:
        psql.rollback()
        print(e)
        return e

def CreateCuammunity(nombre,logo,background):
    try:
        cur = psql.cursor()
        query = "INSERT INTO cuammunitys(nombre,logo_comunidad,fondo_comunidad) values (%s,%s,%s) RETURNING id"
        cur.execute(query,(nombre,logo,background))
        newcua = cur.fetchone()[0]
        cur.close()
        return newcua        
    except Exception as e:
        psql.rollback()
        err = str(e)
        print(err)
        return err
    
def Community(id_com):
    try:
        cur = psql.cursor()
        query = "SELECT * FROM cuammunitys WHERE id = %s"
        cur.execute(query,(id_com,))
        cuaData = cur.fetchone()
        cur.close()
        return cuaData        
    except Exception as e:
        psql.rollback()
        err = str(e)
        print(err)
        return err
    
def join_a_cuammunity(id_user,id_cuammunity,roll):
    
    if roll is not None:
        try:
            cur = psql.cursor()
            query = "INSERT INTO cuammunity_users(id_usuario,id_comunidad,roll) VALUES (%s,%s,%s)"
            cur.execute(query,(id_user,id_cuammunity,roll))
            psql.commit()
            cur.close()
        except Exception as e:
            print(e)
            err = str(e)
            psql.rollback()
            return err
    else:
        try:
            cur = psql.cursor()
            query = "INSERT INTO cuammunity_users(id_usuario,id_comunidad,roll) VALUES (%s,%s)"
            cur.execute(query,(id_user,id_cuammunity))
            psql.commit()
            cur.close()
        except Exception as e:
            print(e)
            err = str(e)
            psql.rollback()
            return err
    
def not_friends(id_u):
    try:
        print(f'heeyyyy{id_u}')
        cur = psql.cursor()
        query = "SELECT * FROM usuarios u LEFT JOIN amigos ag ON ag.id_amigo = u.id WHERE ag.id IS NULL AND  u.id != %s"
        cur.execute(query,(id_u,))
        new_friends = cur.fetchall()
        psql.commit()
        cur.close()
        return new_friends
    except Exception as e:
        print(e)
        err = str(e)
        psql.rollback()
        return err