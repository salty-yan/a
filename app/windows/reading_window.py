from PyQt5.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QTextEdit, QComboBox, QFrame, QScrollArea,
    QMessageBox, QSpacerItem, QSizePolicy, QGridLayout, QWidget
)
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt5.QtGui import QFont

from app.utils.constants import STYLE_COLORS, FONT_FAMILY
from app.services.interpretation_service import InterpretationService
from app.widgets.card_widget import DrawnCardWidget

from app.windows.result_window import ResultWindow


class ReadingWindow(QDialog):
    """占卜窗口"""

    def __init__(self, tarot_service, parent=None):
        super().__init__(parent)
        self.tarot_service = tarot_service
        self.interpretation_service = InterpretationService()
        self.draw_results = None
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle("🔮 开始占卜")
        self.setMinimumSize(800, 600)
        self.setStyleSheet(f"background-color: {STYLE_COLORS['bg_primary']};")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 20, 25, 20)
        main_layout.setSpacing(12)

        # 标题
        title_label = QLabel("🔮 塔罗牌占卜")
        title_label.setFont(QFont(FONT_FAMILY, 26, QFont.Bold))
        title_label.setStyleSheet(f"color: {STYLE_COLORS['accent_gold']};")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # 内容区域（左右布局）
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # 左侧：输入区域
        left_frame = QFrame()
        left_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {STYLE_COLORS['bg_secondary']};
                border-radius: 12px;
                padding: 15px;
            }}
        """)
        left_layout = QVBoxLayout(left_frame)
        left_layout.setSpacing(12)

        # 问题输入
        q_label = QLabel("💭 你想探索的问题：")
        q_label.setFont(QFont(FONT_FAMILY, 15, QFont.Bold))
        q_label.setStyleSheet(f"color: {STYLE_COLORS['text_primary']};")
        left_layout.addWidget(q_label)

        self.question_input = QTextEdit()
        self.question_input.setPlaceholderText("请输入你想探索的问题，例如：我最近应该如何调整学习状态？")
        self.question_input.setMaximumHeight(100)
        self.question_input.setFont(QFont(FONT_FAMILY, 14))
        self.question_input.setStyleSheet(f"""
            QTextEdit {{
                background-color: {STYLE_COLORS['bg_card']};
                color: {STYLE_COLORS['text_primary']};
                border: 1px solid #d5c9b0;
                border-radius: 8px;
                padding: 8px;
            }}
        """)
        left_layout.addWidget(self.question_input)

        # 问题类型
        type_label = QLabel("📂 问题类型：")
        type_label.setFont(QFont(FONT_FAMILY, 15, QFont.Bold))
        type_label.setStyleSheet(f"color: {STYLE_COLORS['text_primary']};")
        left_layout.addWidget(type_label)

        self.type_combo = QComboBox()
        self.type_combo.addItems(self.tarot_service.get_question_types())
        self.type_combo.setFont(QFont(FONT_FAMILY, 14))
        self.type_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {STYLE_COLORS['bg_card']};
                color: {STYLE_COLORS['text_primary']};
                border: 1px solid #d5c9b0;
                border-radius: 8px;
                padding: 8px 15px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox QAbstractItemView {{
                background-color: {STYLE_COLORS['bg_card']};
                color: {STYLE_COLORS['text_primary']};
                selection-background-color: {STYLE_COLORS['accent_purple']};
            }}
        """)
        left_layout.addWidget(self.type_combo)

        # 牌阵选择
        spread_label = QLabel("🃏 选择牌阵：")
        spread_label.setFont(QFont(FONT_FAMILY, 15, QFont.Bold))
        spread_label.setStyleSheet(f"color: {STYLE_COLORS['text_primary']};")
        left_layout.addWidget(spread_label)

        self.spread_combo = QComboBox()
        spreads = self.tarot_service.get_spreads()
        self.spread_combo.addItems([s["name"] for s in spreads])
        self.spread_combo.setFont(QFont(FONT_FAMILY, 14))
        self.spread_combo.setStyleSheet(f"""
            QComboBox {{
                background-color: {STYLE_COLORS['bg_card']};
                color: {STYLE_COLORS['text_primary']};
                border: 1px solid #d5c9b0;
                border-radius: 8px;
                padding: 8px 15px;
            }}
            QComboBox::drop-down {{
                border: none;
            }}
            QComboBox QAbstractItemView {{
                background-color: {STYLE_COLORS['bg_card']};
                color: {STYLE_COLORS['text_primary']};
                selection-background-color: {STYLE_COLORS['accent_purple']};
            }}
        """)
        self.spread_combo.currentTextChanged.connect(self._on_spread_changed)
        left_layout.addWidget(self.spread_combo)

        # 牌阵说明
        self.spread_desc_label = QLabel()
        self.spread_desc_label.setFont(QFont(FONT_FAMILY, 13))
        self.spread_desc_label.setStyleSheet(f"color: {STYLE_COLORS['text_secondary']};")
        self.spread_desc_label.setWordWrap(True)
        left_layout.addWidget(self.spread_desc_label)
        self._on_spread_changed(self.spread_combo.currentText())

        left_layout.addStretch()

        # 按钮
        btn_layout = QHBoxLayout()

        self.draw_btn = QPushButton("🎴 开始抽牌")
        self.draw_btn.setFont(QFont(FONT_FAMILY, 16, QFont.Bold))
        self.draw_btn.setMinimumHeight(45)
        self.draw_btn.setCursor(Qt.PointingHandCursor)
        self.draw_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {STYLE_COLORS['accent_purple']};
                color: {STYLE_COLORS['text_primary']};
                border: none;
                border-radius: 10px;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: #dbb960;
                border: 2px solid {STYLE_COLORS['accent_gold']};
                color: #ffffff;
            }}
        """)
        self.draw_btn.clicked.connect(self._on_draw_cards)
        btn_layout.addWidget(self.draw_btn)

        self.view_btn = QPushButton("📖 查看解读")
        self.view_btn.setFont(QFont(FONT_FAMILY, 16, QFont.Bold))
        self.view_btn.setMinimumHeight(45)
        self.view_btn.setCursor(Qt.PointingHandCursor)
        self.view_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {STYLE_COLORS['bg_card']};
                color: {STYLE_COLORS['text_secondary']};
                border: none;
                border-radius: 10px;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: #dbb960;
                color: #ffffff;
            }}
        """)
        self.view_btn.clicked.connect(self._on_view_interpretation)
        self.view_btn.setEnabled(False)
        btn_layout.addWidget(self.view_btn)

        left_layout.addLayout(btn_layout)

        content_layout.addWidget(left_frame, 2)

        # 右侧：卡牌展示区域
        self.right_frame = QFrame()
        self.right_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {STYLE_COLORS['bg_secondary']};
                border-radius: 12px;
                padding: 15px;
            }}
        """)
        self.right_layout = QVBoxLayout(self.right_frame)
        self.right_layout.setContentsMargins(10, 10, 10, 10)

        right_title = QLabel("🎴 抽牌结果")
        right_title.setFont(QFont(FONT_FAMILY, 17, QFont.Bold))
        right_title.setStyleSheet(f"color: {STYLE_COLORS['accent_gold']};")
        right_title.setAlignment(Qt.AlignCenter)
        right_title.setMaximumHeight(30)
        self.right_layout.addWidget(right_title)

        # 初始占位区域
        self._build_placeholder()

        content_layout.addWidget(self.right_frame, 5)

        main_layout.addLayout(content_layout)

        # 底部返回按钮
        back_btn = QPushButton("← 返回主界面")
        back_btn.setFont(QFont(FONT_FAMILY, 14))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet(f"""
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
        back_btn.clicked.connect(self.close)
        main_layout.addWidget(back_btn, alignment=Qt.AlignLeft)

    def _build_placeholder(self):
        """构建初始占位提示"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { background-color: transparent; border: none; }")

        container = QWidget()
        layout = QVBoxLayout(container)
        placeholder = QLabel("点击「开始抽牌」\n查看你的塔罗指引")
        placeholder.setFont(QFont(FONT_FAMILY, 16))
        placeholder.setStyleSheet(f"color: {STYLE_COLORS['text_secondary']};")
        placeholder.setAlignment(Qt.AlignCenter)
        placeholder.setWordWrap(True)
        layout.addWidget(placeholder)
        scroll.setWidget(container)

        self.right_layout.addWidget(scroll, 1)

    def _on_spread_changed(self, spread_name):
        """牌阵选择变化"""
        spread = self.tarot_service.get_spread_by_name(spread_name)
        if spread:
            desc = spread.get("description", "")
            positions = spread.get("positions", [])
            pos_desc = "\n".join([f"• {p['name']}：{p['meaning']}" for p in positions])
            self.spread_desc_label.setText(f"{desc}\n\n牌阵位置：\n{pos_desc}")

    def _on_draw_cards(self):
        """抽牌"""
        question = self.question_input.toPlainText().strip()
        if not question:
            QMessageBox.warning(self, "提示", "请先输入想探索的问题。")
            return

        spread_name = self.spread_combo.currentText()
        if not spread_name:
            QMessageBox.warning(self, "提示", "请选择一种牌阵。")
            return

        results, error = self.tarot_service.draw_cards(spread_name)
        if error:
            QMessageBox.critical(self, "错误", f"抽牌失败：{error}")
            return

        self.draw_results = results
        self._display_cards(results)
        self.view_btn.setEnabled(True)
        self.view_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {STYLE_COLORS['accent_gold']};
                color: #ffffff;
                border: none;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: #dbb960;
            }}
        """)

    def _display_cards(self, results):
        """展示抽牌结果 - 重建右侧滚动区域"""
        # 移除旧的 scroll area（right_layout 中第2个，第1个是 title）
        for i in range(self.right_layout.count() - 1, 0, -1):
            item = self.right_layout.itemAt(i)
            if item.widget():
                item.widget().deleteLater()
            self.right_layout.removeItem(item)

        # 创建全新的 scroll area 和卡片容器
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { background-color: transparent; border: none; }")

        container = QWidget()
        layout = QGridLayout(container)
        layout.setSpacing(12)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setAlignment(Qt.AlignCenter)

        cols = min(len(results), 3)
        for i, result in enumerate(results):
            card_widget = DrawnCardWidget(
                result["card"],
                result["position"],
                result["is_reversed"]
            )
            row = i // cols
            col = i % cols
            layout.addWidget(card_widget, row, col)

        scroll.setWidget(container)
        self.right_layout.addWidget(scroll, 1)

    def _on_view_interpretation(self):
        """查看解读"""
        if not self.draw_results:
            QMessageBox.warning(self, "提示", "请先抽牌。")
            return

        question = self.question_input.toPlainText().strip()
        question_type = self.type_combo.currentText()
        spread_name = self.spread_combo.currentText()

        interpretation = self.interpretation_service.interpret(
            question, question_type, spread_name, self.draw_results
        )

        result_window = ResultWindow(
            question, question_type, spread_name,
            self.draw_results, interpretation, self
        )
        result_window.exec_()
