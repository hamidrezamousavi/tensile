from pyqtgraph import(
    PlotWidget,
    mkPen,
)

class Graph(PlotWidget):
    def __init__(self):
        super().__init__()
        self.forces =[]
        self.r100=[]
        self.ext=[] 
        self.unit = ''
        self.ext_pen = mkPen(width=1, color=(255,0,0))
        self.force_ext_line = self.plot(pen = self.ext_pen)
        self.r100_pen = mkPen(width=1, color=(0,255,0))
        self.force_r100_line = self.plot(pen = self.r100_pen)

        self.showGrid(x=True, y=True)

    def update(self, unit, force, ext, r100):

        self.ext.append(ext)
        self.r100.append(r100)
        self.forces.append(force)
        self.force_ext_line.setData( self.ext, self.forces )
        self.force_r100_line.setData( self.r100, self.forces )

    def refresh_graph(self):
        self.ext=[]
        self.r100=[]
        self.forces=[]
        self.force_ext_line.setData(self.ext, self.forces)
        self.force_r100_line.setData(self.r100, self.forces)

