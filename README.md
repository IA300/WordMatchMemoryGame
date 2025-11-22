# 🎮 Word-match Memory Game

轻量级的单词记忆配对游戏（基于 `tkinter`）。本仓库包含 UI 界面、游戏逻辑、资源文件和简单的排行榜保存功能，适合在 Windows 上使用 Python 本地运行与调试。🚀

## ⚡ 快速开始

1. 确保使用的 Python 已包含 `tkinter`（Windows 下默认包含）。🐍
2. 在项目根目录打开终端（例如 PowerShell 或 cmd）：
   - 推荐创建虚拟环境（可选）：
     - `python -m venv .venv`
     - `.venv\Scripts\activate`
   - 运行：
     - `python main.py`

## 📁 项目结构（关键文件）

- main.py — 程序入口
- ui/
  - app_window.py — 主窗口与页面管理（class: [`AppWindow`](ui/app_window.py)）
  - pages/
    - menu_page.py — 主菜单页面（[`MenuPage`](ui/pages/menu_page.py)）
    - new_game_page.py — 新游戏配置页面（[`NewGamePage`](ui/pages/new_game_page.py)）
    - game_page.py — 游戏主页面、UI 与键盘支持（[`GamePage`](ui/pages/game_page.py)）
    - rating_page.py — 排行榜页面（[`RatingPage`](ui/pages/rating_page.py)）
    - settings_page.py — 设置页面（导入词库）（[`SettingsPage`](ui/pages/settings_page.py)）⚙️
- game/
  - config.py — 全局配置常量（难度、颜色、计分、延时等）([`game/config.py`](game/config.py))
  - game_logic.py — 主要的配对逻辑与计分（[`GameLogic`](game/game_logic.py)）🧠
  - file_tool.py — 词库与排行榜的加载/保存工具（[`load_words`, `load_ratings`, `save_rating`](game/file_tool.py)）💾
- assets/
  - words.json — 默认词库
  - ratings.json — 排行榜数据
  - 其他示例资源（cheat.json, alphabeta.json）
- test.json — 测试用小词库示例

## ✨ 功能说明

- 新游戏配置：选择难度（`Easy`/`Mid`/`Hard`），选择模式（`A-A` / `B-B` / `A-B`），以及是否彩色卡片。🎚️
  - 难度对应网格大小定义在 [`game/config.py`](game/config.py) 的 DIFFICULTIES。
- 三种配对模式：
  - A-A：相同词对（英文字母/单词与单词）
  - B-B：相同含义对（词义与词义）
  - A-B：单词与其含义配对（默认）
- 计分机制：基于 [`game/game_logic.py`](game/game_logic.py) 的 BASE_SCORE 与 COMBO_BONUS；完成时会根据时间、罚时、分数和最大连击计算最终 rating 并保存到排行榜。🏆
- 排行榜：保存在 `assets/ratings.json`，在完成游戏后会提示输入名字并自动写入（[`game/file_tool.py`](game/file_tool.py)）。📈
- 设置页：支持导入 JSON 格式的词库，通过文件对话框加载并替换当前词库（[`ui/pages/settings_page.py`](ui/pages/settings_page.py)）。🗂️
- 键盘操作：
  - 方向键移动选择（上下左右）
  - Enter / Space 翻牌
  - Esc 回到菜单 ⌨️

## 🎨 游戏图片

- new game 界面

<p align="center">
  <img src="docs/newgame.png" alt="new game" style="max-width:80%; height:auto;">
</p>

- gaming 界面

<p align="center">
  <img src="docs/gaming.gif" alt="gaming" style="max-width:80%; height:auto;">
</p>

- ratings 界面（配色灵感来自 [Codeforces](https://codeforces.com/blog/entry/3064)）

<p align="center">
  <img src="docs/ratings.png" alt="ratings" style="max-width:80%; height:auto;">
</p>

## 🗂️ 资源与数据格式

- 词库（`assets/words.json`）格式：顶层 JSON 对象，键为单词，值为含义，例如：
~~~json
  {
    "abandon": "v. 放弃",
    "Apple": "n. 苹果"
  }
~~~
- 排行榜（`assets/ratings.json`）格式：数组，每项包含 name 和 rating。如：
~~~json
  [
    {"name": "Alice", "rating": 1500},
    {"name": "Bob", "rating": 1200}
  ]
~~~

## 🐞 常见问题 & 调试提示

- 如果提示找不到单词文件或出现空白词库，请检查 `assets/words.json` 是否存在且为合法 JSON。默认加载路径在 [`game/file_tool.py`](game/file_tool.py) 中。
- 若在 Windows 上发现 tkinter 未安装，安装或使用带 tkinter 的 Python 发行版（Windows 官方安装包通常包含）。🔧
- 调试 UI：在 VS Code 中打开项目根目录，运行 `main.py`，或在 IDE 的 Python 交互/调试配置中设置断点查看页面与逻辑。
- 日志/错误：项目当前使用简单的 messagebox 或 try/except 捕获，运行时请在终端查看 Python 输出以获得堆栈信息。📝

## 🚀 发布与下载

- 新增：[release-v1.0](https://github.com/IA300/Python-Tkinter-WordMatchMemoryGame/releases/tag/pyinstaller)（已使用 PyInstaller 打包，Windows 可直接运行）—— 下载即玩。
  - 在仓库 Releases 页面找到 releasev1.0（通常为 zip 或 exe），下载后解压运行目录下的 main.exe 或双击可执行文件即可开始游戏。📦
- 注意：打包文件可能依赖本地环境（例如防病毒拦截或缺少 VC 运行时），遇到问题请参考 PyInstaller 文档或直接通过源码运行。⚠️

## 🔮 未来可扩展点

- 添加单元测试覆盖关键逻辑（例如 [`game/game_logic.py`](game/game_logic.py)）。✅
- 支持更多词库格式（CSV、TSV）。📄
- 增加游戏声音、动画或更加细化的评分与难度调整。🎵
- 导出/导入排行榜支持 CSV。📤

## 🤝 贡献

欢迎提交 issue 或 pr。🤗

> 2025.11.22