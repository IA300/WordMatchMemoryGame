import tkinter as tk
from tkinter import Button, Label
from game.config import *

class MenuPage(tk.Frame):
    def __init__(self, parent):

        super().__init__(parent)
        self.parent = parent

        # 标题（与 BUTTON_CONFIG 颜色一致）
        title_style = LABEL_CONFIG.copy()
        title_style['font'] = (title_style['font'][0],int(title_style['font'][1]*1.5))
        title_style["bg"] = self.cget("bg")  # 让 Label 看起来透明
        title = Label(self, text="Word-match Memory Game", **title_style)
        title.place(anchor="n", relx=0.5, rely=0.08)

        # 主菜单的 新游戏 按钮
        btn_new = Button(self, text="New Game", **BUTTON_CONFIG,command=lambda: parent.show_page("new_game"))
        btn_new.place(anchor="center", relx=0.5, rely=0.3)

        # rating 按钮
        def load_ratings():
            parent.pages["rating"].load()
            parent.show_page("rating")
        btn_rating = Button(self, text="Rating", **BUTTON_CONFIG,command=load_ratings)
        btn_rating.place(anchor="center", relx=0.5, rely=0.6)

        # settings 按钮
        btn_settings = Button(self, text="Settings", **BUTTON_CONFIG,command=lambda: parent.show_page("settings"))
        btn_settings.place(anchor="se", relx=1.0, rely=1.0)
