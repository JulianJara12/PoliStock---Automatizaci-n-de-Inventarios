from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QLineEdit,
    QMessageBox, QInputDialog
)

from services.producto_service import ProductoService
from services.inventario_service import InventarioService
from ui.usuarios_window import UsuariosWindow


class InventarioWindow(QWidget):

    def __init__(self, usuario):
        super().__init__()

        self.usuario = usuario
        self.ventana_usuarios = None

        self.setWindowTitle("Sistema de Inventario")

        layout_principal = QVBoxLayout()

        # TABLA PRODUCTOS
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(6)
        self.tabla.setHorizontalHeaderLabels(
            ["ID", "Código", "Nombre", "Precio", "Stock", "Activo"]
        )

        layout_principal.addWidget(self.tabla)

        # FORM CREAR PRODUCTO
        form_layout = QHBoxLayout()

        self.input_codigo = QLineEdit()
        self.input_codigo.setPlaceholderText("Código")

        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre")

        self.input_precio = QLineEdit()
        self.input_precio.setPlaceholderText("Precio")

        btn_crear = QPushButton("Crear Producto")
        btn_crear.clicked.connect(self.crear_producto)

        btn_eliminar = QPushButton("Eliminar Producto")
        btn_eliminar.clicked.connect(self.eliminar_producto)

        form_layout.addWidget(QLabel("Producto:"))
        form_layout.addWidget(self.input_codigo)
        form_layout.addWidget(self.input_nombre)
        form_layout.addWidget(self.input_precio)
        form_layout.addWidget(btn_crear)
        form_layout.addWidget(btn_eliminar)

        layout_principal.addLayout(form_layout)

        # MOVIMIENTOS
        movimiento_layout = QHBoxLayout()

        self.input_cantidad = QLineEdit()
        self.input_cantidad.setPlaceholderText("Cantidad")

        btn_entrada = QPushButton("Registrar Entrada")
        btn_salida = QPushButton("Registrar Salida")

        btn_entrada.clicked.connect(self.registrar_entrada)
        btn_salida.clicked.connect(self.registrar_salida)

        movimiento_layout.addWidget(QLabel("Cantidad:"))
        movimiento_layout.addWidget(self.input_cantidad)
        movimiento_layout.addWidget(btn_entrada)
        movimiento_layout.addWidget(btn_salida)

        layout_principal.addLayout(movimiento_layout)

        # BOTONES
        btn_actualizar = QPushButton("Actualizar Tabla")
        btn_actualizar.clicked.connect(self.cargar_productos)

        btn_usuarios = QPushButton("Administrar Usuarios")
        btn_usuarios.clicked.connect(self.abrir_usuarios)

        layout_principal.addWidget(btn_actualizar)
        layout_principal.addWidget(btn_usuarios)

        self.setLayout(layout_principal)

        self.cargar_productos()

    # CARGAR PRODUCTOS

    def cargar_productos(self):

        productos = ProductoService.listar_productos()

        self.tabla.setRowCount(len(productos))

        for fila, producto in enumerate(productos):

            self.tabla.setItem(fila, 0, QTableWidgetItem(str(producto.id_producto)))
            self.tabla.setItem(fila, 1, QTableWidgetItem(producto.codigo))
            self.tabla.setItem(fila, 2, QTableWidgetItem(producto.nombre))
            self.tabla.setItem(fila, 3, QTableWidgetItem(str(producto.precio)))
            self.tabla.setItem(fila, 4, QTableWidgetItem(str(producto.stock)))
            self.tabla.setItem(fila, 5, QTableWidgetItem(str(producto.activo)))

    # CREAR PRODUCTO

    def crear_producto(self):

        codigo = self.input_codigo.text()
        nombre = self.input_nombre.text()
        precio = self.input_precio.text()

        if not codigo or not nombre or not precio:
            QMessageBox.warning(self, "Error", "Campos incompletos")
            return

        try:

            ProductoService.crear_producto(
                codigo,
                nombre,
                float(precio)
            )

            QMessageBox.information(self, "Éxito", "Producto creado")

            self.cargar_productos()

        except Exception as e:

            QMessageBox.warning(self, "Error", str(e))

    # PRODUCTO SELECCIONADO

    def obtener_producto_seleccionado(self):

        fila = self.tabla.currentRow()

        if fila == -1:
            return None

        producto_id = int(self.tabla.item(fila, 0).text())

        return producto_id

    # ENTRADA

    def registrar_entrada(self):

        producto_id = self.obtener_producto_seleccionado()

        if producto_id is None:
            QMessageBox.warning(self, "Error", "Seleccione un producto")
            return

        cantidad = int(self.input_cantidad.text())

        InventarioService.registrar_entrada(
            producto_id,
            cantidad,
            self.usuario.id_usuario
        )

        self.cargar_productos()

        
        self.input_cantidad.clear()

    # SALIDA

    def registrar_salida(self):


        producto_id = self.obtener_producto_seleccionado()

        if producto_id is None:
            QMessageBox.warning(self, "Error", "Seleccione un producto")
            return

        cantidad = int(self.input_cantidad.text())

        InventarioService.registrar_salida(
            producto_id,
            cantidad,
            self.usuario.id_usuario
        )

        self.cargar_productos()

        self.input_cantidad.clear()

    # ABRIR USUARIOS

    def abrir_usuarios(self):

        if self.ventana_usuarios is None:

            self.ventana_usuarios = UsuariosWindow()

        self.ventana_usuarios.show()

    # ELIMINAR PRODUCTOS

    def eliminar_producto(self):
        id_producto, ok = QInputDialog.getInt(
            self, "Elimar producto",
            "Ingrese el ID del producto:"
        )

        if not ok:
            return
        try:
            ProductoService.eliminar_producto(id_producto)

            QMessageBox.information(self, "Exito", "Producto eliminado")
            self.cargar_productos()
        
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

        self.cargar_productos