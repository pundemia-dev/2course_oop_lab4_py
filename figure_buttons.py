import customtkinter
import inspect


class Figures(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.parent = master
        self.selected_figure = None
        self.buttons = list()
        self.icons = [
                ("─", 25, "line"),
                ("▭", 25, "rectangle"),
                ("□", 25, "square"),
                ("⬭", 25, "oval"),
                ("◯", 20, "circle"),
                ("△", 25, "triangle")
            ]
        self.buttons_template = [{
            "master": self,
            "text": icon,
            "width": 40,
            "height": 40,
            "border_spacing": 0,
            "fg_color": "gray20",
            "hover_color": "#D3869B",
            "text_color": "#B16286",
            "border_color": "#B16286",
            "font": ("Roboto Medium", size),
            "command": lambda cmd=cmd: self.select_figure(cmd)
            } for icon, size, cmd in self.icons]
        
        self.buttons = [customtkinter.CTkButton(**t) for t in self.buttons_template]
        i = 0
        for y in range(2):
             for x in range(3):
                self.buttons[i].grid(row=y, column=x, padx=2, pady=2, sticky="nsew")
                i += 1

    def select_figure(self, figure):
        # print(list(inspect.signature(self.buttons[0].cget("command")).parameters.values())[0].default, "|", figure)
        if self.selected_figure != figure and self.selected_figure != None:
            list(filter(lambda x: list(inspect.signature(x.cget("command")).parameters.values())[0].default==self.selected_figure, self.buttons))[0].configure(border_width=0)
        self.selected_figure = figure if self.selected_figure != figure else None
        list(filter(lambda x: list(inspect.signature(x.cget("command")).parameters.values())[0].default==figure, self.buttons))[0].configure(border_width=2 if self.selected_figure == figure else 0)

    def unselect_figure(self, _):
        if self.selected_figure != None:
            self.select_figure(self.selected_figure)

