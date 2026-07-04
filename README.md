# TarotInsight 塔罗牌心理探索工具

基于 PyQt5 开发的桌面端塔罗牌心理探索与占卜工具。

## 软件简介

TarotInsight 是一款塔罗牌心理探索工具，核心流程是：用户输入想要探索的问题，选择问题类型和牌阵，系统随机抽取塔罗牌并生成正逆位结果，再根据卡牌含义、牌阵位置和问题类型生成解读。

**本工具定位为「心理探索、情绪整理、娱乐辅助工具」，不宣称真实预测未来。**

## 功能特性

- 🔮 **占卜抽牌**：输入问题，选择类型和牌阵，随机抽取塔罗牌
- 📖 **智能解读**：根据卡牌、正逆位、牌阵位置和问题类型生成综合解读
- 📜 **历史记录**：保存、查看、筛选和删除占卜记录
- ⭐ **收藏功能**：收藏重要的占卜结果
- 🃏 **塔罗牌库**：浏览完整 78 张经典韦特塔罗牌（含高清图像）
- 📊 **统计分析**：通过饼图/柱状图/趋势图展示占卜数据
- 📄 **导出报告**：导出为 TXT 或 Word 格式
- 🎨 **白金色系主题**：暖白配典雅金，优雅舒适

## 技术栈

- Python 3
- PyQt5（图形界面）
- SQLite（数据存储）
- matplotlib（统计图表）
- python-docx（Word 导出）

## 安装与运行

### 环境要求

- Python 3.7+
- Windows / macOS / Linux

### 安装依赖

```bash
cd TarotInsight
pip install -r requirements.txt
```

### 运行软件

```bash
python main.py
```

## 项目结构

```
TarotInsight/
  main.py                 # 程序入口
  requirements.txt        # Python 依赖
  README.md               # 项目说明
  app/
    windows/              # 窗口模块
      main_window.py      # 主窗口
      reading_window.py   # 占卜窗口
      result_window.py    # 解读结果窗口
      history_window.py   # 历史记录窗口
      card_library_window.py  # 塔罗牌库窗口
      stats_window.py     # 统计分析窗口
      about_window.py     # 帮助/关于窗口
    services/             # 服务层
      tarot_service.py    # 卡牌数据和抽牌逻辑
      interpretation_service.py  # 解读规则引擎
      database_service.py # SQLite 数据库
      export_service.py   # TXT/Word 导出
      stats_service.py    # 统计服务
    widgets/              # 自定义控件
      card_widget.py      # 卡牌展示控件
      chart_widget.py     # matplotlib 图表控件
    utils/                # 工具模块
      paths.py            # 路径管理
      constants.py        # 常量配置
  ui/                     # Qt Designer UI 文件（预留）
  data/
    tarot_cards.json      # 78 张塔罗牌数据
    tarot_app.db          # SQLite 数据库（自动生成）
  assets/
    style.qss             # QSS 样式表（白金色系）
    cards/                # 78 张 RWS 经典卡牌图片
  docs/                   # 文档目录
    软件使用说明书.docx
    成员信息及贡献表.xlsx
  exports/                # 导出报告目录
```

## 打包为可执行程序

> **注意：PyInstaller 不支持跨平台编译。**
> - 在 macOS 上打包 → 生成 `.app`
> - 在 Windows 上打包 → 生成 `.exe`

### macOS（生成 .app）

```bash
pip install pyinstaller
python build_exe.py
```

输出在 `dist/TarotInsight.app`

### Windows（生成 .exe）

**方法一：自动脚本（推荐）**
```cmd
build_exe.bat
```

**方法二：手动执行**
```cmd
pip install pyinstaller
python build_exe.py
```

输出在 `dist\TarotInsight\TarotInsight.exe`

> 分发时请将 `dist\TarotInsight\` 整个文件夹复制，因为其中包含卡牌图片等必要资源。

### 使用 GitHub Actions 自动构建（免费云打包）

如果你没有 Windows 电脑，可以使用 GitHub Actions 在云端自动构建 `.exe`：

1. 将项目推送到 GitHub 仓库
2. GitHub Actions 会自动运行 `.github/workflows/build-exe.yml`
3. 在仓库页面的 **Actions** 标签页 → 点击最新的运行记录
4. 在 **Artifacts** 区域下载 `TarotInsight-Windows-exe.zip`

也可以在 Actions 页面手动点击 **Run workflow** 触发构建。

## 注意事项

- 本软件为本地桌面应用，不联网，不调用 AI API
- 所有解读内容由本地规则生成，仅供参考
- 如需专业心理帮助，请咨询专业心理咨询师
