from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib

from app.utils.constants import FONT_FAMILY

matplotlib.use("Qt5Agg")
matplotlib.rcParams["font.sans-serif"] = [FONT_FAMILY, "Arial Unicode MS", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False


class ChartWidget(QWidget):
    """统计图表控件"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(8, 6), facecolor="#faf8f3")
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        self.setStyleSheet("background-color: #faf8f3;")

    def draw_pie_chart(self, labels, values, title="分布图", ax_idx=0):
        """绘制饼图"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor("#faf8f3")

        colors = ["#c9a84c", "#b8860b", "#d4b896", "#c0392b", "#a0a870", "#c4a882"]
        wedges, texts, autotexts = ax.pie(
            values, labels=labels, autopct="%1.1f%%",
            colors=colors[:len(labels)],
            textprops={"color": "#3d3220", "fontsize": 14}
        )
        for at in autotexts:
            at.set_color("#3d3220")
            at.set_fontsize(13)

        ax.set_title(title, color="#b8860b", fontsize=18, fontweight="bold", pad=15)
        self.canvas.draw()

    def draw_bar_chart(self, labels, values, title="柱状图", xlabel="", ylabel=""):
        """绘制柱状图"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor("#f3efe5")

        colors = ["#c9a84c", "#b8860b", "#d4b896", "#c0392b", "#a0a870"]
        bars = ax.bar(labels, values, color=colors[:len(labels)], edgecolor="#b8860b", linewidth=0.5)

        ax.set_title(title, color="#b8860b", fontsize=18, fontweight="bold", pad=15)
        ax.set_xlabel(xlabel, color="#3d3220")
        ax.set_ylabel(ylabel, color="#3d3220")
        ax.tick_params(colors="#8a7a60", labelsize=13)
        for spine in ax.spines.values():
            spine.set_color("#d5c9b0")

        self.canvas.draw()

    def draw_line_chart(self, x_data, y_data, title="趋势图", xlabel="", ylabel=""):
        """绘制折线图"""
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_facecolor("#f3efe5")

        ax.plot(x_data, y_data, color="#c9a84c", marker="o", linewidth=2, markersize=6)

        ax.set_title(title, color="#b8860b", fontsize=18, fontweight="bold", pad=15)
        ax.set_xlabel(xlabel, color="#3d3220")
        ax.set_ylabel(ylabel, color="#3d3220")
        ax.tick_params(colors="#8a7a60", labelsize=13)
        for spine in ax.spines.values():
            spine.set_color("#d5c9b0")
        self.figure.autofmt_xdate()

        self.canvas.draw()

    def clear_chart(self):
        """清空图表"""
        self.figure.clear()
        self.canvas.draw()
