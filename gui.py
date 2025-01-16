from PyQt5.QtWidgets import (
    QMainWindow,
    QPushButton,
    QLabel,
    QGridLayout,
    QWidget,
    QLineEdit,
    QFileDialog,
    QRadioButton,
    QButtonGroup,
    QGroupBox,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QToolBar,
    QAction,

)
from PyQt5.QtCore import QThreadPool, Qt, QSize
from PyQt5.QtGui import QIcon, QCursor, QPainter
import csv
from widgets import (
    InputLabel,
    InputLine,
    UpTriAngleButton,
    DownTriAngleButton,
    BlackLabel,
    BorderlessGroupBox,

)
from reader import Reader
from graphgui import Graph
from resultgui import ResultWindow
from setting import DisplacementControl, ForceDirection, GraphType, LengthDevice, Setting


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hounsfield")
        self.setGeometry(100, 100, 900, 700)
        #  self.setStyleSheet("""
        #  background-color: black;
        #  """)
        self.threadpool = QThreadPool()
        self.total_result = []
        self.connection = False


        self.main_toolbar = QToolBar('main toolbar')
        self.addToolBar(self.main_toolbar)

        self.connect_action = QAction(QIcon('inst.png'), "Connect To Instrument", self)
        self.connect_action.setStatusTip("Connect to Instrument")
        self.connect_action.triggered.connect(self.connect_to_tensile)
        # self.connect_action.setCheckable(True)
        self.main_toolbar.addAction(self.connect_action)

        self.result_action = QAction(QIcon('graph3.png'), "Results Window", self)
        self.result_action.setStatusTip("Results Window")
        self.result_action.triggered.connect(self.show_result)

        # self.result_action.setCheckable(True)
        self.main_toolbar.addAction(self.result_action)

        self.new_test_action = QAction(QIcon('new.png'), "New Test", self)
        self.new_test_action.setStatusTip("New Test")
        self.new_test_action.triggered.connect(self.new_test)
        self.main_toolbar.addAction(self.new_test_action)

        self.up_button = UpTriAngleButton('')
        self.down_button = DownTriAngleButton('')
        self.up_button.clicked.connect(self.up_button_act)
       # self.up_button.clicked.connect(self.up_button.refresh)
        self.down_button.clicked.connect(self.down_button_act)
        #self.down_button.clicked.connect(self.down_button.refresh)

        self.button_layout = QVBoxLayout()
        self.button_layout.setAlignment(Qt.AlignCenter)
        self.button_layout.addWidget(self.up_button)
        self.button_layout.addWidget(self.down_button)

        self.const_speed_button = QRadioButton('Constant Speed')
        self.const_strain_button = QRadioButton('Constant Strain')
        self.rate_button_group = QButtonGroup()
        self.rate_button_group.addButton(self.const_speed_button)
        self.rate_button_group.addButton(self.const_strain_button)
        self.radio_button_layout = QHBoxLayout()
        self.radio_button_layout.addWidget(self.const_speed_button)
        self.radio_button_layout.addWidget(self.const_strain_button)
        # self.radio_button_layout.setStretchFactor(self.const_speed_button,1)
        # self.radio_button_layout.setStretchFactor(self.const_strain_button,3)

        self.rate_label = InputLabel('Rate')
        self.rate_input = InputLine()
        self.rate_input.returnPressed.connect(self.set_speed)
        self.rate_input.textChanged.connect(self.set_speed)
        # self.rate_input.setFixedSize(QSize(50,10))
        self.rate_layout = QHBoxLayout()

        self.rate_layout.addWidget(self.rate_label)
        self.rate_layout.addWidget(self.rate_input)



        self.force_amount = BlackLabel('000.0')

        self.ext_amount = BlackLabel('00.00')

        self.r100_amount = BlackLabel('00.00')


        self.state_layout = QVBoxLayout()
        self.state_layout.setSpacing(3)
        self.state_layout.setContentsMargins(0, 0, 0, 0)

        self.state_layout.addWidget(self.force_amount)

        self.state_layout.addWidget(self.ext_amount)

        self.state_layout.addWidget(self.r100_amount)


        self.state_box = BorderlessGroupBox()
        self.state_box.setLayout(self.state_layout)






        # self.connect_button = QPushButton('connect to instrument')
        # self.connect_button.clicked.connect(self.connect_to_tensile)

        self.graph = Graph()

        self.layout = QGridLayout()
        self.layout.setContentsMargins(50, 20, 50, 100)
        self.layout.setSpacing(0)

        self.layout.addWidget(self.graph, 0, 0, 10, 10)
        self.layout.addWidget(self.state_box, 8, 9, 1, 1)
      #  self.layout.addWidget(self.ext_box, 1, 9, 1, 1)
      #  self.layout.addWidget(self.r100_box, 2, 9, 1, 1)
        self.layout.addLayout(self.button_layout, 2, 18, 3, 1)
        self.layout.addLayout(self.radio_button_layout, 0, 17, 1, 2)
        self.layout.addLayout(self.rate_layout, 1, 17)
        #  self.layout.addWidget(self.connect_button,6,18)
        self.layout.setColumnStretch(0, 9)

        self.layout.setAlignment(Qt.AlignHCenter)
        self.w = QWidget()
        self.w.setLayout(self.layout)
        self.setCentralWidget(self.w)

    def connect_to_tensile(self):
        try:
            self.reader = Reader()
        except Exception as e:
            QMessageBox.information(self, "", 'Make sure Instrument is On ', QMessageBox.Ok)
            return
        self.threadpool.start(self.reader)
        self.reader.signals.data.connect(self.receive_data)
        self.connection = True

    def set_speed(self):
        if not self.connection:
            self.rate_input.setText('')
            self.connection_alert()
            return
        self.reader.tensile.set_speed(float(self.rate_input.text()))
    def show_result(self):
        self.result_window = ResultWindow(self.total_result)
        self.result_window.show()

    def new_test(self):
        self.total_result = []
        print(self.total_result)
        self.graph.refresh_graph()

    def up_button_act(self, e):
        if not self.connection:
            self.connection_alert()
            return
        self.up_button.refresh()
        if self.up_button.isChecked():
            if self.down_button.isChecked():
                self.down_button.click()
            self.reader.tensile.set_speed(float(self.rate_input.text()))
            self.reader.tensile.move_up()
            # self.graph.refresh_line()
        # setting = self.get_setting()
        # self.reader = Reader()

        # self.threadpool.start(self.reader)
        # self.start_button.setText('STOP')
        else:
            self.reader.tensile.stop()
        # self.reader.close()
        # self.unit, self.samples, self.forces = \
        # self.reader.get_total_measurment()
        # self.start_button.setText('START')

    def down_button_act(self, e):
        if not self.connection:
            self.connection_alert()
            return
        self.down_button.refresh()
        if self.down_button.isChecked():
            if self.up_button.isChecked():
                self.up_button.click()
            self.reader.tensile.move_down()
        # self.graph.refresh_line()
        # self.refresh_calculation()
        # setting = self.get_setting()
        #  print(setting.__dict__ )
        # self.reader = Reader()
        #
        # self.reader.signals.data.connect(self.receive_data)
        # self.threadpool.start(self.reader)
        # self.start_button.setText('STOP')
        else:
            self.reader.tensile.stop()
            # self.down_button.off()

            # self.reader.close()
        # self.unit, self.samples, self.forces = \
        # self.reader.get_total_measurment()
        # self.start_button.setText('START')

    def receive_data(self, tensile_output):

     #   self.graph.show_state(tensile_output.force, tensile_output.ext, tensile_output.r100)
        force = f'force = {tensile_output.force} N'
        self.force_amount.setText(force)
        ext = f'ext = {tensile_output.ext} mm'
        self.ext_amount.setText(ext)
        r100 = f'r100 = {tensile_output.r100} mm'
        self.r100_amount.setText(r100)
        if self.up_button.isChecked() or self.down_button.isChecked():
            self.graph.update('unit', tensile_output.force, tensile_output.ext, tensile_output.r100)
            self.total_result.append(tensile_output)

    # self.force_amount.setText(str(force))
    # self.force_unit.setText(unit)

    def get_setting(self):

        if self.tension_button.isChecked():
            self.tensile_setting.force_direction = ForceDirection.Tension
        if self.compression_button.isChecked():
            self.tensile_setting.force_direction = ForceDirection.Compression

        if self.displacement_button.isChecked():
            self.tensile_setting.displacement_control = DisplacementControl.Displacement
        if self.strain_button.isChecked():
            self.tensile_setting.displacement_control = DisplacementControl.Strain

        if self.instrument_button.isChecked():
            self.tensile_setting.length_measurement_device = LengthDevice.Instrument
        if self.extensometer_button.isChecked():
            self.tensile_setting.length_measurement_device = LengthDevice.Extensometer

        if self.force_displacement_button.isChecked():
            self.tensile_setting.graph_type = GraphType.ForceDislacement
        if self.eng_stress_strain_button.isChecked():
            self.tensile_setting.graph_type = GraphType.EngineeringStressStrain
        if self.real_stress_strain_button.isChecked():
            self.tensile_setting.graph_type = GraphType.RealStressStrain

        self.tensile_setting.strain_rate = float(self.strain_rate_input.text())
        self.tensile_setting.speed_rate = float(self.speed_input.text())
        self.tensile_setting.l0_length = float(self.l0_input.text())
        self.tensile_setting.widht = float(self.widht_input.text())
        self.tensile_setting.thickness = float(self.thickness_input.text())

        return self.tensile_setting

    def calculate_button_click(self):
        low = int(self.lower_range.text())
        upper = int(self.upper_range.text())
        self.min_out.setText(str(min(self.forces[low:upper])))
        self.max_out.setText(str(max(self.forces[low:upper])))
        self.mean_out.setText(str(round(mean(self.forces[low:upper]), 2)))

    def refresh_calculation(self):
        self.lower_range.setText('')
        self.upper_range.setText('')
        self.min_out.setText('')
        self.max_out.setText('')
        self.mean_out.setText('')

    def export_button_click(self):
        self.file_dialog = QFileDialog()

        self.file_path = self.file_dialog.getSaveFileName()[0]
        if not self.file_path:
            return
        if not self.file_path.endswith('.csv'):
            self.file_path += '.csv'

        with open(self.file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, dialect='excel', delimiter=';')
            writer.writerow(self.total_result)

    def connection_alert(self):
        # Ask for confirmation before closing

       QMessageBox.critical(self, "Alert", "Connect to the Instrument",
                                             )





    def closeEvent(self, event):
        # Ask for confirmation before closing

        confirmation = QMessageBox.question(self, "Confirmation", "Do You Want Close App Without Saving?",
                                            QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            if hasattr(self, 'reader'):
                self.reader.close()
            event.accept()  # Close the app
        else:
            event.ignore()  # Don't close the app


