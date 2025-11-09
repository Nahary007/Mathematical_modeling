import tkinter as tk
from model.model import Model
from controller.controller import Controller
from view.view import View

def main():
    root = tk.Tk()

    model = Model()
    view = View(root)
    controller = Controller(model, view)

    root.mainloop()

main()