<div align="center">

# 🍱 BentoTerm

```text
 ____             _     _____               
|  _ \           | |   |_   _|              
| |_) | ___ _ __ | |_ ___| | ___ _ __ _ __ ___  
|  _ < / _ \ '_ \| __/ _ \ |/ _ \ '__| '_ ` _ \ 
| |_) |  __/ | | | || (_) | |  __/ |  | | | | | |
|____/ \___|_| |_|\__\___/|_|\___|_|  |_| |_| |_|
A highly customizable, modular TUI dashboard for your terminal.

[ 特性 ] • [ 安装 ] • [ 配置 ] • [ 路线图 ]

</div>

💡 为什么选择 BentoTerm？
作为开发者，我们不应该在终端里开启数十个零散的监控窗口。BentoTerm 通过极其优雅的 YAML 声明式配置，让你像拼便当（Bento）一样，将系统资源、网络延迟、本地守护进程等关键数据，完美整合进一个现代化的终端图形界面 (TUI) 中。

Demo 演示图预留位 > (提示：后续可以用录屏工具录制一张 BentoTerm 在 MacBook 终端里运行的 GIF 动图放在这里，视觉效果拉满)

⚡ 核心特性
🧱 声明式网格系统：基于 YAML 的零代码布局，自由定义模块的行列占比。

🚀 异步非阻塞引擎：底层采用现代化的 Python Textual 框架，毫秒级渲染，极低资源占用。

🔌 即插即用的组件库 (Widgets)：

sys_monitor：硬件状态看板（CPU、内存、磁盘）。

network_ping：全球关键节点连通性与延迟探测。

agent_monitor：本地守护进程（如 OpenClaw）存活状态监控。

🛠️ 极客友好：跨平台原生支持，纯键盘快捷键驱动。

📦 极速构建
推荐使用虚拟环境进行隔离安装，保持系统环境纯净：

Bash
# 1. 克隆仓库
git clone [https://github.com/HZZZZ77/BentoTerm.git](https://github.com/HZZZZ77/BentoTerm.git)
cd BentoTerm

# 2. 构建沙盒环境
python3 -m venv venv
source venv/bin/activate

# 3. 安装依赖引擎
pip install -r requirements.txt
🎮 玩法指南
在终端中启动你的仪表盘：

Bash
python main.py
⚙️ 定制你的面板
BentoTerm 的灵魂在于数据驱动。打开项目根目录的 config.yaml，按你的喜好修改它，终端世界将随之改变：

YAML
# 定义全局网格：2列 x 2行
layout:
  columns: 2
  rows: 2

# 挂载监控模块
widgets:
  - type: sys_monitor
  - type: network_ping
  - type: agent_monitor
  - type: text_placeholder
🗺️ 演进路线图
[x] 核心引擎：YAML 动态解析与网格布局系统

[ ] 数据注入：接入真实物理机数据流

[ ] 视觉进阶：引入 Catppuccin 等极客主题色与动态边框

[ ] 扩展生态：支持通过 Bash/Python 脚本自定义 Widget

🤝 参与重构
如果你想开发一个新的 Widget（比如 GitHub 消息流、服务器 SSH 状态），请随时提交 Pull Request！

📄 许可证
本项目基于 MIT License 协议开源。