import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont


class treeview(dict):
    # def __setitem__(self, k, v):
    #     self.lb[k]=v 

    # def __getitem__(self, key):
    #     return getattr(self, key)

    def __init__(self, *,parent, place, headers:list[str]) -> None:
        container = ttk.Frame(parent)
        container.pack()#fill='both', expand=True
        # create a treeview with dual scrollbars
        self.headers = headers
        tree = ttk.Treeview(container, columns=headers, selectmode="browse", show="headings")
        vsb = ttk.Scrollbar(orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar( orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        container.place(**place)
        self.container = container
        self.tree = tree
        self.set_headers(headers)    

        

    def destroy(self):
        self.tree.destroy()
        self.container.destroy()
    
    def set_headers(self, headers:list[str]):
        for col in headers:
            self.tree.heading(col, text=col.title(), command=lambda c=col: sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            # self.tree.column(col, width=tkFont.Font().measure(col.title()))

    def set_lists(self, lists:list[tuple]):
        for item in lists:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            try:
                for ix, val in enumerate(item):
                    col_w = tkFont.Font().measure(val)
                    if self.tree.column(self.headers[ix],width=None)<col_w:
                        self.tree.column(self.headers[ix], width=col_w)
            except BaseException as err:
                pass
                # print("error occured in set_lists: ", err)
def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) \
        for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    #data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
        int(not descending)))