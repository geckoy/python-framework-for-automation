import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont


class listbox(dict):
    def __setitem__(self, k, v):
        self.lb[k]=v 

    def __init__(self, *,parent, place:dict, values:tuple, justify:str = "center", onselect=None) -> None:
        listbox=tk.Listbox(parent)
        listbox["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        listbox["font"] = ft
        listbox["fg"] = "#333333"
        listbox["justify"] = justify
        listvar = tk.StringVar(value=values)
        listbox["listvariable"] = listvar
        self.lb = listbox
        self.place(**place)
        if onselect != None:
            self.lb.bind("<<ListboxSelect>>", onselect(self.lb))
           
    def destroy(self):
        self.lb.destroy()

    def place(self, **kwargs):
        self.lb.place(**kwargs)