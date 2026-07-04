import os
import sys


def get_project_root():
    """获取项目根目录"""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_data_dir():
    """获取数据目录"""
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'data')
    return os.path.join(get_project_root(), 'data')


def get_assets_dir():
    """获取资源目录"""
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'assets')
    return os.path.join(get_project_root(), 'assets')


def get_ui_dir():
    """获取UI文件目录"""
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'ui')
    return os.path.join(get_project_root(), 'ui')


def get_data_file(filename):
    """获取数据文件路径"""
    return os.path.join(get_data_dir(), filename)


def get_asset_file(filename):
    """获取资源文件路径"""
    return os.path.join(get_assets_dir(), filename)


def get_ui_file(filename):
    """获取UI文件路径"""
    return os.path.join(get_ui_dir(), filename)


def get_card_image_path(relative_path):
    """获取卡牌图片路径"""
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(get_project_root(), relative_path)
