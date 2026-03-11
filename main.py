import sys
from PySide6.QtWidgets import QApplication
from ui.login_window import LoginWindow
from ui.inventario_window import InventarioWindow


def abrir_inventario(usuario):

    ventana = InventarioWindow(usuario)
    ventana.show()


def main():

    app = QApplication(sys.argv)

    login = LoginWindow(abrir_inventario)
    login.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()