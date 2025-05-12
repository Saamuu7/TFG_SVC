import os

class Config:
    # Credenciales de la base de datos
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'  # Usuario de MySQL
    MYSQL_PASSWORD = 'root'  # Contraseña de MySQL
    MYSQL_DB = 'tienda_online'  # Nombre de la base de datos
    MYSQL_PORT = 3306  # Puerto de MySQL (por defecto)

    # Clave secreta para las sesiones
    SECRET_KEY = os.urandom(24)  # Generar una clave secreta aleatoria
