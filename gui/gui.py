import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import boltzmann.gui.tab as tab
import boltzmann.configuration as b_cnf


class WMain(QMainWindow):

    """To Do:
    -swap to Box/Grid Layout for relative sizechanges
    -swap to single files for widgets (not everything here!...probably...)
    -config + initialization (2 config with subtabs?)
    """

    def __init__(self, cnf):
        super().__init__()

        # setting main window properties
        self.title = 'Main Window'
        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 600
        self.cnf = cnf

        # creating main window widgets
        self.tabWidget = tab.TabWidget(self)

        # initializing gui
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.setCentralWidget(self.tabWidget)

        self.show()


config = b_cnf.Configuration()

app = QApplication(sys.argv)
ex = WMain(config)

sys.exit(app.exec_())
