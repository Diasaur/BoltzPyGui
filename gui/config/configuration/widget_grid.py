from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton


class Window(QWidget):

    """ To Do:
    -deactivate position grid... if n < 2 ?
    -check if grid setting went right --> green button
    -big grid layout for lining up titles
    """

    def __init__(self, main):
        super().__init__()

        self.cnf = main.cnf

        # setting grid sub window properties
        self.title = 'Time and Grids'

        # setting:

        # creating layout boxes
        self.layout_main = QHBoxLayout(self)
        self.layout_time = QVBoxLayout()
        self.gLayout_time_input = QGridLayout()
        self.layout_position = QVBoxLayout()
        self.gLayout_position_input = QGridLayout()
        self.layout_velocity = QVBoxLayout()
        self.gLayout_velocity_input = QGridLayout()

        # creating objects:
        # time grid
        self.tb_time_max = QLineEdit()
        self.tb_time_steps = QLineEdit()
        self.tb_time_calculations = QLineEdit()
        self.b_time = QPushButton('set timegrid')

        # position grid
        self.tb_position_dimension = QLineEdit()
        self.b_position_dimension = QPushButton('set')
        self.tb_position_points = [QLineEdit() for i in range(0,3)]
        self.tb_position_stepsize = QLineEdit()
        self.b_position_set = QPushButton('set positiongrid')

        # velocity grid
        self.tb_velocity_dimension = QLineEdit()
        self.tb_velocity_axispoints = QLineEdit()
        self.tb_velocity_max = QLineEdit()
        self.b_velocity_set = QPushButton('set velocitygrid')

        # initializing specimen window
        self.init_ui()

    def init_ui(self):

        # adding objects to boxes
        self.layout_main.addLayout(self.layout_time)
        self.layout_main.addLayout(self.layout_position)
        self.layout_main.addLayout(self.layout_velocity)

        # time layout
        self.layout_time.addWidget(QLabel('time grid'))
        self.layout_time.addLayout(self.gLayout_time_input)
        self.gLayout_time_input.addWidget(QLabel('max time'), 0, 0)
        self.gLayout_time_input.addWidget(self.tb_time_max, 0, 1)
        self.gLayout_time_input.addWidget(QLabel('time steps'), 1, 0)
        self.gLayout_time_input.addWidget(self.tb_time_steps, 1, 1)
        self.gLayout_time_input.addWidget(QLabel('calculations/step'), 2, 0)
        self.gLayout_time_input.addWidget(self.tb_time_calculations, 2, 1)
        self.gLayout_time_input.addWidget(self.b_time, 3, 0, 1, 2)

        # position layout
        self.layout_position.addWidget(QLabel('position grid'))
        self.layout_position.addLayout(self.gLayout_position_input)
        self.gLayout_position_input.addWidget(QLabel('dimension'), 0, 0)
        self.gLayout_position_input.addWidget(self.tb_position_dimension, 0, 1, 1, 2)
        self.gLayout_position_input.addWidget(self.b_position_dimension, 0, 3)
        self.gLayout_position_input.addWidget(QLabel('points'), 1, 0)
        for i in range(0, len(self.tb_position_points)):
            self.gLayout_position_input.addWidget(self.tb_position_points[i], 1, i+1)
        self.gLayout_position_input.addWidget(QLabel('stepsize'), 2, 0)
        self.gLayout_position_input.addWidget(self.tb_position_stepsize, 2, 1, 1, 3)
        self.gLayout_position_input.addWidget(self.b_position_set, 3, 0, 1, 4)

        # velocity layout
        self.layout_velocity.addWidget(QLabel('velocity grid'))
        self.layout_velocity.addLayout(self.gLayout_velocity_input)
        self.gLayout_velocity_input.addWidget(QLabel('dimension'), 0 ,0)
        self.gLayout_velocity_input.addWidget(self.tb_velocity_dimension, 0, 1)
        self.gLayout_velocity_input.addWidget(QLabel('axispoints'), 1, 0)
        self.gLayout_velocity_input.addWidget(self.tb_velocity_axispoints)
        self.gLayout_velocity_input.addWidget(QLabel('maximum'), 2, 0)
        self.gLayout_velocity_input.addWidget(self.tb_velocity_max, 2, 1)
        self.gLayout_velocity_input.addWidget(self.b_velocity_set, 3, 0, 1, 2)

        # time setup
        self.tb_time_max.setText('1')
        self.tb_time_max.returnPressed.connect(self.check_time_max)
        self.tb_time_steps.setText('101')
        self.tb_time_steps.returnPressed.connect(self.check_time_steps)
        self.tb_time_calculations.setText('1')
        self.tb_time_calculations.returnPressed.connect(self.check_time_calculations)
        self.b_time.pressed.connect(self.set_time)
        self.b_time.setAutoDefault(True)

        # position setup
        self.tb_position_dimension.setText('1')
        self.tb_position_dimension.returnPressed.connect(self.set_dimension)
        self.b_position_dimension.pressed.connect(self.set_dimension)
        self.b_position_dimension.setAutoDefault(True)
        [self.tb_position_points[i].setText('101') for i in range(3)]
        [self.tb_position_points[i].returnPressed.connect(self.check_position_points) for i in range(3)]
        [self.tb_position_points[i].setHidden(True) for i in range(3) if i > 0]
        self.tb_position_stepsize.setText('1')
        self.tb_position_stepsize.returnPressed.connect(self.check_position_stepsize)
        self.b_position_set.pressed.connect(self.set_position)

    # events
    # set functions

    def set_time(self):
        if self.check_time_max() & self.check_time_steps() & self.check_time_calculations():
            time_max = int(self.tb_time_max.text())
            time_steps = int(self.tb_time_steps.text())
            time_calculations = int(self.tb_time_calculations.text())
            self.cnf.configure_time(time_max, time_steps, time_calculations)

    def set_dimension(self):
        if not self.check_position_dimension():
            return
        for i in range(3):
            if i < int(self.tb_position_dimension.text()):
                self.tb_position_points[i].setHidden(False)
            else:
                self.tb_position_points[i].setHidden(True)

    def set_position(self):
        if self.check_position_dimension() & self.check_position_points() & self.check_position_stepsize():
            position_dimension = int(self.tb_position_dimension.text())
            position_points_per_dimension = [int(self.tb_position_points[i].text()) for i in range(position_dimension)]
            position_stepsize = int(self.tb_position_stepsize.text())
            self.cnf.configure_position_space(position_dimension, position_points_per_dimension, position_stepsize)

    # check functions
    def check_time_max(self):
        try:
            if isinstance(int(self.tb_time_max.text()), int):
                if int(self.tb_time_max.text()) > 0:
                    self.tb_time_max.setStyleSheet('background-color: rgb(0,255,0)')
                    return True
                else:
                    self.tb_time_max.setStyleSheet('background-color: rgb(255,0,0)')
                    return False
            else:
                self.tb_time_max.setStyleSheet('background-color: rgb(255,0,0)')
                return False
        except ValueError:
            self.tb_time_max.setStyleSheet('background-color: rgb(255,0,0)')
            return False

    def check_time_steps(self):
        try:
            if isinstance(int(self.tb_time_steps.text()), int):
                if int(self.tb_time_steps.text()) > 0:
                    self.tb_time_steps.setStyleSheet('background-color: rgb(0,255,0)')
                    return True
                else:
                    self.tb_time_steps.setStyleSheet('background-color: rgb(255,0,0)')
                    return False
            else:
                self.tb_time_steps.setStyleSheet('background-color: rgb(255,0,0)')
                return False
        except ValueError:
            self.tb_time_steps.setStyleSheet('background-color: rgb(255,0,0)')
            return False

    def check_time_calculations(self):
        try:
            if isinstance(int(self.tb_time_calculations.text()), int):
                if int(self.tb_time_calculations.text()) > 0:
                    self.tb_time_calculations.setStyleSheet('background-color: rgb(0,255,0)')
                    return True
                else:
                    self.tb_time_calculations.setStyleSheet('background-color: rgb(255,0,0)')
                    return False
            else:
                self.tb_time_calculations.setStyleSheet('background-color: rgb(255,0,0)')
                return False
        except ValueError:
            self.tb_time_calculations.setStyleSheet('background-color: rgb(255,0,0)')
            return False

    def check_position_dimension(self):
        try:
            if isinstance(int(self.tb_position_dimension.text()), int):
                if int(self.tb_position_dimension.text()) in {1, 2, 3}:
                    self.tb_position_dimension.setStyleSheet('background-color: rgb(0,255,0)')
                    return True
                else:
                    self.tb_position_dimension.setStyleSheet('background-color: rgb(255,0,0)')
                    return False
        except ValueError:
            self.tb_position_dimension.setStyleSheet('background-color: rgb(255,0,0)')
            return False

    def check_position_points(self):

        for points in self.tb_position_points:
            points.setStyleSheet('background-color: rgb(255,255,255)')

        if self.check_position_dimension():
            for i in range(int(self.tb_position_dimension.text())):
                try:
                    if isinstance(int(self.tb_position_points[i].text()), int):
                        if int(self.tb_position_points[i].text()) > 0:
                            self.tb_position_points[i].setStyleSheet('background-color: rgb(0,255,0)')
                    else:
                        self.tb_position_points[i].setStyleSheet('background-color: rgb(255,0,0)')
                        return False
                except ValueError:
                    self.tb_position_points[i].setStyleSheet('background-color: rgb(255,0,0)')
                    return False
            return True

    def check_position_stepsize(self):
        try:
            if isinstance(int(self.tb_position_stepsize.text()), int):
                if int(self.tb_position_stepsize.text()) > 0:
                    self.tb_position_stepsize.setStyleSheet('background-color: rgb(0,255,0)')
                    return True
                else:
                    self.tb_position_stepsize.setStyleSheet('background-color: rgb(255,0,0)')
                    return False
        except ValueError:
            self.tb_position_stepsize.setStyleSheet('background-color: rgb(255,0,0)')
            return False
