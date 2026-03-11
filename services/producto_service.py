from database.conexion import conectar
from models.producto import Producto


class ProductoService:

    @staticmethod
    def listar_productos():

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
        SELECT id_producto, codigo, nombre, precio, stock
        FROM productos
        """)

        filas = cursor.fetchall()

        productos = []

        for fila in filas:
            producto = Producto(*fila)
            productos.append(producto)

        cursor.close()
        conexion.close()

        return productos


    @staticmethod
    def crear_producto(codigo, nombre, precio):

        conexion = conectar()
        cursor = conexion.cursor()

        query = """
        INSERT INTO productos (codigo, nombre, precio)
        VALUES (%s,%s,%s)
        """

        cursor.execute(query, (codigo, nombre, precio))

        conexion.commit()

        cursor.close()
        conexion.close()