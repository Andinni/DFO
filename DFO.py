import sys
from PyQt4 import QtGui, QtCore
import ConfigParser
from analyser import Analyser
from fit_config_Widget import CfgWidget

TEST_PATH = r"C:\Users\Andreas\Documents\Python Scripts\GUI stuff\dynamic file opener\test_data\10K"


class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow,self).__init__()

        self.initUI()

    def initUI(self): 
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))        
        self.config = ConfigParser.RawConfigParser()
        self.config.read('DFO.cfg')
        file_selector = QtGui.QVBoxLayout()
        # Set up selector and showing buttons        
        self.data_dir_btn = QtGui.QPushButton('DuT S-directory',self)     
        self.data_dir_Text = QtGui.QTextEdit(str(read_config(self.config,'main','dut-dir')))
        self.dummy_file_btn = QtGui.QPushButton('Dummy S-file',self)  
        self.dummy_file_path = QtGui.QTextEdit(read_config(self.config,'main','dummy-dir'))
        self.thru_file_btn = QtGui.QPushButton('THRU S-file',self)  
        self.thru_file_path = QtGui.QTextEdit(read_config(self.config,'main','thru-dir'))     
        self.save_paths_btn = QtGui.QPushButton('Save paths',self)
        self.save_paths_btn.setToolTip('Saves the current paths.')
        self.analyze_btn = QtGui.QPushButton('ANALYSE!',self)  
        self.fit_cfg_btn = QtGui.QPushButton('Configure fit',self)
        self.fit_btn = QtGui.QPushButton('Fit!',self)
        
        

        for w in [self.data_dir_btn,self.data_dir_Text, 
                  self.dummy_file_btn, self.dummy_file_path,
                  self.thru_file_btn, self.thru_file_path,
                  self.save_paths_btn, self.analyze_btn,
                  self.fit_cfg_btn, self.fit_btn ]:              
                      file_selector.addWidget(w)
        
        
        self.data_dir_btn.clicked.connect(self.folderDialog)
        self.dummy_file_btn.clicked.connect(self.fileDialog)
        self.thru_file_btn.clicked.connect(self.fileDialog)
        self.save_paths_btn.clicked.connect(self.save_config)
        self.analyze_btn.clicked.connect(self.analyzer)
        self.fit_cfg_btn.clicked.connect(self.configure_fit)
        self.fit_btn.clicked.connect(self.fitter) 
        
        self.setLayout(file_selector)       
        self.setGeometry(500, 400, 300, 150)
        self.setWindowTitle('RP Analysis and File Navigator')   
        self.show()
        
        

    def fileDialog(self):
        sender = self.sender()
        fname = QtGui.QFileDialog.getOpenFileName(self,"Open File", TEST_PATH,'*.txt')

        if sender == self.thru_file_btn:
            edit_field = self.thru_file_path
        elif sender == self.dummy_file_btn:
            edit_field = self.dummy_file_path
        edit_field.setText(fname)
        
            
    def folderDialog(self):
        fname = QtGui.QFileDialog.getExistingDirectory(self,"Open File", TEST_PATH)
        self.data_dir_Text.setText(fname)
        
        
    def analyzer(self):
        data_path = self.data_dir_Text.toPlainText()        
        dummy_file = self.dummy_file_path.toPlainText()
        thru_file = self.thru_file_path.toPlainText()
        # This can take some time. Eventually create a new Thread for this!
        self.analysed_data = Analyser(data_path,thru_file,dummy_file)
        
    def fitter(self):
        self.analysed_data.fit('y12','fit_cfg')#dummy args so far!
        print self.analysed_data.all_de_meas[0].fit_res
        
    def save_config(self):
        self.config.set('main', 'dut-dir', str(self.data_dir_Text.toPlainText()))
        self.config.set('main', 'dummy-dir', str(self.dummy_file_path.toPlainText()))
        self.config.set('main', 'thru-dir', str(self.thru_file_path.toPlainText()))
        with open('DFO.cfg', 'wb') as configfile:
            self.config.write(configfile)
            
    def configure_fit(self):
        self.fit_cfg = CfgWidget()
        #TO: Connect this somehow to the config file.
        return 

def read_config(cfg,section,option):
    try:
        val = cfg.get(section,option)
    except ConfigParser.NoSectionError:
        cfg.add_section(section)
        val = None
    except ConfigParser.NoOptionError:
        val = None
    return val
        
def main():


    # Start application    
    app = QtGui.QApplication(sys.argv)
    ex = MainWindow()
    ret = app.exec_()
#    sys.exit(app.exec_())

    
if __name__ == '__main__':
    main()
    










    
