import customtkinter
from tkinter import colorchooser


class Palette(customtkinter.CTkFrame):
    def __init__(self, master, fill_function):
        super().__init__(master)
        self.fill_function = fill_function
        self.selected_color = "#B16286"
        self.buttons = list()
        self.colors = [
                ("#CC241D", "#fb4934"),
                ("#98971A", "#B8BB26"),
                ("#D79921", "#fABD2F"),
                ("#458588", "#83A598"),
                ("#B16286", "#D3869B"),
                ("#689D6A", "#8EC07C"),
                ("#D65D0E", "#FE8019"),
                ("#D5C4A1", "#EBDBB2"),
                ("#282828", "#3C3836"),
                ("gray15", "gray20")
            ]
        self.buttons_template = [{
            "master": self, 
            "text": "", 
            "width": 40, 
            "height": 40, 
            "border_width": 2,
            "fg_color": fg,
            "hover_color": hv,
            "border_color": "gray25",
            "command": lambda fg=fg: self.select_color(fg)
            } for fg, hv in self.colors]
        self.buttons_template[-1]["text"] = "..."
        self.buttons_template[-1]["command"] = self.fill

        self.buttons = [customtkinter.CTkButton(**t) for t in self.buttons_template]
        self.buttons[-1].bind("<Button-3>", self.colorchanger)
        i = 0
        for y in range(2):
            for x in range(5):
                self.buttons[i].grid(row=y, column=x, padx=2, pady=2, sticky="nsew")
                i += 1
    
    def colorchanger(self, _):
        (rgb, hx) = colorchooser.askcolor()
        if hx != None:
            self.select_color(hx)

    def select_color(self, color):
        self.buttons[-1].configure(fg_color=color)
        self.selected_color = color

    def get(self):
        return self.selected_color

    def fill(self):
        self.fill_function(self.selected_color)

