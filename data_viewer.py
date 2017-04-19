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
    def __init__(self, parent=None,filename=r'D:\Users\inhofer\Documents\shared_for_measurements\python\test\Code\L59W20\2017-04-13_15h30m38s_Vg2_0.00V\results + sigma.txt'):
        super(PointBrowser, self).__init__(parent)
        self.filename = filename
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
       
        self.lastind = 0 # Initiate the selected index.
        
        # Set up the plots.
        self.res_ax = self.figure.add_subplot(211)
        self.spec_ax = self.figure.add_subplot(212)
        
        self.data = np.genfromtxt(self.filename, skip_header = 1, dtype = None, names=True, delimiter = '\t')
        self.selector_entries = [name for name in self.data.dtype.names]
        self.spectra_files = self.data[self.selector_entries[-1]]
               
        self.selector = QtGui.QComboBox(self)
        
        self.selector.addItems(self.selector_entries[:-1])
        
        self.selector.currentIndexChanged.connect(self.upper_plot)
        

        PlotLayout = QtGui.QVBoxLayout() 
        PlotLayout.addWidget(self.selector)

        PlotLayout.addWidget(self.canvas)
        PlotLayout.addWidget(self.toolbar)
        self.setLayout(PlotLayout)
        
        
        self.upper_plot()
        self.canvas.draw()

        
        
    def upper_plot(self):
        self.xs = np.array(self.data['Vg'])
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
        print event.ind
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
        
        spec_data = np.genfromtxt(self.spectra_files[dataind],delimiter = '\t', skip_header = 1).T
        
        self.spec_ax.hold(True)        
        self.spec_ax.clear()                
        self.spec_ax.cla()

        exp_real_line, = self.spec_ax.plot(spec_data[0],spec_data[1],'ro')
        exp_imag_line, = self.spec_ax.plot(spec_data[0],spec_data[2],'bo')
        fit_real_line, = self.spec_ax.plot(spec_data[0],spec_data[3],'k--')
        fit_imag_line, = self.spec_ax.plot(spec_data[0],spec_data[4],'k--')
        
        exp_real_line.set_ydata = spec_data[1]
        exp_real_line.set_xdata = spec_data[0]
        exp_imag_line.set_ydata = spec_data[2]
        exp_imag_line.set_xdata = spec_data[0]
        fit_real_line.set_ydata = spec_data[3]
        fit_real_line.set_xdata = spec_data[0]
        fit_imag_line.set_ydata = spec_data[4]
        fit_imag_line.set_xdata = spec_data[0]
        
        
#        
        self.canvas.draw() # Needed for actual update of the figure.


        

        
def main():
    # Start application    
    app = QtGui.QApplication(sys.argv)
    ex = PointBrowser()
    ex.show()
    ret = app.exec_()
#    sys.exit(app.exec_())


if __name__=='__main__':
    main()
    
    