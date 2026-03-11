import psycopg2

def conectar():
    return psycopg2.connect(
        host="localhost",
        database="inventario_db",
        user="postgres",
        password="julian"
    )