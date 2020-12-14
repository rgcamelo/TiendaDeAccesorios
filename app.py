from flask import Flask, render_template, url_for, request, redirect, session, g, flash
from flask_sqlalchemy import SQLAlchemy
from utils import isPasswordValid, isUsernameValid
from datetime import datetime
from flask_bootstrap import Bootstrap
import functools
import os



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accesorios.db'
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
app.secret_key = os.urandom( 24 )

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(200), nullable=False)
    referencia = db.Column(db.String(25), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Integer, nullable =False)
    cantidad = db.Column(db.Integer, nullable=False)
    imagen = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Product %r>' % self.id

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(25), nullable=False)
    nombres = db.Column(db.String(50), nullable=False)
    apellidos = db.Column(db.String(50), nullable=False)
    contrasena = db.Column(db.String(50), nullable=False)
    identificacion = db.Column(db.String(15), nullable=False)
    fechaNacimiento = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(30), nullable=False)
    direccion = db.Column(db.String(25), nullable=False)
    celular = db.Column(db.String(15), nullable=False)
    tipo = db.Column(db.String, nullable=False)
    estado = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

class User_Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable = False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),nullable=False)
    description = db.Column(db.String(50), nullable=False)



    def __repr__(self):
        return '<User_Product %r>' % self.id




@app.route('/')
def index():
    if g.user:
        return redirect( url_for('home'))    
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    try:
        if g.user:
            return redirect(url_for('home'))
            
        if request.method == 'POST':
            error = None
            usuario = request.form['usuario']
            contrasena = request.form['contrasena']
            #return(usuario+contrasena)

            if not usuario:
                #return('Debe ingresar el usuario')
                return render_template('index.html')

            if not contrasena:
                #return('Contraseña requerida')
                return render_template('index.html')

            user = User.query.filter_by(usuario=usuario,contrasena=contrasena).first()

            if user is None:
                return('No encontro')
                error = 'Usuario o contraseña invalidos'
            else:
                session.clear()
                id= str(user.id)
                session['user_id'] = id
                return redirect( url_for('home'))
        return render_template('index.html')
    except:
        return render_template('index.html')

def login_required(view):
    @functools.wraps( view )
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect( url_for( 'index' ) )

        return view( **kwargs )

    return wrapped_view

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/user')
@login_required
def user():
    users = User.query.all()
    return render_template('gestionUsuarios.html',users=users)

@app.route('/addUser')
@login_required
def addUser():
    return render_template('addUser.html')

@app.route('/product')
@login_required
def product():
    products = Product.query.order_by(Product.date_created).all()
    return render_template('gestionProductos.html',products=products)

@app.route('/addProduct')
@login_required
def addProduct():
    return render_template('addProduct.html')

@app.route('/registrarProduct', methods=['POST'])
@login_required
def registrarProduct():
    if request.method == 'POST':
        nombre = request.form['nombre']
        referencia = request.form['referencia']
        marca = request.form['marca']
        cantidad = request.form['cantidad']
        new_Accesorio = Product(nombre=nombre,referencia=referencia,marca=marca,cantidad=cantidad)

        try:
            db.session.add(new_Accesorio)
            db.session.commit()
            return redirect('/product')
        except:
            return 'Error'

    else:
        return render_template('index.html')


@app.route('/deleteProduct/<int:id>')
@login_required
def delete(id):
    accessorioDelete = Product.query.get_or_404(id)

    try:
        db.session.delete(accessorioDelete)
        db.session.commit()
        return redirect('/product')
    except:
        return 'Error'

@app.route('/updateProduct/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    product = Product.query.get_or_404(id)

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
@login_required
def registrarUser():
    if request.method == 'POST':
        usuario = request.form['usuario']
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        contrasena = request.form['contrasena']
        cedula = request.form['cedula']
        fechaNacimiento = request.form['fechaNacimiento']
        format = '%Y-%m-%d'
        fecha = datetime.strptime(fechaNacimiento, format)
        email = request.form['email']
        direccion = request.form['direccion']
        celular = request.form['celular']
        tipoUsuario = request.form['tipoUsuario']
        estadoUsuario = request.form['estadoUsuario']
        new_User = User(estado = estadoUsuario, apellidos = apellidos,
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
@login_required
def deleteUser(id):
    userDelete = User.query.get_or_404(id)

    try:
        db.session.delete(userDelete)
        db.session.commit()
        return redirect('/user')
    except:
        return 'Error'
    
@app.route('/updateUser/<int:id>', methods=['GET', 'POST'])
@login_required
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




@app.before_request
def load_logged_in_user():
    user_id = session.get( 'user_id' )

    if user_id is None:
        g.user = None
    else:
        user = User.query.filter_by(id = user_id).first()
        g.user = user


@app.route( '/logout' )
def logout():
    session.clear()
    return redirect( url_for( 'index' ) )

if __name__ == "__main__":
    app.run(debug=True)
