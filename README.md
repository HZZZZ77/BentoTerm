# 🍱 BentoTerm

```text
 ____             _     _____               
|  _ \           | |   |_   _|              
| |_) | ___ _ __ | |_ ___| | ___ _ __ _ __ ___  
|  _ < / _ \ '_ \| __/ _ \ |/ _ \ '__| '_ ` _ \ 
| |_) |  __/ | | | || (_) | |  __/ |  | | | | | |
|____/ \___|_| |_|\__\___/|_|\___|_|  |_| |_| |_|
A highly customizable, modular TUI dashboard for your terminal.

[ Features ] • [ Installation ] • [ Configuration ] • [ Roadmap ]

</div>

💡 Why BentoTerm?
As developers, we shouldn't have to juggle dozens of scattered monitoring windows in our terminals. BentoTerm leverages elegant, declarative YAML configuration, allowing you to assemble critical data—like system resources, network latency, and local daemons—into a modern Terminal User Interface (TUI), just like packing a Bento box.

[Demo GIF Placeholder] > (Drop a cool GIF of BentoTerm running in your terminal here later)

⚡ Features
🧱 Declarative Grid System: Zero-code layout based on YAML. Freely define the row and column ratios of your modules.

🚀 Asynchronous Engine: Powered by the modern Python Textual framework. Millisecond rendering with a minimal resource footprint.

🔌 Plug-and-Play Widgets:

sys_monitor: Hardware status board (CPU, RAM, Disk).

network_ping: Global node connectivity and latency probing.

agent_monitor: Local daemon (e.g., OpenClaw AI Agent) survival status monitoring.

🛠️ Geek Friendly: Native cross-platform support, driven entirely by keyboard shortcuts.

📦 Installation
It is highly recommended to use a virtual environment for an isolated installation to keep your system clean:

Bash
# 1. Clone the repository
git clone [https://github.com/HZZZZ77/BentoTerm.git](https://github.com/HZZZZ77/BentoTerm.git)
cd BentoTerm

# 2. Setup the sandbox environment
python3 -m venv venv
source venv/bin/activate

# 3. Install the core engine
pip install -r requirements.txt
🎮 Usage
Fire up your dashboard in the terminal:

Bash
python main.py
⚙️ Configuration
The soul of BentoTerm is data-driven. Open config.yaml in the project root, tweak it to your liking, and watch your terminal world transform instantly:

YAML
# Define the global grid: 2 columns x 2 rows
layout:
  columns: 2
  rows: 2

# Mount the monitoring widgets
widgets:
  - type: sys_monitor
  - type: network_ping
  - type: agent_monitor
  - type: text_placeholder
🗺️ Roadmap
[x] Core Engine: Dynamic YAML parsing & grid layout system

[ ] Data Injection: Integrate real-time physical machine data streams (e.g., psutil)

[ ] Visuals: Introduce geeky themes (Catppuccin, Dracula) and dynamic borders

[ ] Ecosystem: Support custom Widgets via Bash/Python scripts

🤝 Contributing
Any crazy ideas are welcome here. If you want to develop a new Widget (e.g., GitHub feed, server SSH status, weather), feel free to submit a Pull Request!

📄 License
This project is open-sourced under the MIT License.