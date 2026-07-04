"""
TarotInsight 打包脚本
使用 PyInstaller 将程序打包为 macOS .app 或 Windows .exe

使用方法：
    python build_exe.py          # 直接打包
    python build_exe.py --clean  # 清理后重新打包

注意：PyInstaller 不支持跨平台编译。
    - 在 macOS 上运行 → 生成 TarotInsight.app
    - 在 Windows 上运行 → 生成 TarotInsight.exe
"""

import os
import sys
import shutil
import subprocess

# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "dist")
BUILD_DIR = os.path.join(BASE_DIR, "build")
SPEC_FILE = os.path.join(BASE_DIR, "TarotInsight.spec")

# 检测当前操作系统
IS_WINDOWS = sys.platform == "win32"
IS_MAC = sys.platform == "darwin"
SEP = ";" if IS_WINDOWS else ":"


def clean_build():
    """清理旧的构建文件"""
    for d in [DIST_DIR, BUILD_DIR]:
        if os.path.exists(d):
            print(f"  清理: {d}")
            shutil.rmtree(d)
    for f in [SPEC_FILE]:
        if os.path.exists(f):
            print(f"  清理: {f}")
            os.remove(f)


def build():
    """使用 PyInstaller 打包"""
    print("=" * 60)
    print("  TarotInsight 打包工具")
    print(f"  当前系统: {'Windows' if IS_WINDOWS else 'macOS' if IS_MAC else 'Linux'}")
    print(f"  将生成: {'TarotInsight.exe' if IS_WINDOWS else 'TarotInsight.app'}")
    print("=" * 60)

    if len(sys.argv) > 1 and sys.argv[1] == "--clean":
        clean_build()

    os.chdir(BASE_DIR)

    # 构建 PyInstaller 命令
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--name=TarotInsight",
        "--windowed",
        f"--add-data=data{SEP}data",
        f"--add-data=assets{SEP}assets",
        "--hidden-import=matplotlib.backends.backend_qt5agg",
        "--hidden-import=matplotlib.backends.backend_qtagg",
        "--hidden-import=docx",
        "--hidden-import=openpyxl",
        "--noconfirm",
        "--clean",
        "main.py"
    ]

    # Windows 下额外配置
    if IS_WINDOWS:
        # 如果安装了 pillow，确保包含
        cmd.insert(-1, "--hidden-import=PIL")
        cmd.insert(-1, "--hidden-import=PIL.Image")

    print(f"\n执行命令:")
    print(" ".join(cmd))
    print("\n开始打包，请耐心等待（约 2-5 分钟）...\n")

    result = subprocess.run(cmd, cwd=BASE_DIR)

    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("  打包成功！")
        if IS_MAC:
            app_path = os.path.join(DIST_DIR, "TarotInsight.app")
            if os.path.exists(app_path):
                print(f"  ✅ {app_path}")
        elif IS_WINDOWS:
            exe_path = os.path.join(DIST_DIR, "TarotInsight", "TarotInsight.exe")
            if os.path.exists(exe_path):
                print(f"  ✅ {exe_path}")
        else:
            print(f"  输出目录: {DIST_DIR}")
        print("=" * 60)
    else:
        print("\n打包失败，请检查错误信息。")
        sys.exit(1)


if __name__ == "__main__":
    build()
