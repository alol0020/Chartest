import tkinter as tk
from tkinter import ttk

class DirectionalPad(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.chart_image = None
        self.controller = controller
        self.chart_frame_height = None
        self.chart_frame_width = None

        # 3x3 grid layout
        for row in range(4):
            self.rowconfigure(row, weight=1, uniform="padrow")
        for col in range(3):
            self.columnconfigure(col, weight=1, uniform="padcol")

        # Map button labels to positions
        positions = {
            "zoom out": (0,0),
            "zoom in": (0,1),
            "up":    (1, 1),
            "left":  (2, 0),
            "right": (2, 2),
            "down":  (3, 1),
        }

        # Create buttons dynamically from dict
        for direction, (r, c) in positions.items():

            btn = ttk.Button(
                self,
                text=direction.capitalize(),
                command=lambda d=direction: self.controller.nav(d),
                width=6
            )
            btn.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)

        # Fill empty cells with frames for spacing
        for r in range(4):
            for c in range(3):
                if (r, c) not in positions.values():
                    frame = tk.Frame(self)
                    frame.grid(row=r, column=c, sticky="nsew")
