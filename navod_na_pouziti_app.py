#!/usr/bin/python3
import pathlib
import tkinter as tk
import pygubu

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "navod_na_pouziti_app.ui"


class NavodNaPouzitiAppApp:
    def __init__(self, master=None):
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow: tk.Toplevel = builder.get_object("toplevel1", master)
        builder.connect_callbacks(self)

    def run(self):
        self.mainwindow.mainloop()

    def onCallClose(self):
        self.mainwindow.destroy()

if __name__ == "__main__":
    app = NavodNaPouzitiAppApp()
    app.run()
