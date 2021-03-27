from PIL import Image, ImageTk, ImageFont, ImageDraw
import tkinter as tk
import os
import copy
from operator import add

MAX_TEAMNAME_LENGTH = 16
MAX_MATCHNAME_LENGTH = 20

OFFSET_X_TEAMNAMES = 192
OFFSET_Y_TEAMNAMES = 11

OFFSET_Y_MATCHNAME = 88

SPACING_X_WINBOXES = 45
OFFSET_Y_WINBOXES = 80
OFFSET_X_BLUEWINS = 745
OFFSET_X_ORANGEWINS = 1093

class InGameOverlayTab(tk.Frame):
    def __init__(self, root):
        super().__init__()
        self.root = root
        ## BLUE TEAM
        self.blueteamframe = tk.Frame(master=self, relief=tk.RIDGE, borderwidth=2, width = 200, height=200, padx=10, pady=10)
        self.blueteamframe.grid(row=0,column=0)

        #tk.Label(text="Blue Team", fg="blue").grid(row=0,column=0, columnspan=2)
        self.blueteamfile = Image.open("img/blueteambar.png")
        self.blueteamfile = ImageTk.PhotoImage(self.blueteamfile.resize((int(self.blueteamfile.width/2),int(self.blueteamfile.height/2)),Image.ANTIALIAS))
        self.blueteamiconlabel = tk.Label(master=self.blueteamframe, image=self.blueteamfile)
        #rhiconlabel.image = rhicon
        self.blueteamiconlabel.grid(row=0,column=0,padx=10,columnspan=2)

        self.team1namestring = tk.StringVar()
        self.team1namestring.set("Blue Team")
        self.team1namestring.trace('w', self.limitStrings)
        self.team1namebox = tk.Entry(master=self.blueteamframe, textvariable=self.team1namestring,width=25, justify='center')
        self.team1namebox.grid(row=1,column=0,padx=10, pady=10, columnspan=2)

        tk.Label(master=self.blueteamframe, text="Wins:").grid(row=2,column=0, sticky=tk.E)

        self.team1winspinbox = tk.Spinbox(master=self.blueteamframe, from_=0, to=5, width=5)
        self.team1winspinbox.grid(row=2,column=1,padx=10,sticky=tk.W)


        ## ORANGE TEAM
        self.orangeteamframe = tk.Frame(master=self, relief=tk.RIDGE, borderwidth=2, width=200, height=200, padx=10,
                                      pady=10)
        self.orangeteamframe.grid(row=0, column=2)

        # tk.Label(text="Blue Team", fg="blue").grid(row=0,column=0, columnspan=2)
        self.orangeteamfile = Image.open("img/orangeteambar.png")
        self.orangeteamfile = ImageTk.PhotoImage(self.orangeteamfile.resize((int(self.orangeteamfile.width / 2), int(self.orangeteamfile.height / 2)),Image.ANTIALIAS))
        self.orangeteamiconlabel = tk.Label(master=self.orangeteamframe, image=self.orangeteamfile)
        # rhiconlabel.image = rhicon
        self.orangeteamiconlabel.grid(row=0, column=3, padx=10, columnspan=2)

        self.team2namestring = tk.StringVar()
        self.team2namestring.set("Orange Team")
        self.team2namestring.trace('w', self.limitStrings)
        self.team2namebox = tk.Entry(master=self.orangeteamframe, textvariable=self.team2namestring, width=25, justify='center')
        self.team2namebox.grid(row=1, column=3, padx=10, pady=10, columnspan=2)

        tk.Label(master=self.orangeteamframe, text="Wins:").grid(row=2, column=3, sticky=tk.E)

        self.team2winspinbox = tk.Spinbox(master=self.orangeteamframe, from_=0, to=5, width=5)
        self.team2winspinbox.grid(row=2, column=4, padx=10, sticky=tk.W)


        ## GAME CONFIG
        self.logoframe = tk.Frame(master=self, width=200, height=200)
        self.logoframe.grid(row=0, column=1)

        self.rhiconfile = Image.open("img/rhicon.png")
        self.rhicon = ImageTk.PhotoImage(self.rhiconfile.resize((100,100),Image.ANTIALIAS))
        self.rhiconlabel = tk.Label(master=self.logoframe, image=self.rhicon)
        #rhiconlabel.image = rhicon
        self.rhiconlabel.grid(row=0,column=1)

        self.gamenamestring = tk.StringVar()
        self.gamenamestring.set("R1W - BO3")
        self.gamenamestring.trace('w', self.limitStrings)
        self.gamenamebox = tk.Entry(master=self.logoframe, textvariable=self.gamenamestring,width=24, justify='center')
        self.gamenamebox.grid(row=3,column=1,padx=5)


        ## SCREEN INFORMATION
        self.monitorframe = tk.Frame(master=self, width=200, height=200, pady=10)
        self.monitorframe.grid(row=1, column=1,sticky=tk.S)

        tk.Label(master=self.monitorframe, text="Resolution:").grid(row=96,column=1)

        self.monitorxstring = tk.StringVar()
        self.monitorxstring.set("1920")
        self.monitorxbox = tk.Entry(master=self.monitorframe, textvariable=self.monitorxstring, width=8, justify='center')
        self.monitorxbox.grid(row=97,column=1,padx=15)

        self.monitorystring = tk.StringVar()
        self.monitorystring.set("1080")
        self.monitorybox = tk.Entry(master=self.monitorframe, textvariable=self.monitorystring, width=8, justify='center')
        self.monitorybox.grid(row=98, column=1,padx=15)


        ## BUTTONS
        self.buttonframe = tk.Frame(master=self, width=200, height=200,pady=46)
        self.buttonframe.grid(row=3, column=0, columnspan=3, sticky=tk.S)

        self.resetbuttonimage = tk.PhotoImage(file="img/resetbutton.png")
        self.resetbutton = tk.Button(master=self.buttonframe, image=self.resetbuttonimage,command=self.ResetValues)
        self.resetbutton.config(image=self.resetbuttonimage)
        self.resetbutton.grid(row=99,column=0,padx=30,pady=10)

        self.viewbuttonimage = tk.PhotoImage(file="img/viewbutton.png")
        self.viewbutton = tk.Button(master=self.buttonframe, image=self.viewbuttonimage,command=self.ShowImage)
        self.viewbutton.grid(row=99,column=2,padx=30,pady=10)

        self.generatebuttonimage = tk.PhotoImage(file="img/generatebutton.png")
        self.generatebutton = tk.Button(master=self.buttonframe, image=self.generatebuttonimage,command=self.GenerateImage)
        self.generatebutton.grid(row=99,column=1,padx=30,pady=10)

        #self.quitbutton = tk.Button(self, text="Quit", command=self.quit)
        #self.quitbutton.grid(row=100,column=3,pady=10)

        self.bind("<Button-1>", lambda event: self.focus_set())
        self.blueteamframe.bind("<Button-1>", lambda event: self.focus_set())
        self.orangeteamframe.bind("<Button-1>", lambda event: self.focus_set())
        self.blueteamiconlabel.bind("<Button-1>", lambda event: self.focus_set())
        self.orangeteamiconlabel.bind("<Button-1>", lambda event: self.focus_set())

        self.rhiconlabel.bind("<Button-1>", lambda event: self.focus_set())
        self.resetbutton.bind("<Button-1>", lambda event: self.focus_set())
        self.viewbutton.bind("<Button-1>", lambda event: self.focus_set())
        self.generatebutton.bind("<Button-1>", lambda event: self.focus_set())

    def limitStrings(self, *args):
        name1 = self.team1namestring.get()
        if len(name1) > MAX_TEAMNAME_LENGTH:
            self.team1namestring.set(name1[:MAX_TEAMNAME_LENGTH])

        name2 = self.team2namestring.get()
        if len(name2) > MAX_TEAMNAME_LENGTH:
            self.team2namestring.set(name2[:MAX_TEAMNAME_LENGTH])

        game = self.gamenamestring.get()
        if len(game) > MAX_MATCHNAME_LENGTH:
            self.gamenamestring.set(game[:MAX_MATCHNAME_LENGTH])

        return

    def ResetValues(self):
        self.team1namestring.set("Blue Team")
        self.team2namestring.set("Orange Team")
        self.team1winspinbox.delete(0,"end")
        self.team1winspinbox.insert(0,"0")
        self.team2winspinbox.delete(0,"end")
        self.team2winspinbox.insert(0,"0")
        self.gamenamestring.set("BO3")
        self.monitorxstring.set("1920")
        self.monitorystring.set("1080")
        return

    def ShowImage(self):
        self.outframe = self.GenerateImage()
        self.outframe.show()
        return

    def GenerateImage(self):
        overlayimage = Image.open("img/ingame_blank.png")
        winblue_off = Image.open("img/win_blue_off.png")
        winblue_on = Image.open("img/win_blue_on.png")
        winorange_off = Image.open("img/win_orange_off.png")
        winorange_on = Image.open("img/win_orange_on.png")

        outframe = copy.deepcopy(overlayimage)

        W = int(self.monitorxstring.get())
        H = int(self.monitorystring.get())

        ## TEAM 1
        draw = ImageDraw.Draw(outframe)
        teamname1 = self.team1namestring.get().upper()
        if len(teamname1) > MAX_TEAMNAME_LENGTH:
            teamname1 = teamname1[0:MAX_TEAMNAME_LENGTH]

        font = ImageFont.truetype("img/ChangaOne-Regular.ttf",44)
        w,h = draw.textsize(teamname1, font)
        draw.text((W/2 - w - OFFSET_X_TEAMNAMES, OFFSET_Y_TEAMNAMES), teamname1, (255,255,255,220), font=font)

        ## TEAM 2
        teamname2 = self.team2namestring.get().upper()
        if len(teamname2) > MAX_TEAMNAME_LENGTH:
            teamname2 = teamname2[0:MAX_TEAMNAME_LENGTH]

        w,h = draw.textsize(teamname2, font)
        draw.text((W/2 + OFFSET_X_TEAMNAMES, OFFSET_Y_TEAMNAMES), teamname2, (255,255,255,220), font=font)

        ## GAME DESCRIPTION
        gamedesc = self.gamenamestring.get().upper()
        if len(gamedesc) > MAX_MATCHNAME_LENGTH:
            gamedesc = gamedesc[0:MAX_MATCHNAME_LENGTH]

        font2 = ImageFont.truetype("img/Montserrat-Black.TTF", 16)
        w, h = draw.textsize(gamedesc, font2)
        draw.text(((W - w)/2, OFFSET_Y_MATCHNAME), gamedesc, (255, 255, 255, 255), font=font2)


        ## WIN BOXES
        if "BO1" in self.gamenamestring.get().upper():
            numgames = 1
        elif "BO3" in self.gamenamestring.get().upper():
            numgames = 2
        elif "BO5" in self.gamenamestring.get().upper():
            numgames = 3
        elif "BO7" in self.gamenamestring.get().upper():
            numgames = 4
        elif "BO9" in self.gamenamestring.get().upper():
            numgames = 5
        else:
            numgames = 0

        for g in range(numgames):
            for j in range(winblue_off.height):
                for i in range(winblue_off.width):
                    outpixel = outframe.getpixel((i+OFFSET_X_BLUEWINS - SPACING_X_WINBOXES*g, j+OFFSET_Y_WINBOXES))
                    newpixel = winblue_off.getpixel((i,j))
                    alphascaled = tuple(map(lambda x: int(x/(255/(outpixel[-1]+1))), outpixel))
                    newpixel = tuple(map(add, newpixel, alphascaled))
                    outframe.putpixel((i+OFFSET_X_BLUEWINS - SPACING_X_WINBOXES*g, j+OFFSET_Y_WINBOXES), newpixel)

            for l in range(winorange_off.height):
                for k in range(winorange_off.width):
                    outpixel = outframe.getpixel((k+OFFSET_X_ORANGEWINS + SPACING_X_WINBOXES*g, l+OFFSET_Y_WINBOXES))
                    newpixel = winorange_off.getpixel((k,l))
                    alphascaled = tuple(map(lambda x: int(x/(255/(outpixel[-1]+1))), outpixel))
                    newpixel = tuple(map(add, newpixel, alphascaled))
                    outframe.putpixel((k+OFFSET_X_ORANGEWINS + SPACING_X_WINBOXES*g, l+OFFSET_Y_WINBOXES), newpixel)

        ##WINS
        for x in range(int(self.team1winspinbox.get())):
            for j in range(winblue_on.height):
                for i in range(winblue_on.width):
                    outpixel = outframe.getpixel((i + OFFSET_X_BLUEWINS - SPACING_X_WINBOXES * x, j + OFFSET_Y_WINBOXES))
                    newpixel = winblue_on.getpixel((i, j))
                    alphascaled = tuple(map(lambda x: int(x / (255 / (outpixel[-1] + 1))), outpixel))
                    newpixel = tuple(map(add, newpixel, alphascaled))
                    outframe.putpixel((i + OFFSET_X_BLUEWINS - SPACING_X_WINBOXES * x, j + OFFSET_Y_WINBOXES), newpixel)


        for y in range(int(self.team2winspinbox.get())):
            for j in range(winorange_on.height):
                for i in range(winorange_on.width):
                    outpixel = outframe.getpixel((i + OFFSET_X_ORANGEWINS + SPACING_X_WINBOXES * y, j + OFFSET_Y_WINBOXES))
                    newpixel = winorange_on.getpixel((i, j))
                    alphascaled = tuple(map(lambda x: int(x / (255 / (outpixel[-1] + 1))), outpixel))
                    newpixel = tuple(map(add, newpixel, alphascaled))
                    outframe.putpixel((i + OFFSET_X_ORANGEWINS + SPACING_X_WINBOXES * y, j + OFFSET_Y_WINBOXES), newpixel)


        ## RESIZE
        #if not os.path.exists("/out"):
        #    os.makedirs("/out")

        outframe = outframe.resize((int(self.monitorxstring.get()),int(self.monitorystring.get())),resample=Image.ANTIALIAS)
        outframe.save("output/ingame_current.png")

        return outframe