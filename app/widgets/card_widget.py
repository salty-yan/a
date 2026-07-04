import os

from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QFont, QPainter, QColor, QBrush

from app.utils.paths import get_card_image_path
from app.utils.constants import FONT_FAMILY


class CardWidget(QFrame):
    """卡牌展示控件"""
    clicked = pyqtSignal(dict)

    def __init__(self, card_data, is_reversed=False, show_meaning=False, parent=None):
        super().__init__(parent)
        self.card_data = card_data
        self.is_reversed = is_reversed
        self.show_meaning = show_meaning
        self._setup_ui()

    def _setup_ui(self):
        self.setFrameStyle(QFrame.Box)
        self.setFixedSize(220, 340)
        self.setStyleSheet("""
            CardWidget {
                background-color: #fdf9f0;
                border: 2px solid #c9a84c;
                border-radius: 12px;
                padding: 10px;
            }
            CardWidget:hover {
                border-color: #b8860b;
                background-color: #faf3e0;
            }
        """)
        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(4)

        if self.show_meaning:
            # 显示卡牌详细含义
            name_label = QLabel(self.card_data.get("name_cn", ""))
            name_label.setFont(QFont(FONT_FAMILY, 15, QFont.Bold))
            name_label.setStyleSheet("color: #b8860b;")
            name_label.setAlignment(Qt.AlignCenter)
            name_label.setWordWrap(True)
            layout.addWidget(name_label)

            direction = "逆位" if self.is_reversed else "正位"
            dir_label = QLabel(direction)
            dir_label.setFont(QFont(FONT_FAMILY, 12))
            dir_label.setStyleSheet(
                "color: #8a7a60;" if not self.is_reversed else "color: #c0392b;"
            )
            dir_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(dir_label)

            kw = ", ".join(self.card_data.get("keywords", [])[:4])
            kw_label = QLabel(kw)
            kw_label.setFont(QFont(FONT_FAMILY, 11))
            kw_label.setStyleSheet("color: #a89880;")
            kw_label.setAlignment(Qt.AlignCenter)
            kw_label.setWordWrap(True)
            layout.addWidget(kw_label)

            meaning_text = self.card_data.get(
                "reversed_meaning" if self.is_reversed else "upright_meaning", ""
            )
            if len(meaning_text) > 80:
                meaning_text = meaning_text[:80] + "..."
            meaning_label = QLabel(meaning_text)
            meaning_label.setFont(QFont(FONT_FAMILY, 11))
            meaning_label.setStyleSheet("color: #6b5d4a;")
            meaning_label.setAlignment(Qt.AlignCenter)
            meaning_label.setWordWrap(True)
            layout.addWidget(meaning_label)
        else:
            # 显示卡背或卡面
            img_label = QLabel()
            img_label.setAlignment(Qt.AlignCenter)
            img_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            img_path = self.card_data.get("image_path", "")
            full_path = get_card_image_path(img_path) if img_path else ""

            if os.path.exists(full_path):
                pixmap = QPixmap(full_path).scaled(190, 270, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                img_label.setPixmap(pixmap)
            else:
                # 卡牌占位
                color = "#e8dcc8"
                pixmap = QPixmap(190, 270)
                pixmap.fill(QColor(color))
                img_label.setPixmap(pixmap)

            layout.addWidget(img_label)

            # 卡牌名称
            name_label = QLabel(self.card_data.get("name_cn", ""))
            name_label.setFont(QFont(FONT_FAMILY, 17, QFont.Bold))
            name_label.setStyleSheet("color: #b8860b;")
            name_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(name_label)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.card_data)
        super().mousePressEvent(event)


class DrawnCardWidget(QFrame):
    """已抽卡牌展示控件（含正逆位标记）- 自适应填满"""
    clicked = pyqtSignal(dict)

    def __init__(self, card_data, position_name, is_reversed=False, parent=None):
        super().__init__(parent)
        self.card_data = card_data
        self.position_name = position_name
        self.is_reversed = is_reversed
        self._reversed = is_reversed
        self._flipped = False
        self._setup_ui()

    def _setup_ui(self):
        self.setMinimumSize(250, 380)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        # 牌阵位置标签
        pos_label = QLabel(self.position_name)
        pos_label.setFont(QFont(FONT_FAMILY, 16, QFont.Bold))
        pos_label.setStyleSheet("color: #b8860b; background: transparent;")
        pos_label.setAlignment(Qt.AlignCenter)
        pos_label.setMaximumHeight(24)
        layout.addWidget(pos_label)

        # 卡牌图片 - 直接加载
        self.img_label = QLabel()
        self.img_label.setAlignment(Qt.AlignCenter)
        self.img_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.img_label.setMinimumSize(200, 300)
        layout.addWidget(self.img_label, 1)

        # 加载图片
        img_path = self.card_data.get("image_path", "")
        full_path = get_card_image_path(img_path) if img_path else ""
        if full_path and os.path.exists(full_path):
            pixmap = QPixmap(full_path)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(300, 420, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                self.img_label.setPixmap(pixmap)
        if self.img_label.pixmap() is None:
            pixmap = QPixmap(300, 420)
            pixmap.fill(QColor("#e8dcc8"))
            self.img_label.setPixmap(pixmap)

        # 名称和方向
        name_label = QLabel(self.card_data.get("name_cn", ""))
        name_label.setFont(QFont(FONT_FAMILY, 15, QFont.Bold))
        name_label.setStyleSheet("color: #3d3220; background: transparent;")
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setMaximumHeight(22)
        layout.addWidget(name_label)

        direction_text = "⬇ 逆位" if self.is_reversed else "⬆ 正位"
        direction_color = "#c0392b" if self.is_reversed else "#5a8f4a"
        dir_label = QLabel(direction_text)
        dir_label.setFont(QFont(FONT_FAMILY, 13, QFont.Bold))
        dir_label.setStyleSheet(f"color: {direction_color}; background: transparent;")
        dir_label.setAlignment(Qt.AlignCenter)
        dir_label.setMaximumHeight(18)
        layout.addWidget(dir_label)

        self.setStyleSheet("""
            DrawnCardWidget {
                background-color: #f3efe5;
                border: 2px solid #c9a84c;
                border-radius: 12px;
            }
            DrawnCardWidget:hover {
                border-color: #b8860b;
            }
        """)
        self.setCursor(Qt.PointingHandCursor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.card_data)
        super().mousePressEvent(event)
