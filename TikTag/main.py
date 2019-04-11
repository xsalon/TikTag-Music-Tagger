import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from TikTagGui.MainWindow import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()
    sys.exit(app.exec_())


