from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFrame, QTabWidget, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from app.utils.constants import STYLE_COLORS, FONT_FAMILY
from app.services.stats_service import StatsService
from app.widgets.chart_widget import ChartWidget


class StatsWindow(QDialog):
    """统计分析窗口"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.stats_service = StatsService()
        self._setup_ui()
        self._load_stats()

    def _setup_ui(self):
        self.setWindowTitle("📊 统计分析")
        self.setMinimumSize(800, 600)
        self.setStyleSheet(f"background-color: {STYLE_COLORS['bg_primary']};")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(10)

        # 标题
        title_label = QLabel("📊 占卜统计分析")
        title_label.setFont(QFont(FONT_FAMILY, 24, QFont.Bold))
        title_label.setStyleSheet(f"color: {STYLE_COLORS['accent_gold']};")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # 统计概览
        overview_frame = QFrame()
        overview_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {STYLE_COLORS['bg_secondary']};
                border-radius: 10px;
                padding: 12px;
            }}
        """)
        overview_layout = QHBoxLayout(overview_frame)
        overview_layout.setSpacing(20)

        self.total_label = QLabel("总占卜次数：0")
        self.total_label.setFont(QFont(FONT_FAMILY, 16, QFont.Bold))
        self.total_label.setStyleSheet(f"color: {STYLE_COLORS['accent_gold']};")
        overview_layout.addWidget(self.total_label)

        self.fav_label = QLabel("收藏记录：0")
        self.fav_label.setFont(QFont(FONT_FAMILY, 16, QFont.Bold))
        self.fav_label.setStyleSheet(f"color: {STYLE_COLORS['accent_gold']};")
        overview_layout.addWidget(self.fav_label)

        overview_layout.addStretch()
        main_layout.addWidget(overview_frame)

        # 图表选项卡
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet(f"""
            QTabWidget::pane {{
                background-color: {STYLE_COLORS['bg_secondary']};
                border-radius: 10px;
                border: none;
            }}
            QTabBar::tab {{
                background-color: {STYLE_COLORS['bg_card']};
                color: {STYLE_COLORS['text_secondary']};
                padding: 10px 20px;
                border-radius: 8px;
                margin-right: 4px;
                font-weight: bold;
            }}
            QTabBar::tab:selected {{
                background-color: {STYLE_COLORS['accent_gold']};
                color: #ffffff;
            }}
        """)

        # 问题类型分布
        self.type_chart = ChartWidget()
        self.tabs.addTab(self.type_chart, "📂 问题类型分布")

        # 常抽卡牌
        self.cards_chart = ChartWidget()
        self.tabs.addTab(self.cards_chart, "🃏 常抽卡牌 Top5")

        # 正逆位比例
        self.direction_chart = ChartWidget()
        self.tabs.addTab(self.direction_chart, "🔄 正逆位比例")

        # 占卜趋势
        self.trend_chart = ChartWidget()
        self.tabs.addTab(self.trend_chart, "📈 占卜趋势")

        # 牌阵分布
        self.spread_chart = ChartWidget()
        self.tabs.addTab(self.spread_chart, "🎴 牌阵使用分布")

        main_layout.addWidget(self.tabs)

        # 按钮
        btn_layout = QHBoxLayout()
        refresh_btn = QPushButton("🔄 刷新数据")
        refresh_btn.setFont(QFont(FONT_FAMILY, 14, QFont.Bold))
        refresh_btn.setCursor(Qt.PointingHandCursor)
        refresh_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {STYLE_COLORS['bg_card']};
                color: {STYLE_COLORS['text_primary']};
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
            }}
            QPushButton:hover {{
                border: 2px solid {STYLE_COLORS['accent_gold']};
            }}
        """)
        refresh_btn.clicked.connect(self._load_stats)
        btn_layout.addWidget(refresh_btn)

        close_btn = QPushButton("关闭")
        close_btn.setFont(QFont(FONT_FAMILY, 14))
        close_btn.setCursor(Qt.PointingHandCursor)
        close_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {STYLE_COLORS['text_secondary']};
                border: 1px solid {STYLE_COLORS['text_secondary']};
                border-radius: 6px;
                padding: 8px 20px;
            }}
            QPushButton:hover {{
                color: {STYLE_COLORS['accent_gold']};
                border-color: {STYLE_COLORS['accent_gold']};
            }}
        """)
        close_btn.clicked.connect(self.close)
        btn_layout.addWidget(close_btn)

        main_layout.addLayout(btn_layout)

    def _load_stats(self):
        """加载统计数据"""
        stats = self.stats_service.get_stats()

        # 概览
        self.total_label.setText(f"总占卜次数：{stats['total']}")
        self.fav_label.setText(f"收藏记录：{stats['favorites_count']}")

        # 问题类型分布
        if stats["type_distribution"]:
            labels = [t[0] for t in stats["type_distribution"]]
            values = [t[1] for t in stats["type_distribution"]]
            self.type_chart.draw_pie_chart(labels, values, "问题类型分布")
        else:
            self.type_chart.clear_chart()

        # 常抽卡牌 Top5
        if stats["top_cards"]:
            labels = [t[0] for t in stats["top_cards"]]
            values = [t[1] for t in stats["top_cards"]]
            self.cards_chart.draw_bar_chart(labels, values, "常抽卡牌 Top 5", "卡牌", "次数")
        else:
            self.cards_chart.clear_chart()

        # 正逆位比例
        if stats["upright_count"] > 0 or stats["reversed_count"] > 0:
            self.direction_chart.draw_pie_chart(
                ["正位", "逆位"],
                [stats["upright_count"], stats["reversed_count"]],
                "正逆位比例"
            )
        else:
            self.direction_chart.clear_chart()

        # 占卜趋势
        if stats["daily_trend"]:
            dates = [t[0] for t in stats["daily_trend"]]
            counts = [t[1] for t in stats["daily_trend"]]
            self.trend_chart.draw_line_chart(dates, counts, "每日占卜次数趋势", "日期", "次数")
        else:
            self.trend_chart.clear_chart()

        # 牌阵分布
        if stats["spread_distribution"]:
            labels = [t[0] for t in stats["spread_distribution"]]
            values = [t[1] for t in stats["spread_distribution"]]
            self.spread_chart.draw_pie_chart(labels, values, "牌阵使用分布")
        else:
            self.spread_chart.clear_chart()
