# ui/pages/new_game_page.py

import tkinter as tk
from tkinter import Button, Label, OptionMenu, Checkbutton, StringVar, BooleanVar
from game.config import *

class NewGamePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        # 标题与副标题
        title_style = LABEL_CONFIG.copy()
        title_style["bg"] = self.cget("bg")
        title = Label(self, text="New Game", **title_style)
        title.place(anchor="n", relx=0.5, rely=0.04)
        # 副标题使用相同字体主题但更小字号
        f = title_style.get("font", FONT_DATA)
        try:
            sub_font = (f[0], 14)
        except Exception:
            sub_font = (FONT_DATA[0], 14)
        sub = Label(self, text="choose difficulty and mode, and type START! ", font=sub_font, fg=LABEL_CONFIG["fg"], bg=self.cget("bg"))
        sub.place(anchor="n", relx=0.5, rely=0.12)

        # 选项(str)列表，从 DIFFICULTIES 中获取
        diff_options = [
            f"{name}({attr['rows']}x{attr['cols']})" for name, attr in DIFFICULTIES.items()
        ]

        self.diff = StringVar(value=diff_options[0])
        
        # 创建 菜单选项 
        self.om_diff = OptionMenu(self, self.diff, *diff_options)
        self.om_diff.config(font=FONT_DATA)
        self._update_diff_color()
        self.om_diff["menu"].config(font=FONT_DATA)
        for i, (name, attr) in enumerate(DIFFICULTIES.items()):
            self.om_diff["menu"].entryconfig(i, foreground=attr["color"])
        self.diff.trace_add("write", self._update_diff_color)
        self.om_diff.place(anchor="center", relx=0.5, rely=0.2)

        # 动态变量：模式选择
        self.mode = StringVar(value="A-B")

        # 又一个选项框
        self.om_mode = OptionMenu(self, self.mode, "A-A", "B-B", "A-B")
        self.om_mode.config(font=FONT_DATA)
        self.om_mode["menu"].config(font=FONT_DATA)
        self.om_mode.place(anchor="center", relx=0.5, rely=0.4)

        # Colorful 动态变量
        self.colorful = BooleanVar(value=False)

        # colorful 按钮
        cb = Checkbutton(self, text="Colorful", variable=self.colorful, font=FONT_DATA)
        cb.place(anchor="center", relx=0.5, rely=0.6)

        # Start 按钮
        btn_start = Button(self, text="START", **BUTTON_CONFIG, command=self._start_game)
        btn_start.place(anchor="center", relx=0.5, rely=0.8)

        # 跳转Menu 按钮
        btn_menu = Button(self, text="Menu", **BUTTON_CONFIG,command=lambda: parent.show_page("menu"))
        btn_menu.place(anchor="se", relx=1.0, rely=1.0)

    # 配置选中后的颜色
    def _update_diff_color(self, *args):
        diff_name = self.diff.get().split("(")[0]
        color = DIFFICULTIES[diff_name]["color"]
        self.om_diff.config(fg=color, activeforeground=color)

    # 开始游戏
    def _start_game(self):
        # 传递配置给 GamePage
        config = {
            "difficulty": self.diff.get().split("(")[0],
            "mode": self.mode.get(),
            "colorful": self.colorful.get(),
            "word_dict": self.parent.word_dict
        }
        # 依然需要额外配置
        self.parent.pages["game"].start(config)
        self.parent.show_page("game")