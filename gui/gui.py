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

    def __init__(self):
        super().__init__()

        # setting main window properties
        self.title = 'Main Window'
        self.left = 0
        self.top = 0
        self.width = 1000
        self.height = 600

        # creating main window widgets
        self.tabWidget = tab.TabWidget(self, cnf)

        # initializing gui
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.setCentralWidget(self.tabWidget)

        self.show()


cnf = b_cnf.Configuration()

app = QApplication(sys.argv)
ex = WMain()

sys.exit(app.exec_())
