from database.conexion import conectar
from models.usuario import Usuario


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