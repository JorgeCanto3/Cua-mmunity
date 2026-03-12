from flask import Flask, render_template,request,redirect,url_for,flash 
from flask_bcrypt import Bcrypt
import psycopg2 #Esta biblioteca sirve para conectar python se conecte con la BD

app = Flask(__name__)
app.secret_key = 'coloca_contra'
bcrypt = Bcrypt(app) 
  
psql = psycopg2.connect(
    database ="cuammunity", # Coloca el nombre de tu BD 
    user ="postgres",
    password="123", # Coloca tu contraseña
    host="localhost",
    port="5432"
)


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
                return redirect(url_for('main')) 
            else:
                return "Usuario o contraseña incorrectos"

    return render_template('iniciar-sesion.html')

@app.route('/registro', methods=["GET", "POST"])
def registro():
    
    if request.method == 'POST':
            
            name = request.form['name']
            f_last_name = request.form['first_LastName']
            s_last_name = request.form['second_LastName']
            birth = request.form['birth']
            email = request.form['email']
            psswrd = request.form['pswd']
            career = request.form['career']

            hashed_password = bcrypt.generate_password_hash (psswrd).decode('utf-8')
            
            try:
                cur = psql.cursor() 
                acceso = cur.execute("INSERT INTO usuarios(nombre,apellido_p,apellido_M,birth,correo,password,carrera) VALUES (%s,%s,%s,%s,%s,%s,%s)",(name,f_last_name,s_last_name,birth,email,hashed_password,career))
                
                psql.commit()

                usuario = cur.rowcount

                cur.close()

                flash("Registro Exitoso!","success")
                return redirect(url_for('index')) 

            except Exception as e:
                psql.rollback() 
                flash("Correo ya registrado","Error")
                return redirect(url_for('registro'))
            
    return render_template('registro.html')

@app.route('/main')
def main():
    return render_template('index.html')
    
@app.route('/Community')
def community():
    return render_template('community.html')
    

    



if __name__ == '__main__':
    app.run(debug=True,port=8000)