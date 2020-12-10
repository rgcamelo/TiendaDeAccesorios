from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from utils import isPasswordValid, isUsernameValid
from datetime import datetime
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accesorios.db'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    referencia = db.Column(db.String(25), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Product %r>' % self.id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(25), nullable=False)
    nombres = db.Column(db.String(50), nullable=False)
    contrasena = db.Column(db.String(50), nullable=False)
    identificacion = db.Column(db.String(15), nullable=False)
    fechaNacimiento = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(30), nullable=False)
    direccion = db.Column(db.String(25), nullable=False)
    celular = db.Column(db.String(15), nullable=False)
    tipo = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id




@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']

        men = ''
        if not isUsernameValid(usuario):
            men= men + 'Usuario invalido'
        if not isPasswordValid(contrasena):
            men = men + ' Contraseña invalida'

        if men == '':
            return redirect('/home')
        else:
            return render_template('home.html', mensaje=men)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/user')
def user():
    users = User.query.all()
    return render_template('gestionUsuarios.html',users=users)

@app.route('/addUser')
def addUser():
    return render_template('addUser.html')

@app.route('/product')
def product():
    products = Producto.query.order_by(Producto.date_created).all()
    return render_template('gestionProductos.html',products=products)

@app.route('/addProduct')
def addProduct():
    return render_template('addProduct.html')

@app.route('/registrarProduct', methods=['POST'])
def registrarProduct():
    if request.method == 'POST':
        nombre = request.form['nombre']
        referencia = request.form['referencia']
        marca = request.form['marca']
        cantidad = request.form['cantidad']
        new_Accesorio = Producto(nombre=nombre,referencia=referencia,marca=marca,cantidad=cantidad)

        try:
            db.session.add(new_Accesorio)
            db.session.commit()
            return redirect('/product')
        except:
            return 'Error'

    else:
        return render_template('index.html')


@app.route('/deleteProduct/<int:id>')
def delete(id):
    accessorioDelete = Producto.query.get_or_404(id)

    try:
        db.session.delete(accessorioDelete)
        db.session.commit()
        return redirect('/product')
    except:
        return 'Error'

@app.route('/updateProduct/<int:id>', methods=['GET', 'POST'])
def update(id):
    product = Producto.query.get_or_404(id)

    if request.method == 'POST':
        product.nombre = request.form['nombre']
        product.referencia = request.form['referencia']
        product.marca = request.form['marca']
        product.cantidad = request.form['cantidad']

        try:
            db.session.commit()
            return redirect('/product')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('updateProduct.html', product=product)


@app.route('/registrarUser', methods=['POST'])
def registrarUser():
    if request.method == 'POST':
        usuario = request.form['usuario']
        nombres = request.form['nombres']
        contrasena = request.form['contrasena']
        cedula = request.form['cedula']
        fechaNacimiento = request.form['fechaNacimiento']
        format = '%Y-%m-%d'
        fecha = datetime.strptime(fechaNacimiento, format)
        email = request.form['email']
        direccion = request.form['direccion']
        celular = request.form['celular']
        tipoUsuario = request.form['tipoUsuario']
        new_User = User(
        usuario=usuario,nombres=nombres,email=email,tipo=tipoUsuario,identificacion=cedula,direccion=direccion,celular=celular, fechaNacimiento=fecha,contrasena=contrasena)

        #return(new_User.nombres+new_User.apellidos+new_User.celular+new_User.direccion+new_User.email+new_User.fechaNacimiento+new_User.identificacion+new_User.tipo+new_User.usuario)

        try:
            db.session.add(new_User)
            db.session.commit()
            return redirect('/user')
        except:
            return 'Error'

    else:
        return render_template('index.html')

@app.route('/deleteUser/<int:id>')
def deleteUser(id):
    userDelete = User.query.get_or_404(id)

    try:
        db.session.delete(userDelete)
        db.session.commit()
        return redirect('/user')
    except:
        return 'Error'
    
@app.route('/updateUser/<int:id>', methods=['GET', 'POST'])
def updateUser(id):
    user = User.query.get_or_404(id)

    if request.method == 'POST':
        user.nombres = request.form['nombres']
        user.usuario = request.form['usuario']
        user.contrasena = request.form['contrasena']
        user.identificacion = request.form['cedula']
        fechaNacimiento = request.form['fechaNacimiento']
        format = '%Y-%m-%d'
        fecha = datetime.strptime(fechaNacimiento, format)
        user.fechaNacimiento = fecha
        user.email = request.form['email']
        user.direccion = request.form['direccion']
        user.celular = request.form['celular']
        user.tipo = request.form['tipoUsuario']

        try:
            db.session.commit()
            return redirect('/user')
        except:
            return 'Error'

    else:
        return render_template('updateUser.html', user=user)

if __name__ == "__main__":
    app.run(debug=True)
