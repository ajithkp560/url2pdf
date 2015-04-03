import sys
from os.path import expanduser
from PyQt4.QtCore import *
from PyQt4.QtGui import * 
from PyQt4.QtWebKit import * 
from urlparse import urlparse
import urllib2
print """
    [][][]
    [][][]   Coded By Ajith Kp [ajithkp560]
    [][][]   Visit: http://www.terminalcoders.blogspot.de
    [][][]
"""
url = ''
fName = ''
typeFormat = ['A0 (841 x 1189 mm)', 'A1 (594 x 841 mm)', 'A2 (420 x 594 mm)', 'A3 (297 x 420 mm)', 'A4 (210 x 297 mm, 8.26 x 11.69 inches)', 'A5 (148 x 210 mm)', 'A6 (105 x 148 mm)', 'A7 (74 x 105 mm)', 'A8 (52 x 74 mm)', 'A9 (37 x 52 mm)','B0 (1000 x 1414 mm)', 'B1 (707 x 1000 mm)', 'B2 (500 x 707 mm)', 'B3 (353 x 500 mm)', 'B4 (250 x 353 mm)', 'B5 (176 x 250 mm, 6.93 x 9.84 inches)', 'B6 (125 x 176 mm)', 'B7 (88 x 125 mm)', 'B8 (62 x 88 mm)', 'B9 (33 x 62 mm)', 'B10 (31 x 44 mm)', 'C5E (163 x 229 mm)', 'Comm10E (105 x 241 mm, U.S. Common 10 Envelope)', 'DLE (110 x 220 mm)', 'Executive (7.5 x 10 inches, 190.5 x 254 mm)', 'Folio (210 x 330 mm)', 'Ledger (431.8 x 279.4 mm)', 'Legal (8.5 x 14 inches, 215.9 x 355.6 mm)', 'Letter (8.5 x 11 inches, 215.9 x 279.4 mm)', 'Tabloid (279.4 x 431.8 mm)']
typeOrient = ['Portrait', 'Landscape']
typeFormatObject = [QPrinter.A0, QPrinter.A1, QPrinter.A2, QPrinter.A3, QPrinter.A4, QPrinter.A5, QPrinter.A6, QPrinter.A7, QPrinter.A8, QPrinter.A9, QPrinter.B0, QPrinter.B1, QPrinter.B2, QPrinter.B3, QPrinter.B4, QPrinter.B5, QPrinter.B6, QPrinter.B7, QPrinter.B8, QPrinter.B9, QPrinter.B10, QPrinter.C5E, QPrinter.Comm10E, QPrinter.DLE, QPrinter.Executive, QPrinter.Folio, QPrinter.Ledger, QPrinter.Legal, QPrinter.Letter, QPrinter.Tabloid]
OrientedFormatObject = [QPrinter.Portrait, QPrinter.Landscape]

