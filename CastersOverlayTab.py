from PIL import Image, ImageTk, ImageFont, ImageDraw
import tkinter as tk

class CastersOverlayTab(tk.Frame):
    def __init__(self, root):
        super().__init__()
        self.root = root

    ## TOURNAMENT TYPE
        self.tournamenttypeframe = tk.Frame(master=self)
        self.tournamenttypeframe.grid(row=0,column=1)

        tk.Label(master=self.tournamenttypeframe,text="Tournament Type").grid(row=0,column=0,sticky=tk.N)

        self.tournamenttypestring = tk.StringVar()
        self.tournamenttypestring.set("PC + PS4")
        self.tournamenttypemenu = tk.OptionMenu(self.tournamenttypeframe, self.tournamenttypestring, "PC + PS4", "PC + XBOX + SWITCH", "PC ONLY")
        self.tournamenttypemenu.grid(row=1,column=0)

    ## CASTERS
        self.logoframe = tk.Frame(master=self, width=800, height=200)
        self.logoframe.grid(row=1, column=0,columnspan=3)

        tk.Label(master=self.logoframe,text="Caster 1").grid(row=0, column=0, sticky=tk.S)
        self.leftcasterstring = tk.StringVar()
        self.leftcasterentry = tk.Entry(master=self.logoframe,textvariable = self.leftcasterstring,width=30, justify='center')
        self.leftcasterentry.grid(row=1,column=0,padx=80)

        self.leftcasterhandlestring = tk.StringVar()
        self.leftcasterhandleentry = tk.Entry(master=self.logoframe,textvariable = self.leftcasterhandlestring,width=20, justify='center')
        self.leftcasterhandleentry.grid(row=2,column=0,sticky=tk.NE,padx=80)

        self.rhiconfile = Image.open("img/rhicon.png")
        self.rhicon = ImageTk.PhotoImage(self.rhiconfile.resize((100, 100), Image.ANTIALIAS))
        self.rhiconlabel = tk.Label(master=self.logoframe, image=self.rhicon)
        # rhiconlabel.image = rhicon
        self.rhiconlabel.grid(row=0, column=1,rowspan=3,pady=10)

        tk.Label(master=self.logoframe,text="Caster 2").grid(row=0,column=2, sticky=tk.S)
        self.rightcasterstring = tk.StringVar()
        self.rightcasterentry = tk.Entry(master=self.logoframe,textvariable = self.rightcasterstring,width=30, justify='center')
        self.rightcasterentry.grid(row=1,column=2,padx=80)

        self.rightcasterhandlestring = tk.StringVar()
        self.rightcasterhandleentry = tk.Entry(master=self.logoframe,textvariable = self.rightcasterhandlestring,width=20, justify='center')
        self.rightcasterhandleentry.grid(row=2,column=2,sticky=tk.NW,padx=80)


    ## SCREEN INFORMATION
        self.monitorframe = tk.Frame(master=self, width=200, height=200, pady=10)
        self.monitorframe.grid(row=2, column=1)

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
        self.buttonframe = tk.Frame(master=self, width=200, height=200)
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

    def ResetValues(self):
        self.tournamenttypestring.set("PC + PS4")
        self.leftcasterstring.set("")
        self.leftcasterhandlestring.set("")
        self.rightcasterstring.set("")
        self.rightcasterhandlestring.set("")
        self.monitorxstring.set("1920")
        self.monitorystring.set("1080")
        return

    def ShowImage(self):
        self.outframe = self.GenerateImage()
        self.outframe.show()
        return

    def GenerateImage(self):
        overlaybase = Image.open("img/pregame_blank.png")

        outframe = Image.new("RGBA", (1920, 1080))

    ## BANNERS
        for j in range(170):
            for i in range(outframe.width):
                outframe.putpixel((i,j),overlaybase.getpixel((i,j)))

        for j in range(680,1000):
            for i in range(outframe.width):
                outframe.putpixel((i, j), overlaybase.getpixel((i, j)))

    ## TOURNAMENT TYPE
        draw = ImageDraw.Draw(outframe)
        W, H = (400, 100)
        tournamentname = self.tournamenttypestring.get()

        font = ImageFont.truetype("img/Futura Extra Bold.ttf", 50)
        w, h = draw.textsize(tournamentname, font)
        # print(draw.textsize(teamname1, font))
        draw.text(((W - w) / 2 + 760, (H - h) / 2 + 200), tournamentname, (255, 255, 255, 255), font=font)


    ## CASTERS
        W, H = (580, 58)
        caster1name = self.leftcasterstring.get()
        if len(caster1name) > 16:
            caster1name = caster1name[0:16]

        font = ImageFont.truetype("img/GOTHICB.ttf", 60)
        w, h = draw.textsize(caster1name, font)
        draw.text(((W - w) / 2 + 256, (H - h) / 2 + 845), caster1name, (255, 255, 255, 240), font=font)

        caster2name = self.rightcasterstring.get()
        if len(caster2name) > 16:
            caster2name = caster2name[0:16]

        w, h = draw.textsize(caster2name, font)
        draw.text(((W - w) / 2 + (1920 - W - 256), (H - h) / 2 + 845), caster2name, (255, 255, 255, 240), font=font)

        font = ImageFont.truetype("img/GOTHICB.ttf", 30)
        caster1handle = self.leftcasterhandlestring.get()
        if len(caster1handle) > 16:
            caster1handle = caster1handle[0:16]

        w, h = draw.textsize(caster1handle, font)
        draw.text(((W - w) / 2 + 306, (H - h) / 2 + 928), caster1handle, (255, 255, 255, 240), font=font)

        caster2handle = self.rightcasterhandlestring.get()
        if len(caster2handle) > 16:
            caster2handle = caster2handle[0:16]

        w, h = draw.textsize(caster2handle, font)
        draw.text(((W - w) / 2 + (1920 - W - 306), (H - h) / 2 + 928), caster2handle, (255, 255, 255, 240), font=font)


    ## RESIZE
        #if not os.path.exists("/out"):
        #    os.makedirs("/out")

        outframe = outframe.resize((int(self.monitorxstring.get()),int(self.monitorystring.get())),resample=Image.ANTIALIAS)
        outframe.save("output/casters_current.png")

        return outframe