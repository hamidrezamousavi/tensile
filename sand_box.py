"""
Demonstrates some customized mouse interaction by drawing a crosshair that follows
the mouse.
"""

import numpy as np

import pyqtgraph as pg

#generate layout
app = pg.mkQApp("Crosshair Example")
p1 = pg.plot(row=1, col=0)

data1 = 10000 + 15000 * pg.gaussianFilter(np.random.random(size=10000), 10) + 3000 * np.random.random(size=10000)

p1.plot(data1, pen="r")



vLine = pg.InfiniteLine(angle=90, movable=False)
hLine = pg.InfiniteLine(angle=0, movable=False)
p1.addItem(vLine, ignoreBounds=False)
p1.addItem(hLine, ignoreBounds=False)


vb = p1.getViewBox()

def mouseMoved(evt):
    pos = evt
   # if p1.sceneBoundingRect().contains(pos):
    mousePoint = vb.mapSceneToView(pos)
    index = int(mousePoint.x())
    vLine.setPos(mousePoint.x())
    hLine.setPos(mousePoint.y())
    print(mousePoint.x(), mousePoint.y())


p1.scene().sigMouseMoved.connect(mouseMoved)


if __name__ == '__main__':
    pg.exec()
