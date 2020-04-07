from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from gui_elements.gui_textblocks import *
from PyQtRH.PyQtRH import QRHTextPopup

import os, subprocess

class RHMenuBar(QMenuBar):
    """The dropdown menu bar at the top of the window"""
    def __init__(self, master=None, serial=None, protocol=None):
        super().__init__()
        self.master = master
        self.serial = serial
        self.protocol = protocol

        names = ['&File', '&Serial', 'Se&ttings', '&Help']
        self.menus = {}
        self.menuitems = {}
        for name in names:
            self.menus[name] = self.addMenu(name)
            self.menuitems[name] = []

        self.actions = {}

    # Create File menu actions
        self.createAction(master=self, menu=names[0], text='&Open Config File', callback=Callback_FileOpenConfig)
        self.createAction(master=self, menu=names[0], text='&Save Tab to File', callback=Callback_FileSaveTab)
        self.createAction(master=self, menu=names[0], text='Save &All Tabs', callback=Callback_FileSaveAllTabs)
        self.createAction(master=self, menu=names[0], text='Load &Tab from File', callback=Callback_FileLoadTab)
        self.createAction(master=self, menu=names[0], text='&Load All Tabs', callback=Callback_FileLoadAllTabs)
        self.createAction(master=self, menu=names[0], text='&Exit', callback=Callback_FileExit)

    # Create Serial menu actions
        self.createAction(master=self, menu=names[1], text='Dis&connect', callback=Callback_SerialConnect)
        self.createAction(master=self, menu=names[1], text='&Write All Tabs', callback=Callback_SerialWriteAll)
        self.createAction(master=self, menu=names[1], text='&Read All Tabs', callback=Callback_SerialReadAll)
        self.createAction(master=self, menu=names[1], text='&Info', callback=Callback_SerialInfo)

    # Create Help menu actions
        self.createAction(master=self, menu=names[2], text='&Admin Mode', callback=Callback_SettingsAdminMode)

    # Create Help menu actions
        self.createAction(master=self, menu=names[3], text='&Terms of Use', callback=Callback_HelpTermsOfUse)
        self.createAction(master=self, menu=names[3], text='&About', callback=Callback_HelpAbout)


    # Populate File Menu
        self.menus[names[0]].addAction(self.menuitems[names[0]][0])
        self.menus[names[0]].addSeparator()
        self.menus[names[0]].addAction(self.menuitems[names[0]][1])
        self.menus[names[0]].addAction(self.menuitems[names[0]][2])
        self.menus[names[0]].addSeparator()
        self.menus[names[0]].addAction(self.menuitems[names[0]][3])
        self.menus[names[0]].addAction(self.menuitems[names[0]][4])
        self.menus[names[0]].addSeparator()
        self.menus[names[0]].addAction(self.menuitems[names[0]][5])

    # Populate Serial Menu
        self.menus[names[1]].addAction(self.menuitems[names[1]][0])
        self.menus[names[1]].addSeparator()
        self.menus[names[1]].addAction(self.menuitems[names[1]][1])
        self.menus[names[1]].addAction(self.menuitems[names[1]][2])
        self.menus[names[1]].addSeparator()
        self.menus[names[1]].addAction(self.menuitems[names[1]][3])

    # Populate Settings Menu
        self.menus[names[2]].addAction(self.menuitems[names[2]][0])

    # Populate Help Menu
        self.menus[names[3]].addAction(self.menuitems[names[3]][0])
        self.menus[names[3]].addAction(self.menuitems[names[3]][1])


    def createAction(self, master=None, menu="", text="", callback=None):
        """Create a QAction and add it to a dictionary of all callbacks, and add it to a list of actions in a
        dictionary keyed by menu name"""
        self.actions[text] = callback(master=master, text=text)
        self.menuitems[menu].append(self.actions[text])


class Callback_Test(QAction):
    def __init__(self, master=None, text=''):
        super().__init__(text=text)
        self.master = master
        self.triggered.connect(self.action)

    def action(self):
        print("Test")

class Callback_FileOpenConfig(QAction):
    def __init__(self, master=None, text=''):
        super().__init__(text=text)
        self.master = master
        self.triggered.connect(self.action)

    def action(self):
        args = ['notepad', self.master.master.get_resource('config.txt')]
        subprocess.Popen(args)

class Callback_FileSaveTab(QAction):
    def __init__(self, master=None, text=''):
        super().__init__(text=text)
        self.master = master
        self.triggered.connect(self.action)

    def action(self):
        self.master.master.pages[self.master.master.tabs.currentIndex()].SaveToFile()

