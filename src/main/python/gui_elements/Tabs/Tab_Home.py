from PyQtRH.PyQtRH import *
from PyQtRH.widgetStyles import *

import datetime

class Tab_Home(QRHTab):
    def __init__(self, master=None, serial=None, protocol=None, index=0):
        super().__init__(master=master, serial=serial, protocol=protocol,
                         title="Home",
                         icon="images/home_32.png",
                         index=index,
                         widgets=[

                         ]
                         )
        self.ReadAll()
        self.button_active.setContextMenuPolicy(Qt.PreventContextMenu)