import os
import time
import tkinter as tk
from tkinter import *
import pygments.lexers
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox as mb

import codeFrame as codeFrame
import settings as settings
import fileExplorer as fileExpl
import cube as avcube

import pygame
import math
import threading
import numpy as np
from PIL import Image, ImageTk
from pathlib import Path

#test working
class WEdit:
    def __init__(self):
        self.fdir = color_schemes_dir = Path(__file__).parent.parent
        pygame.init()
        pygame.mixer.init()
        self.root = tk.Tk()
        self.root.title("WEdit")
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.keywordList = []
        self.suggestionBox = None
        self.suggestionIndex = 0

        self.totalFrames = []
        self.totalWidgets = []

        self.settingsFrames = []
        self.settingsWidgets = []

        self.activeFilePath = ""
        self.fileExplIsActive = False


        self.codeViewFrame = codeFrame.CallCV(self.root)
        self.toolbarFrame = tk.Frame(self.root)
        self.codeViewFrame.pack(fill=tk.BOTH, expand=True)
        self.codeViewFrame.configure(undo=True)
        self.toolbarFrame.pack(fill=tk.X)
        self.totalFrames.append(self.toolbarFrame)
        self.totalFrames.append(self.codeViewFrame)
        self.totalFrames.append(self.root)
        self.InitUI()
        self.CommandEntryManager()
        self.handle_keyword_list()

        self.mainCanvas = tk.Canvas(self.codeViewFrame, width=75, height=75, border=0, borderwidth=0, highlightthickness=0)
        self.mainCanvas.pack(side=tk.BOTTOM, anchor="se")
        self.totalFrames.append(self.mainCanvas)
        #self.cubeThread = threading.Thread(target=avcube.pygame_setup, args=(self.mainCanvas,), daemon=True).start()
        #avcube.pygame_setup(self.mainCanvas)

        self.root.bind("<KeyPress>", lambda event: self.PlayClickSound(0))
        
        self.commandEntry.bind("<KeyRelease>", self.CommandEntryManager)
        self.commandEntry.bind("<Return>", self.CommandInputManager)
        
        #self.codeViewFrame.bind("<KeyRelease>", self.on_key_release)
        self.codeViewFrame.bind("<Control-Up>", lambda event: self.ChangeFontSize(1))
        self.codeViewFrame.bind("<Control-Down>", lambda event: self.ChangeFontSize(-1)) 
        self.codeViewFrame.bind("<Tab>", lambda event: self.handle_tab_key())

        self.root.bind("<Control-Right>", lambda event: self.ChangeColorScheme(1))
        self.root.bind("<Control-Left>", lambda event: self.ChangeColorScheme(-1))
        
        self.root.bind("<Control-space>", self.ModuleSwapManager)
        #self.root.bind("<Up>", lambda event: self.nav_items(0))
        #self.root.bind("<Down>", lambda event: self.nav_items(0))
        self.volumeValue = tk.DoubleVar(self.root)
        self.volumeValue.set(0.5)
        self.clickSound = pygame.mixer.Sound(f"{self.fdir}\\audio\\click.ogg")

        self.cubeVisualValue = tk.IntVar(self.root)
        self.cubeVisualValue.set(0)
        #self.CubeVelSlower()
        self.ChangeColorScheme(0)
        self.root.mainloop()

    def InitUI(self):
        self.commandEntry = tk.Entry(self.toolbarFrame, font=(settings._selected_typeface, 9))
        self.commandEntry.pack(side=tk.LEFT, fill=X)
        self.totalWidgets.append(self.commandEntry)

        self.infoText = tk.Label(self.toolbarFrame, text=":", font=(settings._selected_typeface, 9))
        self.infoText.pack(side=tk.LEFT, fill=X)
        self.totalWidgets.append(self.infoText)

        self.syntaxText = tk.Label(self.toolbarFrame, text="txt", font=(settings._selected_typeface, 9))
        self.syntaxText.pack(side=tk.RIGHT)
        self.totalWidgets.append(self.syntaxText)

        self.spacer = tk.Label(self.toolbarFrame, text="|", font=(settings._selected_typeface, 9))
        self.spacer.pack(side=tk.RIGHT)
        self.totalWidgets.append(self.spacer)

    def on_exit(self):
        print("have a good day : )")
        exit()

    def ModuleSwapManager(self, event=None):
        if self.commandEntry.focus_get() != self.commandEntry:
            self.commandEntry.focus()
            return
        
        self.codeViewFrame.focus()


    #! COMMAND MANAGER
    def CommandEntryManager(self, *args):
        self.commandEntry.delete(0, 1)
        self.commandEntry.insert(0, '/')

    def CommandInputManager(self, event):
        _input = self.commandEntry.get()[1:]
        
        self.commandEntry.delete(0, tk.END)
        self.CommandEntryManager()

        if _input.lower() in settings.syntaxOptions:
            self.ChangeSyntax(_input.lower())
            return 
        if _input in settings.typefaceOptions:
            self.ChangeTypeface(_input)
        elif _input.lower() == "fe":
            self.FileExplWindowManager()
        elif _input.lower() == "o":
            self.OpenFile()
        elif _input.lower() == "s":
            self.SaveFile()
        elif _input.lower() == "help":
            mb.showinfo("HELP", "FE - File Explorer\nO  - Open File\nS   - Save File\n----------\n<Control-Space> - Fast Focus\n<Control-up>       - Font size up\n<Control-down> - Font size down")
        elif _input.lower() == "!py":
            self.runCommand("py")
        elif _input.lower() == "c":
            self.SettingsWindow()
        elif _input.lower() == "mp":
            self.MusicPlayerWindow()
        elif _input.lower() == "exit":
            exit()
        else:
            self.infoText.configure(text=f":COMMAND NOT FOUND >> {_input.lower()}")
        
    def runCommand(self, _type):
        if _type == "py":
            try:
                os.system(f"py {self.activeFilePath}")
                self.infoText.configure(text=f": RUNNING FILE >> {self.activeFilePath}")
            except Exception as e:
                self.infoText.configure(text=f": CANNOT RUN FILE >> {self.activeFilePath}")            
        else:
            print("command not found")


    #! FILE EXPLORER MANAGEMENT
    def FileExplWindowManager(self):
        if not self.fileExplIsActive:
            self.fileExplFrame = fileExpl.FileExplMain(self.root)
            self.fileExplIsActive = True
            self.fileExplFrame.treeView.bind("<Double-1>", self.FileExpManager)
            self.infoText.configure(text=":FILE MANAGER ACTIVATED")
        else:
            self.fileExplIsActive = False
            self.fileExplFrame.destroy()
            self.infoText.configure(text=":FILE MANAGER DESTROYED")

    def FileExpManager(self, event):
        self.fileExplFrame.TreeViewSelect()
        self.selectedFile = self.fileExplFrame.selectedFile
        if self.selectedFile != "":
            self.OpenFile()


    #! FILE MANAGEMENT
    def OpenFile(self):
        if not self.IsFileEmpty():
            self.AskSaveProgress()

        if self.fileExplIsActive:
            if self.fileExplFrame.selectedFile != "":
                self.activeFilePath = self.fileExplFrame.selectedFile
            else:
                self.activeFilePath = filedialog.askopenfilename()
        else: 
            self.activeFilePath = filedialog.askopenfilename()

        try:
            with open(self.activeFilePath, 'r') as _file:
                _contents = _file.read()
                self.codeViewFrame.delete("1.0", tk.END)
                self.codeViewFrame.insert("1.0", _contents)
            self.infoText.configure(text=f":FILE OPENED >> {self.activeFilePath}")
        except Exception as e:
            self.infoText.configure(text=":CANNOT OPEN FILE")

    def SaveFile(self):
        if self.IsFileEmpty() or self.activeFilePath == "":
            self.activeFilePath = filedialog.asksaveasfilename()
        else:
            _contents = self.codeViewFrame.get("1.0", tk.END)
            with open(self.activeFilePath, "w") as file:
                file.write(_contents)
            _time = time.strftime("%H:%M:%S", time.localtime())
            self.infoText.configure(text=f":FILE SAVED >> {self.activeFilePath} @{_time}")

    def IsFileEmpty(self):
        code = self.codeViewFrame.get("1.0", "end-1c")
        if code != "":
            return False
        return True

    def AskSaveProgress(self):
        _result = mb.askquestion("", "Save File?")
        if (_result == 'yes'):
            self.SaveFile()

    def GetFileName(self, path):
        filename = os.path.basename(path)
        self.root.title(f"{filename}")


    #! KEYS MANAGER
    def handle_tab_key(self):
        self.codeViewFrame.insert("insert", " " * 4)
        return "break"


    #! AUTO FILL OPTIONS
    def handle_keyword_list(self):
        self.keywordList = settings.pythonKeywordList

    def on_key_release(self, event):
        #self.CubeVelManager()
        if self.suggestionBox:
            self.suggestionBox.destroy()
        typed_text = self.get_current_word()
        if typed_text:
            self.show_suggestions(typed_text)

    def get_current_word(self):
        cursor_index = self.codeViewFrame.index(tk.INSERT)
        line = self.codeViewFrame.get(f"{cursor_index.split('.')[0]}.0", f"{cursor_index}")
        # Get the current word based on the cursor position
        words = line.split()
        return words[-1] if words else ''

    def show_suggestions(self, typed_text):
        suggestions = [kw for kw in self.keywordList if kw.startswith(typed_text)]
        if suggestions:
            self.create_suggestion_box(suggestions)

    def create_suggestion_box(self, suggestions):
        print(f"{suggestions}")
        #self.suggestionBox = Listbox(self.root)
        #self.suggestionBox.place(relx=0, rely=0.1, anchor='nw')
        #self.suggestionBox.configure(font=(settings._selected_typeface, 9), bg=settings.backgroundOptions[settings._colorscheme_index], fg="green", borderwidth=0, border=0, highlightthickness=0)
        #for suggestion in suggestions:
        #    self.suggestionBox.insert(tk.END, suggestion)

        #self.suggestionBox.bind("<ButtonRelease-1>", self.on_select)
        #self.suggestionBox.bind("<KeyRelease>", self.on_select_key)

    def nav_items(self, event):
        if self.suggestionBox:
            self.suggestionBox.focus()
            
            if self.suggestionIndex > self.suggestionBox.size()-1:
                self.suggestionIndex = 0

            self.suggestionBox.select_set(self.suggestionIndex)
            self.suggestionIndex+=1

    def on_select(self, event):
        selection = self.suggestionBox.curselection()
        if selection:
            word = self.suggestionBox.get(selection[0])[len(self.get_current_word()):]
            self.codeViewFrame.insert(tk.INSERT, word + ' ')
            self.suggestionBox.destroy()
            self.codeViewFrame.focus()

    def on_select_key(self, event):
        if event.keysym == 'Return':
            selection = self.suggestionBox.curselection()
            if selection:
                word = self.suggestionBox.get(selection[0])[len(self.get_current_word()):]
                self.codeViewFrame.insert(tk.INSERT, word + ' ')
                self.suggestionBox.destroy()
                self.codeViewFrame.focus()


    #! VISUAL METHODS
    def CubeVelManager(self):
        _tempValue = avcube.rot_speed + 0.001
        _tempRounded = round(_tempValue, 3)
        avcube.rot_speed = _tempRounded

    def CubeVelSlower(self, event=None):
        _tempValue = avcube.rot_speed - 0.001
        _tempRounded = round(_tempValue, 3)
        if avcube.rot_speed > 0:
            avcube.rot_speed = _tempRounded
        if avcube.rot_speed < 0:
            avcube.rot_speed = 0
        #self.root.after(1500, self.CubeVelSlower)

    def CubeVisualManager(self, event=None):
        print("Check if cube exists")
        if self.cubeVisualValue.get() == 1:
            print("is enabled and destory")
        else:
            print("Create new cube ref and make sure we clean up the program in general")

    def ChangeColorScheme(self, _index):
        settings._colorscheme_index += _index
        _index = settings._colorscheme_index
        
        if _index > len(settings.backgroundOptions)-1:
            _index = 0

        if _index < 0:
            _index = len(settings.backgroundOptions)-1
        settings._colorscheme_index = _index

        self.infoText.configure(text=f": CHANGING TO COLOR SCHEME {_index}")
        
        _val = settings.colorschemeOptions.get(_index)
        self.codeViewFrame.configure(color_scheme=_val)
        
        for _frame in self.totalFrames:
            _frame.configure(bg=settings.backgroundOptions[_index])

        for _widget in self.totalWidgets:
            _widget.configure(bg=settings.backgroundOptions[_index], fg=settings.fontColorOptions[_index])
        
        self.commandEntry.configure(insertbackground=settings.fontColorOptions[_index])

        self.codeViewFrame.mainStyle.configure("TScrollbar",
            gripcount=0,
            griprelief="flat",
            background=settings.highlightColorOptions[_index],
            
            foreground=settings.backgroundOptions[_index],

            troughcolor=settings.backgroundOptions[_index],

            bordercolor=settings.backgroundOptions[_index],
            darkcolor=settings.backgroundOptions[_index], 
            lightcolor=settings.backgroundOptions[_index]
        )
        
        self.codeViewFrame.mainStyle.map("TScrollbar",
            background=[("active", settings.highlightColorOptions[_index]), ("pressed", settings.highlightColorOptions[_index])],
            troughcolor=[("active", settings.backgroundOptions[_index]), ("pressed", settings.backgroundOptions[_index])],
            arrowcolor=[("active", settings.fontColorOptions[_index]), ("pressed", settings.backgroundOptions[_index])]
        )

    def ChangeSyntax(self, _syntax):
        settings._selected_syntax = _syntax
        self.codeViewFrame.configure(lexer=settings.syntaxOptions[settings._selected_syntax])
        self.infoText.configure(text=f": SYNTAX CHANGED TO >> {_syntax}")
        self.syntaxText.configure(text=f"{_syntax}")

    def ChangeFontSize(self, _amt):
        settings._fontSize += _amt
        self.codeViewFrame.configure(font=(settings._selected_typeface, settings._fontSize))

    def ChangeTypeface(self, _val):
        settings._selected_typeface = _val
        for _widget in self.totalWidgets:
            _widget.configure(font=(_val, 9))
        self.codeViewFrame.configure(font=(_val, settings._fontSize))


    #! SOUND MANAGER
    def PlayClickSound(self, event=None):
        self.clickSound.play()

    def ChangeMixerVolume(self, event=None):
        self.clickSound.set_volume(self.volumeValue.get())


    #! SETTINGS MANAGER
    def SettingsWindow(self):
        _bgc = settings.backgroundOptions[settings._colorscheme_index]
        _fgc = settings.fontColorOptions[settings._colorscheme_index]
        #? Highlight color
        self.settingWindowFrame = tk.Toplevel(self.root)
        self.settingWindowFrame.geometry("300x200")
        self.settingWindowFrame.configure(bg=_bgc)
        
        configNotebook = ttk.Notebook(self.settingWindowFrame)
        configNotebook.pack(fill=tk.BOTH, expand=True)

        settingsTab = tk.Frame(configNotebook, bg=_bgc)
        configNotebook.add(settingsTab, text="EDITOR")

        audioTab = tk.Frame(configNotebook, bg=_bgc)
        configNotebook.add(audioTab, text="AUDIO")

        visualTab = tk.Frame(configNotebook, bg=_bgc)
        configNotebook.add(visualTab, text="VISUAL")
        
        #spacer1 = tk.Label(settingsTab, tex="").pack(pady=2)
        typefaceLabel = tk.Label(settingsTab, text="TYPEFACE", font=(settings._selected_typeface, 9), bg=_bgc, fg=_fgc)
        typefaceLabel.pack(side=tk.TOP)
        self.typefaceValue = tk.StringVar(self.root)
        self.typefaceValue.set(settings._selected_typeface)
        typefaceDropdown = tk.OptionMenu(settingsTab, self.typefaceValue, *settings.typefaceOptions, command=lambda event:self.ChangeTypeface(self.typefaceValue.get()))
        typefaceDropdown.pack(side=tk.TOP)
        

        #! AUDIO
        self.musicVolumeLabel = tk.Label(audioTab, text="MUSIC VOLUME", font=(settings._selected_typeface, 9), bg=_bgc, fg=_fgc)
        self.musicVolumeLabel.pack(side=tk.TOP)

        self.musicVolumeSlider = tk.Scale(audioTab, from_=0.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL)
        self.musicVolumeSlider.pack(side=tk.TOP)
        self.musicVolumeSlider.configure(bg=_bgc, fg=_fgc)


        self.mainVolumeLabel = tk.Label(audioTab, text="SOUND VOLUME", font=(settings._selected_typeface, 9), bg=_bgc, fg=_fgc)
        self.mainVolumeLabel.pack(side=tk.TOP)
        self.mainVolumeSlider = tk.Scale(audioTab, from_=0.0, to=1.0, variable=self.volumeValue, resolution=0.1, orient=tk.HORIZONTAL, command=lambda event: self.ChangeMixerVolume("none"))
        self.mainVolumeSlider.pack(side=tk.TOP)
        self.mainVolumeSlider.configure(bg=_bgc, fg=_fgc)
        

        #! VISUAL
        self.cubeThreadBtn = tk.Checkbutton(visualTab, variable=self.cubeVisualValue, text="Cube Viewer", onvalue=1, offvalue=0, command=lambda: self.CubeVisualManager("none"))
        self.cubeThreadBtn.pack(side=tk.TOP)
        # FG changes the check mark color as well
        self.cubeThreadBtn.configure(bg=_bgc)

        self.SettingsWindowStyle()


    def SettingsWindowStyle(self):
        _tindex = settings._colorscheme_index
        _backgroundColor = settings.backgroundOptions[_tindex]
        _foregroundColor = settings.fontColorOptions[_tindex]
        _highlightColor = settings.highlightColorOptions[_tindex]
        tempStyle = ttk.Style()
        tempStyle.configure('TNotebook', background=_backgroundColor)
        tempStyle.configure('TNotebook.Tab', background=_highlightColor)
        tempStyle.map('TNotebook.Tab', 
            background=[ ('selected', _backgroundColor) ],
            foreground=[ ('selected', _highlightColor) ]
        )


    #! MUSIC PLAYER
    def MusicPlayerWindow(self):
        _bgc = settings.backgroundOptions[settings._colorscheme_index]
        _fgc = settings.fontColorOptions[settings._colorscheme_index]

        self.musicPlayerFrame = tk.Toplevel(self.root)
        self.musicPlayerFrame.title("MUSIC PLAYER")
        self.musicPlayerFrame.configure(bg=_bgc)

        infoFrame = tk.Frame(self.musicPlayerFrame, bg=_bgc)
        infoFrame.pack(fill=tk.BOTH, side=tk.TOP)

        controlFrame = tk.Frame(self.musicPlayerFrame, bg=_bgc)
        controlFrame.pack(fill=tk.BOTH, side=tk.BOTTOM)
        
        self.songTitleLabel = tk.Label(infoFrame, text="SONG TITLE", font=(settings._selected_typeface, 9))
        self.songTitleLabel.pack(side=tk.TOP)
        self.songTitleLabel.configure(bg=_bgc, fg=_fgc)

        self.playButton = tk.Button(controlFrame, text="PLAY", font=(settings._selected_typeface, 9), command=self.PlaySong)
        self.playButton.pack(side=tk.LEFT)
        self.playButton.configure(bg=_bgc, fg=_fgc)

        self.stopButton = tk.Button(controlFrame, text="STOP", font=(settings._selected_typeface, 9), command=self.StopSong)
        self.stopButton.pack(side=tk.LEFT)
        self.stopButton.configure(bg=_bgc, fg=_fgc)

    def PlaySong(self):
        musicFP = filedialog.askopenfilename()
        pygame.mixer.music.load(musicFP)
        pygame.mixer.music.play()

    def StopSong(self):
        pygame.mixer.music.stop()


if __name__ == "__main__":
    WEdit()


