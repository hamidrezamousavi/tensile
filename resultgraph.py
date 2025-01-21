from random import choice
from pyqtgraph import (
    PlotWidget,
    mkPen,
    TargetItem,
    InfiniteLine,
    TextItem,
    LineSegmentROI,
)

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QHBoxLayout,
    QWidget,
)

class SlopLine(LineSegmentROI):
    def __init__(self,pos):
        super().__init__(pos)
        self.label = TextItem(text = '',anchor=(1,1))
        self.label.setParentItem(self)

        self.sigRegionChanged.connect(self.update)
    def update(self):
        if hasattr(self,'label'):
            point1, point2 = self.getState()['points']
            x = (point1.x() + point2.x())/2
            y = (point1.y() + point2.y())/2
            self.label.setPos(x,y)
            try:
                slop = (point2.y() - point1.y())/(point2.x() - point1.x())
            except ZeroDivisionError:
                slop = 'ZeroDivisionError'
            self.label.setText(f'slop = {slop:0.3f}')

class FreeTargetItem(TargetItem):
    def __init__(self):
        super().__init__(symbol='+', size=20)

    def mouseDragEvent(self, ev):
        x = self.pos().x()
        y = self.pos().y()
        self.setLabel(f'x = {x: >.3f}\ny = {y: >.3f}'),
        return super().mouseDragEvent(ev)

class Graph(PlotWidget):
    def __init__(self):
        super().__init__()
        self.larg_graph =  QWidget()
        self.showGrid(x=True, y=True)
        self.v_line = InfiniteLine(angle=90, movable=False)
        self.h_line = InfiniteLine(angle=0, movable=False)
        self.v_h_line_value = TextItem('',anchor=(1,1))
        self.scene().sigMouseMoved.connect(self.mouse_moved)

    def refresh(self, *, data=None,
                title='add Title',
                x_ax_label='x',
                y_ax_label='y'):
        self.data = data
        self.title = title
        self.x_ax_label = x_ax_label
        self.y_ax_label = y_ax_label
        self.clear()
    #    self.target_item = FreeTargetItem()
        self.addItem(self.v_line, ignoreBounds=True)
        self.addItem(self.h_line, ignoreBounds=True)
        self.addItem(self.v_h_line_value,ignoreBounds=True)
    #    self.addItem(self.target_item)
        self.setTitle(self.title, color='red', size="16px", font='courier')
        self.setLabel('left', f'<span style=\"color:#02FD08;font-size:16px;\">{self.y_ax_label}</span>')
        self.setLabel('bottom', f'<span style=\"color:#02FD08;font-size:16px\">{self.x_ax_label}</span>')

        self.pen = mkPen(width=1, color=(255, 0, 0))
        self.line = self.plot(pen=self.pen)

        self.points_x = []
        self.points_y = []
        # self.line.setData(self.points_x, self.points_y )
        try:
            self.points_x, self.points_y = self.data.curve
        except:
            pass

        self.line.setData(self.points_x, self.points_y)


    def mouse_moved(self, evt):
        pos = evt
        mouse_point = self.getViewBox().mapSceneToView(pos)
        self.h_line.setPos(mouse_point.y())
        self.v_line.setPos(mouse_point.x())
        self.v_h_line_value.setPos(mouse_point.x(),mouse_point.y())
        self.v_h_line_value.setText(f'{mouse_point.y():0.2f}\n{mouse_point.x():0.3f}')

    def mouseDoubleClickEvent(self, event):
        self.larg_graph = QWidget()
        self.larg_graph.setWindowTitle(self.title)
        graph = Graph()
        graph.refresh(data = self.data,title= self.title,
                      x_ax_label=self.x_ax_label, y_ax_label=self.y_ax_label)
        layout = QHBoxLayout()
        layout.addWidget(graph)
        self.larg_graph.setLayout(layout)
        self.larg_graph.show()

class GraphEnhanced(Graph):
    def __init__(self):
        super().__init__()

    def refresh(self, *, data=None,
                title='add Title',
                x_ax_label='x',
                y_ax_label='y'):
        super().refresh(data=data,
                        title=title,
                        x_ax_label=x_ax_label,
                        y_ax_label=y_ax_label)

        if not data:
            return
        self.uts_marker = TargetItem(
            pos=(data.strain_at_uts, data.uts),
            symbol='+',
            size=10,
            label=f'uts = {data.uts: >.3f}\nstrain at uts = {data.strain_at_uts: >.3f}',
            movable=False,
        )

        self.addItem(self.uts_marker)

        self.break_marker = TargetItem(
            pos=(data.strain_at_break, data.stress_at_break),
            symbol='+',
            size=10,
            label=f'strain = {data.strain_at_break: >.3f}\n',
            movable=False,
        )

        self.addItem(self.break_marker)

        self.slop_line = SlopLine([(min(self.points_x), min(self.points_y)),
                                   (max(self.points_x), max(self.points_y))])
        self.addItem(self.slop_line)

    def mouseDoubleClickEvent(self, event):
        self.larg_graph = QWidget()
        self.larg_graph.setWindowTitle(self.title)
        graph = GraphEnhanced()
        graph.refresh(data = self.data,title= self.title,
                      x_ax_label=self.x_ax_label, y_ax_label=self.y_ax_label)
        layout = QHBoxLayout()
        layout.addWidget(graph)
        self.larg_graph.setLayout(layout)
        self.larg_graph.show()

    def plot_modulu(self, modulu, data):

        pen = mkPen(width=1, color=choice(['cyan', 'blue', 'yellow', 'magenta']))
        modulu_line = self.plot(pen=pen)
        m_x = []
        m_y = []

        try:

            m_x = [x for x in data.curve[0][:200] if (x - data.curve[0][0]) * modulu < data.uts * 1.4]
            m_y = [(item - data.curve[0][0]) * modulu + data.curve[1][0] for item in m_x]
        except Exception as e:
            print(e)

        modulu_line.setData(m_x, m_y)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.button = QPushButton('tes55t')
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

    window = MainWindow()

    window.show()
    app.exec_()