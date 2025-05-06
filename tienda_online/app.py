from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
from functools import wraps  # <- IMPORTANTE para login_required
from models.modelos import Usuario, Tarjeta

# Inicia Flask
app = Flask(__name__)
app.config.from_object('config.Config')

# Inicializa la base de datos
mysql = MySQL(app)

# Función decoradora para exigir login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Debes iniciar sesión para acceder a esta página", "danger")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('home.html')

# Ruta para el registro de usuarios
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        
        # Comprobar si el usuario ya existe
        usuario_existente = Usuario.obtener_usuario_por_nombre(name)
        if usuario_existente:
            flash("El nombre de usuario ya existe", "danger")
            return redirect(url_for('register'))
        
        # Encriptar la contraseña
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        # Crear el usuario en la base de datos
        Usuario.crear_usuario(name, hashed_password)
        flash("Usuario registrado correctamente", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

# Ruta para el login de usuarios
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['usuario_tienda']
        password = request.form['clave_tienda']
        
        # Obtener el usuario de la base de datos
        usuario = Usuario.obtener_usuario_por_nombre(name)
        if usuario and check_password_hash(usuario[2], password):  # usuario[2] es la contraseña almacenada
            session['user_id'] = usuario[0]
            session['user_name'] = usuario[1]
            flash("Has iniciado sesión correctamente", "success")
            return redirect(url_for('inicio'))
        else:
            flash("Nombre de usuario o contraseña incorrectos", "danger")
            return redirect(url_for('login'))
    
    return render_template('login.html')

# Ruta para cerrar sesión
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    flash("Has cerrado sesión correctamente", "success")
    return redirect(url_for('login'))

@app.route('/perfil')
@login_required
def perfil():
    user_id = session['user_id']
    usuario = Usuario.obtener_usuario_por_id(user_id)
    
    if usuario:
        return render_template('perfil.html', usuario=usuario)
    else:
        flash("No se encontró el usuario", "danger")
        return redirect(url_for('login'))

@app.route('/detalles_cuenta', methods=['POST'])
@login_required
def update_account():
    username = request.form['username']
    password = request.form['password']
    user_id = session['user_id']
    
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    
    Usuario.actualizar_usuario(user_id, username, hashed_password)
    session['user_name'] = username
    flash("Cuenta actualizada correctamente", "success")
    
    return redirect(url_for('perfil'))

@app.route('/eliminar_cuenta', methods=['POST'])
@login_required
def delete_account():
    user_id = session['user_id']
    Usuario.eliminar_usuario(user_id)
    session.clear()
    flash("Cuenta eliminada correctamente", "success")
    return redirect(url_for('home'))

@app.route('/agregar_tarjeta', methods=['POST'])
@login_required
def agregar_tarjeta():
    try:
        data = request.get_json()
        numero = data['numero']
        fecha_caducidad = data['fecha_caducidad']
        cvv = data['cvv']
        id_usuario = data['id_usuario']

        return Tarjeta.agregar_tarjeta(numero, fecha_caducidad, cvv, id_usuario)
    
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error al procesar la solicitud: {str(e)}'}), 500

@app.route('/inicio')
@login_required
def inicio():
    return render_template('inicio.html')

@app.route('/futbol')
@login_required
def futbol():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre, precio, talla, color, imagen FROM productos WHERE id BETWEEN 37 AND 66")
    productos = cur.fetchall()

    productos_info = []
    for producto in productos:
        imagen_url = f"/static/img/{producto[5]}"
        productos_info.append({
            'id': producto[0],
            'nombre': producto[1],
            'precio': producto[2],
            'talla': producto[3],
            'color': producto[4],
            'imagen': imagen_url
        })
    
    cur.close()
    return render_template('futbol.html', productos=productos_info)

@app.route('/padel')
@login_required
def padel():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre, precio, talla, color, imagen FROM productos WHERE id BETWEEN 94 AND 123")
    productos = cur.fetchall()

    productos_info = []
    for producto in productos:
        imagen_url = f"/static/img/{producto[5]}"
        productos_info.append({
            'id': producto[0],
            'nombre': producto[1],
            'precio': producto[2],
            'talla': producto[3],
            'color': producto[4],
            'imagen': imagen_url
        })
    
    cur.close()
    return render_template('padel.html', productos=productos_info)

@app.route('/tenis')
@login_required
def tenis():
    return render_template('tenis.html')

@app.route('/baloncesto')
@login_required
def baloncesto():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre, precio, talla, color, imagen FROM productos WHERE id BETWEEN 67 AND 93")
    productos = cur.fetchall()

    productos_info = []
    for producto in productos:
        imagen_url = f"/static/img/{producto[5]}"
        productos_info.append({
            'id': producto[0],
            'nombre': producto[1],
            'precio': producto[2],
            'talla': producto[3],
            'color': producto[4],
            'imagen': imagen_url
        })
    
    cur.close()
    return render_template('baloncesto.html', productos=productos_info)

@app.route('/contactanos')
@login_required
def contactanos():
    return render_template('contactanos.html')

@app.route('/enviar_contacto', methods=['POST'])
@login_required
def enviar_contacto():
    nombre = request.form['nombre']
    email = request.form['email']
    asunto = request.form['asunto']
    mensaje = request.form['mensaje']

    print(f"Mensaje recibido de {nombre} - {email}: {asunto} -> {mensaje}")

    flash('Tu mensaje ha sido enviado correctamente. Gracias por contactarnos.', 'success')
    return redirect(url_for('contactanos'))

@app.route('/carrito')
@login_required
def carrito():
    return render_template('carrito.html')

@app.route('/finalizar_compra')
@login_required
def finalizar_compra():
    carrito = request.cookies.get('carrito')
    return render_template('finalizar_compra.html', carrito=carrito)

# Iniciar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
