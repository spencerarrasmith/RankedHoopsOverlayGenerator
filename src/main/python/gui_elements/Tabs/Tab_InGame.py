from PyQtRH.PyQtRH import *
from PyQtRH.widgetStyles import *

import datetime

class Tab_InGame(QRHTab):
    def __init__(self, master=None, serial=None, protocol=None, index=0):
        super().__init__(master=master, serial=serial, protocol=protocol,
                         title="In Game",
                         icon="images/game_32.png",
                         index=index,
                         widgets=[

                         ]
                         )
        self.ReadAll()
        self.button_active.setContextMenuPolicy(Qt.PreventContextMenu)