import tkinter as tk

from Gui.pages.Chartlistpage import Chartlistpage
from Gui.pages.Mainpage import Mainpage
from Gui.pages.Settingspage import Settingspage
from db.db import db_init

LARGEFONT = ("Verdana", 35)

class MainView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.pack(fill="both", expand=True)

        # Creating Menubar
        menubar = tk.Menu(self)

        # Adding File Menu and commands
        file = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='File', menu=file)
        # file.add_command(label='New File', command=None)
        # file.add_command(label='Open...', command=None)
        # file.add_command(label='Save', command=None)
        # file.add_separator()
        file.add_command(label='Exit', command=self.destroy)

        menubar.add_command(label='Main', command= lambda : self.show_frame("Mainpage"))
        menubar.add_command(label='Settings', command= lambda : self.show_frame("Settingspage"))
        menubar.add_command(label='Chartlist', command= lambda : self.show_frame("Chartlistpage"))


        # display Menu
        self.config(menu=menubar)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (Mainpage,Settingspage,Chartlistpage):
            frame = F(container, self)

            # initializing frame of that object from
            # startpage, page1, page2 respectively with
            # for loop
            self.frames[type(frame).__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("Mainpage")

    # to display the current frame passed as
    # parameter
    def show_frame(self, pagename):
        frame = self.frames[pagename]
        frame.tkraise()