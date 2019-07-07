import tkinter as tk
from tkinter import font, ttk


class PopupWindow(tk.Toplevel):
    def __init__(self, title="", text=""):
        self.window = super()
        super().__init__()

        self.title = title

        self.resizable(False, False)
        self.wm_title(self.title)
        self.iconbitmap("img/favicon_sls_32.ico")

        self.text = tk.Text(master=self, height=text.count("\n"), width=max([len(line) for line in text.split("\n")])+1)
        self.text.insert(1.0, text)
        self.text.configure(state='disabled')
        self.text.grid(row=0, column=0, sticky=tk.W)

class BlockFrame(tk.Frame):
    def __init__(self, root=None, row=0, column=0, text=""):
        self.frame = super()
        super().__init__(master=root, relief=tk.GROOVE, borderwidth=4)

        self.row = row
        self.column = column
        self.text = text
        self.grid()

        self.frame.grid(row=self.row, column=self.column, columnspan=6, sticky='EW')
        self.grid_columnconfigure(self.column, uniform='smallframewidth', minsize=220)
        self.grid_columnconfigure(self.column+1, uniform='smallframewidth', minsize=220)
        self.grid_columnconfigure(self.column+2, uniform='smallframewidth', minsize=220)

        self.frame.bind("<Button-1>", lambda event: self.focus_set())

        self.label = tk.Label(master=self, text=self.text, font='Arial 16')
        self.label.grid(row=0, column=0, sticky='W')


