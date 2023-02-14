import tkinter as tk
from tkinter import ttk
from App.Helpers import *
from App.tkinter.elements.Label import Label
from App.tkinter.elements.button import button
from App.tkinter.elements.listbox import listbox
from App.tkinter.elements.treeview import treeview
class interface:
    def __init__(self) -> None:
        self.labels=[]
        self.buttons = []
        self.treeview = None
        self.listbox = None
        self.procs = None
        self.currentChoosedProcName = None
        self.subprocs = None

        self.root = tk.Tk()
        #setting title
        self.root.title(env("APP_NAME"))
        #setting window size
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        width=screenwidth-(screenwidth*.023)
        height=screenheight-(screenheight*.11)
        # print(width, height)
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)
        ## set Labels
        labels = [{"text":"Running Processes Stats", "place":{"x":180,"y":20,"width":601,"height":30}}, {"text":"Running Processes", "place":{"x":800,"y":20,"width":177,"height":30}}, {"text":"Actions", "place":{"x":10,"y":20,"width":163,"height":30}}]
        for i in range(len(labels)):
            l = labels[i]
            Label(parent=self.root, **l)
        self.__set_app_buttons()
        self.__fill_interface()
        self.root.after(1000, self.update_root_interface)
    
    def update_root_interface(self):
        # print("checking")
        if not self.__checkprocessesdiff(): self.__fill_interface()
        if self.currentChoosedProcName: 
            if not self.__checksubprocessesdiff(): print("found diff in subprocs");self.display_process_managment_table(self.currentChoosedProcName)
        self.root.after(1000, self.update_root_interface)
    
    def __fill_interface(self):
        # print("interface filled")
        # set list Box
        self.procs = self.__get_running_processes()
        self.__empty_interface()
        if self.procs != None:
            self.listbox = listbox(parent=self.root, **{"place":{"x":800,"y":60,"width":177,"height":520}, "values":tuple(self.procs), "onselect":self.listBoxselection})
        else:
            self.labels.append(Label(parent=self.root, **{"text":"App is Closed", "place":{"x":800,"y":100,"width":177,"height":30}}))
            
        
        
    def display_process_managment_table(self, procName):
        self.currentChoosedProcName = procName
        self.subprocs = self.__get_running_subprocesses(procName)
        self.__empty_management()
        if self.subprocs != None and len(self.subprocs) > 0:
            self.treeview = treeview(parent=self.root, **{"place":{"x":180,"y":60,"width":601,"height":580}, "headers":['proc_name', 'current_status', 'global_status']})
            listitems = []
            for sp in self.subprocs:
                sprcs = self.__get_subproc_ginfo(procName, sp)
                if sprcs["status"]:
                    r = sprcs["response"]
                    listitems.append((sp, r["status"], (("running" if r["isInstantiated"] else "stopped") +"," + ("paused" if r["isPaused"] else "playing"))))
            self.treeview.set_lists(listitems)
            self.display_process_managment_buttons()
            self.treeview.tree.after(100, self.__update_treeview_items)
        else:
            self.labels.append(Label(parent=self.root, **{"text":"Process is empty", "place":{"x":180,"y":100,"width":601,"height":30}}))
        
    def display_process_managment_buttons(self):
        # set buttons for actions
        self.__remove_elements("buttons")
        buttons = [{"text":"start", "command":lambda:self.play_button_action("start")},{"text":"stop", "command":lambda:self.play_button_action("stop")}, {"text":"pause", "command":lambda:self.play_button_action("pause")},{"text":"unpause", "command":lambda:self.play_button_action("unpause")}]
        #,{"text":"destroy", "command":lambda:self.play_button_action("destroy")},{"text":"stats", "command":lambda:print("stats")}
        btPos = 60
        btHeight = 37
        for i in range(len(buttons)):
            b = buttons[i]
            self.buttons.append(button(parent=self.root, place={"x":10,"y":btPos,"width":163,"height":btHeight}, **b))
            btPos += btHeight + 30

    def listBoxselection(self, listbox):
        def cb(e):
            try:
                selectedPrcoess = listbox.get(listbox.curselection())
                self.display_process_managment_table(selectedPrcoess)
            except:
                pass
        return cb




    def play_button_action(self, action):
        try: 
            if self.treeview != None:
                selected = self.treeview.tree.selection()[0]
                if selected != "":
                    el = self.treeview.tree.item(selected)["values"]
                    subprocName = el[0]
                    exec_command(f"{self.currentChoosedProcName}Commands", f"{action}_{self.currentChoosedProcName}", {f"{self.currentChoosedProcName}_name":subprocName, "timeout":1})
                    # print(action, " for item ", selected)
            else:
                print("no tree view available")
        except:
            print("no tree view selected")

    def __update_treeview_items(self):
        if self.treeview!=None:
            chlds = self.treeview.tree.get_children()
            for chld in chlds:
                try:
                    el = self.treeview.tree.item(chld)["values"]
                    subprocName = el[0]
                    info = self.__get_subproc_ginfo(self.currentChoosedProcName, subprocName)
                    if info["status"]:
                        r = info["response"]
                        items = (subprocName, r["status"], (("running" if r["isInstantiated"] else "stopped") +"," + ("paused" if r["isPaused"] else "playing")))
                        self.treeview.tree.item(chld, values=items)
                except:
                    pass
                    # print("error occured __update_treeview_items")
        self.treeview.tree.after(100, self.__update_treeview_items)
    
    def __set_app_buttons(self):
        # button(parent=self.root, place={"x":800,"y":550,"width":163,"height":"37"}, text="start_app", command=lambda:print("start_app"))
        button(parent=self.root, place={"x":800,"y":590,"width":163,"height":"37"}, text="stop_app", command=lambda:exec_command("manage_app","stop_app"))
    
    def __get_subproc_ginfo(self, procName, subprocName):
        return exec_command(f"{procName}Commands", f"get_ginfo_{procName}", {f"{procName}_name":subprocName})

    def __get_running_processes(self) -> None|list:
        processes=exec_command("manage_app", "get_running_processes")
        procs = None
        if processes != None and processes != 'app_is_closed':
                if processes["status"]:
                    procs = processes["response"]

        return procs
        
    def __get_running_subprocesses(self, procName:str) -> None|list:
        processes=exec_command("manage_app", "get_subprocesses_names",{"process_name":procName})
        procs = None
        if processes != None and processes != 'app_is_closed':
                if processes["status"]:
                    procs = processes["response"]

        return procs



    def __checkprocessesdiff(self) -> bool:
        same = True
        procs = self.__get_running_processes()
        if procs == None:
            if type(procs) != type(self.procs):
                # print("same False 1")
                same = False
        else:
            if self.procs != None:
                for p in procs:
                    if not p in self.procs:
                        # print("same False 2 process name ", p, " processes", self.procs)
                        same = False
                        break
            else:
                if type(procs) != type(self.procs):
                    same = False
        return same

    def __checksubprocessesdiff(self) -> bool:
        same = True
        subprocs = self.__get_running_subprocesses(self.currentChoosedProcName)
        if subprocs == None:
            if type(subprocs) != type(self.subprocs):
                # print("same False 1")
                same = False
        else:
            if self.subprocs != None:
                for p in subprocs:
                    if not p in self.subprocs:
                        # print("same False 2 process name ", p, " processes", self.subprocs)
                        same = False
                        break
            else:
                if type(subprocs) != type(self.subprocs):
                    same = False
        return same

    def __remove_elements(self, elsName:str):
        # print("destroying element ", elsName)
        els = getattr(self, elsName)
        for el in els:
            self.__remove_el(el)
        setattr(self, elsName, [])

    def __remove_element(self, elName:str):
        # print("destroying element ", elName)
        el = getattr(self, elName)
        self.__remove_el(el)
        setattr(self, elName, None)
        

    def __remove_el(self, el):
        if hasattr(el,"destroy"): 
            # print("destroyed")
            el.destroy()
    
    def __empty_interface(self):
        self.__remove_element("listbox")
        self.__remove_elements("labels")
        self.__empty_management()
        self.currentChoosedProcName = None
        self.subprocs = None

    def __empty_management(self):
        self.__remove_element("treeview")
        self.__remove_elements("buttons")

    def display(self):
        self.root.mainloop()


