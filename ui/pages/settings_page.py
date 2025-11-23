import json
import tkinter as tk
from tkinter import Button
from tkinter import filedialog,messagebox
from game.file_tool import load_words
from game.config import *

class SettingsPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # 导入按钮的 导入函数，因为复杂 
        def import_words():
            filepath = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
            )
            if filepath:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        parent.word_dict = json.load(f)
                    messagebox.showinfo(
                        title="Info",
                        message=f"导入成功：{filepath}\n{len(parent.word_dict)}个单词"
                    )
                except Exception as e:
                    # 否则弹出一个警告，导入失败
                    messagebox.showerror(title="Error",message="导入失败："+str(e))

        # 导入按钮
        btn_import = Button(self, text="Import...", **BUTTON_CONFIG, command=import_words)
        btn_import.place(anchor="nw", relx=0.1, rely=0.1)

        # 主菜单按钮 
        btn_menu = Button(self, text="Menu", **BUTTON_CONFIG,command=lambda: parent.show_page("menu"))
        btn_menu.place(anchor="se", relx=1.0, rely=1.0)