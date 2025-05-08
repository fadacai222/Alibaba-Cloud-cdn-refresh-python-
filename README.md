---

# 阿里云 CDN 刷新工具

本项目是一个基于 Python 和 CustomTkinter 的图形界面工具，主要用于通过阿里云 API 快速刷新 CDN 缓存，支持多路径、任务状态追踪、配置持久化等功能，适合网站运维人员使用。

## 📦 功能特性

* 图形化界面，简单易用
* 支持刷新文件或目录类型的缓存
* 支持多路径刷新（逐行输入 URL 或目录）
* 自动保存 AccessKey 与刷新路径历史
* 显示任务执行进度与状态

## 🖥️ 界面预览

> 启动后为单窗口图形界面，自动读取 `.env` 中的 AccessKey 信息。

## 🛠️ 安装方式

### 一键安装（推荐）

Windows 用户可直接双击 `一键安装环境.bat` 文件自动创建虚拟环境并安装依赖。

### 手动安装

1. 安装 Python（推荐 3.10+）
2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 运行主程序：

```bash
python main.py
```

## ▶️ 快速启动

Windows 用户可以直接双击 `启动程序.bat` 运行图形界面。

首次使用请填写 AccessKey ID 与 Secret，并点击“保存 AccessKey 到配置”。

然后在文本框中逐行输入要刷新的路径（支持 URL 或以 `/` 结尾的目录），点击“执行刷新”即可。

## 📁 文件结构说明

| 文件/目录名             | 说明                                |
| ------------------ | --------------------------------- |
| `main.py`          | 主程序，图形界面入口                        |
| `requirements.txt` | 项目依赖清单                            |
| `一键安装环境.bat`       | Windows 下自动安装依赖脚本                 |
| `启动程序.bat`         | Windows 下双击运行主程序的启动器              |
| `.env`             | AccessKey ID/Secret 的本地配置文件（自动生成） |
| `path_history.txt` | 上次输入的刷新路径历史记录（自动生成）               |

## 🔒 安全提示

* 请妥善保管 `.env` 中的 AccessKey 信息，避免泄露。
* 建议使用专用 RAM 子账号的临时 AK，以控制权限与风险。

## 🧪 已知问题

* 如果刷新路径非法或权限不足，控制台会显示详细的错误信息
* 不支持多账号并发操作（后续可改进）

## 🧩 开发依赖

* `customtkinter`：美化后的 Tkinter UI 库
* `aliyun-python-sdk-core-v3`：阿里云核心 SDK
* `aliyun-python-sdk-cdn`：阿里云 CDN 接口支持
* `python-dotenv`：用于读取和写入 `.env` 文件

## 📄 License

本项目默认使用 MIT 协议，如需商用请自行评估安全合规问题。

---
