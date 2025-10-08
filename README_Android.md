# 重要信息管理器 - Android 版本

基于 Kivy 框架开发的移动端重要信息管理应用。

## 功能特点

- 📱 移动端优化界面
- 📝 分类管理
- 💾 信息存储
- 🔍 快速查找
- 💾 本地数据存储

## 开发环境要求

### 系统要求

- Ubuntu 20.04+ 或 Windows 10+ (推荐 Ubuntu)
- Python 3.8+
- Android SDK
- Java JDK 8+

### 安装步骤

#### 1. 安装依赖

```bash
# 安装Python依赖
pip install -r requirements_android.txt

# 安装Buildozer
pip install buildozer
```

#### 2. 安装 Android SDK (Ubuntu)

```bash
# 安装Android SDK
sudo apt update
sudo apt install android-sdk

# 设置环境变量
export ANDROID_HOME=/usr/lib/android-sdk
export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools
```

#### 3. 安装 Java JDK

```bash
# Ubuntu
sudo apt install openjdk-8-jdk

# Windows
# 下载并安装Oracle JDK 8
```

## 构建 APK

### 1. 初始化 Buildozer

```bash
# 在项目目录运行
buildozer init
```

### 2. 构建 APK

```bash
# 构建调试版本
buildozer android debug

# 构建发布版本
buildozer android release
```

### 3. 安装到设备

```bash
# 连接Android设备，启用USB调试
adb devices

# 安装APK
adb install bin/info_manager-1.0-debug.apk
```

## 项目结构

```
my_software/
├── android_main.py          # Android主程序
├── buildozer.spec          # Buildozer配置
├── requirements_android.txt # Android依赖
├── README_Android.md       # Android说明
└── bin/                    # 构建输出目录
    └── info_manager-1.0-debug.apk
```

## 开发说明

### Kivy 框架特点

- 跨平台：支持 Android、iOS、Windows、Linux
- Python 原生：使用 Python 开发
- 触摸优化：专为移动设备设计
- 性能良好：基于 OpenGL ES

### 数据存储

- 使用 Kivy 的 JsonStore 存储数据
- 数据文件：`important_info.json`
- 存储位置：应用私有目录

### 界面设计

- 使用 TabbedPanel 组织界面
- 分类管理和信息管理分离
- 移动端友好的触摸操作

## 部署说明

### 1. 测试版本

```bash
# 构建调试版本
buildozer android debug

# 安装到设备测试
adb install bin/info_manager-1.0-debug.apk
```

### 2. 发布版本

```bash
# 构建发布版本
buildozer android release

# 签名APK（需要密钥）
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore my-release-key.keystore bin/info_manager-1.0-release-unsigned.apk alias_name
```

## 注意事项

1. **首次构建**：需要下载 Android SDK 组件，可能需要较长时间
2. **网络要求**：构建过程需要稳定的网络连接
3. **存储空间**：确保有足够的磁盘空间（至少 2GB）
4. **设备兼容**：支持 Android 5.0+设备

## 故障排除

### 常见问题

1. **构建失败**

   - 检查网络连接
   - 确保 Android SDK 正确安装
   - 检查 Java 版本

2. **APK 安装失败**

   - 检查设备 USB 调试是否启用
   - 确保设备有足够存储空间
   - 检查 APK 签名

3. **应用崩溃**
   - 查看 logcat 日志
   - 检查权限设置
   - 验证数据文件完整性

## 许可证

本项目仅供学习和个人使用。
