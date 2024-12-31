from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from gui import MainWindow
import qtmodern.styles
import qtmodern.windows


app = QApplication([])
app.setWindowIcon(QIcon('hounsfile.png'))
#qtmodern.styles.dark(app)

#window = qtmodern.windows.ModernWindow(MainWindow())
window =MainWindow()
window.show()
app.exec_()