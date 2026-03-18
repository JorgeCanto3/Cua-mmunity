from app import psql, User
from flask_bcrypt import bcrypt
from flask import flash

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
    
def Sign_up():
    