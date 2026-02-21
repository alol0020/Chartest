import tkinter as tk
from tkinter import  Frame
from tkinter.constants import RIGHT

from view.Components.ChartFrame import CharFrame
from view.Components.DirectionalPad import DirectionalPad
from view.point_view import PointView

class MainView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.pack(fill="both", expand=True)
        left_frame = Frame(self)
        left_frame = Frame(self, bg='blue')
        left_frame.pack(fill="both", expand=True)

        right_frame = Frame(left_frame, bg='green', width=200)
        right_frame.pack(side=RIGHT, fill="y")  # fill vertically only
        right_frame.pack_propagate(False)  # prevent shrinking to fit content

        # self.point_view = PointView(self, controller.point_controller)
        # self.point_view.pack(fill="both", expand=True)

        self.chart_view = CharFrame(left_frame, controller.chart_controller)
        self.chart_view.pack(side="left", fill="both", expand=True)

        self.nav = DirectionalPad(right_frame,controller.chart_controller)
        self.nav.pack(fill="both")