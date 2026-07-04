import sys
import os
import platform

# 将项目根目录添加到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont

from app.windows.main_window import MainWindow
from app.utils.paths import get_asset_file


def get_default_font():
    """获取跨平台默认中文字体"""
    system = platform.system()
    if system == "Windows":
        for name in ["Microsoft YaHei", "SimHei", "SimSun"]:
            font = QFont(name, 12)
            if font.exactMatch():
                return font
    elif system == "Darwin":  # macOS
        for name in ["PingFang SC", "Heiti SC", "STHeiti"]:
            font = QFont(name, 12)
            if font.exactMatch():
                return font
    else:  # Linux
        for name in ["WenQuanYi Micro Hei", "Noto Sans CJK SC", "Droid Sans Fallback"]:
            font = QFont(name, 12)
            if font.exactMatch():
                return font
    return QFont("Arial", 12)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("TarotInsight")

    # 设置默认字体（跨平台）
    font = get_default_font()
    app.setFont(font)

    # 加载 QSS 样式
    qss_path = get_asset_file("style.qss")
    if os.path.exists(qss_path):
        with open(qss_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())

    # 启动主窗口
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
