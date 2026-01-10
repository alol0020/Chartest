import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

from Gui.DirectionalPad import DirectionalPad
from Gui.Gpsmodule import GPSFrame
from Gui.helpers.mapview import Mapview
from db.coordinateMapping import pixel_to_latlon
from db.db import db_get_chart, db_get_refpoints

LARGEFONT = ("Verdana", 35)


class Mainpage(tk.Frame):
    data = None
    mapView = None

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # -----------------------
        # Top label
        # -----------------------
        self.refs = []
        label = ttk.Label(self, text="Mainpage", font=("Arial", 24))
        label.pack(side="top", fill="x", padx=10, pady=10)

        # -----------------------
        # Bottom container frame (left chart, right GPS+pad)
        # -----------------------
        bottom_frame = tk.Frame(self)
        bottom_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # -----------------------
        # Left chart/image frame
        # -----------------------
        self.chart_frame = tk.Frame(bottom_frame, bg="lightgray")
        self.chart_frame.pack(side="left", fill="both", expand=True)

        # Example: placeholder for your chart/image
        self.chart_label = ttk.Label(self.chart_frame, text="Chart/Image Here", background="lightgray")
        self.chart_label.pack(expand=True, fill="both", padx=5, pady=5)
        self.chart_label.bind('<Motion>', self.movementInChart)
        # -----------------------
        # Right frame: GPS + directional pad
        # -----------------------
        right_frame = tk.Frame(bottom_frame)
        right_frame.pack(side="left", fill="y", padx=10)

        # GPSFrame on top
        gps_frame = GPSFrame(right_frame)
        gps_frame.pack(side="top", fill="x", expand=False, pady=(0,10))  # small gap below GPS

        # DirectionalPad at bottom
        button_cmds = {
            "zoom out": self.zoomOut,
            "zoom in": self.zoomIn,
            "left": self.panLeft,
            "right": self.panRight,
            "up": self.panUp,
            "down": self.panDown
        }
        pad = DirectionalPad(right_frame, button_cmds)
        pad.pack(side="bottom", fill="x", expand=False)

    def movementInChart(self, event):
        # Frame size
        frame_w = self.chart_frame.winfo_width()
        frame_h = self.chart_frame.winfo_height()

        # Current map bounds
        x_min, x_max, y_min, y_max = self.mapView.get_current_bounds()

        # Scaling
        scale_x = (x_max - x_min) / frame_w
        scale_y = (y_max - y_min) / frame_h

        # Map pixel to data index
        data_x = int(x_min + event.x * scale_x)
        data_y = int(y_min + event.y * scale_y)

        # Clamp to bounds
        data_x = min(max(data_x, x_min), x_max - 1)
        data_y = min(max(data_y, y_min), y_max - 1)
        lat,lon = pixel_to_latlon(data_x,data_y,self.refs)
        print("coordinates at mouse:", lat, lon)


    def drawMap(self):
        if self.data is None:
            return

        # Slice the data according to current tile/view
        section = self.data[
                  self.mapView.y_min:self.mapView.y_max,
                  self.mapView.x_min:self.mapView.x_max
                  ]

        # Convert to PIL Image
        img = Image.fromarray(section, mode="RGB")

        # Resize to fixed width while maintaining aspect
        self.chart_frame_width = 400
        self.chart_frame_height = int(self.chart_frame_width * self.mapView.aspect)
        img = img.resize((self.chart_frame_width, self.chart_frame_height), Image.Resampling.NEAREST)

        # Convert to Tk PhotoImage
        self.chart_image  = ImageTk.PhotoImage(img)

        # If chart_label already exists, just update image
        if hasattr(self, "chart_label"):
            self.chart_label.configure(image=self.chart_image , text="")
        else:
            # Create a label inside the chart frame
            self.chart_label = ttk.Label(self.chart_frame, image=self.chart_image , text="")
            self.chart_label.pack(expand=True, fill="both", padx=5, pady=5)

    def tkraise(self, *args, **kwargs):
        self.reloadChart()
        super().tkraise(*args, **kwargs)

    def reloadChart(self):
        self.data = db_get_chart(1)
        self.refs = db_get_refpoints(1)
        (h, w, _) = self.data.shape
        self.mapView = Mapview(w, h)
        self.drawMap()

    def panRight(self):
        self.mapView.tile_x_inc()
        self.drawMap()

    def panLeft(self):
        self.mapView.tile_x_dec()
        self.drawMap()

    def panUp(self):
        self.mapView.tile_y_inc()
        self.drawMap()

    def panDown(self):
        self.mapView.tile_y_dec()
        self.drawMap()

    def zoomIn(self):
        self.mapView.tiles_inc()
        self.drawMap()
    def zoomOut(self):
        self.mapView.tiles_dec()
        self.drawMap()
