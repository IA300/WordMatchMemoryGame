# ui/pages/game_page.py

import random,time,json,os
import tkinter as tk
from tkinter import Button, Label, simpledialog
from game.game_logic import GameLogic
from game.config import *
from game.file_tool import save_rating

class GamePage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        # 页面标题（会在 start 时更新为难度/模式）
        self.title_label = Label(self, text="Memory Game", **LABEL_CONFIG)
        self.title_label.place(anchor="n", relx=0.5, rely=0.02)

        # 时间
        self.time_label = Label(self, text="Time: 0", font=FONT_DATA)
        self.time_label.place(anchor="ne", relx=1, rely=0)

        # 惩罚
        self.penalty_label = Label(self, text="Penalty: 0", font=FONT_DATA, fg="#F59794")
        self.penalty_label.place(anchor="ne", relx=1, rely=0.05)

        # 分数
        self.score_label = Label(self, text="Score: 0", font=FONT_DATA)
        self.score_label.place(anchor="nw", relx=0, rely=0)

        # 连击
        self.combo_label = Label(self, text="Combo: 0", font=FONT_DATA, fg="orange")
        self.combo_label.place(anchor="nw", relx=0, rely=0.05)

        # 返回菜单按钮 
        btn_menu = Button(self,text="Menu",**BUTTON_CONFIG,command=self._exit_game)
        btn_menu.place(anchor="se", relx=1.0, rely=1.0)

        # 游戏状态
        self.reset_game_state()

    # 初始化
    def reset_game_state(self):
        self.game_logic = None
        self.flipped_cards = []
        self.matched_pairs = 0
        self.total_pairs = 0
        self.card_states = {}  # id ->
        self.card_identities = {}  # id -> info
        self.btns = []
        self.penalty_time = 0
        self.game_start_time = None
        self.timer_id = None

        self.sel_r = 0
        self.sel_c = 0
        self.pos_to_id = {}  # (r,c) -> card_id

    # 退出
    def _exit_game(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)
        # 销毁所有按钮
        for row in self.btns:
            for btn in row:
                if btn:
                    btn.destroy()
        # 解除键盘绑定
        self._unbind_keys()
        self.reset_game_state()
        self.parent.show_page("menu")

    # 启动
    def start(self, config):
        self.reset_game_state()
        self.config = config
        self.word_dict = config["word_dict"]
        self.mode = config["mode"]
        self.colorful = config["colorful"]

        # 更新标题，显示当前难度与模式
        try:
            self.title_label.config(text=f"{config['difficulty']}  —  {self.mode}")
        except Exception:
            pass

        diff = DIFFICULTIES[config["difficulty"]]
        self.rows, self.cols = diff["rows"], diff["cols"]

        # 初始化按钮网格
        self.btns = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.pos_to_id = {}

        # 清除旧权重
        max_r = DIFFICULTIES["Hard"]["rows"]+2
        max_c = DIFFICULTIES["Hard"]["cols"]+2
        for i in range(max_r):
            self.grid_rowconfigure(i, weight=0)
        for j in range(max_c):
            self.grid_columnconfigure(j, weight=0)

        # 设置边距
        self.grid_rowconfigure(0, minsize=100)
        self.grid_rowconfigure(max_r-1, minsize=60)
        self.grid_columnconfigure(0, minsize=60)
        self.grid_columnconfigure(max_c-1, minsize=60)

        # 配置卡片区域权重（居中）
        for i in range(1,self.rows+1):
            self.grid_rowconfigure(i, weight=1)
        for j in range(1,self.cols+1):
            self.grid_columnconfigure(j, weight=1)

        # 生成卡片布局
        card_data = self._generate_card_data()
        random.shuffle(card_data)

        # 创建按钮
        for card in card_data:
            x, y = card["position"]
            color = random.choice(COLORS) if self.colorful else "black"

            # 使用一个容器 frame 包裹按钮（不改变按钮 padding）
            cell = tk.Frame(self, highlightthickness=0, bd=0)
            cell.grid(row=1 + x, column=1 + y, sticky="nsew", padx=0, pady=0)

            # 合并配置：以 BUTTON_CONFIG 为基础，再用 CARD_STYLE 覆盖（font/size/width/height）
            btn_style = {}
            # btn_style.update(BUTTON_CONFIG)   
            btn_style.update(CARD_STYLE)      
            # 卡片文本颜色按随机 color 设置（覆盖可能的 fg）
            btn_style["fg"] = color
            # 创建按钮，禁止 Tab 聚焦（takefocus=0）
            btn = Button(
                cell,
                text="?",
                command=lambda cid=card["id"]: self._on_card_click(cid),
                takefocus=0,
                **btn_style,
            )
            btn.pack(expand=True, fill="both", padx=2, pady=2)
            # 存放容器（用于布局），按钮对象仍保存在 card_identities
            self.btns[x][y] = cell

            # 记录默认按钮背景色（用于恢复）；优先取配置里的 bg
            if not hasattr(self, "_default_btn_bg"):
                try:
                    self._default_btn_bg = btn_style.get("bg", btn.cget("bg"))
                except Exception:
                    self._default_btn_bg = self.cget("bg")

            self.card_states[card["id"]] = "hidden"
            self.card_identities[card["id"]] = {
                "button": btn,
                "content": card["content"],
                "pair_id": card["pair_id"],
                "type": card["type"],
                "position": (x, y),
            }
            # map position -> id, 供键盘翻牌使用
            self.pos_to_id[(x, y)] = card["id"]

        self.total_pairs = len(card_data) // 2
        self.game_logic = GameLogic(self.mode)

        self.showing = True
        for identity in self.card_identities.values():
            btn = identity["button"]
            content = identity["content"]
            btn.config(text=content)
        
        def hide():
            for identity in self.card_identities.values():
                btn = identity["button"]
                btn.config(text="?")
            
            self.showing = False
            self._start_timer()
            # 重置 UI 标签
            self.time_label.config(text="Time: 0")
            self.penalty_label.config(text="Penalty: 0")
            self.score_label.config(text="Score: 0")
            self.combo_label.config(text="Combo: 0")

            # 初始化键盘选择并绑定按键
            self.sel_r, self.sel_c = 0, 0
            self._update_selection_highlight()
            self._bind_keys()

        self.parent.after(DELAY_TIME,hide)
        
    # 生成数据 
    def _generate_card_data(self):
        n, m = self.rows, self.cols
        tot = n * m
        assert tot % 2 == 0

        items = list(self.word_dict.items())
        k = len(items)
        positions = list(range(tot))
        random.shuffle(positions)
        indices = list(range(k))
        random.shuffle(indices)

        card_data = []
        card_id = 0

        for i in range(0, tot, 2):
            idx = indices[(i // 2) % k]
            word, meaning = items[idx]
            x1, y1 = positions[i] // m, positions[i] % m
            x2, y2 = positions[i + 1] // m, positions[i + 1] % m

            if self.mode == "A-A":
                c1, t1 = word, "A"
                c2, t2 = word, "A"
                pid = word
            elif self.mode == "B-B":
                c1, t1 = meaning, "B"
                c2, t2 = meaning, "B"
                pid = meaning
            else:  # A-B
                c1, t1 = word, "A"
                c2, t2 = meaning, "B"
                pid = f"{word}|{meaning}"

            card_data.append(
                {
                    "position": (x1, y1),
                    "content": c1,
                    "type": t1,
                    "pair_id": pid,
                    "id": card_id,
                }
            )
            card_id += 1
            card_data.append(
                {
                    "position": (x2, y2),
                    "content": c2,
                    "type": t2,
                    "pair_id": pid,
                    "id": card_id,
                }
            )
            card_id += 1

        return card_data

    def _on_card_click(self, card_id):
        if self.showing or self.card_states[card_id] != "hidden" or len(self.flipped_cards) >= 2:
            return

        info = self.card_identities[card_id]
        btn = info["button"]
        btn.config(text=info["content"])
        self.card_states[card_id] = "flipped"
        self.flipped_cards.append(card_id)

        if len(self.flipped_cards) == 2:
            self.after(800, self._check_match)

    def _check_match(self):
        if len(self.flipped_cards) != 2:
            return

        id1, id2 = self.flipped_cards
        info1 = self.card_identities[id1]
        info2 = self.card_identities[id2]

        if self.game_logic.check_match(info1, info2):
            # 成功
            self.card_states[id1] = "matched"
            self.card_states[id2] = "matched"
            self.matched_pairs += 1

            for cid in [id1, id2]:
                btn = self.card_identities[cid]["button"]
                btn.config(bg="lightgreen", state="disabled")

            combo, score = self.game_logic.on_success()
            self.combo_label.config(text=f"Combo: {combo}")
            self.score_label.config(text=f"Score: {score}")

            if self.matched_pairs == self.total_pairs:
                self.after(500, self._game_complete)
        else:
            # 失败
            self.penalty_time += 5
            self.penalty_label.config(text=f"Penalty: {self.penalty_time}")
            for cid in [id1, id2]:
                self.card_identities[cid]["button"].config(text="?")
                self.card_states[cid] = "hidden"

            self.combo_label.config(text="Combo: 0")

        self.flipped_cards = []

    def _start_timer(self):
        self.game_start_time = time.time()
        self._update_timer()

    def _update_timer(self):
        if self.game_start_time:
            elapsed = int(time.time() - self.game_start_time)
            total = elapsed + self.penalty_time
            self.time_label.config(text=f"Time: {total}")
            self.timer_id = self.after(1000, self._update_timer)

    def _game_complete(self):
        if self.timer_id:
            self.after_cancel(self.timer_id)

        total_time = int(time.time() - self.game_start_time) + self.penalty_time
        base_time = total_time - self.penalty_time
        difficulty = self.config["difficulty"]

        # === 新 Rating 计算（融合 Time, Penalty, Score, Combo）===
        base_rating = 1000

        # 时间奖励（按难度设定上限）
        if difficulty == "Easy":
            time_limit = 180  # 3分钟
        elif difficulty == "Mid":
            time_limit = 360  # 6分钟
        else:  # Hard
            time_limit = 720  # 12分钟

        time_bonus = max(0, time_limit - base_time)*6

        # 罚时惩罚
        penalty_reduction = self.penalty_time * 5

        # 分数奖励
        score_bonus = self.game_logic.score // 10

        # 连击奖励
        combo_bonus = self.game_logic.max_combo * 3

        # 合并
        rating = (
            base_rating
            + time_bonus
            - penalty_reduction
            + score_bonus
            + combo_bonus
        )
        rating = max(800, int(rating))  # 最低 800

        # === 弹出输入名字 ===
        name = simpledialog.askstring(
            "游戏完成！",
            f"总时间: {total_time}秒\n"
            f"Score: {self.game_logic.score}\n"
            f"Max Combo: {self.game_logic.max_combo}\n"
            f"Rating: {rating}\n"
            "请输入你的名字：",
        )
        if not name:
            name = "Anonymous"

        # === 保存到文件 ===
        save_rating(name, int(rating))

        self._exit_game()

    # ====== 新增：键盘支持相关函数 ======
    def _bind_keys(self):
        # 绑定到 root，确保窗口任何地方都能接收按键
        root = self.parent
        root.bind_all("<Left>", lambda e: self._move_selection(0, -1))
        root.bind_all("<Right>", lambda e: self._move_selection(0, 1))
        root.bind_all("<Up>", lambda e: self._move_selection(-1, 0))
        root.bind_all("<Down>", lambda e: self._move_selection(1, 0))
        root.bind_all("<Return>", lambda e: self._flip_selected())
        root.bind_all("<space>", lambda e: self._flip_selected())
        root.bind_all("<Escape>", lambda e: self._exit_game())

    def _unbind_keys(self):
        root = self.parent
        try:
            root.unbind_all("<Left>")
            root.unbind_all("<Right>")
            root.unbind_all("<Up>")
            root.unbind_all("<Down>")
            root.unbind_all("<Return>")
            root.unbind_all("<space>")
            root.unbind_all("<Escape>")
        except Exception:
            pass

    def _move_selection(self, dr, dc):
        if self.showing:
            return
        if not (self.rows and self.cols):
            return
        self.sel_r = (self.sel_r + dr) % self.rows
        self.sel_c = (self.sel_c + dc) % self.cols
        self._update_selection_highlight()

    def _update_selection_highlight(self):
        # 确保 sel_r/sel_c 在有效范围
        if not hasattr(self, "rows") or not hasattr(self, "cols") or self.rows <= 0 or self.cols <= 0:
            return
        self.sel_r = max(0, min(self.sel_r, self.rows - 1))
        self.sel_c = max(0, min(self.sel_c, self.cols - 1))

        default_btn_bg = getattr(self, "_default_btn_bg", self.cget("bg"))
        selected_bg = "lightyellow"

        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.btns[r][c]
                if not cell:
                    continue
                try:
                    card_id = self.pos_to_id.get((r, c))
                    if card_id is None:
                        continue
                    btn = self.card_identities[card_id]["button"]
                    state = self.card_states.get(card_id, "")

                    # 光标指向时优先显示浅黄色（覆盖已配对的 lightgreen）
                    if (r, c) == (self.sel_r, self.sel_c):
                        btn.config(bg=selected_bg)
                    else:
                        # 没被选中：配对过显示 lightgreen，否则恢复默认
                        if state == "matched":
                            btn.config(bg="lightgreen")
                        else:
                            btn.config(bg=default_btn_bg)
                except Exception:
                    pass

    def _flip_selected(self):
        if self.showing:
            return
        card_id = self.pos_to_id.get((self.sel_r, self.sel_c))
        if card_id is None:
            return
        # 如果当前卡片不可翻或已翻，_on_card_click 会自己判断
        self._on_card_click(card_id)

