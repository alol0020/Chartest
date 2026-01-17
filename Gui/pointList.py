import tkinter as tk
from tkinter import Listbox

class PointList(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Listbox
        self.lb = Listbox(self, height=6)
        self.lb.grid(row=0, column=0, columnspan=3, sticky="nsew", pady=(0, 8))

        self.lb.insert(tk.END, "x1,y3")
        self.lb.insert(tk.END, "x2,y3")
        self.lb.insert(tk.END, "x3,y3")

        # X entry
        tk.Label(self, text="X:").grid(row=1, column=0, sticky="e")
        self.x_entry = tk.Entry(self, width=10)
        self.x_entry.grid(row=1, column=1, sticky="w")

        # Y entry
        tk.Label(self, text="Y:").grid(row=2, column=0, sticky="e")
        self.y_entry = tk.Entry(self, width=10)
        self.y_entry.grid(row=2, column=1, sticky="w")

        # Add button
        add_btn = tk.Button(self, text="Add Point", command=self.add_point)
        add_btn.grid(row=1, column=2, rowspan=2, padx=8)

    def add_point(self):
        x = self.x_entry.get().strip()
        y = self.y_entry.get().strip()

        if not x or not y:
            return  # optionally show a validation message

        self.lb.insert(tk.END, f"{x},{y}")

        self.x_entry.delete(0, tk.END)
        self.y_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Point List")

    PointList(root, padx=10, pady=10).pack(fill="both", expand=True)

    root.mainloop()
