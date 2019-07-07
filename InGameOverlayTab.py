from PIL import Image, ImageTk, ImageFont, ImageDraw
import tkinter as tk
import os

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
        self.gamenamebox = tk.Entry(master=self.logoframe, textvariable=self.gamenamestring,width=15, justify='center')
        self.gamenamebox.grid(row=3,column=1,padx=15)


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
        if len(name1) > 18:
            self.team1namestring.set(name1[:18])

        name2 = self.team2namestring.get()
        if len(name2) > 18:
            self.team2namestring.set(name2[:18])

        game = self.gamenamestring.get()
        if len(game) > 9:
            self.gamenamestring.set(game[:9])

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
        winscale = 0.66
        winblue_off = Image.open("img/win_blue_transparent.png")
        winblue_off = winblue_off.resize((int(winblue_off.width*winscale),int(winblue_off.height*winscale)),resample=Image.ANTIALIAS)
        winblue_on = Image.open("img/win_blue_on.png")
        winblue_on = winblue_on.resize((int(winblue_on.width*winscale),int(winblue_on.height*winscale)),resample=Image.ANTIALIAS)
        winorange_off = Image.open("img/win_orange_transparent.png")
        winorange_off = winorange_off.resize((int(winorange_off.width*winscale),int(winorange_off.height*winscale)),resample=Image.ANTIALIAS)
        winorange_on = Image.open("img/win_orange_on.png")
        winorange_on = winorange_on.resize((int(winorange_on.width*winscale),int(winorange_on.height*winscale)),resample=Image.ANTIALIAS)

        outframe = Image.new("RGBA",(1920,1080))
        #self.outframe = Image.new("RGBA",(int(self.monitorxstring.get()),int(self.monitorystring.get())))

        ## TOP BANNER
        for j in range(140):
            for i in range(outframe.width):
                outframe.putpixel((i,j),overlayimage.getpixel((i,j)))


        ## TEAM 1
        draw = ImageDraw.Draw(outframe)
        W,H = (525,58)
        teamname1 = self.team1namestring.get()
        if len(teamname1) > 18:
            teamname1 = teamname1[0:18]

        font = ImageFont.truetype("img/GOTHIC.ttf",48)
        w,h = draw.textsize(teamname1, font)
        #print(draw.textsize(teamname1, font))
        draw.text(((W-w)/2+256,(H-h)/2+8),teamname1,(255,255,255,200),font=font)

        ## TEAM 2
        #draw = ImageDraw.Draw(outframe)
        W,H = (525,58)
        teamname2 = self.team2namestring.get()
        if len(teamname2) > 18:
            teamname2 = teamname2[0:18]

        #font = ImageFont.truetype("img/Gotham Thin Regular.otf",48)
        w,h = draw.textsize(teamname2, font)
        #print(draw.textsize(teamname2, font))
        draw.text(((W-w)/2+(1920-W-256),(H-h)/2+8),teamname2,(255,255,255,200),font=font)

        ## GAME DESCRIPTION
        W,H = (960,111)
        gamedesc = self.gamenamestring.get()
        if len(gamedesc) > 9:
            gamedesc = gamedesc[0:9]

        font2 = ImageFont.truetype("img/GOTHICB.TTF", 15)
        w, h = draw.textsize(gamedesc, font2)
        draw.text(((W - w) / 2 + 481, (H - h) / 2 + 55), gamedesc, (255, 255, 255, 255), font=font2)


        ## WIN BOXES
        if ("BO1" in self.gamenamestring.get()
        or "bo1" in self.gamenamestring.get()
        or "B01" in self.gamenamestring.get()
        or "b01" in self.gamenamestring.get()
        or "b1" in self.gamenamestring.get()
        or "B1" in self.gamenamestring.get()):
            numgames = 1
        elif ("BO3" in self.gamenamestring.get()
        or "bo3" in self.gamenamestring.get()
        or "B03" in self.gamenamestring.get()
        or "b03" in self.gamenamestring.get()
        or "b3" in self.gamenamestring.get()
        or "B3" in self.gamenamestring.get()):
            numgames = 2
        elif ("BO5" in self.gamenamestring.get()
        or "bo5" in self.gamenamestring.get()
        or "B05" in self.gamenamestring.get()
        or "b05" in self.gamenamestring.get()
        or "b5" in self.gamenamestring.get()
        or "B5" in self.gamenamestring.get()):
            numgames = 3
        elif ("BO7" in self.gamenamestring.get()
        or "bo7" in self.gamenamestring.get()
        or "B07" in self.gamenamestring.get()
        or "b07" in self.gamenamestring.get()
        or "b7" in self.gamenamestring.get()
        or "B7" in self.gamenamestring.get()):
            numgames = 4
        elif ("BO9" in self.gamenamestring.get()
        or "bo9" in self.gamenamestring.get()
        or "B09" in self.gamenamestring.get()
        or "b09" in self.gamenamestring.get()
        or "b9" in self.gamenamestring.get()
        or "B9" in self.gamenamestring.get()):
            numgames = 5
        else:
            numgames = 0

        for g in range(numgames):
            for j in range(winblue_off.height):
                for i in range(winblue_off.width):
                    outframe.putpixel((i+745-55*g,j+75),winblue_off.getpixel((i,j)))

            for l in range(winorange_off.height):
                for k in range(winorange_off.width):
                    outframe.putpixel((k + 1116 + 55 * g, l + 75), winorange_off.getpixel((k, l)))

        ##WINS
        for x in range(int(self.team1winspinbox.get())):
            for j in range(winblue_on.height):
                for i in range(winblue_on.width):
                    outframe.putpixel((i + 745 - 55 * x, j + 75), winblue_on.getpixel((i, j)))


        for y in range(int(self.team2winspinbox.get())):
            for j in range(winorange_on.height):
                for i in range(winorange_on.width):
                    outframe.putpixel((i + 1116 + 55 * y, j + 75), winorange_on.getpixel((i, j)))


        ## RESIZE
        #if not os.path.exists("/out"):
        #    os.makedirs("/out")

        outframe = outframe.resize((int(self.monitorxstring.get()),int(self.monitorystring.get())),resample=Image.ANTIALIAS)
        outframe.save("output/ingame_current.png")

        return outframe