# 重要信息管理器

一个简单易用的重要信息管理工具，支持 Windows 桌面版和 Android 移动版。

## 功能特点

- 📝 **分类管理**：创建、删除不同的信息分类
- 💾 **信息存储**：添加、编辑、删除重要信息
- 🔍 **快速查找**：双击信息项查看详细信息
- 💾 **自动保存**：数据自动保存到本地文件
- 🎨 **简洁界面**：现代化 UI 设计
- 📱 **跨平台**：支持 Windows 和 Android

## 版本说明

### Windows 版本

- 基于 tkinter 的桌面应用程序
- 支持 Windows 10/11
- 独立 exe 文件，无需安装 Python

### Android 版本

- 基于 Kivy 框架的移动应用
- 支持 Android 5.0+
- 触摸优化的移动端界面

## 快速开始

### Windows 版本

1. 下载 `dist/重要信息管理器.exe`
2. 双击运行即可使用
3. 数据保存在 exe 同目录的 JSON 文件中

### Android 版本

1. 查看 [Releases](../../releases) 页面
2. 下载最新的 APK 文件
3. 在 Android 设备上安装使用

## 开发说明

### 环境要求

- Python 3.9+
- Conda（推荐）
- Android SDK（Android 版本）

### 本地开发

```bash
# 克隆仓库
git clone https://github.com/yourusername/info-manager.git
cd info-manager

# 创建虚拟环境
conda create -n info_manager python=3.9 -y
conda activate info_manager

# 安装依赖
pip install -r requirements.txt

# 运行Windows版本
python main.py

# 运行Android版本（需要Android SDK）
pip install -r requirements_android.txt
buildozer android debug
```

### 构建说明

#### Windows 版本

```bash
# 安装PyInstaller
pip install pyinstaller

# 构建exe文件
pyinstaller build_exe.spec
```

#### Android 版本

```bash
# 安装Buildozer
pip install buildozer

# 构建APK文件
buildozer android debug
```

## 项目结构

```
info-manager/
├── main.py                    # Windows版本主程序
├── android_main.py           # Android版本主程序
├── build_exe.spec           # Windows构建配置
├── buildozer.spec           # Android构建配置
├── requirements.txt         # Windows依赖
├── requirements_android.txt # Android依赖
├── .github/workflows/       # GitHub Actions配置
├── dist/                    # Windows构建输出
└── bin/                     # Android构建输出
```

## 数据存储

- **Windows 版本**：数据保存在 exe 同目录的`important_info.json`文件中
- **Android 版本**：数据保存在应用私有目录的 JSON 文件中
- **数据格式**：JSON 格式，便于备份和迁移

## 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 许可证

本项目仅供学习和个人使用。

## 更新日志

### v1.0.0

- 初始版本发布
- 支持 Windows 桌面版
- 支持 Android 移动版
- 基本的信息管理功能

## 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 [Issue](../../issues)
- 发送邮件到：your-email@example.com

---

**注意**：本项目仅供学习和个人使用，请勿用于商业用途。
