from app import psql, User
from flask_bcrypt import bcrypt
from flask import flash,request,redirect,jsonify

def Usuarios(psql_db):
        con = psql.cursor()
        query = "Select * FROM Usuarios"
        con.execute(query,)
        users_data = con.fetchall()
        con.close()
        
        return users_data
    
def Usuario(psql_db, id):
    cur = psql.cursor()
    
    User_info = "SELECT * FROM Usuarios where id =%s"
    
    cur.execute(User_info,id)
    
    user = cur.fetchone()
    
    cur.close()
    
    return user;

def Log_in(psql_bd, user_mail,password):
    cur = psql_bd.cursor()
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
    