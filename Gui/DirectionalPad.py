import tkinter as tk
from tkinter import ttk

class DirectionalPad(tk.Frame):
    def __init__(self, parent, commands: dict, button_size=(6, 2), **kwargs):
        """
        commands: dict with keys "up", "down", "left", "right" and callable values
        button_size: (width, height) of buttons
        """
        super().__init__(parent, **kwargs)

        # Ensure all directions are present in commands
        for key in ("zoom out","zoom in","up", "down", "left", "right"):
            if key not in commands:
                commands[key] = lambda: None  # no-op if missing

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
                command=commands[direction],
                width=button_size[0]
            )
            btn.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)

        # Fill empty cells with frames for spacing
        for r in range(4):
            for c in range(3):
                if (r, c) not in positions.values():
                    frame = tk.Frame(self)
                    frame.grid(row=r, column=c, sticky="nsew")
