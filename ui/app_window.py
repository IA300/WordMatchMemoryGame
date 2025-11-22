# ui/app_window.py

import tkinter as tk
from .pages import MenuPage, SettingsPage, NewGamePage, RatingPage, GamePage
from game.file_tool import load_words

# 继承了 Tk 的主窗口
class AppWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Word-match Memory Game")

        self.geometry("1200x900")

        # 自己的窗口自己的属性新增了 dict
        self.word_dict = load_words()
        
        # 各个页面 pages 
        self.pages = {
            "menu": MenuPage(self),
            "settings": SettingsPage(self),
            "new_game": NewGamePage(self),
            "rating": RatingPage(self),
            "game": GamePage(self)
        }

        self.show_page("menu")

    # 隐藏其它，显示对应页（Frame）
    def show_page(self, page_name):
        for name, page in self.pages.items():
            page.pack_forget()
        self.pages[page_name].pack(fill="both", expand=True)