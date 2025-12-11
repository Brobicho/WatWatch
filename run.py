from PySide6.QtWidgets import QApplication
from gui import App


if __name__ == "__main__":
    app = QApplication([])
    gui = App()
    gui.resize(450, 700)
    gui.show()
    app.exec()
