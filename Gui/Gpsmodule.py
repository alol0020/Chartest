import tkinter as tk
import math
import time

class GPSFrame(tk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        # center
        self.cx = 100
        self.cy = 100

        self.speed = 0 #m/s
        self.course = 0 # deg compass

        # UI layout
        self.canvas = tk.Canvas(self, width=200, height=200, bg="white")
        self.canvas.pack(fill="both", expand=True)

        btns = tk.Frame(self)
        btns.pack()

        tk.Button(btns, text="Stop",  command=self.stop).pack(side="left")

        # Click sets vector
        self.canvas.bind("<Button-1>", self.on_click)

        # Draw static polar grid
        self.draw_polar_grid()

    def on_show(self, event=None):
        print("GPSFrame became visible!")

    def on_click(self, event):
        dx = event.x - self.cx
        dy = event.y - self.cy

        # convert pixel vector to meters per second (scale factor)
        self.speed = math.sqrt(dx*dx + dy*dy)

        angle_rad = math.atan2(-dx, -dy)  # invert axes for compass
        heading = math.degrees(angle_rad)
        self.course = (heading + 360) % 360
        self.draw_position()



    def stop(self):
        self.speed = 0
        self.draw_position()


    def draw_polar_grid(self):
        c = self.canvas
        c.delete("grid")


        for r in range(50, 150, 50):
            c.create_oval(self.cx-r, self.cy-r, self.cx+r, self.cy+r, outline="gray", tags="grid")
            c.create_text(self.cx+r, self.cy, text=f"{r} m/s", fill="black", font=("Arial", 10))

        # crosshair
        c.create_line(self.cx-200, self.cy, self.cx+200, self.cy, fill="gray", tags="grid")
        c.create_line(self.cx, self.cy-200, self.cx, self.cy+200, fill="gray", tags="grid")

    def draw_position(self):
        c = self.canvas
        c.delete("pos")

        heading_rad = -math.radians(self.course)
        px = self.cx + math.sin(heading_rad) * self.speed
        py = self.cy  -math.cos(heading_rad) * self.speed

        c.create_oval(px-5, py-5, px+5, py+5, fill="red", tags="pos")

        c.create_line(self.cx, self.cy, px, py, fill="red", tags="pos")



