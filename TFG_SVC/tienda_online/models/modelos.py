from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_mysqldb import MySQL
from datetime import datetime

# Inicializa Flask y la extensión MySQL
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
        cursor.execute("UPDATE usuarios SET name = %s, password = %s WHERE id = %s", (username, password, user_id))
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

# Clase para interactuar con la tabla 'tarjetas'
class Tarjeta:
    @staticmethod
    def agregar_tarjeta(numero, fecha_caducidad, cvv, id_usuario):
        try:
            # Validación básica del número de tarjeta, fecha de caducidad y CVV
            if not numero.isdigit() or len(numero) != 16:
                return {'success': False, 'message': 'El número de tarjeta debe tener 16 dígitos'}, 400
            if not cvv.isdigit() or len(cvv) != 3:
                return {'success': False, 'message': 'El CVV debe tener 3 dígitos'}, 400
            
            # Convertir la fecha de caducidad a un formato de fecha completo (YYYY-MM-01)
            try:
                # Mantener la fecha en formato MM-YYYY
                fecha_caducidad_completa = datetime.strptime(fecha_caducidad, '%Y-%m')
                fecha_caducidad = fecha_caducidad_completa.strftime('%m-%Y')  # Guardar en formato MM-YYYY
            except ValueError:
                return {'success': False, 'message': 'La fecha de caducidad debe tener el formato MM-YYYY'}, 400

            # Verificar si la tarjeta ya está registrada
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM tarjetas WHERE numero = %s AND id_usuario = %s", (numero, id_usuario))
            existing_card = cur.fetchone()
            if existing_card:
                return {'success': False, 'message': 'La tarjeta ya está registrada'}, 400

            # Insertar la tarjeta en la base de datos
            cur.execute("""
                INSERT INTO tarjetas (numero, fecha_caducidad, cvv, id_usuario) 
                VALUES (%s, %s, %s, %s)
            """, (numero, fecha_caducidad, cvv, id_usuario))
            mysql.connection.commit()
            cur.close()
            return {'success': True, 'message': 'Tarjeta agregada exitosamente'}, 200
        except Exception as e:
            return {'success': False, 'message': f'Error al agregar la tarjeta: {str(e)}'}, 500
        
    @staticmethod
    def obtener_tarjetas_por_usuario(id_usuario):
        try:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM tarjetas WHERE id_usuario = %s", (id_usuario,))
            tarjetas = cur.fetchall()  # Obtener todas las tarjetas de la base de datos
            cur.close()
            return tarjetas
        except Exception as e:
            return {'success': False, 'message': f'Error al obtener las tarjetas: {str(e)}'}, 500

class Pago:
    @staticmethod
    def agregar_pago(id_usuario, nombre, correo, direccion):
        try:
            # Insertamos un nuevo pago en la base de datos
            fecha_pago = datetime.now()
            cur = mysql.connection.cursor()
            cur.execute("""
                INSERT INTO pagos (id_usuario, nombre, correo, direccion, fecha) 
                VALUES (%s, %s, %s, %s, %s)
            """, (id_usuario, nombre, correo, direccion, fecha_pago))
            mysql.connection.commit()

            # Obtener el ID del pago recién insertado
            id_pago = cur.lastrowid
            cur.close()

            # Devolvemos el ID del pago insertado junto con un mensaje de éxito
            return {'success': True, 'message': 'Pago registrado exitosamente', 'id_pago': id_pago}, 200
        except Exception as e:
            # En caso de error, devolvemos un mensaje de error
            return {'success': False, 'message': f'Error al registrar el pago: {str(e)}'}, 500

    @staticmethod
    def obtener_pagos_por_usuario(id_usuario):
        try:
            # Obtiene todos los pagos realizados por un usuario
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM pagos WHERE id_usuario = %s", (id_usuario,))
            pagos = cur.fetchall()  # Obtener todos los pagos de un usuario
            cur.close()
            return pagos
        except Exception as e:
            return {'success': False, 'message': f'Error al obtener los pagos: {str(e)}'}, 500

    @staticmethod
    def obtener_pago_por_id(id_pago):
        try:
            # Obtiene los detalles de un pago específico
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM pagos WHERE id = %s", (id_pago,))
            pago = cur.fetchone()
            cur.close()
            return pago
        except Exception as e:
            return {'success': False, 'message': f'Error al obtener el pago: {str(e)}'}, 500

