from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QLineEdit,
    QMessageBox
)

from services.producto_service import ProductoService
from services.inventario_service import InventarioService


class InventarioWindow(QWidget):

    def __init__(self, usuario):
        super().__init__()

        self.usuario = usuario

        self.setWindowTitle("Sistema de Inventario")

        layout_principal = QVBoxLayout()

        # -------- TABLA DE PRODUCTOS --------
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels(
            ["ID", "Código", "Nombre", "Precio", "Stock"]
        )

        layout_principal.addWidget(self.tabla)

        # -------- FORMULARIO CREAR PRODUCTO --------
        form_layout = QHBoxLayout()

        self.input_codigo = QLineEdit()
        self.input_codigo.setPlaceholderText("Código")

        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre")

        self.input_precio = QLineEdit()
        self.input_precio.setPlaceholderText("Precio")

        btn_crear = QPushButton("Crear Producto")
        btn_crear.clicked.connect(self.crear_producto)

        form_layout.addWidget(QLabel("Nuevo Producto:"))
        form_layout.addWidget(self.input_codigo)
        form_layout.addWidget(self.input_nombre)
        form_layout.addWidget(self.input_precio)
        form_layout.addWidget(btn_crear)

        layout_principal.addLayout(form_layout)

        # -------- MOVIMIENTOS INVENTARIO --------
        movimiento_layout = QHBoxLayout()

        self.input_cantidad = QLineEdit()
        self.input_cantidad.setPlaceholderText("Cantidad")

        btn_entrada = QPushButton("Registrar Entrada")
        btn_salida = QPushButton("Registrar Salida")

        btn_entrada.clicked.connect(self.registrar_entrada)
        btn_salida.clicked.connect(self.registrar_salida)

        movimiento_layout.addWidget(QLabel("Movimiento:"))
        movimiento_layout.addWidget(self.input_cantidad)
        movimiento_layout.addWidget(btn_entrada)
        movimiento_layout.addWidget(btn_salida)

        layout_principal.addLayout(movimiento_layout)

        # -------- BOTÓN ACTUALIZAR --------
        btn_actualizar = QPushButton("Actualizar Tabla")
        btn_actualizar.clicked.connect(self.cargar_productos)

        layout_principal.addWidget(btn_actualizar)

        self.setLayout(layout_principal)

        self.cargar_productos()

    # -------- CARGAR PRODUCTOS --------

    def cargar_productos(self):

        productos = ProductoService.listar_productos()

        self.tabla.setRowCount(len(productos))

        for fila, producto in enumerate(productos):

            self.tabla.setItem(fila, 0, QTableWidgetItem(str(producto.id_producto)))
            self.tabla.setItem(fila, 1, QTableWidgetItem(producto.codigo))
            self.tabla.setItem(fila, 2, QTableWidgetItem(producto.nombre))
            self.tabla.setItem(fila, 3, QTableWidgetItem(str(producto.precio)))
            self.tabla.setItem(fila, 4, QTableWidgetItem(str(producto.stock)))

    # -------- CREAR PRODUCTO --------

    def crear_producto(self):

        codigo = self.input_codigo.text()
        nombre = self.input_nombre.text()
        precio = self.input_precio.text()

        if not codigo or not nombre or not precio:
            QMessageBox.warning(self, "Error", "Campos incompletos")
            return

        try:
            ProductoService.crear_producto(codigo, nombre, float(precio))

            QMessageBox.information(self, "Éxito", "Producto creado")

            self.cargar_productos()

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    # -------- OBTENER PRODUCTO SELECCIONADO --------

    def obtener_producto_seleccionado(self):

        fila = self.tabla.currentRow()

        if fila == -1:
            return None

        producto_id = int(self.tabla.item(fila, 0).text())

        return producto_id

    # -------- REGISTRAR ENTRADA --------

    def registrar_entrada(self):

        producto_id = self.obtener_producto_seleccionado()

        if producto_id is None:
            QMessageBox.warning(self, "Error", "Seleccione un producto")
            return

        cantidad = int(self.input_cantidad.text())

        try:

            InventarioService.registrar_entrada(
                producto_id,
                cantidad,
                self.usuario.id_usuario
            )

            self.cargar_productos()

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    # -------- REGISTRAR SALIDA --------

    def registrar_salida(self):

        producto_id = self.obtener_producto_seleccionado()

        if producto_id is None:
            QMessageBox.warning(self, "Error", "Seleccione un producto")
            return

        cantidad = int(self.input_cantidad.text())

        try:

            InventarioService.registrar_salida(
                producto_id,
                cantidad,
                self.usuario.id_usuario
            )

            self.cargar_productos()

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))