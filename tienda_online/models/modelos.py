from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from flask import jsonify
from datetime import datetime

# Inicia Flask y la extensión MySQL
app = Flask(__name__)
app.config.from_object('config.Config')
mysql = MySQL(app)

# Clase para interactuar con la tabla 'usuarios'
class Usuario:
    @staticmethod
    def obtener_usuario_por_id(user_id):
        # Consulta a la base de datos usando el ID del usuario
        query = "SELECT * FROM usuarios WHERE id = %s"
        cursor = mysql.connection.cursor()
        cursor.execute(query, (user_id,))
        usuario = cursor.fetchone()
        cursor.close()
        return usuario
    @staticmethod
    def crear_usuario(name, password):
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios(name, password) VALUES (%s, %s)", (name, password))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def obtener_usuario_por_nombre(name):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE name = %s", (name,))
        usuario = cur.fetchone()
        cur.close()
        return usuario
    
    @staticmethod
    def actualizar_usuario(user_id, username, password):
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE usuarios SET username = %s, password = %s WHERE id = %s", (username, password, user_id))
        mysql.connection.commit()
    
    @staticmethod
    def eliminar_usuario(user_id):
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
        mysql.connection.commit()

# Clase para interactuar con la tabla 'productos'
class Producto:
    @staticmethod
    def obtener_productos():
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nombre, precio, color, talla FROM productos")
        productos = cur.fetchall()
        cur.close()
        return productos

    @staticmethod
    def obtener_producto_por_id(id_producto):
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nombre, precio, color, talla FROM productos WHERE id = %s", (id_producto,))
        producto = cur.fetchone()
        cur.close()
        return producto


class Pedido:
    @staticmethod
    def crear_pedido(usuario, nombre, apellido, dni, cp, calle, numero):
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO pedido(usuario, nombre, apellido, dni, cp, calle, numero)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (usuario, nombre, apellido, dni, cp, calle, numero))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def obtener_pedidos_por_usuario(usuario):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM pedido WHERE usuario = %s", (usuario,))
        pedidos = cur.fetchall()
        cur.close()
        return pedidos
    

class PedidoProducto:
    @staticmethod
    def agregar_producto_a_pedido(pedido_id, producto_id, cantidad):
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO pedido_producto (pedido_id, producto_id, cantidad)
            VALUES (%s, %s, %s)
        """, (pedido_id, producto_id, cantidad))
        mysql.connection.commit()
        cur.close()

    @staticmethod
    def obtener_productos_de_pedido(pedido_id):
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT productos.id, productos.nombre, productos.precio, productos.color, productos.talla, productos.imagen, pedido_producto.cantidad
            FROM pedido_producto
            JOIN productos ON pedido_producto.producto_id = productos.id
            WHERE pedido_producto.pedido_id = %s
        """, (pedido_id,))
        productos = cur.fetchall()
        cur.close()
        return productos
    
# Clase para interactuar con la tabla 'tarjetas'
class Tarjeta:
    @staticmethod
    def agregar_tarjeta(numero, fecha_caducidad, cvv, id_usuario):
        try:
            # Validación básica del número de tarjeta, fecha de caducidad y CVV
            if not numero.isdigit() or len(numero) != 16:
                return jsonify({'success': False, 'message': 'El número de tarjeta debe tener 16 dígitos'}), 400
            if not cvv.isdigit() or len(cvv) != 3:
                return jsonify({'success': False, 'message': 'El CVV debe tener 3 dígitos'}), 400
            
            # Convertir la fecha de caducidad a un formato de fecha completo (YYYY-MM-01)
            try:
                # Mantener la fecha en formato MM-YYYY
                fecha_caducidad_completa = datetime.strptime(fecha_caducidad, '%Y-%m')
                fecha_caducidad = fecha_caducidad_completa.strftime('%m-%Y')  # Guardar en formato MM-YYYY

            except ValueError:
                return jsonify({'success': False, 'message': 'La fecha de caducidad debe tener el formato MM-YYYY'}), 400

            # Insertar una nueva tarjeta en la base de datos
            cur = mysql.connection.cursor()
            cur.execute(""" 
                SELECT * FROM tarjetas WHERE numero = %s AND id_usuario = %s
            """, (numero, id_usuario))
            existing_card = cur.fetchone()
            
            if existing_card:
                return jsonify({'success': False, 'message': 'La tarjeta ya está registrada'}), 400

            # Insertar la tarjeta en la base de datos
            cur.execute("""
                INSERT INTO tarjetas (numero, fecha_caducidad, cvv, id_usuario) 
                VALUES (%s, %s, %s, %s)
            """, (numero, fecha_caducidad, cvv, id_usuario))
            mysql.connection.commit()
            cur.close()
            return jsonify({'success': True, 'message': 'Tarjeta agregada exitosamente'}), 200
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error al agregar la tarjeta: {str(e)}'}), 500
        
    @staticmethod
    def obtener_tarjetas_por_usuario(id_usuario):
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM tarjetas WHERE id_usuario = %s", (id_usuario,))
            tarjetas = cur.fetchall()  # Obtener todas las tarjetas de la base de datos
            cur.close()
            return tarjetas
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error al obtener las tarjetas: {str(e)}'}), 500
