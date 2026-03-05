from flask import Flask, render_template,request
import psycopg2 #Esta biblioteca sirve para conectar python se conecte con la BD


app = Flask(__name__)
  
#psql = psycopg2.connect(
#    database =" ", # Coloca el nombre de tu BD 
#    user ="postgres",
#    password="", # Coloca tu contraseña
#    host="localhost",
#    port="5432"
#)


# La función nos muestra la pagina inicial, podemos enviar parametros de ser necesario
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/iniciar-sesion')
def iniciar_sesion():
    return render_template('iniciar-sesion.html')
    
@app.route('/Community')
def iniciar_sesion():
    return render_template('community.html')
    

@app.route('/iniciar', methods=['POST'])
def iniciar():
    ## Validmos que la base de datos tenga el usuario
 #   user-mail = request.form[user]
  #  psswrd = request.form[password]
        # cur = psql.cursor() <--- sirve para hacer acciones dentro de la bd

    # Creo que estas instrucciónes regresan 1 si se encuentra el dato, caso contrario nos dio 0  y podemos mandarlo alv o darle acceso
         #acceso = cur.execute("SELECT * FROM usuarios WHERE name = user-mail OR password = psswrd",(user-mail, psswrd)) 
    # Redireccionamos a la pagina inicial con sus datos
    return 1; ## Este  1 simula, de momento, que se encontraron los datos y se puede acceder

@app.route('/registrar', methods=['POST'])
def registrar():
    ## Registramos al usuario con los dato recibidos
    

    return 1; ## Este  1 simula, de momento, que se realizo el registro



if __name__ == '__main__':
    app.run(debug=True,port=8000)