class Window(QWidget):
    Tindex = 4
    Oindex = 0
    url = ''
    fName = ''
    printer = None
    web = None
    tObj = None
    oObj = None
    lbl = None
    home = None    
    def __init__(self):
        super(Window, self).__init__()
        self.initUI()     
    def initUI(self):     
        self.urlFld = QLineEdit('URL', self)
        self.urlFld.setGeometry(QRect(10, 10, 690, 31))
        self.urlFld.setFont(QFont('SansSerif', 10))
        self.urlFld.setToolTip('Enter URL of document')
        
        sBtn = QPushButton('Save as PDF', self)
        sBtn.setGeometry(QRect(10, 180, 690, 31))
        sBtn.clicked.connect(self.btnClicked)
        
        typeLbl = QLabel('Paper Size: ', self)      
        typeLbl.setGeometry(QRect(10, 50, 300, 31))
        typeLbl.setFont(QFont('SansSerif', 10, QFont.Bold))
        
        typeCbx = QComboBox(self)
        typeCbx.addItems(typeFormat)
        typeCbx.setGeometry(QRect(310, 50, 300, 31))
        typeCbx.setCurrentIndex(4)
        typeCbx.connect(typeCbx,SIGNAL("currentIndexChanged(int)"), self, SLOT("TindexChanged(int)"))
        
        oriLbl = QLabel('Qrientation: ', self)
        oriLbl.setGeometry(QRect(10, 100, 300, 31))
        oriLbl.setFont(QFont('SansSerif', 10, QFont.Bold))
        
        oriCbx = QComboBox(self)
        oriCbx.addItems(typeOrient)
        oriCbx.setGeometry(QRect(310, 100, 300, 31))
        oriCbx.connect(oriCbx, SIGNAL("currentIndexChanged(int)"), self, SLOT("OindexChanged(int)"))
        
        self.lbl = QLabel('Coded by Ajith Kp [ajithkp560]',self);
        self.lbl.setGeometry(QRect(10, 140, 600, 31))
        self.lbl.setFont(QFont('SansSerif', 10, QFont.Bold))
        col = QPalette()
        col.setColor(QPalette.Foreground,Qt.red)
        self.lbl.setPalette(col)
        
        self.setGeometry(100, 100, 710, 220)
        self.setFixedSize(710, 220)
        self.setWindowTitle('PDF Parser')    
        self.show()
    @pyqtSlot(int)
    def TindexChanged(self, index):
        self.lbl.setText('Type Changed: '+typeFormat[index])
        self.Tindex = index
    @pyqtSlot(int)
    def OindexChanged(self, index):
        self.lbl.setText('Type Changed: '+typeOrient[index])
        self.Oindex = index
        print self.Oindex
    def btnClicked(self):
        try:    
            url = str(self.urlFld.text())
            tObj = typeFormatObject[self.Tindex]
            oObj = OrientedFormatObject[self.Oindex]
            parse = urlparse(url)
            scheme = parse.scheme
            if scheme=='':
                scheme = 'http://'
                url = scheme+url
            print 'Scehme: ',scheme
            fName = parse.netloc+'_'+parse.path+'.pdf'
            fName = fName.replace('/', '_')

            ul = urllib2.urlopen(url)
            u = ul.geturl()
            url = u      
            print 'Target: ', url  
            self.lbl.setText('Target: '+url) 
        except Exception, e:
            print e.args
            m = QMessageBox()
            m.setText('error: '+e.message)
            m.exec_()   
            print e
        try:
            self.setVal(url, fName, tObj, oObj, self.lbl)  
            self.convert()
        except Exception, e:
            print e
            m = QMessageBox()
            m.setText('error: '+e.message)
            m.exec_()   
            
        #setTarget(url, fName, tObj, oObj, self.lbl)
    def closeEvent(self, event):        
        r = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if r == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()   
            
    def setVal(self, url, fName, tObj, oObj, lbl):
        self.url = url
        self.fName = fName
        self.tObj = tObj
        self.oObj = oObj
        self.lbl = lbl
        self.home = expanduser("~")
        print 'Home directory: '+self.home
    
    def convert(self):
        #app = QApplication(sys.argv)
        self.web = QWebView()
        self.web.load(QUrl(self.url))
        self.printer = QPrinter(QPrinterInfo.defaultPrinter(),QPrinter.HighResolution)
        self.printer.setPageSize(self.tObj)
        self.printer.setFullPage(True)
        self.printer.setOutputFormat(QPrinter.PdfFormat)
        self.printer.setOrientation(self.oObj)
        self.printer.setOutputFileName(self.home+'/'+self.fName)
        self.web.loadFinished.connect(self.converter)
        self.web.loadProgress.connect(self.print_perc)
        print 'started...'
    def print_perc(self, perc):
        sys.stdout.write('\rPercentage: %d%%'%perc)
        sys.stdout.flush()        
        self.lbl.setText('Percentage: '+str(perc))
    def converter(self):
        self.web.print_(self.printer)
        msgBox = QMessageBox()
        msgBox.setText('Successfully generated file: <b>'+self.fName+'</b> in home directory')
        msgBox.exec_()        
        self.lbl.setText('Successfully generated file: <b>'+self.fName+'</b> in home directory')
        print '\n\nSuccessfully generated file: '+self.fName+' in home directory'    
def main():
    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())   
    main()
if __name__ == '__main__':
    main()
