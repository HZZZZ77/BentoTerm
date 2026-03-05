# 🍱 BentoTerm 

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**BentoTerm** 是一个高颜值、高度可定制的极客终端仪表盘 (TUI Dashboard)。

告别杂乱的终端窗口！只需一个简单的 YAML 配置文件，你就能像拼乐高一样，把系统资源、网络延迟、本地服务状态等核心信息，优雅地集中在一个面板里。

## ✨ 核心特性

* **🧱 模块化网格布局**：完全自定义面板的大小、位置和排列。
* **⚙️ 数据驱动配置**：无需修改 Python 代码，通过 `config.yaml` 即可动态增删组件。
* **⚡️ 极速启动**：基于强大的 `Textual` 框架构建，毫秒级响应，极低资源占用。
* **🔌 丰富的内置组件**：
  * `sys_monitor`: 监控 CPU、内存、磁盘状态
  * `network_ping`: 实时测试关键节点的网络连通性
  * `agent_monitor`: 监控本地服务 (如 AI Agent) 的运行状态

## 📦 快速上手

1. **克隆仓库**
   ```bash
   git clone [https://github.com/HZZZZ77/BentoTerm.git](https://github.com/HZZZZ77/BentoTerm.git)
   cd BentoTerm