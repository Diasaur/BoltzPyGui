from PyQt5.QtWidgets import QWidget, QScrollArea, QLabel, QVBoxLayout, QHBoxLayout
import boltzmann.gui.config.configuration.widget_specimen as widget_specimen
import boltzmann.gui.config.configuration.widget_grid as widget_time_grid


class Window(QWidget):
    """To Do:

    """

    def __init__(self, main):
        super().__init__()

        # setting specimen window properties
        self.title = 'Configuration'

        # creating widgets
        self.widget_specimen = widget_specimen.Window(main)
        self.widget_time_grid = widget_time_grid.Window(main)

        # setting:

        # creating layout boxes
        self.scroll_area = QScrollArea(self)
        self.scroll_area_content = QWidget()
        self.layout_scroll = QHBoxLayout(self)
        self.layout_main = QVBoxLayout()
        self.layout_h1 = QHBoxLayout()

        # initializing configuration window
        self.init_ui()

    def init_ui(self):

        # setting up scroll area
        self.layout_scroll.addWidget(self.scroll_area)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_area_content)
        self.scroll_area_content.setLayout(self.layout_main)

        # filling layout
        self.layout_main.addWidget(QLabel(self.widget_specimen.title))
        self.layout_main.addWidget(self.widget_specimen)
        self.layout_main.addWidget(self.widget_time_grid)

        # build window
        self.show()
