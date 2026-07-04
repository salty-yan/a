from PyQt5.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QLineEdit, QFrame, QScrollArea, QGridLayout,
    QMessageBox, QAbstractItemView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from app.utils.constants import STYLE_COLORS, ARCANA_TYPES, SUIT_TYPES, FONT_FAMILY
from app.widgets.card_widget import CardWidget


class CardLibraryWindow(QDialog):
    """塔罗牌库窗口"""

    def __init__(self, tarot_service, parent=None):
        super().__init__(parent)
        self.tarot_service = tarot_service
        self._setup_ui()
        self._load_cards()

    def _setup_ui(self):
        self.setWindowTitle("🃏 塔罗牌库")
        self.setMinimumSize(850, 600)
        self.setStyleSheet(f"background-color: {STYLE_COLORS['bg_primary']};")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(10)

        # 标题
        title_label = QLabel("🃏 塔罗牌库（78张）")
        title_label.setFont(QFont(FONT_FAMILY, 24, QFont.Bold))
        title_label.setStyleSheet(f"color: {STYLE_COLORS['accent_gold']};")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # 筛选区域
        filter_frame = QFrame()
        filter_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {STYLE_COLORS['bg_secondary']};
                border-radius: 10px;
                padding: 10px;
            }}
        """)
        filter_layout = QHBoxLayout(filter_frame)
        filter_layout.setSpacing(12)

        filter_layout.addWidget(QLabel("阿卡那："))
        self.arcana_combo = QComboBox()
        self.arcana_combo.addItems(ARCANA_TYPES)
        self.arcana_combo.setFont(QFont(FONT_FAMILY, 13))
        self.arcana_combo.setStyleSheet(self._combo_style())
        self.arcana_combo.currentTextChanged.connect(self._on_filter_changed)
        filter_layout.addWidget(self.arcana_combo)

        filter_layout.addWidget(QLabel("花色："))
        self.suit_combo = QComboBox()
        self.suit_combo.addItems(SUIT_TYPES)
        self.suit_combo.setFont(QFont(FONT_FAMILY, 13))
        self.suit_combo.setStyleSheet(self._combo_style())
        self.suit_combo.currentTextChanged.connect(self._on_filter_changed)
        filter_layout.addWidget(self.suit_combo)

        filter_layout.addWidget(QLabel("搜索："))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("输入关键词搜索...")
        self.search_input.setFont(QFont(FONT_FAMILY, 13))
        self.search_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {STYLE_COLORS['bg_card']};
                color: {STYLE_COLORS['text_primary']};
                border: 1px solid #d5c9b0;
                border-radius: 6px;
                padding: 6px 12px;
            }}
        """)
        self.search_input.textChanged.connect(self._on_filter_changed)
        filter_layout.addWidget(self.search_input)

        filter_layout.addStretch()
        main_layout.addWidget(filter_frame)

        # 卡牌展示区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                background-color: {STYLE_COLORS['bg_secondary']};
                border-radius: 10px;
                border: none;
            }}
        """)

        self.cards_container = QWidget()
        self.cards_grid = QGridLayout(self.cards_container)
        self.cards_grid.setSpacing(12)
        self.cards_grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        scroll.setWidget(self.cards_container)
        main_layout.addWidget(scroll)

        # 底部按钮
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
        main_layout.addWidget(close_btn, alignment=Qt.AlignCenter)

    def _combo_style(self):
        return f"""
            QComboBox {{
                background-color: {STYLE_COLORS['bg_card']};
                color: {STYLE_COLORS['text_primary']};
                border: 1px solid #d5c9b0;
                border-radius: 6px;
                padding: 6px 12px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {STYLE_COLORS['bg_card']};
                color: {STYLE_COLORS['text_primary']};
                selection-background-color: {STYLE_COLORS['accent_purple']};
            }}
        """

    def _get_filtered_cards(self):
        """获取筛选后的卡牌"""
        arcana = self.arcana_combo.currentText()
        suit = self.suit_combo.currentText()
        keyword = self.search_input.text().strip()

        # 优先按花色筛选（小阿卡那）
        if suit != "全部":
            cards = self.tarot_service.get_cards_by_suit(suit)
        elif arcana != "全部":
            cards = self.tarot_service.get_cards_by_arcana(arcana)
        else:
            cards = self.tarot_service.get_all_cards()

        if keyword:
            cards = [c for c in cards if
                     keyword.lower() in c["name_cn"].lower() or
                     keyword.lower() in c["name_en"].lower() or
                     any(keyword.lower() in kw.lower() for kw in c.get("keywords", []))]

        return cards

    def _load_cards(self):
        """加载卡牌显示"""
        # 清除旧内容
        while self.cards_grid.count():
            item = self.cards_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        cards = self._get_filtered_cards()
        cols = 4
        for i, card in enumerate(cards):
            widget = CardWidget(card, show_meaning=True)
            widget.clicked.connect(self._show_card_detail)
            row = i // cols
            col = i % cols
            self.cards_grid.addWidget(widget, row, col)

    def _on_filter_changed(self):
        """筛选条件变化"""
        self._load_cards()

    def _show_card_detail(self, card_data):
        """显示卡牌详情"""
        detail = f"""
卡牌：{card_data['name_cn']} ({card_data['name_en']})
阿卡那：{card_data['arcana']}
"""
        if card_data.get('suit'):
            detail += f"花色：{card_data['suit']}\n"

        detail += f"""
关键词：{'、'.join(card_data['keywords'])}

【正位含义】
{card_data['upright_meaning']}

【逆位含义】
{card_data['reversed_meaning']}
"""
        msg = QMessageBox(self)
        msg.setWindowTitle(f"卡牌详情 - {card_data['name_cn']}")
        msg.setText(detail.strip())
        msg.setStyleSheet(f"""
            QMessageBox {{
                background-color: {STYLE_COLORS['bg_primary']};
                color: {STYLE_COLORS['text_primary']};
            }}
            QLabel {{
                color: {STYLE_COLORS['text_primary']};
                font-size: 12px;
                min-width: 450px;
            }}
        """)
        msg.exec_()
