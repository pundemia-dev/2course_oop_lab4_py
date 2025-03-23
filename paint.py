import customtkinter
from tkinter import Canvas
from container import Container
from figure_buttons import Figures 
from palette import Palette


class Paint(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.default_color = "#6B8E23"  # CD5C5C
        self.brush_size = 40
        self.configure(fg_color="#242424")
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure((0, 1), weight=0)
        self.grid_columnconfigure(2, weight=1)

        self.canvas = Canvas(self, bg="#242424", highlightbackground="#242424")
        self.canvas.grid(row=1, column=0, padx=2, pady=2, sticky="nsew", columnspan=3)
        self.container = Container(self.canvas)
        self.canvas.bind("<Enter>", self.enable_canvas_binds)
        self.canvas.bind("<Leave>", self.disable_canvas_binds)

        self.figures_frame = Figures(self)
        self.figures_frame.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.figures_frame.bind("<Enter>", self.enable_figures_binds)
        self.figures_frame.bind("<Leave>", self.disable_figures_binds)

        self.palette_frame = Palette(self, self.container.fill)
        self.palette_frame.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")
        
    def enable_figures_binds(self, _):
        self.master.bind("<Escape>", self.figures_frame.unselect_figure)
        self.master.bind_class("CTkButton", "<Escape>", self.figures_frame.unselect_figure)

    def disable_figures_binds(self, _):
        self.master.unbind_class("CTkButton", "<Escape>")    

    def enable_canvas_binds(self, _):
        self.canvas.bind("<Button-1>", lambda event: self.container.new_circle(self.palette_frame.get(), event))
        self.canvas.bind("<Button-3>", self.container.select_objects)
        self.master.bind("<Delete>", self.container.delete_objects)
        self.master.bind("<BackSpace>", self.container.delete_objects)
        self.master.bind("<Escape>", self.container.unselect_objects)
        self.canvas.bind("<B1-Motion>", self.container.move)
        self.canvas.bind("<ButtonRelease-1>", self.container.button_release)

    def disable_canvas_binds(self, _):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Button-3>")
        self.master.unbind("<Delete>")
        self.master.unbind("<BackSpace>")
        self.master.unbind("<Escape>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

