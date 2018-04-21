from PyQt5.QtWidgets import QWidget, QTabWidget
import boltzmann.gui.config.config_ui as config_ui


class TabWidget(QTabWidget):

    """ To Do:
    -2 config - init, cf with subtabs?
    (cnf: spec, grid, svgrid)
    """

    def __init__(self, main):
        super(QWidget, self).__init__()

        # setting tab properties
        self.width = main.width
        self.height = main.height

        # create config
        self.tab_config = config_ui.Window(main)

        # initializing tab
        self.init_ui()

    def init_ui(self):

        self.resize(self.width, self.height)

        self.addTab(self.tab_config, self.tab_config.title)
