import tkinter as tk
from controller.app_controller import AppController

def main():
    root = tk.Tk()
    root.title("Tkinter MVC Skeleton")
    root.minsize(600,600)
    app = AppController(root)
    app.run()

if __name__ == "__main__":
    main()
