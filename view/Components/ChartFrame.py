import tkinter as tk
from tkinter import ttk

from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

from Gui.DirectionalPad import DirectionalPad
from Gui.Gpsmodule import GPSFrame
from Gui.helpers.mapview import Mapview
from Gui.pointList import PointList
from db.coordinateMapping import pixel_to_latlon
from db.db import db_get_chart, db_get_refpoints

class CharFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.chart_image = None
        self.controller = controller
        self.chart_frame_height = None
        self.chart_frame_width = None
        self.chart_label = ttk.Label(self, text="Chart/Image Here", background="lightgray")
        self.chart_label.pack(expand=True, fill="both", padx=5, pady=5)
        # self.chart_label.bind('<Motion>', self.movementInChart)
        self.chart_label.bind('<B1-Motion>', self.on_drag)

    def on_drag(self,event):
        self.controller.on_pan(event.x/self.chart_frame_width,event.y/self.chart_frame_height)
    def refresh(self, data):
        if data is None:
            return

        # Convert to PIL Image
        img = Image.fromarray(data, mode="RGB")

        # Resize to fixed width while maintaining aspect
        self.chart_frame_width = 400
        self.chart_frame_height = int(self.chart_frame_width * self.controller.get_aspect())
        img = img.resize((self.chart_frame_width, self.chart_frame_height), Image.Resampling.NEAREST)

        # Convert to Tk PhotoImage
        self.chart_image  = ImageTk.PhotoImage(img)

        # If chart_label already exists, just update image
        if hasattr(self, "chart_label"):
            self.chart_label.configure(image=self.chart_image , text="")
        else:
            # Create a label inside the chart frame
            self.chart_label = ttk.Label(self, image=self.chart_image , text="")
            self.chart_label.pack(expand=True, fill="both", padx=5, pady=5)
