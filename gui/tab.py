from PyQt5.QtWidgets import QWidget, QTabWidget
import boltzmann.gui.config.specimen as specimen
import boltzmann.gui.config.grid as grid
import boltzmann.gui.config.svgrid as svgrid


class TabWidget(QTabWidget):

    """ To Do:
    -2 config - init, cf with subtabs?
    (cnf: spec, grid, svgrid)
    """

    def __init__(self, parent, cnf):
        super(QWidget, self).__init__(parent)

        # setting tab properties
        self.width = parent.width
        self.height = parent.height

        # create config
        self.tSpecimen = specimen.Window(cnf)
        self.tGrid = grid.Window(cnf)
        self.tSVGrid = svgrid.Window(cnf)

        # initializing tab
        self.init_ui()

    def init_ui(self):

        self.resize(self.width, self.height)

        self.addTab(self.tSpecimen, 'Specimen')
        self.addTab(self.tGrid, 'Grid')
        self.addTab(self.tSVGrid, 'SVGrid')
