# 难度配置
DIFFICULTIES = {
    "Easy": {"rows": 2, "cols": 3, "color": "green"},
    "Mid":  {"rows": 3, "cols": 4, "color": "brown"},
    "Hard": {"rows": 6, "cols": 8, "color": "red"}
}

# 字体与样式
FONT_DATA = ("Fixedsys", 30)

CARD_STYLE = {
    "font": ("Times New Roman", 20, "bold"),
    "width": 12,
    "height": 2
}

BUTTON_CONFIG = {
    # "width":8,
    # "height":1,
    "font": ("Fixedsys", 30),# 字体主题，大小
    "bg": "#0643A5",# 背景
    "fg": "white",# 前景
    "activebackground": "red",# 点击背景
    "activeforeground": "white"# 点击前景
}

# 专用 Label 配置：默认黑色前景，使用 BUTTON_CONFIG 的字体主题
LABEL_CONFIG = {
    "font":  ("Fixedsys", 50),
    "fg": "black",
    "bd": 0,
}

# 计分规则
BASE_SCORE = 100
COMBO_BONUS = 50

# 排名颜色映射
RATING_COLOR = {
    "0":"#808080",# color_newbie
    "1200":"#008000",# color_pupil
    "1400":"#03a89e",# color_specialist
    "1600":"#0000ff",# color_expert
    "2000":"#aa00aa",# color_candidate_master
    "2200":"#ff8c00",# color_master
    "2500":"#ff0000"# color_grandmaster
}

# 段位名称映射（供 UI 显示）
RATING_TITLES = {
    "0": "Newbie",
    "1200": "Pupil",
    "1400": "Specialist",
    "1600": "Expert",
    "2000": "Candidate Master",
    "2200": "Master",
    "2500": "Grandmaster"
}

# 卡片颜色

COLORS = ["red", "blue", "green", "purple", "black", "orange", "brown"]

# 卡片状态 

CARD_STATUS_HIDDEN = 1
CARD_STATUS_FLIPPED = 2
CARD_STATUS_MATCHED = 3

# 延迟时间

DELAY_TIME = 5000