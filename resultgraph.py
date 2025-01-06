from pyqtgraph import(
    PlotWidget,
   # Plot,
    mkPen,
    mkBrush,
    mkColor,
    TargetItem,
    InfiniteLine,
   
)
from widgets import (
InputLabel,
InputLine,


BlackLabel,
)
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QHBoxLayout,
    QWidget,
)
from time import time
class MyTargetItem(TargetItem):
    def __init__(self):
        super().__init__(symbol='+',size=20)
    def mouseDragEvent(self, ev):
        x =self.pos().x()
        y =self.pos().y()
        self.setLabel(f'x = {x: >.3f}\ny = {y: >.3f}'),
        return super().mouseDragEvent(ev)



from util import Point
from data import data
class Graph(PlotWidget):
    def __init__(self,*,data=None,
                        title = 'add Title',
                        x_ax_label = 'x',
                        y_ax_label = 'y'):
        super().__init__()
        self.showGrid(x=True, y=True)
    def refresh(self,*,data=None,
                        title = 'add Title',
                        x_ax_label = 'x',
                        y_ax_label = 'y'):
        #self.title = title
        self.clear()
        self.target_item = MyTargetItem()
        self.addItem(self.target_item)
        self.setTitle(title, color='red', size="16px",font='courier')
        self.setLabel('left', f'<span style=\"color:#02FD08;font-size:16px;\">{y_ax_label}</span>')
        self.setLabel('bottom', f'<span style=\"color:#02FD08;font-size:16px\">{x_ax_label}</span>')
        
        self.pen = mkPen(width=1, color=(255,0,0))
        self.line = self.plot(pen = self.pen)
        
        self.points_x = []
        self.points_y = []
       # self.line.setData(self.points_x, self.points_y )
        try:
            self.points_x , self.points_y = data
        except:
            pass
        
        self.line.setData(self.points_x, self.points_y )

        self.l = InfiniteLine(pos = (0,0),
                              angle = 45,
                              movable= True  )
        self.addItem(self.l)

       

        
        
        

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.button = QPushButton('test')
        self.button.clicked.connect(self.do)
        self.graph = Graph()
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.graph)
        self.w = QWidget()
        self.w.setLayout(self.layout)
        self.setCentralWidget(self.w)
       
    def do(self):
        self.graph.refresh()

if __name__ == '__main__':
    app = QApplication([])

    window =MainWindow()
    
    window.show()
    app.exec_()