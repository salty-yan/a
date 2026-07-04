from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTextEdit, QFrame, QScrollArea, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from app.utils.constants import STYLE_COLORS, FONT_FAMILY
from app.services.database_service import DatabaseService
from app.services.export_service import ExportService


class ResultWindow(QDialog):
    """解读结果窗口"""

    def __init__(self, question, question_type, spread_name, draw_results, interpretation, parent=None):
        super().__init__(parent)
        self.question = question
        self.question_type = question_type
        self.spread_name = spread_name
        self.draw_results = draw_results
        self.interpretation = interpretation
        self.db_service = DatabaseService()
        self.export_service = ExportService()
        self.is_saved = False
        self.reading_id = None
        self.is_favorite = False
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle("📖 占卜解读结果")
        self.setMinimumSize(750, 600)
        self.setStyleSheet(f"background-color: {STYLE_COLORS['bg_primary']};")

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 15, 20, 15)
        main_layout.setSpacing(10)

        # 标题
        title_label = QLabel("📖 占卜解读结果")
        title_label.setFont(QFont(FONT_FAMILY, 24, QFont.Bold))
        title_label.setStyleSheet(f"color: {STYLE_COLORS['accent_gold']};")
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # 解读内容滚动区域
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                background-color: {STYLE_COLORS['bg_secondary']};
                border-radius: 10px;
                border: none;
            }}
        """)

        content = QFrame()
        content.setStyleSheet(f"background-color: {STYLE_COLORS['bg_secondary']};")
        content_layout = QVBoxLayout(content)
        content_layout.setSpacing(8)

        # 解读文本
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setFont(QFont(FONT_FAMILY, 14))
        text_edit.setText(self.interpretation)
        text_edit.setStyleSheet(f"""
            QTextEdit {{
                background-color: {STYLE_COLORS['bg_secondary']};
                color: {STYLE_COLORS['text_primary']};
                border: none;
                padding: 10px;
            }}
        """)
        content_layout.addWidget(text_edit)

        scroll.setWidget(content)
        main_layout.addWidget(scroll)

        # 按钮区域
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)

        save_btn = QPushButton("💾 保存记录")
        save_btn.setFont(QFont(FONT_FAMILY, 14, QFont.Bold))
        save_btn.setCursor(Qt.PointingHandCursor)
        save_btn.setStyleSheet(self._btn_style(STYLE_COLORS['bg_card']))
        save_btn.clicked.connect(self._on_save)
        btn_layout.addWidget(save_btn)

        self.fav_btn = QPushButton("⭐ 收藏")
        self.fav_btn.setFont(QFont(FONT_FAMILY, 14, QFont.Bold))
        self.fav_btn.setCursor(Qt.PointingHandCursor)
        self.fav_btn.setStyleSheet(self._btn_style(STYLE_COLORS['bg_card']))
        self.fav_btn.clicked.connect(self._on_favorite)
        btn_layout.addWidget(self.fav_btn)

        export_txt_btn = QPushButton("📄 导出TXT")
        export_txt_btn.setFont(QFont(FONT_FAMILY, 14, QFont.Bold))
        export_txt_btn.setCursor(Qt.PointingHandCursor)
        export_txt_btn.setStyleSheet(self._btn_style("#2a8e4f"))
        export_txt_btn.clicked.connect(lambda: self._on_export("txt"))
        btn_layout.addWidget(export_txt_btn)

        export_docx_btn = QPushButton("📝 导出Word")
        export_docx_btn.setFont(QFont(FONT_FAMILY, 14, QFont.Bold))
        export_docx_btn.setCursor(Qt.PointingHandCursor)
        export_docx_btn.setStyleSheet(self._btn_style("#d4b896"))
        export_docx_btn.clicked.connect(lambda: self._on_export("docx"))
        btn_layout.addWidget(export_docx_btn)

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

    def _on_save(self):
        """保存记录"""
        if self.is_saved:
            QMessageBox.information(self, "提示", "该记录已保存。")
            return

        cards_data = []
        for r in self.draw_results:
            cards_data.append({
                "name_cn": r["card"]["name_cn"],
                "name_en": r["card"]["name_en"],
                "position": r["position"],
                "is_reversed": r["is_reversed"],
            })

        rid = self.db_service.save_reading(
            self.question, self.question_type, self.spread_name,
            cards_data, self.interpretation
        )
        if rid:
            self.is_saved = True
            self.reading_id = rid
            QMessageBox.information(self, "成功", "占卜记录已保存！")
        else:
            QMessageBox.critical(self, "错误", "记录保存失败，请检查数据库文件权限。")

    def _on_favorite(self):
        """收藏/取消收藏"""
        if not self.is_saved:
            QMessageBox.warning(self, "提示", "请先保存记录后再收藏。")
            return

        if self.db_service.toggle_favorite(self.reading_id):
            self.is_favorite = not self.is_favorite
            status = "已收藏 ⭐" if self.is_favorite else "已取消收藏"
            self.fav_btn.setText(status if self.is_favorite else "⭐ 收藏")
            QMessageBox.information(self, "提示", status)

    def _on_export(self, format_type):
        """导出报告"""
        if format_type == "txt":
            path, error = self.export_service.export_txt(
                self.question, self.question_type, self.spread_name,
                self.draw_results, self.interpretation
            )
        else:
            path, error = self.export_service.export_docx(
                self.question, self.question_type, self.spread_name,
                self.draw_results, self.interpretation
            )

        if error:
            QMessageBox.critical(self, "导出失败", f"导出失败：{error}")
        else:
            QMessageBox.information(self, "导出成功", f"报告已导出到：\n{path}")
