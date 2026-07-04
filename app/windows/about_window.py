from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from app.utils.constants import APP_TITLE, APP_VERSION, STYLE_COLORS, FONT_FAMILY


class AboutWindow(QDialog):
    """帮助/关于窗口"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle("❓ 使用帮助")
        self.setMinimumSize(600, 500)
        self.setStyleSheet(f"background-color: {STYLE_COLORS['bg_primary']};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(12)

        # 标题
        title_label = QLabel(f"关于 {APP_TITLE}")
        title_label.setFont(QFont(FONT_FAMILY, 24, QFont.Bold))
        title_label.setStyleSheet(f"color: {STYLE_COLORS['accent_gold']};")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # 内容
        help_text = f"""
版本：v{APP_VERSION}

【软件简介】
TarotInsight 是一款基于塔罗牌的心理探索与情绪整理工具。
本软件仅供心理探索、情绪整理和娱乐参考，不宣称真实预测未来。

【功能介绍】
1. 开始占卜：输入问题，选择类型和牌阵，随机抽取塔罗牌获取指引。
2. 历史记录：查看、筛选、收藏和删除过往的占卜记录。
3. 塔罗牌库：浏览完整的 78 张塔罗牌资料，包含正位和逆位含义。
4. 统计分析：通过图表了解你的占卜习惯和趋势。
5. 导出报告：将占卜结果导出为 TXT 或 Word 文档。

【使用步骤】
1. 在主界面点击「开始占卜」进入占卜窗口。
2. 输入你想探索的问题。
3. 选择问题类型（学习事业/人际关系/情绪状态/未来选择）。
4. 选择牌阵（单牌指引/三牌牌阵/十字牌阵）。
5. 点击「开始抽牌」，系统随机抽取卡牌。
6. 点击「查看解读」，查看完整解读结果。
7. 可选择保存记录、收藏或导出报告。

【注意事项】
• 本软件为本地桌面应用，不联网，不调用 AI API。
• 所有解读内容由本地规则生成，仅供参考。
• 卡牌图片缺失时，软件会使用占位图，不影响正常使用。
• 如遇到任何问题，请检查 data 和 assets 文件夹是否完整。
• 本软件最终解释权归开发团队所有。

【免责声明】
本工具定位为「心理探索、情绪整理、娱乐辅助工具」，
不提供任何形式的专业心理咨询或预测服务。
如您有严重的心理困扰，请及时寻求专业心理咨询师的帮助。
"""

        help_frame = QFrame()
        help_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {STYLE_COLORS['bg_secondary']};
                border-radius: 10px;
                padding: 10px;
            }}
        """)
        help_layout = QVBoxLayout(help_frame)

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setFont(QFont(FONT_FAMILY, 14))
        text_edit.setText(help_text)
        text_edit.setStyleSheet(f"""
            QTextEdit {{
                background-color: {STYLE_COLORS['bg_secondary']};
                color: {STYLE_COLORS['text_primary']};
                border: none;
            }}
        """)
        help_layout.addWidget(text_edit)

        layout.addWidget(help_frame)

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
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)
