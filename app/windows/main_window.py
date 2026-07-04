import random

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QPushButton, QStatusBar, QFrame, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap, QIcon

from app.utils.constants import APP_TITLE, APP_SUBTITLE, APP_VERSION, STYLE_COLORS, FONT_FAMILY
from app.utils.paths import get_asset_file
from app.services.tarot_service import TarotService

from app.windows.reading_window import ReadingWindow
from app.windows.history_window import HistoryWindow
from app.windows.card_library_window import CardLibraryWindow
from app.windows.stats_window import StatsWindow
from app.windows.about_window import AboutWindow


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self):
        super().__init__()
        self.tarot_service = TarotService()
        self._sub_windows = []
        self._setup_ui()
        self._load_daily_card()

    def _setup_ui(self):
        self.setWindowTitle(APP_TITLE)
        self.setMinimumSize(900, 650)
        self.setStyleSheet(f"""
            QMainWindow {{
                background-color: {STYLE_COLORS['bg_primary']};
            }}
        """)

        # 中央控件
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(40, 30, 40, 30)
        main_layout.setSpacing(15)

        # 标题区域
        title_frame = QFrame()
        title_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {STYLE_COLORS['bg_secondary']};
                border-radius: 15px;
                padding: 20px;
            }}
        """)
        title_layout = QVBoxLayout(title_frame)

        title_label = QLabel(APP_TITLE)
        title_label.setFont(QFont(FONT_FAMILY, 32, QFont.Bold))
        title_label.setStyleSheet(f"color: {STYLE_COLORS['accent_gold']};")
        title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_label)

        subtitle_label = QLabel(APP_SUBTITLE)
        subtitle_label.setFont(QFont(FONT_FAMILY, 17))
        subtitle_label.setStyleSheet(f"color: {STYLE_COLORS['text_secondary']};")
        subtitle_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(subtitle_label)

        main_layout.addWidget(title_frame)

        # 今日推荐牌
        daily_frame = QFrame()
        daily_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {STYLE_COLORS['bg_card']};
                border-radius: 10px;
                padding: 12px;
            }}
        """)
        daily_layout = QHBoxLayout(daily_frame)
        daily_layout.setAlignment(Qt.AlignCenter)

        self.daily_card_label = QLabel("✨ 今日指引 ✨")
        self.daily_card_label.setFont(QFont(FONT_FAMILY, 14, QFont.Bold))
        self.daily_card_label.setStyleSheet(f"color: {STYLE_COLORS['accent_gold']};")
        self.daily_card_label.setAlignment(Qt.AlignCenter)
        daily_layout.addWidget(self.daily_card_label)

        main_layout.addWidget(daily_frame)

        # 功能按钮区域
        buttons_layout = QGridLayout()
        buttons_layout.setSpacing(15)

        buttons = [
            ("🔮 开始占卜", "reading", "#c9a84c"),
            ("📜 历史记录", "history", "#d4b896"),
            ("🃏 塔罗牌库", "card_library", "#b8860b"),
            ("📊 统计分析", "stats", "#a0a870"),
            ("❓ 使用帮助", "about", "#c4a882"),
        ]

        for idx, (text, action, color) in enumerate(buttons):
            btn = QPushButton(text)
            btn.setFont(QFont(FONT_FAMILY, 17, QFont.Bold))
            btn.setMinimumHeight(65)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: {STYLE_COLORS['text_primary']};
                    border: none;
                    border-radius: 12px;
                    padding: 10px 20px;
                }}
                QPushButton:hover {{
                    background-color: {self._lighten(color)};
                    border: 2px solid {STYLE_COLORS['accent_gold']};
                    color: #ffffff;
                }}
                QPushButton:pressed {{
                    background-color: {color};
                }}
            """)
            btn.clicked.connect(lambda checked, a=action: self._on_button_click(a))
            row = idx // 2
            col = idx % 2
            buttons_layout.addWidget(btn, row, col)

        main_layout.addLayout(buttons_layout)

        # 版本和退出
        bottom_layout = QHBoxLayout()
        version_label = QLabel(f"v{APP_VERSION}")
        version_label.setFont(QFont(FONT_FAMILY, 12))
        version_label.setStyleSheet(f"color: {STYLE_COLORS['text_secondary']};")
        bottom_layout.addWidget(version_label)
        bottom_layout.addStretch()

        exit_btn = QPushButton("退出软件")
        exit_btn.setFont(QFont(FONT_FAMILY, 13))
        exit_btn.setCursor(Qt.PointingHandCursor)
        exit_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {STYLE_COLORS['text_secondary']};
                border: 1px solid {STYLE_COLORS['text_secondary']};
                border-radius: 6px;
                padding: 6px 20px;
            }}
            QPushButton:hover {{
                color: #e06060;
                border-color: #e06060;
            }}
        """)
        exit_btn.clicked.connect(self.close)
        bottom_layout.addWidget(exit_btn)

        main_layout.addLayout(bottom_layout)

        # 状态栏
        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet(f"""
            QStatusBar {{
                background-color: {STYLE_COLORS['bg_secondary']};
                color: {STYLE_COLORS['text_secondary']};
                border-top: 1px solid #d5c9b0;
            }}
        """)
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("✨ 欢迎使用 TarotInsight 塔罗牌心理探索工具")

    def _load_daily_card(self):
        """加载今日推荐牌"""
        card = self.tarot_service.get_daily_card()
        if card:
            self.daily_card_label.setText(
                f"✨ 今日指引：{card['name_cn']} - {'、'.join(card['keywords'][:3])} ✨"
            )

    def _on_button_click(self, action):
        """按钮点击处理"""
        window = None
        if action == "reading":
            window = ReadingWindow(self.tarot_service)
        elif action == "history":
            window = HistoryWindow()
        elif action == "card_library":
            window = CardLibraryWindow(self.tarot_service)
        elif action == "stats":
            window = StatsWindow()
        elif action == "about":
            window = AboutWindow()

        if window:
            self._sub_windows.append(window)
            window.destroyed.connect(lambda: self._sub_windows.remove(window) if window in self._sub_windows else None)
            window.show()

    def _lighten(self, hex_color, factor=0.15):
        """颜色变亮"""
        hex_color = hex_color.lstrip("#")
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = min(255, int(r + (255 - r) * factor))
        g = min(255, int(g + (255 - g) * factor))
        b = min(255, int(b + (255 - b) * factor))
        return f"#{r:02x}{g:02x}{b:02x}"

