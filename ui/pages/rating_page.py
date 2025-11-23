import json,os
import tkinter as tk
from tkinter import Button, Listbox, Label, messagebox
from game.config import *
from game.file_tool import load_ratings

class RatingPage(tk.Frame):

    # rating 是动态的 不要只在 init 执行加载，而是封装一个 load_ratings 灵活调用
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # 标题
        title_style = LABEL_CONFIG.copy()
        title_style["bg"] = self.cget("bg")
        # title_style["font"] = (title_style["font"][0],50)
        title = Label(self, text="Ratings", **title_style)
        title.place(anchor="n", relx=0.3, rely=0.06)

        # listbox部件 
        self.lb = Listbox(self, font=("Fixedsys", 30), width=30, height=20)
        self.lb.place(anchor="center", relx=0.3, rely=0.55)

        # 返回 menu 按钮 
        btn_menu = Button(self, text="Menu",**BUTTON_CONFIG,command=lambda: parent.show_page("menu"))
        btn_menu.place(anchor="se", relx=1.0, rely=1.0)

        # 右侧段位说明（使用透明背景 Label）
        legend_frame = tk.Frame(self, bg=self.cget("bg"))
        legend_frame.place(anchor="ne", relx=0.98, rely=0.25)

        # 侧栏小标题使用 LABEL_CONFIG 的字体主题但更小字号
        base_font = LABEL_CONFIG.get("font", FONT_DATA)
        base_font = (base_font[0],int(base_font[1]*0.7))
        try:
            hdr_font = (base_font[0], max(12, (base_font[1] if len(base_font) > 1 else FONT_DATA[1]) - 6))
        except Exception:
            print("error")
            hdr_font = (FONT_DATA[0], max(12, FONT_DATA[1]-6))
        hdr = Label(legend_frame, text="Ranks", font=hdr_font, fg=LABEL_CONFIG["fg"], bg=self.cget("bg"), bd=0)
        hdr.pack(anchor="ne", pady=(0,60))

        # 按阈值从高到低显示（高段位在上）
        thresholds = sorted((int(k), k) for k in RATING_TITLES.keys())
        for th_int, th_key in sorted(thresholds, reverse=True):
            title_text = RATING_TITLES.get(th_key, th_key)
            color = RATING_COLOR.get(th_key, "black")
            row = tk.Frame(legend_frame, bg=self.cget("bg"))
            # 小色块作为色标
            sw = Label(row, width=2, bg=color, bd=0, relief="flat")
            sw.pack(side="left", padx=(0,6))
            # 段位名称（透明背景）
            try:
                txt_font = (base_font[0], max(10, (base_font[1] if len(base_font) > 1 else FONT_DATA[1]) - 10))
            except Exception:
                txt_font = (FONT_DATA[0], max(10, FONT_DATA[1]-10))
            txt = Label(row, text=f"{title_text} ({th_int})", font=txt_font, fg=color, bg=self.cget("bg"), bd=0)
            txt.pack(side="left")
            row.pack(anchor="ne", pady=2)

    def _color_for_rating(self, rating):
        try:
            r = int(rating)
        except Exception:
            return "black"

        # 把阈值键转换为整数并排序
        thresholds = sorted((int(k), v) for k, v in RATING_COLOR.items())
        chosen = "black"
        for th, col in thresholds:
            if r >= th:
                chosen = col
            else:
                break
        return chosen

    def load(self):
         # lb 的区间删除函数
         self.lb.delete(0, tk.END)  # 清空
         ratings = load_ratings()
         if not ratings: 
             self.lb.insert(tk.END, "暂无记录")
         else:
             # 否则 遍历 dict 
             for i, r in enumerate(ratings, 1):
                 text = f"{i}. {r['name']} - {r['rating']}"
                 self.lb.insert(tk.END, text)
                 # 根据 rating 设置该行文字颜色
                 try:
                     color = self._color_for_rating(r.get("rating", 0))
                 except Exception:
                     color = "black"
                 # listbox 的索引从 0 开始
                 try:
                     self.lb.itemconfig(i - 1, fg=color)
                 except Exception:
                     try:
                         self.lb.itemconfig(i - 1, foreground=color)
                     except Exception:
                         pass