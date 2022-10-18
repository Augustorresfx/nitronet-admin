
from flask import Flask, flash, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
from config import config

from flask_login import LoginManager, login_user, logout_user, login_required
#Modelos
from models.ModelUser import ModelUser
 
#Entities/Entidades
from models.entities.User import User
load_dotenv()


app=Flask(__name__)




total_sept=0
total_septiembre=total_sept

db=MySQL(app)

login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form['username'])
        print(request.form['password'])
        user = User(0, request.form['username'], request.form['password'])
        logged_user = ModelUser.login(db, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                flash("Contraseña invalida...")
                return render_template('auth/login.html')
        else:
            flash("Usuario no encontrado...")
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/agregar')
@login_required
def agregar():
    return render_template('client/agregar.html')

@app.route('/buscar_cliente')
@login_required
def buscar_cliente():
    return render_template('client/buscar.html')

@app.route('/reportes')
@login_required
def reportes():
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM clientes_marilo_2023')
    data = cur.fetchall()
    acumulador_clientes=0
    total_sept=0
    for x in data:
        if x[14] >= 1000:
            acumulador_clientes+=1
        total_sept+=x[14]
        print(acumulador_clientes, total_sept)
    return render_template('estadisticas/reportes.html', data = total_sept)

@app.route('/buscar', methods = ['POST'])
@login_required
def buscar():
    if request.method == 'POST':
        fullname=request.form['fullname']
        address=request.form['address']
        ip=request.form['ip']
        cur = db.connection.cursor()
        cur.execute("""SELECT * FROM clientes_marilo_2023
        WHERE fullname RLIKE %s""", (fullname,))
        data = cur.fetchall()
        print(data)
        return render_template('client/buscar.html', clientes = data)

@app.route('/home')
@login_required
def home():
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM clientes_marilo_2023')
    data = cur.fetchall()
    return render_template('home.html', clientes = data)
@app.route('/add_client', methods=['POST'])
@login_required
def add_client():
    if request.method == 'POST':
        fullname=request.form['fullname']
        address=request.form['address']
        ip=request.form['ip']
        tel=request.form['tel']
        email=request.form['email']
        cur = db.connection.cursor()
        cur.execute('INSERT INTO clientes_marilo_2023 (fullname, address, ip, tel, email) VALUES(%s, %s, %s, %s, %s)', 
        (fullname, address, ip, tel, email))
        db.connection.commit()
        flash('Se ha creado el cliente con éxito')
    return redirect(url_for('home'))

@app.route('/edit/<id_cliente>')
@login_required
def get_client(id_cliente):
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM clientes_marilo_2023 WHERE id_cliente = %s', [id_cliente] )
    data = cur.fetchall()
    
    return render_template('client/client.html', cliente = data[0])

@app.route('/update/<id_cliente>', methods = ['POST'])
@login_required
def update_client(id_cliente):
    if request.method == 'POST':
        fullname=request.form['fullname']
        address=request.form['address']
        ip=request.form['ip']
        tel=request.form['tel']
        email=request.form['email']
        cur = db.connection.cursor()
        cur.execute('UPDATE clientes_marilo_2023 SET fullname = %s, address = %s, ip = %s, tel = %s, email = %s WHERE id_cliente = %s', (fullname, address, ip, tel, email, [id_cliente]))
        
        db.connection.commit()
        flash('Cliente editado con éxito')
        return redirect(url_for('home'))

@app.route('/update_abonos/<id_cliente>', methods = ['POST'])
@login_required
def update_client_abonos(id_cliente):
    if request.method == 'POST':
        enero=request.form['enero']
        febrero=request.form['febrero']
        marzo=request.form['marzo']
        abril=request.form['abril']
        mayo=request.form['mayo']
        junio=request.form['junio']
        julio=request.form['julio']
        agosto=request.form['agosto']
        septiembre=request.form['septiembre']
        octubre=request.form['octubre']
        noviembre=request.form['noviembre']
        diciembre=request.form['diciembre']
        cur = db.connection.cursor()
        cur.execute('UPDATE clientes_marilo_2023 SET enero = %s, febrero = %s, marzo = %s, abril = %s, mayo = %s, junio = %s, julio = %s, agosto = %s, septiembre = %s, octubre = %s, noviembre = %s, diciembre = %s WHERE id_cliente = %s', (enero, febrero, marzo, abril, mayo, junio, julio, agosto, septiembre, octubre, noviembre, diciembre, [id_cliente]))
        
        db.connection.commit()
        flash('Abonos actualizados con éxito')
        return redirect(url_for('home'))

@app.route('/delete/<id_cliente>')
@login_required
def delete_cliente(id_cliente):
    cur = db.connection.cursor()
    cur.execute('DELETE FROM clientes_marilo_2023 WHERE id_cliente = {0}'.format(id_cliente))
    db.connection.commit()
    flash('Se ha eliminado el cliente con éxito')
    return redirect(url_for('home'))

@app.route('/protected')
@login_required
def protected():
    return "<h1>Esta es una vista protegida, solo para usuarios autenticados.</h1>"


def status_401(error):
    return redirect(url_for('login'))


def status_404(error):
    return "<h1>Página no encontrada</h1>", 404

def create_app():
   return app

if __name__=='__main__':
    """app.config["MYSQL_USER"] = os.getenv('MYSQL_USER')
    app.config["MYSQL_PASSWORD"] = os.getenv('MYSQL_PASSWORD')
    app.config["MYSQL_DB"] = os.getenv('MYSQL_DB')
    app.config["MYSQL_PORT"] = os.getenv('MYSQL_PORT')
    app.config["SECRET_KEY"] = os.getenv('SECRET_KEY')
    app.config["MYSQL_HOST"] = os.getenv('MYSQL_HOST')
    app.config["DEBUG"] = os.getenv('DEBUG') """
    app.config.from_object(config['development'])
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run()

