from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QLabel, QComboBox, QListWidget, QVBoxLayout,
                             QHBoxLayout, QGridLayout, QListWidgetItem)
import boltzmann.gui.config.configuration.window_specimen_add as spec_add
import boltzmann.gui.config.configuration.window_specimen_edit as spec_edit


class Window(QWidget):
    """To Do:
    -edit more than one specimen at once?
    -LIST: lookup and edit specimen --> new Window and just a List for Specimen?
    -set size policies / resize modes
    -list/items (also see below)
    -other parameters + defaults
    -auto add items(or auto read from file)
    -as Object directly ...
        list:
    GETTING INFO
    add just names and get indices from them to show the rest?
    create seperate species objects? (probably worst - unnecessary data doubling)
    list refreshing instead of adding? - easier for deleting stuff
    does it need to be an item? - possibilities
    first would be cool
    just indices?
    tooltips with info? or new window... message box? - options for existing specimen needed? (like changing)

    """

    def __init__(self, main):
        super().__init__()

        self.cnf = main.cnf

        # setting specimen sub window properties
        self.title = 'Specimen'

        # setting:

        # creating layout boxes
        self.layout_main = QHBoxLayout(self)
        self.layout_buttons = QVBoxLayout()

        # creating objects:
        self.list_specimen = QListWidget()

        self.b_add_specimen = QPushButton('Add Specimen')
        self.b_edit_specimen = QPushButton('Edit Specimen')
        self.b_check = QPushButton('Check Integrity')

        # initializing specimen window
        self.init_ui()

    def init_ui(self):

        # adding objects to boxes
        self.layout_main.addWidget(self.list_specimen)
        self.layout_main.addLayout(self.layout_buttons)

        self.layout_buttons.addWidget(self.b_add_specimen)
        self.layout_buttons.addWidget(self.b_edit_specimen)
        self.layout_buttons.addWidget(self.b_check)
        self.layout_buttons.addStretch(1)

        # list
        self.list_specimen.doubleClicked.connect(self.specimen_edit)

        # add specimen button
        self.b_add_specimen.pressed.connect(self.specimen_add)
        self.b_add_specimen.setAutoDefault(True)

        # edit specimen button
        self.b_edit_specimen.pressed.connect(self.specimen_edit)
        self.b_edit_specimen.setAutoDefault(True)

        # check integrity button
        self.b_check.clicked.connect(self.check_integrity)
        self.b_check.setAutoDefault(True)

        # build window
        # self.show()

    # events:
    def specimen_edit(self):
        self.window_edit = spec_edit.Window(self, self.list_specimen.currentItem().data(QListWidgetItem.UserType))
        self.window_edit.show()

    def check_integrity(self):
        try:
            self.cnf.s.check_integrity()
        except AssertionError:
            self.b_check.setStyleSheet('background-color: rgb(255,0,0)')
        else:
            self.b_check.setStyleSheet('background-color: rgb(0,255,0)')

    def specimen_add(self):
        self.window_add = spec_add.Window(self)
        self.window_add.show()
