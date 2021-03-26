import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QIcon
### Using the grid layout making buttons

class Window(QMainWindow):

    country_selected = QtCore.pyqtSignal(str)

    def __init__(self):
        self.left = 300
        self.top = 300
        self.width = 500
        self.height = 300


        ### Containts Window method and main menu ###
        super(Window, self).__init__() # Super returns parent object (Which is a QMainWindow)
        self.setWindowTitle('Engineering Map')
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.initWindow()


    def initWindow(self):
        self.setWindowTitle('PyQt5 Grid-Layout Test')
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createLayout_countrySelect() # Runs the method so it initialises the layout

        wid = QWidget(self) # Makes a Widget and sets it as the central widget because you cannot place directly on...
        self.setCentralWidget(wid) # ... the main window.
        vbox = QVBoxLayout()
        vbox.addWidget(self.groupBox)
        wid.setLayout(vbox)

        self.show()


    def createLayout_countrySelect(self):
        ## Making Group Box
        self.groupBox = QGroupBox('Welcome to Engineering Map Generator')
        ## Defining the layout
        gridLayout = QGridLayout()

        ## Making the buttons and adding them to the layout
        self.btn1 = QPushButton('United Kingdom', self)
        self.btn1.setIcon(QIcon('uk.png'))
        self.btn1.setIconSize(QtCore.QSize(40,40))
        self.btn1.setMinimumHeight(20)
        self.btn1.clicked.connect(self.on_clicked_btn1)
        gridLayout.addWidget(self.btn1, 0, 0)
        #btn2.clicked.connect(self.close_application)

        btn2 = QPushButton('Canada', self)
        btn2.setIcon(QIcon('canada.png'))
        btn2.setIconSize(QtCore.QSize(40,40))
        btn2.setMinimumHeight(20)
        gridLayout.addWidget(btn2, 0, 1)

        btn3 = QPushButton('United States', self)
        btn3.setIcon(QIcon('flag.png'))
        btn3.setIconSize(QtCore.QSize(40,40))
        btn3.setMinimumHeight(20)
        gridLayout.addWidget(btn3, 2, 0)
        #btn2.clicked.connect(self.close_application)

        btn4 = QPushButton('Australia', self)
        btn4.setIcon(QIcon('australia.png'))
        btn4.setIconSize(QtCore.QSize(40,40))
        btn4.setMinimumHeight(20)
        gridLayout.addWidget(btn4, 2, 1)
        #btn2.clicked.connect(self.close_application)

        # UK
        label = QLabel('             Companies:     50 \n' +
                       '                     Cities:     10 \n' +
                       'Range of Industries:   Good')
        label.setFont(QtGui.QFont('Sanserif ', 15))
        label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        label.setMinimumHeight(10)
        gridLayout.addWidget(label, 1, 0)
        # Canada
        label2 = QLabel('             Companies:    30 \n' +
                       '                     Cities:     7 \n' +
                       'Range of Industries:   Poor')
        label2.setFont(QtGui.QFont('Sanserif ', 15))
        label2.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        label2.setMinimumHeight(10)
        gridLayout.addWidget(label2, 1, 1)
        # USA
        label3 = QLabel('             Companies:        50 \n' +
                       '                     Cities:        30 \n' +
                       'Range of Industries:   Excellent')
        label3.setFont(QtGui.QFont('Sanserif ', 15))
        label3.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        label3.setMinimumHeight(10)
        gridLayout.addWidget(label3, 3, 0)
        # Australia
        label4 = QLabel('             Companies:    5 \n' +
                       '                     Cities:     7 \n' +
                       'Range of Industries:   Poor')
        label4.setFont(QtGui.QFont('Sanserif ', 15))
        label4.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        label4.setMinimumHeight(10)
        gridLayout.addWidget(label4, 3, 1)

        ## Setting layout in the groupbox (Which is a widget)
        self. groupBox.setLayout(gridLayout)

    def on_clicked_btn1(self):
        self.country_selected.emit(self.btn1.text())
        #print(self.btn1.text())



# def run():
#     app = QApplication(sys.argv)
#     GUI = Window()
#     sys.exit(app.exec_())
#
# run()

