from PySide6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QPushButton, QLabel
from services.usuario_service import UsuarioService


class LoginWindow(QDialog):

    def __init__(self, abrir_inventario):
        super().__init__()

        self.abrir_inventario = abrir_inventario
        self.usuario_service = UsuarioService()

        layout = QVBoxLayout()

        self.usuario_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        boton = QPushButton("Ingresar")
        boton.clicked.connect(self.login)

        layout.addWidget(QLabel("Usuario"))
        layout.addWidget(self.usuario_input)

        layout.addWidget(QLabel("Contraseña"))
        layout.addWidget(self.password_input)

        layout.addWidget(boton)

        self.setLayout(layout)

    def login(self):

        usuario = self.usuario_input.text()
        password = self.password_input.text()

        resultado = self.usuario_service.login(usuario, password)

        if resultado:
            self.abrir_inventario(usuario)
            self.close()