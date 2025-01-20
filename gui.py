from PyQt5.QtWidgets import (
    QMainWindow,
    QGridLayout,
    QWidget,
    QFileDialog,
    QVBoxLayout,
    QMessageBox,
    QToolBar,
    QAction,
)
from PyQt5.QtCore import QThreadPool, Qt
from PyQt5.QtGui import QIcon
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
        self.main_toolbar.addAction(self.connect_action)

        self.result_action = QAction(QIcon('graph3.png'), "Results Window", self)
        self.result_action.setStatusTip("Results Window")
        self.result_action.triggered.connect(self.show_result)

        self.main_toolbar.addAction(self.result_action)

        self.new_test_action = QAction(QIcon('new.png'), "New Test", self)
        self.new_test_action.setStatusTip("New Test")
        self.new_test_action.triggered.connect(self.new_test)
        self.main_toolbar.addAction(self.new_test_action)

        self.up_button = UpTriAngleButton('')
        self.down_button = DownTriAngleButton('')
        self.up_button.clicked.connect(self.up_button_act)
        self.down_button.clicked.connect(self.down_button_act)

        self.button_layout = QVBoxLayout()
        self.button_layout.setAlignment(Qt.AlignCenter)
        self.button_layout.addWidget(self.up_button)
        self.button_layout.addWidget(self.down_button)

        self.rate_label = InputLabel('Speed (mm/min)' )
        self.rate_input = InputLine()
        self.rate_input.returnPressed.connect(self.set_speed)
        self.rate_input.textChanged.connect(self.set_speed)
        # self.rate_input.setFixedSize(QSize(50,10))
        self.rate_layout = QVBoxLayout()

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

        self.graph = Graph()

        self.layout = QGridLayout()
        self.layout.setContentsMargins(50, 20, 50, 100)
        self.layout.setSpacing(0)

        self.layout.addWidget(self.graph, 0, 0, 10, 10)
        self.layout.addWidget(self.state_box, 8, 9, 1, 1)
        self.layout.addLayout(self.button_layout, 2, 18, 3, 1)
        self.layout.addLayout(self.rate_layout, 1, 18)
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
        confirmation = QMessageBox.question(self, "Confirmation", "Do You Want Start New Test Without Saving?",
                                            QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            self.total_result = []
            self.graph.refresh_graph()
        else:
            pass

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
        else:
            self.reader.tensile.stop()

    def down_button_act(self, e):
        if not self.connection:
            self.connection_alert()
            return
        self.down_button.refresh()
        if self.down_button.isChecked():
            if self.up_button.isChecked():
                self.up_button.click()
            self.reader.tensile.move_down()
        else:
            self.reader.tensile.stop()

    def receive_data(self, tensile_output):
        force = f'force = {tensile_output.force} N'
        self.force_amount.setText(force)
        ext = f'ext = {tensile_output.ext} mm'
        self.ext_amount.setText(ext)
        r100 = f'r100 = {tensile_output.r100} mm'
        self.r100_amount.setText(r100)

        if self.up_button.isChecked() or self.down_button.isChecked():
            self.graph.update('unit', tensile_output.force, tensile_output.ext, tensile_output.r100)
            self.total_result.append(tensile_output)

    def connection_alert(self):
       QMessageBox.critical(self, "Alert", "Connect to the Instrument")

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


