from PIL import Image, ImageTk, ImageFont, ImageDraw
import tkinter as tk
from tkinter import ttk, Tk
from InGameOverlayTab import InGameOverlayTab
from CastersOverlayTab import CastersOverlayTab
from InterviewOverlayTab import InterviewOverlayTab

color_inactive = "#E8E8E8"
color_active = "#F49C23"

class OverlayGenerator(tk.Frame):
    def __init__(self, master=None):
        self.root = Tk()
        self.root.resizable(False, False)

        tk.Frame.__init__(self, master=self.root)

        style = ttk.Style()
        style.theme_create("MyStyle", parent="alt", settings={
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
            "TNotebook.Tab": {
                "focus" : {},
                "configure": {"width": 10, "background": color_inactive, "font": ('Corbel',14)},
                "map": {"background": [("selected", color_active)],
                        "expand": [("selected", [1, 1, 1, 0])]}}})

        style.theme_use("MyStyle")

        self.grid()
        self.createWidgets()

    def createWidgets(self):
        self.notebook = ttk.Notebook(self.master)

        self.tab1 = InGameOverlayTab(self.notebook)
        self.notebook.add(self.tab1, text="In Game")

        self.tab2 = CastersOverlayTab(self.notebook)
        self.notebook.add(self.tab2, text="Casters")

        self.tab3 = InterviewOverlayTab(self.notebook)
        self.notebook.add(self.tab3, text="Interview")

        self.notebook.grid(row=0,column=0,sticky=tk.W)


#casters = Image.open("img/casters.png")
#casters.show()

if __name__ == "__main__":
    app = OverlayGenerator()
    app.root.title("Ranked Hoops Overlay Generator")
    app.root.iconbitmap("img/favicon.ico")
    app.mainloop()