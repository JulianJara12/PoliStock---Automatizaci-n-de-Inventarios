from database.conexion import conectar


class InventarioService:

    @staticmethod
    def registrar_entrada(producto_id, cantidad, usuario_id):

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("""
        INSERT INTO movimientos(producto_id, tipo, cantidad, usuario_id)
        VALUES (%s,'entrada',%s,%s)
        """, (producto_id, cantidad, usuario_id))

        cursor.execute("""
        UPDATE productos
        SET stock = stock + %s
        WHERE id_producto = %s
        """, (cantidad, producto_id))

        conexion.commit()

        cursor.close()
        conexion.close()


    @staticmethod
    def registrar_salida(producto_id, cantidad, usuario_id):

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT stock FROM productos WHERE id_producto=%s",
            (producto_id,)
        )

        stock = cursor.fetchone()[0]

        if cantidad > stock:
            raise Exception("Stock insuficiente")

        cursor.execute("""
        INSERT INTO movimientos(producto_id, tipo, cantidad, usuario_id)
        VALUES (%s,'salida',%s,%s)
        """, (producto_id, cantidad, usuario_id))

        cursor.execute("""
        UPDATE productos
        SET stock = stock - %s
        WHERE id_producto=%s
        """, (cantidad, producto_id))

        conexion.commit()

        cursor.close()
        conexion.close()