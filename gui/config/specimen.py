from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QLabel, QComboBox, QListWidget, QVBoxLayout,
                             QHBoxLayout, QGridLayout)


class Window(QWidget):
    """To Do:
    - dictionary
    - alpha - cast in list, or add separately
    -cnf or parent?
    -list/items (also see below)
    -out of colors problem (get that there are no items in cb_color)
    -other parameters + defaults
    -auto add items(or auto read from file)
    -in specimen tab(layout)
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

    def __init__(self, cnf):
        super().__init__()

        self.cnf = cnf

        # setting specimen window properties
        self.title = 'Specimen'

        # setting:

        # creating layout boxes
        self.g_input = QGridLayout()
        self.vb_input = QVBoxLayout()
        self.vb_list = QVBoxLayout()
        self.hb = QHBoxLayout()

        # creating objects:
        self.lb_mass = QLabel('mass', self)
        self.tb_mass = QLineEdit(self)
        self.lb_name = QLabel('name', self)
        self.tb_name = QLineEdit(self)
        self.lb_color = QLabel('color', self)
        self.cb_color = QComboBox(self)
        self.lb_alpha = QLabel('alpha_list', self)
        self.tb_alpha = QLineEdit(self)

        self.list_spc = QListWidget(self)

        self.b_check = QPushButton('Check Integrity', self)
        self.b_add_spec = QPushButton('Add Specimen', self)

        # initializing specimen window
        self.init_ui()

    def init_ui(self):

        # adding objects to boxes
        self.g_input.addWidget(self.lb_mass, 0, 1)
        self.g_input.addWidget(self.tb_mass, 0, 1)
        self.g_input.addWidget(self.lb_name, 1, 0)
        self.g_input.addWidget(self.tb_name, 1, 1)
        self.g_input.addWidget(self.lb_color, 2, 0)
        self.g_input.addWidget(self.cb_color, 2, 1)
        self.g_input.addWidget(self.lb_alpha, 3, 0)
        self.g_input.addWidget(self.tb_alpha, 3, 1)

        self.vb_input.addLayout(self.g_input)
        self.vb_input.addStretch(1)
        self.vb_input.addWidget(self.b_check)

        self.vb_list.addWidget(self.list_spc)
        self.vb_list.addWidget(self.b_add_spec)

        self.hb.addLayout(self.vb_input)
        self.hb.addLayout(self.vb_list)

        self.setLayout(self.hb)

        # mass
        self.tb_mass.setToolTip('integer')
        self.tb_mass.setText('1')
        self.tb_mass.returnPressed.connect(self.check_mass)

        # name
        self.tb_name.setText('Specimen_' + str(self.cnf.s.n))
        self.tb_name.returnPressed.connect(self.check_name)

        # color
        self.cb_color.addItems(self.cnf.s.supported_colors)

        # alpha list
        self.tb_alpha.setText('[0]')
        self.tb_alpha.setToolTip('list of numbers >=0, currently evaluated')
        self.tb_alpha.returnPressed.connect(self.check_alpha)

        # check integrity button
        self.b_check.clicked.connect(self.check_integrity)
        self.b_check.setAutoDefault(True)

        # add specimen button
        self.b_add_spec.clicked.connect(self.add_spec)
        self.b_add_spec.setAutoDefault(True)

        # list

        # build window
        self.show()

    # events:
    def check_mass(self):
        try:
            if isinstance(int(self.tb_mass.text()), int):
                self.tb_mass.setStyleSheet('background-color: rgb(0,255,0)')
                self.tb_name.setFocus(True)
                return True
            else:
                self.tb_mass.setStyleSheet('background-color: rgb(255,0,0)')
                return False
        except ValueError:
            self.tb_mass.setStyleSheet('background-color: rgb(255,0,0)')
            return False

    def check_name(self):
        if (self.tb_name.text() not in self.cnf.s.names) & (self.tb_name.text() != ''):
            self.tb_name.setStyleSheet('background-color: rgb(0,255,0)')
            self.cb_color.setFocus(True)
            return True
        elif self.tb_name.text() == '':
            self.tb_name.setText('Specimen_' + str(self.cnf.s.n))
            return False
        else:
            self.tb_name.setStyleSheet('background-color: rgb(255,0,0)')
            return False

    def check_color(self):
        if self.cb_color.count() == 0:
            self.cb_color.setStyleSheet('background-color: rgb(255,0,0)')
            raise ValueError("All Colors are used, add more.")
        else:
            return True

    def check_alpha(self):
        if self.tb_alpha.text() == '':
            self.tb_alpha.setText('[0' + ',0' * self.cnf.s.n + ']')
        alpha_input = eval(self.tb_alpha.text())
        if alpha_input == '':
            self.tb_alpha.setStyleSheet('background-color: rgb(255,0,0)')
            return False
        if type(alpha_input) is list:
            if all([type(x) in [int, float] and x >= 0 for x in alpha_input]) & (len(alpha_input) == (self.cnf.s.n+1)):
                self.tb_alpha.setStyleSheet('background-color: rgb(0,255,0)')
                return True
            else:
                self.tb_alpha.setStyleSheet('background-color: rgb(255,0,0)')
                return False
        else:
            self.tb_alpha.setStyleSheet('background-color: rgb(255,0,0)')
            return False

    def check_integrity(self):
        try:
            self.cnf.s.check_integrity()
        except AssertionError:
            self.b_check.setStyleSheet('background-color: rgb(255,0,0)')
        else:
            self.b_check.setStyleSheet('background-color: rgb(0,255,0)')

    def add_spec(self):
        if self.check_mass() & self.check_name() & self.check_color() & self.check_alpha():
            # add specimen
            self.cnf.add_specimen(int(self.tb_mass.text()), name=str(self.tb_name.text()),
                                  color=str(self.cb_color.currentText()),
                                  alpha_list=eval(self.tb_alpha.text()))

            # add to list
            self.list_spc.addItem(self.tb_name.text())

            # check integrity
            self.check_integrity()

            # resetting boxes
            self.tb_mass.setStyleSheet('background-color: rgb(255,255,255)')
            self.tb_name.setStyleSheet('background-color: rgb(255,255,255)')
            self.tb_name.setText('Specimen_' + str(self.cnf.s.n))
            self.cb_color.removeItem(self.cb_color.currentIndex())
            self.tb_alpha.setText('[0' + ',0' * self.cnf.s.n + ']')

            self.cnf.s.print()
