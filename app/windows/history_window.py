import json

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox,
    QFrame, QMessageBox, QCheckBox, QAbstractItemView
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

from app.utils.constants import STYLE_COLORS, QUESTION_TYPES, FONT_FAMILY
from app.services.database_service import DatabaseService


class HistoryWindow(QDialog):
    """历史记录窗口"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_service = DatabaseService()
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        self.setWindowTitle("📜 历史记录")
        self.setMinimumSize(850, 550)
        self.setStyleSheet(f"background-color: {STYLE_COLORS['bg_primary']};")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(10)

        # 标题
        title_label = QLabel("📜 占卜历史记录")
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

        filter_layout.addWidget(QLabel("问题类型："))
        self.type_filter = QComboBox()
        self.type_filter.addItems(["全部"] + QUESTION_TYPES)
        self.type_filter.setFont(QFont(FONT_FAMILY, 13))
        self.type_filter.setStyleSheet(f"""
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
        """)
        filter_layout.addWidget(self.type_filter)

        self.fav_only_check = QCheckBox("仅显示收藏")
        self.fav_only_check.setFont(QFont(FONT_FAMILY, 13))
        self.fav_only_check.setStyleSheet(f"color: {STYLE_COLORS['text_primary']};")
        filter_layout.addWidget(self.fav_only_check)

        filter_btn = QPushButton("🔍 筛选")
        filter_btn.setFont(QFont(FONT_FAMILY, 13, QFont.Bold))
        filter_btn.setCursor(Qt.PointingHandCursor)
        filter_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {STYLE_COLORS['bg_card']};
                color: {STYLE_COLORS['text_primary']};
                border: none;
                border-radius: 6px;
                padding: 6px 16px;
            }}
            QPushButton:hover {{
                border: 2px solid {STYLE_COLORS['accent_gold']};
            }}
        """)
        filter_btn.clicked.connect(self._load_data)
        filter_layout.addWidget(filter_btn)

        reset_btn = QPushButton("🔄 重置")
        reset_btn.setFont(QFont(FONT_FAMILY, 13, QFont.Bold))
        reset_btn.setCursor(Qt.PointingHandCursor)
        reset_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {STYLE_COLORS['bg_card']};
                color: {STYLE_COLORS['text_primary']};
                border: none;
                border-radius: 6px;
                padding: 6px 16px;
            }}
            QPushButton:hover {{
                border: 2px solid {STYLE_COLORS['accent_gold']};
            }}
        """)
        reset_btn.clicked.connect(self._reset_filter)
        filter_layout.addWidget(reset_btn)

        filter_layout.addStretch()
        main_layout.addWidget(filter_frame)

        # 表格
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "时间", "问题", "问题类型", "牌阵", "收藏"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.setColumnHidden(0, True)
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background-color: {STYLE_COLORS['bg_secondary']};
                color: {STYLE_COLORS['text_primary']};
                border: none;
                border-radius: 10px;
                gridline-color: #d5c9b0;
                alternate-background-color: #f5ede0;
            }}
            QTableWidget::item {{
                padding: 8px;
                border-bottom: 1px solid #e0d5c0;
            }}
            QHeaderView::section {{
                background-color: {STYLE_COLORS['bg_card']};
                color: {STYLE_COLORS['accent_gold']};
                padding: 8px;
                border: none;
                font-weight: bold;
            }}
            QTableWidget::item:selected {{
                background-color: {STYLE_COLORS['accent_purple']};
            }}
        """)
        self.table.cellDoubleClicked.connect(self._on_view_detail)
        main_layout.addWidget(self.table)

        # 操作按钮
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        view_btn = QPushButton("📖 查看详情")
        view_btn.setFont(QFont(FONT_FAMILY, 14, QFont.Bold))
        view_btn.setCursor(Qt.PointingHandCursor)
        view_btn.setStyleSheet(self._btn_style(STYLE_COLORS['bg_card']))
        view_btn.clicked.connect(self._on_view_selected)
        btn_layout.addWidget(view_btn)

        toggle_fav_btn = QPushButton("⭐ 切换收藏")
        toggle_fav_btn.setFont(QFont(FONT_FAMILY, 14, QFont.Bold))
        toggle_fav_btn.setCursor(Qt.PointingHandCursor)
        toggle_fav_btn.setStyleSheet(self._btn_style("#c9a84c"))
        toggle_fav_btn.clicked.connect(self._on_toggle_favorite)
        btn_layout.addWidget(toggle_fav_btn)

        delete_btn = QPushButton("🗑 删除记录")
        delete_btn.setFont(QFont(FONT_FAMILY, 14, QFont.Bold))
        delete_btn.setCursor(Qt.PointingHandCursor)
        delete_btn.setStyleSheet(self._btn_style("#c0392b"))
        delete_btn.clicked.connect(self._on_delete)
        btn_layout.addWidget(delete_btn)

        main_layout.addLayout(btn_layout)

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

    def _btn_style(self, bg_color):
        return f"""
            QPushButton {{
                background-color: {bg_color};
                color: {STYLE_COLORS['text_primary']};
                border: none;
                border-radius: 8px;
                padding: 10px 18px;
            }}
            QPushButton:hover {{
                border: 2px solid {STYLE_COLORS['accent_gold']};
            }}
        """

    def _load_data(self):
        """加载数据"""
        question_type = self.type_filter.currentText()
        favorite_only = self.fav_only_check.isChecked()

        if question_type == "全部" and not favorite_only:
            rows = self.db_service.get_all_readings()
        else:
            rows = self.db_service.search_readings(
                question_type=question_type, favorite_only=favorite_only
            )

        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            # id, question, question_type, spread_type, cards_json, interpretation, is_favorite, note, created_at
            self.table.setItem(i, 0, QTableWidgetItem(str(row[0])))
            self.table.setItem(i, 1, QTableWidgetItem(row[8] if len(row) > 8 else ""))
            self.table.setItem(i, 2, QTableWidgetItem(row[1]))
            self.table.setItem(i, 3, QTableWidgetItem(row[2]))
            self.table.setItem(i, 4, QTableWidgetItem(row[3]))
            fav_text = "⭐" if row[6] else ""
            self.table.setItem(i, 5, QTableWidgetItem(fav_text))

    def _reset_filter(self):
        """重置筛选"""
        self.type_filter.setCurrentIndex(0)
        self.fav_only_check.setChecked(False)
        self._load_data()

    def _get_selected_id(self):
        """获取选中行ID"""
        current_row = self.table.currentRow()
        if current_row < 0:
            return None
        item = self.table.item(current_row, 0)
        return int(item.text()) if item else None

    def _on_view_detail(self, row, col):
        """双击查看详情"""
        self._on_view_selected()

    def _on_view_selected(self):
        """查看选中记录详情"""
        reading_id = self._get_selected_id()
        if not reading_id:
            QMessageBox.warning(self, "提示", "请先选择一条记录。")
            return

        row = self.db_service.get_reading_by_id(reading_id)
        if not row:
            return

        detail_text = f"问题：{row[1]}\n类型：{row[2]}\n牌阵：{row[3]}\n时间：{row[8]}\n\n"
        try:
            cards = json.loads(row[4])
            for c in cards:
                direction = "逆位" if c.get("is_reversed") else "正位"
                detail_text += f"• {c['name_cn']} [{direction}] - {c.get('position', '')}\n"
        except json.JSONDecodeError:
            pass

        detail_text += f"\n--- 综合解读 ---\n{row[5]}"

        msg = QMessageBox(self)
        msg.setWindowTitle("记录详情")
        msg.setText(detail_text)
        msg.setStyleSheet(f"""
            QMessageBox {{
                background-color: {STYLE_COLORS['bg_primary']};
                color: {STYLE_COLORS['text_primary']};
            }}
            QLabel {{
                color: {STYLE_COLORS['text_primary']};
                font-size: 12px;
                min-width: 500px;
            }}
        """)
        msg.exec_()

    def _on_toggle_favorite(self):
        """切换收藏"""
        reading_id = self._get_selected_id()
        if not reading_id:
            QMessageBox.warning(self, "提示", "请先选择一条记录。")
            return
        self.db_service.toggle_favorite(reading_id)
        self._load_data()

    def _on_delete(self):
        """删除记录"""
        reading_id = self._get_selected_id()
        if not reading_id:
            QMessageBox.warning(self, "提示", "请先选择一条记录。")
            return

        reply = QMessageBox.question(
            self, "确认删除", "确定要删除这条历史记录吗？此操作不可恢复。",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.db_service.delete_reading(reading_id)
            self._load_data()