class Callback_FileSaveAllTabs(QAction):
    def __init__(self, master=None, text=''):
        super().__init__(text=text)
        self.master = master
        self.triggered.connect(self.action)

    def action(self):
        for tab in self.master.master.pages:
            tab.SaveToFile()

class Callback_FileLoadTab(QAction):
    def __init__(self, master=None, text=''):
        super().__init__(text=text)
        self.master = master
        self.triggered.connect(self.action)

    def action(self):
        self.master.master.pages[self.master.master.tabs.currentIndex()].LoadFromFile()

class Callback_FileLoadAllTabs(QAction):
    def __init__(self, master=None, text=''):
        super().__init__(text=text)
        self.master = master
        self.triggered.connect(self.action)

    def action(self):
        for tab in self.master.master.pages:
            tab.LoadFromFile()

class Callback_FileExit(QAction):
    def __init__(self, master=None, text=''):
        super().__init__(text=text)
        self.master = master
        self.triggered.connect(self.action)

    def action(self):
        self.master.serial.serial_port_close()
        self.master.master.window.close()



class Callback_SerialConnect(QAction):
    def __init__(self, master=None, text=''):
        super().__init__(text=text)
        self.master = master
        if self.master.serial.isConnected:
            self.setText('Dis&connect')
        else:
            self.setText('&Connect')

        self.triggered.connect(self.action)


    def action(self):
        if self.master.serial.isConnected:
            self.master.serial.serial_port_close()
            self.setText('&Connect')
        else:
            self.master.serial.findConnection()
            if self.master.serial.isConnected:
                self.master.serial.serial_port_open()
                self.setText('Dis&connect')
            else:
                print("Unable To Connect")
                self.setText('&Connect')


class Callback_SerialReadAll(QAction):
    def __init__(self, master=None, text=''):
        super().__init__(text=text)
        self.master = master
        if self.master.serial.isConnected:
            self.setDisabled(False)
        else:
            self.setDisabled(True)

        self.triggered.connect(self.action)

        self.master.protocol.parameters["COMMPORT"].variable.bind_to(lambda e: self.setDisabled(self.master.protocol.parameters["COMMPORT"].variable.value == "None"))


    def action(self):
        if self.master.serial.isConnected:
            for tab in self.master.master.pages:
                tab.ReadAll()
                self.popup = QRHTextPopup(title=''.join(self.text.split('&')), text="Please wait 30 seconds...")

                self.popup.show()
                self.popup.setFixedHeight(self.popup.height())
                self.popup.setFixedWidth(self.popup.width())


class Callback_SerialWriteAll(QAction):
    def __init__(self, master=None, text=''):
        super().__init__(text=text)
        self.master = master
        if self.master.serial.isConnected:
            self.setDisabled(False)
        else:
            self.setDisabled(True)

        self.triggered.connect(self.action)

        self.master.protocol.parameters["COMMPORT"].variable.bind_to(lambda e: self.setDisabled(self.master.protocol.parameters["COMMPORT"].variable.value == "None"))


    def action(self):
        if self.master.serial.isConnected:
            for tab in self.master.master.pages:
                tab.WriteAll()


class Callback_SerialInfo(QAction):
    def __init__(self, master=None, text=''):
        super().__init__(text=text)
        self.master = master
        self.text = text
        self.triggered.connect(self.action)

    def action(self):
        self.popup = QRHTextPopup(title=''.join(self.text.split('&')), text=text_serial)

        self.popup.show()
        self.popup.setFixedHeight(self.popup.height())
        self.popup.setFixedWidth(self.popup.width())



class Callback_SettingsAdminMode(QAction):
    def __init__(self, master=None, text=''):
        super().__init__(text=text)
        self.master = master
        self.triggered.connect(self.action)

    def action(self):
        self.master.master.showAdminModePopup()



class Callback_HelpTermsOfUse(QAction):
    def __init__(self, master=None, text=''):
        super().__init__(text=text)
        self.master = master
        self.text = text
        self.triggered.connect(self.action)

    def action(self):
        args = ['notepad', self.master.master.get_resource('eula.txt')]
        subprocess.Popen(args)

class Callback_HelpAbout(QAction):
    def __init__(self, master=None, text=''):
        super().__init__(text=text)
        self.master = master
        self.text = text
        self.triggered.connect(self.action)

    def action(self):
        self.popup = QRHTextPopup(title=''.join(self.text.split('&')), text=text_about)

        self.popup.show()
        self.popup.setFixedHeight(self.popup.height())
        self.popup.setFixedWidth(self.popup.width())