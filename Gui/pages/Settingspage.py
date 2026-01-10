import tkinter as tk
from tkinter import ttk, filedialog

from db.KapParsing import parse_kap_file

LARGEFONT = ("Verdana", 35)


class Settingspage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # label of frame Layout 2
        label = ttk.Label(self, text="Settings", font=LARGEFONT)
        # putting the grid in its place by using
        # grid
        label.grid(row=0, column=1, padx=10, pady=10)
        b1 = tk.Button(self,text="Load charts", command=self.browseFiles )
        b1.grid(row=1,column=0)

    def browseFiles(self):
        filename = filedialog.askopenfilename(initialdir="H:/Sjökort/",
                                              title="Select a File",
                                              filetype=(("Charts","*.KAP"), ("all files","*.*"))
                                              )

        parse_kap_file(filename)
