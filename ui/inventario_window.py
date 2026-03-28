from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem,
    QPushButton, QLabel, QLineEdit,
    QMessageBox, QInputDialog, QDialog
)

from datetime import datetime

from services.producto_service import ProductoService
from services.inventario_service import InventarioService
from ui.usuarios_window import UsuariosWindow
from fpdf import FPDF


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

        btn_historial_movimientos = QPushButton("Historial Movimientos")
        btn_historial_movimientos.clicked.connect(self.historial_movimientos)

        btn_reporte_inventario = QPushButton("Generar Reporte")
        btn_reporte_inventario.clicked.connect(lambda: self.generar_pdf_inventario(self.tabla))

        layout_principal.addWidget(btn_actualizar)
        layout_principal.addWidget(btn_usuarios)
        layout_principal.addWidget(btn_historial_movimientos)
        layout_principal.addWidget(btn_reporte_inventario)

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
        cantidad = self.input_cantidad.text()

        if not codigo or not nombre or not precio or not cantidad:
            QMessageBox.warning(self, "Error", "Campos incompletos")
            return

        try:

            ProductoService.crear_producto(
                codigo,
                nombre,
                float(precio),
                cantidad
            )

            QMessageBox.information(self, "Éxito", "Producto creado")

            self.cargar_productos()

            self.input_codigo.clear()
            self.input_nombre.clear()
            self.input_precio.clear()
            self.input_cantidad.clear()

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
    
    def historial_movimientos(self):

     dialogo = QDialog(self)
     dialogo.setWindowTitle("Historial de movimientos")
     dialogo.resize(700, 500)

     layout = QVBoxLayout()

     tabla = QTableWidget()
     movimientos = InventarioService.obtener_movimientos()

     tabla.setRowCount(len(movimientos))
     tabla.setColumnCount(6)
     tabla.setHorizontalHeaderLabels(["ID", "Producto", "Tipo", "Cantidad", "Usuario", "Fecha"])

     for fila_idx, fila in enumerate(movimientos):
         for col_idx, valor in enumerate(fila):
             
             if isinstance(valor,datetime):
                valor = valor.strftime("%Y-%m-%d %H:%M")

             tabla.setItem(fila_idx, col_idx, QTableWidgetItem(str(valor)))

     btn_pdf = QPushButton("generar pdf")
     btn_pdf.clicked.connect(lambda: self.generar_pdf(tabla))

     btn_salir = QPushButton("Cerrar")
     btn_salir.clicked.connect(dialogo.close)

     layout.addWidget(tabla)
     layout.addWidget(btn_pdf)
     layout.addWidget(btn_salir)

     dialogo.setLayout(layout)

     dialogo.exec_()


    def generar_pdf(self, tabla):
        pdf = FPDF(orientation="L", unit="mm", format="A4")
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Reporte de Historial de Movimientos", ln=True, align="C")
        pdf.ln(5)

        anchos = [15, 60, 30, 20, 40, 40]  


        pdf.set_font("Arial", "B", 12)
        for col in range(tabla.columnCount()):
            pdf.cell(anchos[col], 10, tabla.horizontalHeaderItem(col).text(), border=1, align="C")
        pdf.ln()

        pdf.set_font("Arial", "", 11)
        for fila in range(tabla.rowCount()):
            y_inicio = pdf.get_y()  # Posición vertical al inicio de la fila
            x_inicio = pdf.get_x()  # Posición horizontal al inicio
            max_y = y_inicio

        # Primero dibujamos cada celda con multi_cell
            for col in range(tabla.columnCount()):
                item = tabla.item(fila, col)
                texto = item.text() if item else ""
            
            # Guardamos posición para cada celda
                pdf.set_xy(x_inicio, y_inicio)
                pdf.multi_cell(anchos[col], 7, texto, border=1)
            
            # Calculamos hasta dónde llegó esta celda verticalmente
                if pdf.get_y() > max_y:
                    max_y = pdf.get_y()
            
            # Avanzamos la posición horizontal para la siguiente celda
                x_inicio += anchos[col]

        # Ajustamos el cursor para la siguiente fila
            pdf.set_y(max_y)

    # Guardar PDF en la carpeta actual
        pdf.output("reporte_historial.pdf")
        print("PDF generado correctamente!")


    def generar_pdf_inventario(self, tabla):
        pdf = FPDF(orientation="L", unit="mm", format="A4")  # Horizontal
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Reporte de Inventario Actual", ln=True, align="C")
        pdf.ln(5)

    # Anchos personalizados para cada columna (ajusta si necesitas más espacio)
        anchos = [20, 40, 60, 30, 25, 25]  # ID, Código, Nombre, Precio, Stock, Activo

    # --- Cabecera de tabla ---
        pdf.set_font("Arial", "B", 12)
        for col in range(tabla.columnCount()):
            pdf.cell(anchos[col], 10, tabla.horizontalHeaderItem(col).text(), border=1, align="C")
        pdf.ln()

    # --- Filas de datos ---
        pdf.set_font("Arial", "", 11)
        for fila in range(tabla.rowCount()):
            y_inicio = pdf.get_y()
            x_inicio = pdf.get_x()
            max_y = y_inicio

            for col in range(tabla.columnCount()):
                item = tabla.item(fila, col)
                texto = item.text() if item else ""
                pdf.set_xy(x_inicio, y_inicio)
                pdf.multi_cell(anchos[col], 7, texto, border=1)
                if pdf.get_y() > max_y:
                    max_y = pdf.get_y()
                x_inicio += anchos[col]

            pdf.set_y(max_y)

    # Guardar PDF
        pdf.output("reporte_inventario.pdf")
        print("PDF de inventario generado correctamente!")  