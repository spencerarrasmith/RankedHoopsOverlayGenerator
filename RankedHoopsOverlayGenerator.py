from PyQt5 import QtGui, QtWidgets, QtCore
from fbs_runtime.application_context.PyQt5 import ApplicationContext

import sys
import ctypes

import queue

# Import all the GUI elements from their respective files
from gui_elements.BPSerialController.BPSerialController import BPSerialController
from gui_elements.BPSerialController.BPSerialProtocol import BPSerialProtocol
from gui_elements.BPMenuBar import BPMenuBar

from gui_elements.Tabs.Tab_Home import Tab_Home
from gui_elements.Tabs.Tab_InGame import Tab_InGame
from gui_elements.Tabs.Tab_Intermission import Tab_Intermission
from gui_elements.Tabs.Tab_Interview import Tab_Interview

from gui_elements import _version


class BPLowPowerModuleGUI(ApplicationContext):
    """The main GUI window"""
    def __init__(self):
        super().__init__() #sys.argv)

        self.window = QtWidgets.QMainWindow()
        self.window.setWindowTitle(_version.__appname__)
        self.window.setStyleSheet(widgetStyle_mainWindow)

        #self.setWindowIcon(QtGui.QIcon(self.get_resource('images/bplogo_128.ico')))
        self.window.setWindowIcon(QtGui.QIcon(self.get_resource('images/bplogo_128.ico')))

        self.frame = QtWidgets.QFrame()
        self.window.setCentralWidget(self.frame)

        self.frame.setStyleSheet(widgetStyle_mainWindow)

    # Assemble the splash screen, with messages and durations
        self.splash = QSLSSplash(master=self.window, image=self.get_resource('images/splash3.png'), mask=self.get_resource('images/splash3_mask.png'))
        self.splash.AddMessage("Building Window", 0.1)
        self.splash.AddMessage("Connecting to System", 0.1)
        self.splash.AddMessage("Creating Widgets", 0.1)
        self.splash.AddMessage("Reading LO Controller", 6) #6
        self.splash.AddMessage("Reading MO1 Controller", 6) #6
        self.splash.AddMessage("Reading MO2 Controller", 6) #6
        self.splash.AddMessage("Reading OLC1 Controller", 4) #4
        self.splash.AddMessage("Reading OLC2 Controller", 4) #4
        self.splash.AddMessage("Reading Interface Controller", 5) #5
        self.splash.AddMessage("Done", 4) #4

        self.splash.NextMessage()

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
        self.protocol = BPSerialProtocol(master=self, hfile=self.get_resource("MOLO_defines.h"))

    # Create the serial controller with info from the config file
        self.splash.NextMessage()
        self.parseConfigFile()

    # Create the serial comms queues
        self.rxQueue = queue.Queue()
        self.txQueue = queue.Queue()

        self.serial = BPSerialController(root=None, rxQueue=self.rxQueue, txQueue=self.txQueue,
                                         protocol=self.protocol,
                                         COMM=self.protocol.parameters["COMMPORT"].variable.value,
                                         baudRate=int(self.protocol.parameters["BAUDRATE"].variable.value),
                                         testMessage=self.protocol.parameters["TESTMESSAGE"].variable.value,
                                         testResponse=self.protocol.parameters["TESTRESPONSE"].variable.value)

        self.updateConfigFile()

    # Build all window contents
        self.splash.NextMessage(timed=self.serial.isConnected)
        self.menuBar = BPMenuBar(master=self, serial=self.serial, protocol=self.protocol)
        self.window.setMenuBar(self.menuBar)

        self.label_logo = QtWidgets.QLabel()
        self.pixmap_logo = QtGui.QPixmap(self.get_resource('images/bplogo_linear_600x73.png'))
        self.label_logo.setPixmap(self.pixmap_logo)
        #self.label_logo.installEventFilter(self)
        self.layout.addWidget(self.label_logo, 0, 0)

        self.layout.addWidget(QSLSLine(thickness=2), 1, 0, 1, 10)

        self.pages = []
        self.pages.append(Tab_Home(master=self, serial=self.serial, protocol=self.protocol, index=len(self.pages)))
        self.splash.NextMessage(timed=self.serial.isConnected)
        self.pages.append(Tab_LO(master=self, serial=self.serial, protocol=self.protocol, index=len(self.pages)))
        self.splash.NextMessage(timed=self.serial.isConnected)
        self.pages.append(Tab_MO1(master=self, serial=self.serial, protocol=self.protocol, index=len(self.pages)))
        self.splash.NextMessage(timed=self.serial.isConnected)
        self.pages.append(Tab_MO2(master=self, serial=self.serial, protocol=self.protocol, index=len(self.pages)))
        self.splash.NextMessage(timed=self.serial.isConnected)
        self.pages.append(Tab_OLC1(master=self, serial=self.serial, protocol=self.protocol, index=len(self.pages)))
        self.splash.NextMessage(timed=self.serial.isConnected)
        self.pages.append(Tab_OLC2(master=self, serial=self.serial, protocol=self.protocol, index=len(self.pages)))
        self.splash.NextMessage(timed=self.serial.isConnected)
        self.pages.append(Tab_InterfaceController(master=self, serial=self.serial, protocol=self.protocol, index=len(self.pages)))

        self.tabs = QSLSTabWidget(pages=self.pages)
        self.tabs.blockSignals(True)
        self.tabs.currentChanged.connect(self.configureTab)
        self.tabs.blockSignals(False)
        for page in self.pages:
            page.SlowAllTimers(True)
        self.configureTab()


        self.layout.addWidget(self.tabs, 2, 0, 1, 10)

        self.frame.setLayout(self.layout)

    # Done loading
        self.splash.NextMessage(timed=self.serial.isConnected)
        self.splash.Finish()
        self.window.show()

        #self.WriteProtocolToFile()

    def WriteProtocolToFile(self):
        """Write the serial protocol out to a tab delimited text file"""
        f = open(self.get_resource("SerialProtocol.txt"), 'w+')
        serialprotocolout = ''
        for parameter in self.protocol.parameters.keys():
            line = ''
            line += str(self.protocol.parameters[parameter].parameter) + '\t'
            line += str(self.protocol.parameters[parameter].description) + '\t'
            line += str(self.protocol.parameters[parameter].group) + '\t'
            line += str(self.protocol.parameters[parameter].command) + '\t'
            line += str(self.protocol.parameters[parameter].permission) + '\t'
            line += str(self.protocol.parameters[parameter].type) + '\t'
            line += str(self.protocol.parameters[parameter].mode) + '\t'
            line += str(self.protocol.parameters[parameter].units) + '\t'
            line += str(self.protocol.parameters[parameter].min) + '\t'
            line += str(self.protocol.parameters[parameter].max) + '\t'
            line += str(self.protocol.parameters[parameter].precision) + '\n'
            serialprotocolout += line

        f.write(serialprotocolout)
        f.close()


    def setAdminMode(self, mode):
        """Toggle a boolean to show or hide certain protected parameters"""
        self.inAdminMode = mode
        self.configureTab()
        if mode:
            self.pages[0].button_active.setContextMenuPolicy(Qt.CustomContextMenu)
        else:
            self.pages[0].button_active.setContextMenuPolicy(Qt.PreventContextMenu)


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


    #def eventFilter(self, watched, event):
    def showAdminModePopup(self):
        """Trigger admin mode popup"""
        #if watched == self.label_logo and event.type() == QtCore.QEvent.MouseButtonDblClick:
        if not self.inAdminMode:
            self.login = Popup_AdminLogin(master=self, callback=self.setAdminMode)
            self.login.show()
        else:
            self.logout = Popup_AdminLogout(master=self, callback=self.setAdminMode)
            self.logout.show()
        #return super().eventFilter(self, event)



if __name__ == "__main__":
    appctxt = ApplicationContext()
    app = BPLowPowerModuleGUI()
    exit_code = appctxt.app.exec_()
    sys.exit(exit_code)
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(_version.__appid__)