class EntryFrame(tk.Frame):
    def __init__(self, master=None, serial=None, row=0, column=0, text="", command="", variable=None):
        self.frame = super()
        super().__init__(master=master)

        self.master = master
        self.serial = serial
        self.row = row
        self.column = column
        self.text = text
        self.command = command
        self.variable = variable

        self.grid(row=self.row, column=self.column, sticky='EW')

        self.frame = tk.Frame(master=self.master, relief=tk.GROOVE, borderwidth=2)#, width=239, height=30)
        self.frame.grid(row=self.row, column=self.column, sticky='NSEW', padx=1, pady=1)
        self.frame.grid_columnconfigure(0, weight=1, uniform='smallframelabel')
        self.frame.grid_columnconfigure(1, weight=1, uniform='smallframecontrol')
        self.frame.grid_rowconfigure(0, weight=1, uniform='smallframeheight', minsize=28)

        self.label = tk.Label(master=self.frame, text=self.text, justify='left')
        self.label.grid(row=0, column=0, sticky='W', padx=5)
        #self.grid_columnconfigure(0, weight=1)

        self.vcmd = (self.register(self.validateNum), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        self.entry = tk.Entry(master=self.frame, textvariable=self.variable, justify='right', width=12, validate='key', validatecommand=self.vcmd)
        self.entry.grid(row=0, column=1, padx=5, pady=3, sticky='E')
        #self.grid_columnconfigure(1, minsize=100)

        self.frame.bind("<Button-1>", lambda event: self.entry.focus_set())
        self.frame.bind("<Button-1>", lambda event: self.entry.icursor(tk.END), add='+')

        self.label.bind("<Button-1>", lambda event: self.entry.focus_set())
        self.label.bind("<Button-1>", lambda event: self.entry.icursor(tk.END), add='+')

        self.entry.bind("<FocusIn>", lambda event: self.frame.configure(highlightbackground='blue', highlightcolor='blue', highlightthickness=1, borderwidth=1))
        self.entry.bind("<FocusOut>", self.validateNonEmpty)
        self.entry.bind("<FocusOut>", lambda event: self.frame.configure(highlightbackground=None, highlightthickness=0,
                                                                         borderwidth=2), add='+')
        self.entry.bind("<FocusOut>", self.sendCommand, add='+')

        #self.entry.bind("<Escape>", lambda event: self.master.focus_set())
        self.entry.bind("<Button-1>", lambda event: self.entry.focus_set())
        self.entry.bind("<Return>", self.sendCommand)

        self.entry.bind("<Up>", lambda event: self.moveValue(direction=1))
        self.entry.bind("<Down>", lambda event: self.moveValue(direction=-1))

    def sendCommand(self, event=None):
        self.serial.sendSerial(message="set " + self.command + " " + self.entry.get())

    def validateNum(self, action, index, value_if_allowed,
                       prior_value, text, validation_type, trigger_type, widget_name):
        if len(text) > 1:
            try:
                float(value_if_allowed + "0")
                return True
            except ValueError:
                return False

        if self.variable.__class__.__name__ == "DoubleVar":
            if text in '0123456789-+.eE':
                try:
                    float(value_if_allowed+"0")
                    return True
                except ValueError:
                    return False
            else:
                return False

        if self.variable.__class__.__name__ == "IntVar":
            if text in '0123456789-':
                try:
                    float(value_if_allowed+"0")
                    return True
                except ValueError:
                    return False
            else:
                return False

    def validateNonEmpty(self, event=None):
        if len(self.entry.get()) < 1:
            self.variable.set(0)

    def moveValue(self, event=None, direction=0):
        if self.variable.__class__.__name__ == "IntVar":
            num_digits = len(str(self.variable.get()))
            pos_cursor = self.entry.index(tk.INSERT)
            if (pos_cursor<=1 and self.variable.get() < 0) or pos_cursor==0:
                return
            self.entry.selection_range(0, self.entry.index(tk.INSERT))
            step = 10**(num_digits-pos_cursor)
            self.variable.set(self.variable.get() + (direction * step))
            self.sendCommand()

        if self.variable.__class__.__name__ == "DoubleVar":
            str_entry = str(self.entry.get())
            pos_e = len(str_entry)
            pos_dec = len(str_entry)
            e = ""
            str_exp = ""

            has_dec = False
            has_e = False

            if "E" in str(str_entry):
                e = "E"
                pos_e = str_entry.find(e)
                str_exp = str_entry.split(e)[1]
                has_e = True

            if "e" in str(self.entry.get()):
                e = "e"
                pos_e = str_entry.find(e)
                str_exp = str_entry.split(e)[1]
                has_e = True

            if "." in str(self.entry.get()):
                pos_dec = str_entry.find(".")
                has_dec = True

            num = float(str_entry[0:pos_e])
            pos_cursor = self.entry.index(tk.INSERT)

            if pos_cursor <= pos_e:
                if (num >= 0 and pos_cursor > 0) or (num < 0 and pos_cursor > 1):
                    if pos_cursor <= pos_dec or (pos_cursor > pos_dec and pos_cursor <= pos_e):
                        if (pos_cursor == 0 and self.variable.get() < 0) or pos_cursor-1 == pos_dec:
                            return

                        self.entry.selection_range(0, self.entry.index(tk.INSERT))
                        if pos_dec > pos_e:
                            pos_dec = pos_e
                        scale = pos_dec - pos_cursor
                        if scale < 0:
                            scale += 1
                        step = 10 ** scale
                        if has_dec and has_e:
                            str_out = ('{0:.'+str(pos_e-pos_dec-1)+'f}').format(num + (direction * step)) + e + str_exp
                        if has_dec and not has_e:
                            str_out = ('{0:.' + str(pos_dec - 1) + 'f}').format(num + (direction * step))
                        if not has_dec and has_e:
                            str_out = ('{0:d}').format(int(num) + (direction * step)) + e + str_exp
                        if not has_dec and not has_e:
                            str_out = ('{0:d}').format(int(num) + (direction * step))
                        self.variable.set(str_out)
                        self.sendCommand()
            if pos_cursor > pos_e + 1:
                self.entry.selection_range(pos_e, self.entry.index(tk.INSERT))
                str_exp = str(int(str_exp) + direction)
                if has_dec:
                    str_out = ('{0:.' + str(pos_e - pos_dec - 1) + 'f}').format(num) + e + str_exp
                else:
                    str_out = ('{0:d}').format(int(num)) + e + str_exp
                self.entry.icursor(len(str_out))
                self.variable.set(str_out)
                self.sendCommand()


class EntryMultiFrame(EntryFrame):
    def __init__(self, master=None, serial=None, row=0, column=0, text="", commands=[], variables=[], scales=[]):
        super().__init__(master=master, serial=serial, row=row, column=column, text=text, command="", variable=variables[0])
        self.commands = commands
        self.variables = variables
        self.scales = scales

    def sendCommand(self, event=None):
        for i in range(len(self.commands)):
            if self.variables[i].__class__.__name__ == "IntVar":
                self.serial.sendSerial(message="set " + self.commands[i] + " " + str(int(self.entry.get()) * self.scales[i]))
            if self.variables[i].__class__.__name__ == "DoubleVar":
                self.serial.sendSerial(message="set " + self.commands[i] + " " + str(float(self.entry.get()) * self.scales[i]))

    def validateNum(self, action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if len(text) > 1:
            try:
                float(value_if_allowed + "0")
                return True
            except ValueError:
                return False

        if self.variable.__class__.__name__ == "DoubleVar":
            if text in '0123456789-+.eE':
                try:
                    float(value_if_allowed+"0")
                    return True
                except ValueError:
                    return False
            else:
                return False

        if self.variable.__class__.__name__ == "IntVar":
            if text in '0123456789-':
                try:
                    float(value_if_allowed+"0")
                    return True
                except ValueError:
                    return False
            else:
                return False

    def validateNonEmpty(self, event=None):
        if len(self.entry.get()) < 1:
            for variable in self.variables:
                variable.set(0)

    def moveValue(self, event=None, direction=0):
        if self.variable.__class__.__name__ == "IntVar":
            num_digits = len(str(self.variable.get()))
            pos_cursor = self.entry.index(tk.INSERT)
            if (pos_cursor<=1 and self.variable.get() < 0) or pos_cursor==0:
                return
            self.entry.selection_range(0, self.entry.index(tk.INSERT))
            step = 10**(num_digits-pos_cursor)
            for i in range(len(self.commands)):
                newval = (self.variables[i].get() + (direction * step  * self.scales[i]))
                self.variables[i].set(newval)
            self.sendCommand()

        if self.variable.__class__.__name__ == "DoubleVar":
            str_entry = str(self.entry.get())
            pos_e = len(str_entry)
            pos_dec = len(str_entry)
            e = ""
            str_exp = ""
            str_out = ""

            has_dec = False
            has_e = False

            if "E" in str(str_entry):
                e = "E"
                pos_e = str_entry.find(e)
                str_exp = str_entry.split(e)[1]
                has_e = True

            if "e" in str(self.entry.get()):
                e = "e"
                pos_e = str_entry.find(e)
                str_exp = str_entry.split(e)[1]
                has_e = True

            if "." in str(self.entry.get()):
                pos_dec = str_entry.find(".")
                has_dec = True

            num = float(str_entry[0:pos_e])
            pos_cursor = self.entry.index(tk.INSERT)

            if pos_cursor <= pos_e:
                if (num >= 0 and pos_cursor > 0) or (num < 0 and pos_cursor > 1):
                    if pos_cursor <= pos_dec or (pos_cursor > pos_dec and pos_cursor <= pos_e):
                        if (pos_cursor == 0 and self.variable.get() < 0) or pos_cursor-1 == pos_dec:
                            return

                        self.entry.selection_range(0, self.entry.index(tk.INSERT))
                        if pos_dec > pos_e:
                            pos_dec = pos_e
                        scale = pos_dec - pos_cursor
                        if scale < 0:
                            scale += 1
                        step = 10 ** scale
                        if has_dec and has_e:
                            str_out = ('{0:.'+str(pos_e-pos_dec-1)+'f}').format(num + (direction * step)) + e + str_exp
                        if has_dec and not has_e:
                            str_out = ('{0:.' + str(pos_dec - 1) + 'f}').format(num + (direction * step))
                        if not has_dec and has_e:
                            str_out = ('{0:d}').format(int(num) + (direction * step)) + e + str_exp
                        if not has_dec and not has_e:
                            str_out = ('{0:d}').format(int(num) + (direction * step))
                        self.variable.set(str_out)
                        self.sendCommand()
            if pos_cursor > pos_e + 1:
                self.entry.selection_range(pos_e, self.entry.index(tk.INSERT))
                str_exp = str(int(str_exp) + direction)
                if has_dec:
                    str_out = ('{0:.' + str(pos_e - pos_dec - 1) + 'f}').format(num) + e + str_exp
                else:
                    str_out = ('{0:d}').format(int(num)) + e + str_exp
                self.entry.icursor(len(str_out))
                self.variable.set(str_out)
                self.sendCommand()



class CheckButtonFrame(tk.Frame):
    def __init__(self, master=None, serial=None, row=0, column=0, text="", command="", variable=None):
        self.frame = super()
        super().__init__(master=master)

        self.master = master
        self.serial = serial
        self.row = row
        self.column = column
        self.text = text
        self.command = command
        self.variable = variable

        self.grid(row=self.row, column=self.column)
        self.grid_columnconfigure(0, weight=1, uniform='smallframelabel')

        self.frame = tk.Frame(master=self.master, relief=tk.GROOVE, borderwidth=2)
        self.frame.grid(row=self.row, column=self.column, sticky='EW', padx=1, pady=1)
        self.frame.grid_columnconfigure(0, weight=1, uniform='smallframelabel')
        self.frame.grid_columnconfigure(1, weight=1, uniform='smallframecontrol')
        self.frame.grid_rowconfigure(0, weight=1, uniform='smallframeheight', minsize=28)

        self.label = tk.Label(master=self.frame, text=self.text)
        self.label.grid(row=0, column=0, sticky='W', padx=5)
        self.check = tk.Checkbutton(master=self.frame, variable=self.variable, command=self.sendCommand)
        self.check.deselect()
        self.check.grid(row=0, column=1, sticky='E', padx=5)

        self.frame.bind("<Button-1>", lambda event: self.check.focus_set(), add='+')
        self.frame.bind("<Button-1>",
                        lambda event: self.frame.configure(highlightbackground='blue', highlightcolor='blue', highlightthickness=1, borderwidth=1), add='+')

        #self.label.bind("<Button-1>", lambda event: self.check.toggle())
        self.label.bind("<Button-1>", lambda event: self.check.focus_set(), add='+')
        #self.label.bind("<Button-1>", self.sendCommand, add='+')
        self.label.bind("<Button-1>",
                        lambda event: self.frame.configure(highlightbackground='blue', highlightcolor='blue', highlightthickness=1, borderwidth=1), add='+')

        self.check.bind("<FocusIn>",
                        lambda event: self.frame.configure(highlightbackground='blue', highlightcolor='blue', highlightthickness=1, borderwidth=1))

        self.check.bind("<FocusOut>", lambda event: self.frame.configure(highlightbackground=None, highlightthickness=0,
                                                                         borderwidth=2))

        self.check.bind("<Button-1>", lambda event: self.check.focus_set())
        #self.check.bind("<Button-1>", self.sendCommand, add='+')  ### This triggers before state toggle, so it was always wrong. Use _command instead.


    def sendCommand(self, event=None):
        self.serial.sendSerial(message="set " + self.command + " " + str(int(self.variable.get())))


class ToggleButtonFrame(tk.Frame, object):
    def __init__(self, master=None, serial=None, row=0, column=0, text="", command="", variable=None, ontext="", offtext="", buttonstate=None):
        self.frame = super()
        super().__init__(master=master)

        self.master = master
        self.serial = serial
        self.row = row
        self.column = column
        self.text = text
        self.command = command
        self.variable = variable
        self.ontext = ontext
        self.offtext = offtext

        self.buttonstate = buttonstate
        self.buttonstate.bind_to(self.update_state)

        self.grid(row=self.row, column=self.column)
        self.grid_columnconfigure(0, weight=1, uniform='smallframelabel')

        self.frame = tk.Frame(master=self.master, relief=tk.GROOVE, borderwidth=2)
        self.frame.grid(row=self.row, column=self.column, sticky='EW', padx=1, pady=1)
        self.frame.grid_columnconfigure(0, weight=1, uniform='smallframelabel')
        self.frame.grid_columnconfigure(1, weight=1, uniform='smallframecontrol')
        self.frame.grid_rowconfigure(0, weight=1, uniform='smallframeheight', minsize=28)

        self.label = tk.Label(master=self.frame, text=self.text)
        self.label.grid(row=0, column=0, sticky='W', padx=5)

        self.button = tk.Button(master=self.frame, text=self.offtext, width=9, height=1, command=self.toggle)
        self.button.configure(text=self.offtext, bg='red', activebackground='red', fg='yellow')
        self.button.grid(row=0, column=1, sticky='E', padx=5)

        self.button.bind("<FocusIn>",
                        lambda event: self.frame.configure(highlightbackground='blue', highlightcolor='blue',
                                                           highlightthickness=1, borderwidth=1))

        self.button.bind("<FocusOut>",
                        lambda event: self.frame.configure(highlightbackground=None, highlightthickness=0,
                                                           borderwidth=2))

        self.button.bind("<Button-1>", lambda event: self.button.focus_set())
        #self.button.bind("<Button-1>", self.toggle, add='+')
        #self.button.bind("<Button-1>", self.sendCommand, add='+')

    def sendCommand(self, event=None):
        self.serial.sendSerial(message="set " + self.command + " " + str(int(self.variable.get())))

    def toggle(self, event=None):
        if self.variable.get():
            self.variable.set(0)
            self.button.configure(text=self.offtext, bg='red', activebackground='red', fg='yellow')
            self.sendCommand()
        else:
            self.variable.set(1)
            self.button.configure(text=self.ontext, bg='green', activebackground='green', fg='yellow')
            self.sendCommand()

    def update_state(self, buttonstate):
        self.variable.set(buttonstate)
        if self.variable.get() == 0:
            self.button.configure(text=self.offtext, bg='red', activebackground='red', fg='yellow')
        else:
            self.button.configure(text=self.ontext, bg='green', activebackground='green', fg='yellow')


class ButtonState(object):
    def __init__(self):
        self._button_state = 0
        self._observers = []

    @property
    def button_state(self):
        return self._button_state

    @button_state.setter
    def button_state(self, state):
        self._button_state = state
        for callback in self._observers:
            callback(self._button_state)

    def bind_to(self, callback):
        self._observers.append(callback)


class DropdownFrame(tk.Frame):
    def __init__(self, master=None, serial=None, row=0, column=0, text="", command="", variable=None, entries=[], offset=0, state=None):
        self.frame = super()
        super().__init__(master=master)

        self.master = master
        self.serial = serial
        self.row = row
        self.column = column
        self.text = text
        self.command = command
        self.variable = tk.StringVar()
        self.entries = entries
        self.offset = offset

        self.state = state
        self.state.bind_to(self.update_state)

        self.grid(row=self.row, column=self.column)
        self.grid_columnconfigure(0, weight=1, uniform='smallframelabel')

        self.frame = tk.Frame(master=self.master, relief=tk.GROOVE, borderwidth=2)
        self.frame.grid(row=self.row, column=self.column, sticky='EW', padx=1, pady=1)
        self.frame.grid_columnconfigure(0, weight=1, uniform='smallframelabel')
        self.frame.grid_columnconfigure(1, weight=1, uniform='smallframecontrol')
        self.frame.grid_rowconfigure(0, weight=1, uniform='smallframeheight', minsize=28)

        self.label = tk.Label(master=self.frame, text=self.text)
        self.label.grid(row=0, column=0, sticky='W', padx=5)

        #self.dropdown = tk.OptionMenu(self.frame, self.variable, self.entries.keys()[0], *self.entries.keys)

        self.dropdown = ttk.Combobox(master=self.frame, values=self.entries, state='readonly', width=9)
        self.dropdown.set(self.entries[0])
        self.dropdown.grid(row=0, column=1, sticky='E', padx=5)

        self.frame.bind("<Button-1>", lambda event: self.dropdown.focus_set(), add='+')
        self.frame.bind("<Button-1>",
                        lambda event: self.frame.configure(highlightbackground='blue', highlightcolor='blue', highlightthickness=1, borderwidth=1), add='+')

        #self.label.bind("<Button-1>", lambda event: self.check.toggle())
        self.label.bind("<Button-1>", lambda event: self.dropdown.focus_set(), add='+')
        #self.label.bind("<Button-1>", self.sendCommand, add='+')
        self.label.bind("<Button-1>",
                        lambda event: self.frame.configure(highlightbackground='blue', highlightcolor='blue', highlightthickness=1, borderwidth=1), add='+')

        self.dropdown.bind("<FocusIn>",
                        lambda event: self.frame.configure(highlightbackground='blue', highlightcolor='blue', highlightthickness=1, borderwidth=1))

        self.dropdown.bind("<FocusOut>", lambda event: self.frame.configure(highlightbackground=None, highlightthickness=0,
                                                                         borderwidth=2))

        self.dropdown.bind("<Button-1>", lambda event: self.dropdown.focus_set())
        self.dropdown.bind("<Return>", self.sendCommand)
        self.dropdown.bind("<<ComboboxSelected>>", self.sendCommand)


    def sendCommand(self, event=None):
        self.serial.sendSerial(message="set " + self.command + " " + str(int(self.entries.index(self.dropdown.get()))+self.offset))


    def update_state(self, state):
        if state-self.offset > 0:
            self.dropdown.set(self.entries[state-self.offset])
        else:
            self.dropdown.set(self.entries[0])


class GradientFrame(tk.Canvas):
    '''A gradient frame which uses a canvas to draw the background'''
    def __init__(self, parent, borderwidth=0):
        tk.Canvas.__init__(self, parent, borderwidth=borderwidth)
        #self._color1 = "#68C6C5"
        #self._color2 = "#1176BC"

        #self._color1 = "#A3D1D1"
        #self._color2 = "#6B9CBE"

        self._color1 = "#C2DEDD"
        self._color2 = "#9AB7CC"
        self.bind("<Configure>", self._draw_gradient)
        self.bind("<Button-1>", lambda event: self.focus_set())

    def _draw_gradient(self, event=None):
        '''Draw the gradient'''
        self.delete("gradient")
        width = self.winfo_width()
        height = self.winfo_height()
        limit = width if width > height else height
        (r1,g1,b1) = self.winfo_rgb(self._color1)
        (r2,g2,b2) = self.winfo_rgb(self._color2)
        r_ratio = float(r2-r1) / limit
        g_ratio = float(g2-g1) / limit
        b_ratio = float(b2-b1) / limit

        for i in range(limit):
            nr = int(r1 + (r_ratio * i))
            ng = int(g1 + (g_ratio * i))
            nb = int(b1 + (b_ratio * i))
            color = "#%4.4x%4.4x%4.4x" % (nr,ng,nb)
            self.create_line(0,i,limit,i, tags=("gradient",), fill=color)
        self.lower("gradient")