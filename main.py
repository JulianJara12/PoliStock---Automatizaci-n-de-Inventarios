import sys
from PySide6.QtWidgets import QApplication
from ui.login_window import LoginWindow
from ui.inventario_window import InventarioWindow

ventana_inventario = None


def abrir_inventario(usuario):
    global ventana_inventario

    ventana_inventario = InventarioWindow(usuario)
    ventana_inventario.show()


def main():

    app = QApplication(sys.argv)

    login = LoginWindow(abrir_inventario)
    login.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()