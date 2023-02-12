import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont

class button:
    def __setitem__(self, k, v):
        self.bt[k]=v 

    # def __getitem__(self, key):
    #     return getattr(self, key)

    def __init__(self, *,parent, place, justify = "center", text = "", command = None) -> None:
        self.identification = text
        button=tk.Button(parent)
        button["bg"] = "#efefef"
        ft = tkFont.Font(family='Times',size=10)
        button["font"] = ft
        button["fg"] = "#000000"
        button["justify"] = "center"
        button["text"] = text
        button.place(**place)
        button["command"] = command
        self.bt = button
        self.place(**place)

    def destroy(self):
        self.bt.destroy()
    
    def place(self, **kwargs):
        self.bt.place(**kwargs)