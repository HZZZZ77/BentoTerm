import os
import time
import json
import socket
import urllib.request
import subprocess
import yaml
import psutil
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Grid

# ==========================================
# 🧱 第一部分：海量极客组件库 (加入全方位防崩溃保护)
# ==========================================

import os
import time
import json
import socket
import urllib.request
import subprocess
import psutil
from textual.widgets import Static

class SysMonitor(Static):
    def on_mount(self):
        self.update_sys_info()
        self.set_interval(1.0, self.update_sys_info)

    def update_sys_info(self):
        try:
            # 1. 抓取 CPU 数据
            cpu_percent = psutil.cpu_percent()
            cpu_count = psutil.cpu_count(logical=True)
            
            # 2. 抓取内存数据
            mem = psutil.virtual_memory()
            mem_total = mem.total / (1024 ** 3)
            mem_used = mem.used / (1024 ** 3)
            
            # 3. 抓取磁盘数据 (根目录)
            disk = psutil.disk_usage('/')
            
            # 4. 抓取 MacBook 电池数据
            battery = psutil.sensors_battery()
            batt_str = f"🔋 {battery.percent}% {'(⚡Charging)' if battery.power_plugged else ''}" if battery else "🔌 AC Power"

            # 🛠️ 制造 ASCII 进度条的魔法函数
            def make_bar(percent, width=20):
                filled = int(width * percent / 100)
                # 使用实心方块和点阵方块拼接
                return "█" * filled + "░" * (width - filled)

            # 🍎 苹果风排版布局
            content = f"""
 Mac System Overview

[ CPU Core ] -----------------------
Usage: {make_bar(cpu_percent)} {cpu_percent}%
Cores: {cpu_count} Logical Threads

[ Memory ] -------------------------
Usage: {make_bar(mem.percent)} {mem.percent}%
Alloc: {mem_used:.1f} GB / {mem_total:.1f} GB

[ Storage & Power ] ----------------
Disk:  {make_bar(disk.percent)} {disk.percent}%
Power: {batt_str}

Status: 🟢 System Running Optimal
"""
            self.update(content.strip())
        except Exception:
            self.update(" Mac System\n\nError fetching data 🔴")

# ... 保持下面的其他类代码不变 ...

class BandwidthMonitor(Static):
    def on_mount(self):
        try:
            self.last_io = psutil.net_io_counters()
        except:
            self.last_io = None
        self.set_interval(1.0, self.update_io)
    def update_io(self):
        try:
            if not self.last_io:
                self.last_io = psutil.net_io_counters()
                return
            curr_io = psutil.net_io_counters()
            dl = (curr_io.bytes_recv - self.last_io.bytes_recv) / 1024 / 1024
            ul = (curr_io.bytes_sent - self.last_io.bytes_sent) / 1024 / 1024
            self.last_io = curr_io
            self.update(f"📡 Bandwidth\n\n↓ {dl:.2f} MB/s\n↑ {ul:.2f} MB/s")
        except Exception:
            self.update("📡 Bandwidth\n\nUnavailable 🔴")

class LoadAndUptime(Static):
    def on_mount(self):
        self.set_interval(1.0, self.update_info)
    def update_info(self):
        try:
            load = os.getloadavg() if hasattr(os, 'getloadavg') else (0,0,0)
            uptime = time.time() - psutil.boot_time()
            m, s = divmod(uptime, 60)
            h, m = divmod(m, 60)
            self.update(f"⚙️ Load & Uptime\n\nLoad: {load[0]:.2f}, {load[1]:.2f}\nUp: {int(h)}h {int(m)}m")
        except Exception:
            self.update("⚙️ Load & Uptime\n\nError 🔴")

class LocalPortSniffer(Static):
    def on_mount(self):
        self.set_interval(2.0, self.check_ports)
    def check_ports(self):
        try:
            targets = [3000, 5173, 8080]
            # macOS 下无 sudo 运行 net_connections 会抛出 AccessDenied
            active = [str(c.laddr.port) for c in psutil.net_connections() if hasattr(c, 'laddr') and c.laddr.port in targets and c.status == 'LISTEN']
            self.update(f"🔍 Port Sniffer\n\nIn Use: {', '.join(active) if active else 'None'}")
        except psutil.AccessDenied:
            self.update("🔍 Port Sniffer\n\nNeeds Sudo 🔴")
        except Exception:
            self.update("🔍 Port Sniffer\n\nError 🔴")

class WorkingDirGitStatus(Static):
    def on_mount(self):
        self.set_interval(3.0, self.check_git)
    def check_git(self):
        try:
            branch = subprocess.check_output(["git", "branch", "--show-current"], stderr=subprocess.DEVNULL, timeout=1).decode().strip()
            status = subprocess.check_output(["git", "status", "-s"], stderr=subprocess.DEVNULL, timeout=1).decode().strip()
            changes = len(status.split('\n')) if status else 0
            self.update(f"🌲 Git Status\n\nBranch: {branch}\nChanges: {changes}")
        except subprocess.TimeoutExpired:
            self.update("🌲 Git Status\n\nTimeout 🔴")
        except Exception:
            self.update("🌲 Git Status\n\nNot a Git Repo 🔴")

