from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QLabel, QComboBox, QListWidget, QVBoxLayout,
                             QHBoxLayout, QGridLayout, QListWidgetItem)


class Window(QWidget):
    """To Do:
    """

    def __init__(self, parent, specimen):
        super().__init__()

        self.parent = parent
        self.specimen = specimen

        # setting specimen window properties
        self.title = 'Edit Specimen'
        self.width = 400
        self.height = 300
        self.pos_x = 200
        self.pos_y = 350

        # setting:

        # creating layout boxes
        self.layout_main = QVBoxLayout(self)
        self.gLayout_input = QGridLayout()
        self.layout_buttons = QHBoxLayout()

        # creating objects:
        self.tb_mass = QLineEdit()
        self.tb_name = QLineEdit()
        self.cb_color = QComboBox()
        self.list_alpha = [QLineEdit() for i in range(len(self.specimen[4]))]

        self.b_check = QPushButton('Check Integrity')
        self.b_add_spec = QPushButton('Add Specimen')
        self.b_cancel = QPushButton('Cancel')

        # initializing specimen window
        self.init_ui()

    def init_ui(self):

        # layout setup
        self.setWindowTitle(self.title)
        self.setGeometry(self.pos_x, self.pos_y, self.width, self.height)

        self.layout_main.addLayout(self.gLayout_input)
        self.layout_main.addLayout(self.layout_buttons)

        self.gLayout_input.addWidget(QLabel('mass'), 0, 0)
        self.gLayout_input.addWidget(self.tb_mass, 0, 1, 1, len(self.list_alpha))
        self.gLayout_input.addWidget(QLabel('name'), 1, 0)
        self.gLayout_input.addWidget(self.tb_name, 1, 1, 1, len(self.list_alpha))
        self.gLayout_input.addWidget(QLabel('color'), 2, 0)
        self.gLayout_input.addWidget(self.cb_color, 2, 1, 1, len(self.list_alpha))
        self.gLayout_input.addWidget(QLabel('alpha'), 3, 0)
        for i in range(0, len(self.list_alpha)):
            self.gLayout_input.addWidget(self.list_alpha[i], 3, i + 1)

        self.layout_buttons.addWidget(self.b_add_spec)
        self.layout_buttons.addWidget(self.b_check)
        self.layout_buttons.addWidget(self.b_cancel)

        # mass
        self.tb_mass.setToolTip('integer')
        self.tb_mass.setText(str(self.specimen[1]))
        self.tb_mass.returnPressed.connect(self.check_mass)

        # name
        self.tb_name.setText(str(self.specimen[2]))
        self.tb_name.returnPressed.connect(self.check_name)

        # color
        self.cb_color.addItems(self.parent.cnf.s.supported_colors)

        # alpha list
        for i in range(0, len(self.list_alpha)):
            self.list_alpha[i].setText(str(self.specimen[4][i]))
            self.list_alpha[i].returnPressed.connect(self.check_alpha)
            self.list_alpha[i].setToolTip('complicated')

        # add specimen button
        self.b_add_spec.clicked.connect(self.add_spec)
        self.b_add_spec.setAutoDefault(True)

        # check integrity button
        self.b_check.clicked.connect(self.check_integrity)
        self.b_check.setAutoDefault(True)

        # cancel button
        self.b_cancel.pressed.connect(self.cancel)
        self.b_cancel.setAutoDefault(True)

        # build window
        # self.show()

    def refresh_ui(self):

        self.gLayout_input.addWidget(QLabel('mass'), 0, 0)
        self.gLayout_input.addWidget(self.tb_mass, 0, 1, 1, len(self.list_alpha))
        self.gLayout_input.addWidget(QLabel('name'), 1, 0)
        self.gLayout_input.addWidget(self.tb_name, 1, 1, 1, len(self.list_alpha))
        self.gLayout_input.addWidget(QLabel('color'), 2, 0)
        self.gLayout_input.addWidget(self.cb_color, 2, 1, 1, len(self.list_alpha))
        self.gLayout_input.addWidget(QLabel('alpha'), 3, 0)
        for i in range(0, len(self.list_alpha)):
            self.gLayout_input.addWidget(self.list_alpha[i], 3, i + 1)

        self.tb_mass.setStyleSheet('background-color: rgb(255,255,255)')
        self.tb_name.setStyleSheet('background-color: rgb(255,255,255)')
        self.tb_name.setText('Specimen_' + str(self.parent.cnf.s.n))
        for alpha in self.list_alpha:
            alpha.setText('1')
            alpha.setStyleSheet('background-color: rgb(255,255,255)')

    # events
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
        if (self.tb_name.text() not in self.parent.cnf.s.names) & (self.tb_name.text() != ''):
            self.tb_name.setStyleSheet('background-color: rgb(0,255,0)')
            self.cb_color.setFocus(True)
            return True
        elif self.tb_name.text() == '':
            self.tb_name.setText('Specimen_' + str(self.parent.cnf.s.n))
            return False
        else:
            self.tb_name.setStyleSheet('background-color: rgb(255,0,0)')
            return False

    # def check_color(self):
    #     if self.cb_color.count() == 0:
    #         self.cb_color.setStyleSheet('background-color: rgb(255,0,0)')
    #         raise ValueError("All Colors are used, add more.")
    #     else:
    #         return True

    def check_alpha(self):
        for alpha in self.list_alpha:
            alpha.setStyleSheet('background-color: rgb(255,255,255)')
        for i in range(0, len(self.list_alpha)):
            try:
                if isinstance(float(self.list_alpha[i].text()), float):
                    self.list_alpha[i].setStyleSheet('background-color: rgb(0,255,0)')
                else:
                    self.list_alpha[i].setStyleSheet('background-color: rgb(255,0,0)')
                    return False
            except ValueError:
                self.list_alpha[i].setStyleSheet('background-color: rgb(255,0,0)')
                return False
        self.b_add_spec.setFocus(True)
        return True

    def check_integrity(self):
        try:
            self.parent.cnf.s.check_integrity()
        except AssertionError:
            self.b_check.setStyleSheet('background-color: rgb(255,0,0)')
        else:
            self.b_check.setStyleSheet('background-color: rgb(0,255,0)')

    def cancel(self):
        self.destroy()

    def add_spec(self):
        if self.check_mass() & self.check_name() & self.check_alpha():
            # add specimen
            mass = int(self.tb_mass.text())
            name = str(self.tb_name.text())
            color = str(self.cb_color.currentText())
            alpha_list = [float(alpha.text()) for alpha in self.list_alpha if not alpha.isHidden()]

            self.parent.cnf.add_specimen(mass, name=name,
                                         color=color,
                                         alpha_list=alpha_list)

            # add to list
            specimen = QListWidgetItem()
            specimen.setText(name)
            specimen.setData(QListWidgetItem.UserType, [self.parent.list_specimen.count(), mass, name, color, alpha_list])
            self.parent.list_specimen.addItem(specimen)

            # check integrity
            self.check_integrity()

            # resetting boxes
            self.list_alpha.append(QLineEdit())
            self.refresh_ui()
