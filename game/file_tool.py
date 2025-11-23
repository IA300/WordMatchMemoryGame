import json,os
import tkinter as tk
from tkinter import messagebox

# 从对应的文件路径中加载数据 
def load_words(filepath=None):
    # 如果空 就找默认的 assets/words.json
    if filepath is None:
        filepath = os.path.join(os.path.dirname(__file__),"..", "assets", "words.json")
    try:
        # 否则尝试使用 utf-8 编码 读取 该文件 
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # 就 报错
        messagebox.showerror("错误","找不到单词文件，请检查单词文件是否存在！")
    

def load_ratings():
    rating_file = os.path.join(os.path.dirname(__file__),"..", "assets", "ratings.json")
    # os.path模块 的 exits函数 ，没有 file 就没有记录， 尾插一个即可
    if not os.path.exists(rating_file):
        return []
    try:
        with open(rating_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return []

# 保存 ratings.json
def save_rating(name, rating):
    rating_file = os.path.join(os.path.dirname(__file__), "..", "assets", "ratings.json")
    ratings = []
    if os.path.exists(rating_file):
        try:
            with open(rating_file, "r", encoding="utf-8") as f:
                ratings = json.load(f)
        except Exception as e:
            pass
    ratings.append({"name": name, "rating": rating})
    ratings.sort(key=lambda x: x["rating"], reverse=True)

    with open(rating_file, "w", encoding="utf-8") as f:
        json.dump(ratings, f, ensure_ascii=False, indent=2)