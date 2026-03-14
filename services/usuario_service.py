from database.conexion import conectar
from models.usuario import Usuario
import bcrypt

class UsuarioService:

    @staticmethod
    def login(username, password):

        conexion = conectar()
        cursor = conexion.cursor()

        query = """
        SELECT id_usuario, username, rol_id
        FROM usuarios
        WHERE username=%s AND password_hash=%s
        """

        cursor.execute(query, (username, password))

        fila = cursor.fetchone()

        cursor.close()
        conexion.close()

        if fila:
            return Usuario(*fila)

        return None
    
    @staticmethod
    def crear_usuario(username, password, rolId):
        
        print ("entro al service")

        conexion = conectar()
        cursor = conexion.cursor()

        #password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        query = """
        INSERT INTO usuarios (username, password_hash, rol_id)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (username,password, rolId))

        conexion.commit()
        print ("insert ejecutado")
        cursor.close()
        conexion.close()
