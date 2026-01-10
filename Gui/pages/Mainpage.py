import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

from Gui.Gpsmodule import GPSFrame
from Gui.helpers.mapview import Mapview
from db.db import db_get_chart

LARGEFONT = ("Verdana", 35)

class Mainpage(tk.Frame):
    data = None
    mapView = None
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # label of frame Layout 2
        label = ttk.Label(self, text="Mainpage", font=LARGEFONT)

        # putting the grid in its place by using
        # grid
        label.grid(row=0, column=1, padx=10, pady=10)

        self.reloadChart()


        self.drawMap()

        frame2 = GPSFrame(self)

        # fire event when frame2 is raised
        frame2.bind("<Map>", frame2.on_show)
        frame2.grid(row=1, column=2, padx=10, pady=10)

        buttons = [{"label": "left", "cmd": self.panLeft}, {"label": "right", "cmd": self.panRight}]
        i = 3
        for b in buttons:
            tk.Button(self, text=b["label"], command=b["cmd"]).grid(row=2, column=i, padx=10, pady=10)
            i = i + 1

    def drawMap(self):
        if self.data is None:
            return
        # Extract section
        section = self.data[self.mapView.y_min:self.mapView.y_max,self.mapView.x_min: self.mapView.x_max]
        # Normalize to 0–255
        section = section.astype("uint8")
        # section = section.astype(float)
        # section -= section.min()
        # if section.max() > 0:
        #     section /= section.max()
        #
        # section = (section * 255).astype("uint8")

        img = Image.fromarray(section, mode="RGB")

        # Optional: resize to fixed display size
        img = img.resize((400, int(400 * self.mapView.aspect)), Image.Resampling.NEAREST)

        # Convert to Tk image
        self.photo = ImageTk.PhotoImage(img)

        # Display image
        img_label = ttk.Label(self, image=self.photo)
        img_label.grid(row=1, column=1, padx=10, pady=10)

    def tkraise(self, *args, **kwargs):
        self.reloadChart()
        super().tkraise(*args, **kwargs)

    def reloadChart(self):
            self.data = db_get_chart(1)
            (h,w,_) = self.data.shape
            self.mapView = Mapview(w,h)



    def panRight(self):
        self.mapView.tile_x_inc()

        self.drawMap()

    def panLeft(self):

        self.mapView.tile_x_dec()
        self.drawMap()
