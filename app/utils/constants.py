APP_NAME = "TarotInsight"
APP_TITLE = "塔罗牌心理探索工具"
APP_VERSION = "1.0.0"
APP_SUBTITLE = "探索内心 · 寻找指引"

import platform

def _get_platform_font():
    """获取跨平台中文字体"""
    system = platform.system()
    if system == "Windows":
        return "Microsoft YaHei"
    elif system == "Darwin":
        return "PingFang SC"
    else:
        return "WenQuanYi Micro Hei"

FONT_FAMILY = _get_platform_font()

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 720

QUESTION_TYPES = ["学习事业", "人际关系", "情绪状态", "未来选择"]

SPREADS = [
    {"name": "单牌指引", "card_count": 1, "description": "快速获取一个方向的指引，适合日常简单问题。"},
    {"name": "三牌牌阵", "card_count": 3, "description": "经典的三张牌牌阵，揭示过去的影响、现在的状态和未来的建议。"},
    {"name": "十字牌阵", "card_count": 5, "description": "较为全面的五张牌牌阵，从多个角度探索问题的深层原因和解决方向。"},
]

ARCANA_TYPES = ["全部", "大阿卡那", "小阿卡那"]
SUIT_TYPES = ["全部", "权杖", "圣杯", "宝剑", "星币"]

DATABASE_NAME = "tarot_app.db"

STYLE_COLORS = {
    "bg_primary": "#faf8f3",
    "bg_secondary": "#f3efe5",
    "bg_card": "#fdf9f0",
    "accent_gold": "#c9a84c",
    "accent_purple": "#b8860b",
    "accent_red": "#c0392b",
    "text_primary": "#3d3220",
    "text_secondary": "#8a7a60",
    "text_gold": "#b8860b",
    "btn_primary": "#c9a84c",
    "btn_hover": "#dbb960",
    "btn_secondary": "#e8dcc8",
}
