import tkinter as tk

from view.Components.Chart import CharFrame
from view.point_view import PointView

class MainView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.pack(fill="both", expand=True)

        # self.point_view = PointView(self, controller.point_controller)
        # self.point_view.pack(fill="both", expand=True)
        self.chart_view = CharFrame(self, controller.chart_controller)
        self.chart_view.pack(fill="both", expand=True)