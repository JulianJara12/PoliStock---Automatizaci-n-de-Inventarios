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
        
        conexion = conectar()
        cursor = conexion.cursor()

        query = """
        INSERT INTO usuarios (username, password_hash, rol_id)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (username,password, rolId))

        conexion.commit()
        cursor.close()
        conexion.close()

    @staticmethod
    def eliminar_usuario(id_usuario):

        conexion = conectar()
        cursor = conexion.cursor()

        query = """
        DELETE FROM usuarios
        WHERE id_usuario = %s
        """
        cursor.execute(query,(id_usuario,))
        if cursor.rowcount == 0:
            raise Exception ("No existe un usuario con ese ID")
        
        conexion.commit()
        cursor.close()
        conexion.close()