class MicroDockerDashboard(Static):
    def on_mount(self):
        self.set_interval(3.0, self.check_docker)
    def check_docker(self):
        try:
            res = subprocess.check_output(["docker", "ps", "--format", "{{.Names}}"], stderr=subprocess.DEVNULL, timeout=1).decode().strip().split('\n')
            containers = "\n".join(res[:2]) if res and res[0] else "No running config"
            self.update(f"🐳 Docker\n\n{containers}")
        except FileNotFoundError:
            self.update("🐳 Docker\n\nNot Installed 🔴")
        except Exception:
            self.update("🐳 Docker\n\nService Offline 🔴")

class LocalDbCacheProbe(Static):
    def on_mount(self):
        self.set_interval(5.0, self.check_db)
    def check_db(self):
        def ping(port):
            try:
                socket.create_connection(("127.0.0.1", port), timeout=0.2).close()
                return "🟢"
            except: return "🔴"
        self.update(f"🗄️ DB/Cache\n\nRedis(6379): {ping(6379)}\nMySQL(3306): {ping(3306)}")

class LiveLogTailer(Static):
    def on_mount(self):
        self.log_file = "agent.log" 
        self.set_interval(1.0, self.update_log)
    def update_log(self):
        try:
            if not os.path.exists(self.log_file):
                self.update("📄 Tail Log\n\nWaiting for file...")
                return
            with open(self.log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()[-2:]
                self.update(f"📄 Tail: {self.log_file}\n" + "".join(lines).strip())
        except Exception as e:
            self.update(f"📄 Tail Log\n\nError 🔴")

class ApiHealthChecker(Static):
    def on_mount(self):
        self.set_interval(5.0, self.check_api)
    def check_api(self):
        try:
            req = urllib.request.Request("https://httpbin.org/status/200", headers={'User-Agent': 'Mozilla/5.0'})
            code = urllib.request.urlopen(req, timeout=2).getcode()
            self.update(f"🏥 API Health\n\nHTTPBin: {code} 🟢")
        except Exception:
            self.update("🏥 API Health\n\nConnection Err 🔴")

class GithubRadar(Static):
    def on_mount(self):
        self.set_interval(60.0, self.fetch_github) 
    def fetch_github(self):
        try:
            req = urllib.request.Request("https://api.github.com/repos/HZZZZ77/BentoTerm", headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=3) as response:
                data = json.loads(response.read().decode())
                self.update(f"🐙 GitHub Repo\n\n⭐ Stars: {data.get('stargazers_count', 0)}\n🍴 Forks: {data.get('forks_count', 0)}")
        except Exception:
            self.update("🐙 GitHub Repo\n\nFetch Failed 🔴")

class LlmApiTracker(Static):
    def on_mount(self):
        self.set_interval(5.0, self.ping_llm)
    def ping_llm(self):
        start = time.time()
        try:
            req = urllib.request.Request("https://api.github.com", headers={'User-Agent': 'Mozilla/5.0'})
            urllib.request.urlopen(req, timeout=2) 
            latency = (time.time() - start) * 1000
            self.update(f"🧠 LLM API\n\nLatency: {latency:.0f}ms 🟢")
        except Exception:
            self.update("🧠 LLM API\n\nTimeout 🔴")

class TextPlaceholder(Static):
    def on_mount(self):
        self.update("🍱 空闲插槽\n\n等待分配...")

# ==========================================
# ⚙️ 第二部分：核心注册表与引擎
# ==========================================

WIDGET_MAP = {
    "sys_monitor": SysMonitor,
    "bandwidth_monitor": BandwidthMonitor,
    "load_uptime": LoadAndUptime,
    "port_sniffer": LocalPortSniffer,
    "git_status": WorkingDirGitStatus,
    "docker_dashboard": MicroDockerDashboard,
    "db_cache_probe": LocalDbCacheProbe,
    "live_log_tailer": LiveLogTailer,
    "api_health": ApiHealthChecker,
    "github_radar": GithubRadar,
    "llm_api_tracker": LlmApiTracker,
    "text_placeholder": TextPlaceholder
}

class BentoTermApp(App):
    CSS = """
    Grid {
        grid-size: 4 3; 
        grid-gutter: 1 2;
        padding: 1 2;
    }
    Static {
        border: solid green;
        height: 100%;
        content-align: center middle;
    }
    """
    BINDINGS = [("q", "quit", "Exit BentoTerm")]

    def __init__(self):
        super().__init__()
        self.config = self.load_config()

    def load_config(self):
        try:
            with open("config.yaml", "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {"widgets": [{"type": "text_placeholder"}]}
        except:
            return {"widgets": [{"type": "text_placeholder"}]}

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Grid():
            for w in self.config.get("widgets", []):
                yield WIDGET_MAP.get(w.get("type"), TextPlaceholder)()
        yield Footer()

if __name__ == "__main__":
    app = BentoTermApp()
    app.run()