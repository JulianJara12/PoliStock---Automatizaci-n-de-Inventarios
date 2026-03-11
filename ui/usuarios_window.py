from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from services.usuario_service import UsuarioService


class UsuariosWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gestión de Usuarios")

        layout = QVBoxLayout()

        self.input_usuario = QLineEdit()
        self.input_usuario.setPlaceholderText("Nombre de usuario")

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Contraseña")

        btn_crear = QPushButton("Crear usuario")
        btn_crear.clicked.connect(self.crear_usuario)

        layout.addWidget(QLabel("Nuevo usuario"))
        layout.addWidget(self.input_usuario)
        layout.addWidget(self.input_password)
        layout.addWidget(btn_crear)

        self.setLayout(layout)

    def crear_usuario(self):

        username = self.input_usuario.text()
        password = self.input_password.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Campos vacíos")
            return

        UsuarioService.crear_usuario(username, password)

        QMessageBox.information(self, "Correcto", "Usuario creado")