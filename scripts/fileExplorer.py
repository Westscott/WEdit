import os
import tkinter as tk
from tkinter import * 
from tkinter.ttk import *
import settings as settings

class FileExplMain(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

        self.selectedFile = ""
        self.openFile = False

        self.totalWidgets = []
        self.totalFrames = []

        self.FileExpOpen = True
        self.fileExplorerWindow = Toplevel(self)
        self.fileExplorerWindow.attributes('-topmost', True)
        self.fileExplorerWindow.title("FILE EXPLORER")
        self.fileExplorerWindow.geometry("450x225")
        self.fileExplorerWindow.protocol("WM_DELETE_WINDOW", self.FileExpClose)
        self.totalFrames.append(self.fileExplorerWindow)

        self.urlEntry = tk.Entry(self.fileExplorerWindow, font=(settings._selected_typeface, 9))
        self.urlEntry.pack(side=tk.BOTTOM, fill=tk.X)
        self.totalWidgets.append(self.urlEntry)
        self.urlEntry.bind("<Return>", lambda event: self.TreeViewSelect(self.urlEntry.get()))

        self.topExpFrame = tk.Frame(self.fileExplorerWindow)
        self.topExpFrame.pack(side="top", anchor="nw")
        #self.topExpFrame.configure(bg="black")

        #self.openWinExpBtn = tk.Button(self.topExpFrame, text="WinExp", font=(settings._selected_typeface, 9), command= lambda:os.startfile(self.rootDir))
        #self.openWinExpBtn.pack(side="left")
        #self.totalWidgets.append(self.openWinExpBtn)

        self.backButton = tk.Button(self.topExpFrame, text="<", font=(settings._selected_typeface, 9), command=self.GoBackTree)
        self.backButton.pack(side="left")
        self.totalWidgets.append(self.backButton)

        drives = [ chr(x) + ":" for x in range(65,91) if os.path.exists(chr(x) + ":") ]
        self.driveBtns = []
        i = 0
        for x in drives:
            self.driveBtns.append(tk.Button(self.topExpFrame, text=x, font=(settings._selected_typeface, 9), command= lambda x=x: self.ChangeDriveLocation(x)))
            self.driveBtns[i].pack(side="left", expand=1)
            self.totalWidgets.append(self.driveBtns[i])
            i += 1

        self.style = tk.ttk.Style()
        

        self.treeView = tk.ttk.Treeview(self.fileExplorerWindow, show="tree")
        self.treeView.pack(side="left", expand=1, fill="both", anchor="center")
        self.scrollBar = tk.ttk.Scrollbar(self.fileExplorerWindow, command=self.treeView.yview)
        self.scrollBar.pack(side="right", fill="y")
        self.treeView.configure(yscrollcommand=self.scrollBar.set)

        
        #self.treeView.bind("<Double-1>", self.TreeViewSelect)

        self.rootDir = os.path.expanduser("~")
        self.populateTree(self.rootDir)
        self.ColorThemeSetup()

    def TreeViewSelect(self, override=""):
        selected_item = self.treeView.focus()
        if selected_item or override != "":
            selected_path = os.path.join(self.rootDir, self.treeView.item(selected_item, "text"))
            if override != "":
                selected_path = override
            if os.path.isdir(selected_path):
                self.populateTree(selected_path)
                self.rootDir = selected_path
                self.selectedFile = ""
            elif os.path.isfile(selected_path):
                self.selectedFile = selected_path
            else:
                self.selectedFile = ""

    def GoBackTree(self):
        if self.rootDir != os.path.expanduser("~"):
            self.rootDir = os.path.dirname(self.rootDir)
            self.selectedFile = ""
            self.populateTree(self.rootDir)

    def ChangeDriveLocation(self, drive):
        self.selectedFile = ""
        append = "\\"
        self.rootDir = f"{drive+append}"
        self.populateTree(self.rootDir)
    
    def populateTree(self, path):

        self.treeView.delete(*self.treeView.get_children())
        for dirname in os.listdir(path):
            dir_path = os.path.join(path, dirname)
            if os.path.isdir(dir_path):
                self.treeView.insert("", "end", text=dirname, tags="directory")
        # Add the files
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                self.treeView.insert("", "end", text=filename, tags="file")
        self.urlEntry.delete(0, tk.END)
        self.urlEntry.insert(tk.END, path)

    def ColorThemeSetup(self):
        _index = settings._colorscheme_index

        self.style.configure("Treeview",
                             background=settings.backgroundOptions[_index],  # Default background
                             foreground=settings.fontColorOptions[_index],  # Default text color
                             fieldbackground=settings.backgroundOptions[_index],
                             font=(settings._selected_typeface, 9),
                             borderwidth=0,
                             rowheight=20)

        # Set colors for selected items
        self.style.map("Treeview",
                       background=[("selected", settings.fontColorOptions[_index])],
                       foreground=[("selected", settings.backgroundOptions[_index])])

        for _widget in self.totalWidgets:
            _widget.configure(bg=settings.backgroundOptions[_index], fg=settings.fontColorOptions[_index])

        for _tframe in self.totalFrames:
            _tframe.configure(bg=settings.backgroundOptions[_index])

        self.urlEntry.configure(insertbackground=settings.fontColorOptions[_index])

    def FileExpClose(self):
        self.FileExpOpen = False
        self.fileExplorerWindow.destroy()