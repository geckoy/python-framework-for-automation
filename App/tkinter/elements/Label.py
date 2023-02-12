import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont


class Label(dict):
    def __setitem__(self, k, v):
        self.lb[k]=v 

    # def __getitem__(self, key):
    #     return getattr(self, key)

    def __init__(self, *,parent, place, justify = "center", text = "") -> None:
        Label=tk.Label(parent)
        ft=tkFont.Font(family='Times',size=15)
        Label["font"] = ft
        Label["fg"] = "#000000"
        Label["justify"] = justify
        Label["text"] = text
        self.lb = Label
        self.place(**place)
    
    def destroy(self):
        self.lb.destroy()

    def place(self, **kwargs):
        self.lb.place(**kwargs)