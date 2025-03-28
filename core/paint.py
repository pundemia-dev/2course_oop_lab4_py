import customtkinter
from tkinter import Canvas
from core.container import Container
from core.figure_buttons import Figures 
from core.palette import Palette
import importlib
import os

class Paint(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.default_color = "#6B8E23"  # CD5C5C
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
        
        for file in filter(lambda x: ".py" in x, os.listdir("core/figures/")):
            module = importlib.import_module(f"core.figures.{file.split(".")[0]}")
            info = getattr(module, "info")
            new_class = getattr(module, info[-1])
            self.container.add_class(new_class, info[-1])
            self.figures_frame.add_info(info)

        self.figures_frame.create_buttons()
        
    def enable_figures_binds(self, _):
        self.master.bind("<Escape>", self.figures_frame.unselect_figure)
        self.master.bind_class("CTkButton", "<Escape>", self.figures_frame.unselect_figure)

    def disable_figures_binds(self, _):
        self.master.unbind_class("CTkButton", "<Escape>")    

    def enable_canvas_binds(self, _):
        self.canvas.bind("<ButtonRelease-1>", lambda event, class_id=self.figures_frame.selected_figure: self.container.new_obj(self.palette_frame.get(), class_id, event) if class_id else None)
        self.canvas.bind("<Button-3>", self.container.select_objects)
        self.master.bind("<Delete>", self.container.delete_objects)
        self.master.bind("<BackSpace>", self.container.delete_objects)
        self.master.bind("<Escape>", self.container.unselect_objects)
        self.canvas.bind("<B1-Motion>", lambda event: self.container.process_interaction("move", event))
        self.canvas.bind("<Shift-B1-Motion>", lambda event: self.container.process_interaction("resize", event))
        self.master.bind("<Control-a>", self.container.select_all_objects)

    def disable_canvas_binds(self, _):
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.unbind("<Button-3>")
        self.master.unbind("<Delete>")
        self.master.unbind("<BackSpace>")
        self.master.unbind("<Escape>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<Shift-B1-Motion>")
        self.master.unbind("Control-a")

