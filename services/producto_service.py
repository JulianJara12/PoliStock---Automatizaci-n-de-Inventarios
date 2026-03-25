from database.conexion import conectar
from models.producto import Producto


class ProductoService:

    @staticmethod
    def listar_productos():

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
        SELECT id_producto, codigo, nombre, precio, stock, activo
        FROM productos
        WHERE activo = TRUE
        ORDER BY id_producto
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
    def crear_producto(codigo, nombre, precio, cantidad):

        conexion = conectar()
        cursor = conexion.cursor()

        query = """
        INSERT INTO productos (codigo, nombre, precio, stock)
        VALUES (%s,%s,%s,%s)
        """

        cursor.execute(query, (codigo, nombre, precio, cantidad))

        conexion.commit()

        cursor.close()
        conexion.close()

    @staticmethod
    def eliminar_producto(id_producto):

        conexion = conectar()
        cursor = conexion.cursor()

        try:

         cursor.execute("""
                UPDATE productos
                SET activo = FALSE
                WHERE id_producto = %s 
         """, (id_producto,))

         if cursor.rowcount == 0:
            raise Exception("No existe un producto con ese ID")

         conexion.commit()

        except Exception as e:
          conexion.rollback()
          print("Error:", e)
          raise

        finally:

         cursor.close()
         conexion.close()