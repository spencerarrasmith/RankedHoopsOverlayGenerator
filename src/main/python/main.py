from PyQt5 import QtGui, QtWidgets, QtCore
from fbs_runtime.application_context.PyQt5 import ApplicationContext

import sys
import ctypes

import queue

# Import all the GUI elements from their respective files
from PyQtRH.widgetStyles import *
from PyQtRH.PyQtRH import *

from gui_elements.RHMenuBar import RHMenuBar

from gui_elements.Tabs.Tab_Home import Tab_Home
from gui_elements.Tabs.Tab_InGame import Tab_InGame
from gui_elements.Tabs.Tab_Intermission import Tab_Intermission
from gui_elements.Tabs.Tab_Interview import Tab_Interview

from gui_elements import _version


class RankedHoopsOverlayGenerator(ApplicationContext):
    """The main GUI window"""
    def __init__(self):
        super().__init__() #sys.argv)

        self.window = QtWidgets.QMainWindow()
        self.window.setWindowTitle(_version.__appname__)
        self.window.setStyleSheet(widgetStyle_mainWindow)

        self.window.setWindowIcon(QtGui.QIcon(self.get_resource('images/Icon.ico')))

        self.frame = QtWidgets.QFrame()
        self.window.setCentralWidget(self.frame)

        self.frame.setStyleSheet(widgetStyle_mainWindow)

    # Set the default size and position of the window
        width = 1000
        height = 500
        #xpos = int((self.primaryScreen().size().width()-width)/2)
        #ypos = int((self.primaryScreen().size().height()-height)/2)

        self.window.setGeometry(0, 0, width, height)

        self.layout = QtWidgets.QGridLayout()
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(10, 10, 10, 10)

        self.inAdminMode = False

    # Create the serial protocol
        #self.protocol = RHSerialProtocol(master=self, hfile=self.get_resource("MOLO_defines.h"))

    # Create the serial controller with info from the config file
        #self.parseConfigFile()

    # Create the serial comms queues
        #self.rxQueue = queue.Queue()
        #self.txQueue = queue.Queue()

        self.serial = None
        self.protocol = None
        #self.serial = RHSerialController(root=None, rxQueue=self.rxQueue, txQueue=self.txQueue,
        #                                 protocol=self.protocol,
        #                                 COMM=self.protocol.parameters["COMMPORT"].variable.value,
        #                                 baudRate=int(self.protocol.parameters["BAUDRATE"].variable.value),
        #                                 testMessage=self.protocol.parameters["TESTMESSAGE"].variable.value,
        #                                 testResponse=self.protocol.parameters["TESTRESPONSE"].variable.value)

        #self.updateConfigFile()

    # Build all window contents
        #self.menuBar = RHMenuBar(master=self, serial=self.serial, protocol=self.protocol)
        #self.window.setMenuBar(self.menuBar)

        self.label_logo = QtWidgets.QLabel()
        self.pixmap_logo = QtGui.QPixmap(self.get_resource('images/overlaygenerator.png'))
        self.label_logo.setPixmap(self.pixmap_logo)

        self.layout.addWidget(self.label_logo, 0, 0)

        self.layout.addWidget(QRHLine(thickness=2), 1, 0, 1, 10)

        self.pages = []
        self.pages.append(Tab_Home(master=self, serial=self.serial, protocol=self.protocol, index=len(self.pages)))
        self.pages.append(Tab_InGame(master=self, serial=self.serial, protocol=self.protocol, index=len(self.pages)))
        self.pages.append(Tab_Intermission(master=self, serial=self.serial, protocol=self.protocol, index=len(self.pages)))
        self.pages.append(Tab_Interview(master=self, serial=self.serial, protocol=self.protocol, index=len(self.pages)))

        self.tabs = QRHTabWidget(pages=self.pages)
        self.tabs.blockSignals(True)
        self.tabs.currentChanged.connect(self.configureTab)
        self.tabs.blockSignals(False)

        self.configureTab()

        self.layout.addWidget(self.tabs, 2, 0, 1, 10)

        self.frame.setLayout(self.layout)

        self.window.show()


    def configureTab(self):
        """Update polled loop timers and hidden protected parameters when changing between tabs"""
        self.window.repaint()
        self.tabs.tabBar().setTabButton(self.tabs.index_previous, QTabBar.LeftSide,
                                        self.tabs.pages[self.tabs.index_previous].button_inactive)
        self.tabs.tabBar().setTabButton(self.tabs.currentIndex(), QTabBar.LeftSide,
                                        self.tabs.pages[self.tabs.currentIndex()].button_active)

    # Set background tab readouts to poll once per minute
        self.tabs.pages[self.tabs.previousIndex()].SlowAllTimers(True)

    # Set active tab readouts to poll once per second
        self.tabs.pages[self.tabs.currentIndex()].SlowAllTimers(False)

        for cluster in self.tabs.pages[self.tabs.currentIndex()].widgets:
            cluster.setAdminMode(self.inAdminMode)

        self.tabs.index_previous = self.tabs.currentIndex()


    def parseConfigFile(self):
        """Read the contents of the config file for the serial port information and test message/response"""
        self.protocol.parameters["COMMPORT"].variable.value = ""
        self.protocol.parameters["BAUDRATE"].variable.value = "38400"
        self.protocol.parameters["TESTMESSAGE"].variable.value = "@00000R"
        self.protocol.parameters["TESTRESPONSE"].variable.value = "00000"
        try:
            f = open(self.get_resource("config.txt"), 'r')
            config = f.read()
            f.close()
            config_array = config.split('\n')
            for item in config_array:
                if item.split(':')[0] in self.protocol.parameters.keys():
                    self.protocol.parameters[item.split(':')[0]].variable.value = item.split(':')[1].rstrip().lstrip()
        except:
            return


    def updateConfigFile(self):
        """Update the config file with the COM port which was found to be active"""
        if self.serial.isConnected:
            self.protocol.parameters["COMMPORT"].variable.value = self.serial.commPort
            self.protocol.parameters["BAUDRATE"].variable.value = str(self.serial.baudRate)
            try:
                f = open(self.get_resource("config.txt"), 'w+')
                txt = ""
                for item in ["COMMPORT", "BAUDRATE", "TESTMESSAGE", "TESTRESPONSE"]:
                    txt += item + ': ' + str(self.protocol.parameters[item].variable.value) + '\n'
                f.write(txt)
                f.close()
            except:
                pass
        else:
            self.protocol.parameters["COMMPORT"].variable.value = "None"


if __name__ == "__main__":
    appctxt = ApplicationContext()
    app = RankedHoopsOverlayGenerator()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(_version.__appid__)
