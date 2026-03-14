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
        self.input_password.setEchoMode(QLineEdit.Password)

        self.input_rolId = QLineEdit()
        self.input_rolId.setPlaceholderText("ID de Rol")


        btn_crear = QPushButton("Crear usuario")
        btn_crear.clicked.connect(self.crear_usuario)

        layout.addWidget(QLabel("Nuevo usuario"))
        layout.addWidget(self.input_usuario)
        layout.addWidget(self.input_password)
        layout.addWidget(self.input_rolId)
        
        layout.addWidget(btn_crear)

        self.setLayout(layout)

    def crear_usuario(self):

     username = self.input_usuario.text()
     password = self.input_password.text()
     rolId = self.input_rolId.text()

     if not username or not password:
        QMessageBox.warning(self, "Error", "Campos vacíos")
        return

     try:
        UsuarioService.crear_usuario(username, password, rolId)

        QMessageBox.information(self, "Correcto", "Usuario creado")

        self.input_usuario.clear()
        self.input_password.clear()
        self.input_rolId.clear()

     except Exception as e:
        QMessageBox.critical(self, "Error", str(e))