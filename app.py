from flask import Flask, render_template,request,redirect,url_for,flash 
from flask_bcrypt import Bcrypt
from flask_login import UserMixin,login_user,current_user,login_required,logout_user,LoginManager
import psycopg2 #Esta biblioteca sirve para conectar python se conecte con la BD

app = Flask(__name__)
app.secret_key = 'coloca_contra'
bcrypt = Bcrypt(app) 
login_manager = LoginManager()
login_manager.init_app(app)

psql = psycopg2.connect(
    database ="cuammunity", # Coloca el nombre de tu BD 
    user ="postgres",
    password="123", # Coloca tu contraseña
    host="localhost",
    port="5432"
)

class User(UserMixin):
    def __init__(self, id, email):
        self.id = id
        self.email = email

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
                flash("Correo ya registrado","error")
                return redirect(url_for('registro'))
            
    return render_template('registro.html')

@app.route('/feed/<int:id>')
@login_required
def main(id):
    if(current_user.id!=id):
         
        flash("Error no puedes cambiar de usuario","Error")
        return redirect(url_for('index'))
    else:
        cur = psql.cursor()
        usuario = cur.execute("select * from usuarios where id = %s",(current_user.id,))

        data_user = cur.fetchone()
        #feed = cur.execute("SELECT * From")

        cur.close()
         
    return render_template('index.html',profile_data = data_user)
    
@app.route('/Community')
def community():
    return render_template('community.html')
    

    



if __name__ == '__main__':
    app.run(debug=True,port=8000)