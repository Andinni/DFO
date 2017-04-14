import sys
from PyQt4 import QtGui, QtCore
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
try:
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
except ImportError:
    from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

#def results_opener(filename=r'D:\tests\DFO-test_data\results.txt'):
#    data = np.genfromtxt(filename, dtype = None)
#    spectra_files = data['f0']
#    Vg = np.array(data['f1'])
#    C = data['f2']
#    R = data['f3']
#    print Vg,C,R


class PointBrowser(QtGui.QDialog):
    def __init__(self, parent=None,filename=r'D:\tests\DFO-test_data\results.txt'):
        super(PointBrowser, self).__init__(parent)
        self.filename = filename
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
       
        self.lastind = 0 # Initiate the selected index.
        
        # Set up the plots.
        self.res_ax = self.figure.add_subplot(211)
        self.spec_ax = self.figure.add_subplot(212)
        
        self.data = np.genfromtxt(self.filename, dtype = None,names=True)
        self.selector_entries = [name for name in self.data.dtype.names]
        self.spectra_files = self.data[self.selector_entries[0]]
               
        self.selector = QtGui.QComboBox(self)
        
        self.selector.addItems(self.selector_entries[1:])
        
        self.selector.currentIndexChanged.connect(self.upper_plot)
        

        PlotLayout = QtGui.QVBoxLayout() 
        PlotLayout.addWidget(self.selector)

        PlotLayout.addWidget(self.canvas)
        PlotLayout.addWidget(self.toolbar)
        self.setLayout(PlotLayout)
        
        
        self.upper_plot()
        self.canvas.draw()

        
        
    def upper_plot(self):
        self.xs = np.array(self.data[self.selector_entries[1]])
        selected_item = self.selector.currentText()
        self.ys = np.array(self.data[selected_item])
        
        self.res_ax.hold(False)        
        self.res_ax.clear()                
        self.res_ax.cla()        
        
        self.line, = self.res_ax.plot(self.xs,self.ys,'o',picker = 5) 
        self.figure.canvas.draw()
        self.canvas.mpl_connect('pick_event', self.onpick)

    def onpick(self, event):
        if event.artist != self.line:
            return True

        N = len(event.ind)
        if not N:
            return True

        # the click locations
        x = event.mouseevent.xdata
        y = event.mouseevent.ydata
    
        # Avoid crash if user clickes outside of canvas.        
        if x is None:
            x=0
        if y is None:
            y=0
            
        distances = np.hypot(x - self.xs[event.ind], y - self.ys[event.ind])
        indmin = distances.argmin()
        dataind = event.ind[indmin]

        self.lastind = dataind
        self.update()
        self.figure.canvas.draw()
        
        
    def update(self):
        if self.lastind is None:
            return
        dataind = self.lastind
        newX = np.genfromtxt(self.spectra_files[dataind]).T
        self.spec_ax.hold(False)        
        self.spec_ax.clear()                
        self.spec_ax.cla()
        spec_line, = self.spec_ax.plot(newX[0],newX[1],'ro')
        spec_line.set_ydata = newX[1]
        spec_line.set_xdata = newX[0]
        
        self.canvas.draw() # Needed for actual update of the figure.


        

        
def main():
    # Start application    
    app = QtGui.QApplication(sys.argv)
    ex = PointBrowser()
    ex.show()
    ret = app.exec_()
#    sys.exit(app.exec_())


if __name__=='__main__':
#    results_opener()
    main()
    
    