import tkinter as tk

class PointView(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.x_entry = tk.Entry(self)
        self.y_entry = tk.Entry(self)

        self.add_btn = tk.Button(
            self,
            text="Add Point",
            command=self.on_add_clicked
        )

        self.listbox = tk.Listbox(self)

        self.x_entry.pack()
        self.y_entry.pack()
        self.add_btn.pack()
        self.listbox.pack(fill="both", expand=True)

    def on_add_clicked(self):
        self.controller.add_point(
            self.x_entry.get(),
            self.y_entry.get()
        )

    def refresh(self, points):
        self.listbox.delete(0, tk.END)
        for p in points:
            self.listbox.insert(tk.END, f"{p[0]}, {p[1]}")
