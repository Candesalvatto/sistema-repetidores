import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

# Carga las variables del archivo .env al entorno
load_dotenv()

# Configuración de parámetros de conexión a la base de datos
# (los valores se leen del archivo .env, no se escriben en el código)
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME', 'repetidores'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'auth_plugin': 'mysql_native_password'
}


def obtener_conexion():
    """
    Establece una conexión a la base de datos MySQL utilizando los parámetros de configuración.
    
    """
    try:
        conexion = mysql.connector.connect(**DB_CONFIG)
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos")
            return conexion
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None


def cerrar_conexion(conexion, cursor=None):
    """
    Cierra la conexión a la base de datos y el cursor si se proporciona.
    
    :param conexion: Objeto de conexión a la base de datos.
    :param cursor: (Opcional) Objeto cursor de la base de datos.
    """
    if cursor is not None:
        cursor.close()
    if conexion is not None and conexion.is_connected():
        conexion.close()
        print("Conexión cerrada")