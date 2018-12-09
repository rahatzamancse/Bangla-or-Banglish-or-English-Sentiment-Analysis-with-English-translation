import sys
from PyQt5.QtWidgets import QApplication
from MainWindow import MainWindow


def main():
    app = QApplication(sys.argv)
    main_window = MainWindow()
    DARK_STYLE = False

    if DARK_STYLE:
        import qdarkstyle
        app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    main_window.show()
    sys.exit(app.exec_())


main()
