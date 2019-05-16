import sys
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow
from TikTagGui.MainWindow import MainWindow

if __name__ == '__main__':
    with open('tiktag.log', 'w'):
        pass
    logging.basicConfig(filename='tiktag.log', format='%(asctime)s %(levelname)s : %(message)s', level=logging.INFO)
    logging.info('TikTag has started!')
    app = QApplication(sys.argv)
    myapp = MainWindow()
    myapp.show()
    logging.info('TikTag has finished!')
    sys.exit(app.exec_())


