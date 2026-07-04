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


def run_check(cmd_args, desc):
    """运行命令并检查结果，失败时打印错误并退出"""
    print(f"\n>>> {desc}")
    r = subprocess.run(cmd_args, cwd=BASE_DIR, capture_output=True, text=True)
    print(r.stdout.strip()[-1000:] if r.stdout else "(无输出)")
    if r.returncode != 0:
        print(f"[错误] {desc} 失败: {r.stderr.strip()[-2000:]}")
        sys.exit(1)
    return r


def build():
    """使用 PyInstaller 打包"""
    print("=" * 60)
    print("  TarotInsight 打包工具")
    print(f"  当前系统: {'Windows' if IS_WINDOWS else 'macOS' if IS_MAC else 'Linux'}")
    print(f"  Python: {sys.version}")
    print(f"  将生成: {'TarotInsight.exe' if IS_WINDOWS else 'TarotInsight.app'}")
    print("=" * 60)

    if len(sys.argv) > 1 and sys.argv[1] == "--clean":
        clean_build()

    os.chdir(BASE_DIR)

    # 验证关键目录存在
    for d in ["data", "assets", "assets/cards"]:
        if not os.path.isdir(d):
            print(f"[错误] 目录不存在: {d}")
            sys.exit(1)

    # 验证关键文件
    for f in ["main.py", "data/tarot_cards.json"]:
        if not os.path.isfile(f):
            print(f"[错误] 文件不存在: {f}")
            sys.exit(1)

    # 验证模块导入
    run_check(
        [sys.executable, "-c",
         "import PyQt5; import matplotlib; import docx; import openpyxl; "
         "from app.windows.main_window import MainWindow; "
         "print('所有模块导入成功')"],
        "验证模块导入"
    )

    # 统一 PyInstaller 参数
    common_args = [
        "--name=TarotInsight",
        "--windowed",
        "--onedir",
        f"--add-data=data{SEP}data",
        f"--add-data=assets{SEP}assets",
        "--noconfirm",
        "--clean",
    ]

    # 使用 --collect-all 确保完整收集 PyQt5 和 matplotlib（避免 hidden-import 遗漏）
    if IS_WINDOWS:
        common_args.append("--collect-all=PyQt5")
        common_args.append("--collect-all=matplotlib")

    cmd = [sys.executable, "-m", "PyInstaller"] + common_args + ["main.py"]

    print(f"\n执行命令:")
    print(" ".join(cmd))
    print("\n开始打包，请耐心等待（约 3-8 分钟）...\n")
    sys.stdout.flush()

    # 直接用 run 让输出实时显示（GitHub Actions 才能捕获日志）
    result = subprocess.run(cmd, cwd=BASE_DIR)

    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("  打包成功！")
        target = os.path.join(DIST_DIR, "TarotInsight", "TarotInsight.exe" if IS_WINDOWS else "TarotInsight.app")
        if os.path.exists(target):
            print(f"  ✅ {target}")
            # 列出产物大小
            total_size = 0
            for root, dirs, files in os.walk(os.path.join(DIST_DIR, "TarotInsight")):
                for fn in files:
                    total_size += os.path.getsize(os.path.join(root, fn))
            print(f"  产物大小: {total_size / 1024 / 1024:.1f} MB")
        print("=" * 60)
    else:
        print(f"\n打包失败 (返回码={result.returncode})")
        # 检查是否有 spec 文件留下
        if os.path.exists(SPEC_FILE):
            print(f"  spec 文件保留在: {SPEC_FILE}")
        sys.exit(1)
        sys.exit(1)


if __name__ == "__main__":
    build()
