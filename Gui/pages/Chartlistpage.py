import tkinter as tk
from tkinter import ttk

from db.db import db_get_chart_names

LARGEFONT = ("Verdana", 35)


class Chartlistpage(tk.Frame):
    charts = []
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Chartlistpage", font=LARGEFONT)
        # putting the grid in its place by using
        # grid
        label.grid(row=0, column=4, padx=10, pady=10)

        self.listbox = tk.Listbox(self, height=10,
                             width=15,
                             bg="grey",
                             activestyle='dotbox',
                             font="Helvetica",
                             fg="yellow")
        self.reloadList()
        self.listbox.grid(row=1,column=1)

    def tkraise(self, *args, **kwargs):
        self.reloadList()
        super().tkraise(*args, **kwargs)

    def reloadList(self):
        self.charts = db_get_chart_names()
        self.listbox.delete(0,'end')
        for i,c in enumerate(self.charts):
            self.listbox.insert(i,c)