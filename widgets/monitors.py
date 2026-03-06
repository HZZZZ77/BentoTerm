import os
import time
import json
import socket
import urllib.request
import subprocess
import psutil
from textual.widgets import Static

# ==========================================
# 🧱 核心组件库 (Apple 极简排版版)
# ==========================================

class SysMonitor(Static):
    """1. 系统资源监控 (真实物理机)"""
    def on_mount(self):
        self.update_sys_info()
        self.set_interval(1.0, self.update_sys_info)

    def update_sys_info(self):
        try:
            # 抓取 CPU 数据
            cpu_percent = psutil.cpu_percent()
            cpu_count = psutil.cpu_count(logical=True)
            
            # 抓取内存数据
            mem = psutil.virtual_memory()
            mem_total = mem.total / (1024 ** 3)
            mem_used = mem.used / (1024 ** 3)
            
            # 抓取磁盘数据
            disk = psutil.disk_usage('/')
            
            # 抓取电池数据
            battery = psutil.sensors_battery()
            batt_str = f"🔋 {battery.percent}% {'(⚡)' if battery.power_plugged else ''}" if battery else "🔌 AC Power"

           # 🛠️ 颜色魔法：会根据负载自动变色的 ASCII 进度条
            def make_bar(percent, width=12):
                filled = int(width * percent / 100)
                bar_str = "█" * filled + "░" * (width - filled)
                
                # 动态判断颜色
                if percent < 50:
                    color = "green"
                elif percent <= 80:
                    color = "yellow"
                else:
                    color = "red"
                    
                # 返回带有富文本标记的字符串 (Textual 会自动解析并上色)
                return f"[{color}]{bar_str}[/{color}]"
                
            def get_color(percent):
                if percent < 50: return "green"
                elif percent <= 80: return "yellow"
                else: return "red"

            # 🍎 苹果极简排版：加入动态颜色标签
            content = f"""
 Mac System Overview

[ CPU ] -------------
Use: {make_bar(cpu_percent)} [{get_color(cpu_percent)}]{cpu_percent}%[/{get_color(cpu_percent)}]
Cor: {cpu_count} Threads

[ Memory ] ----------
Use: {make_bar(mem.percent)} [{get_color(mem.percent)}]{mem.percent}%[/{get_color(mem.percent)}]
Cap: {mem_used:.1f}G / {mem_total:.1f}G

[ Storage & Bat ] ---
HDD: {make_bar(disk.percent)} [{get_color(disk.percent)}]{disk.percent}%[/{get_color(disk.percent)}]
Pwr: {batt_str}

🟢 System Optimal
"""
            self.update(content.strip())
        except Exception:
            self.update(" Mac System\n\nError fetching data 🔴")


class BandwidthMonitor(Static):
    """2. 实时网络吞吐量雷达"""
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
    """3. 系统负载与运行时间"""
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
    """4. 核心端口雷达"""
    def on_mount(self):
        self.set_interval(2.0, self.check_ports)
    def check_ports(self):
        try:
            targets = [3000, 5173, 8080]
            active = [str(c.laddr.port) for c in psutil.net_connections() if hasattr(c, 'laddr') and c.laddr.port in targets and c.status == 'LISTEN']
            self.update(f"🔍 Port Sniffer\n\nIn Use: {', '.join(active) if active else 'None'}")
        except psutil.AccessDenied:
            self.update("🔍 Port Sniffer\n\nNeeds Sudo 🔴")
        except Exception:
            self.update("🔍 Port Sniffer\n\nError 🔴")

class WorkingDirGitStatus(Static):
    """5. 当前目录 Git 状态"""
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
    """6. Docker 容器看板"""
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
    """7. 数据库/缓存探针"""
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
    """8. 滚动日志"""
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
        except Exception:
            self.update(f"📄 Tail Log\n\nError 🔴")

class ApiHealthChecker(Static):
    """9. API 健康探针 (更换为全球最稳定的 Cloudflare 节点)"""
    def on_mount(self):
        self.set_interval(5.0, self.check_api)
    def check_api(self):
        try:
            # 换成极速响应的 1.1.1.1，并将超时放宽到 5 秒
            req = urllib.request.Request("https://1.1.1.1", headers={'User-Agent': 'Mozilla/5.0'})
            code = urllib.request.urlopen(req, timeout=5).getcode()
            self.update(f"🏥 API Health\n\nCloudflare: {code} 🟢")
        except Exception:
            self.update("🏥 API Health\n\nTimeout 🔴")

class GithubRadar(Static):
    """10. GitHub 雷达 (增加限流防爆保护)"""
    def on_mount(self):
        # 刷新频率降到 120 秒，防止被 GitHub 官方封禁 IP
        self.set_interval(120.0, self.fetch_github)
        # 启动时先执行一次
        self.fetch_github()
        
    def fetch_github(self):
        try:
            req = urllib.request.Request("https://api.github.com/repos/HZZZZ77/BentoTerm", headers={'User-Agent': 'Mozilla/5.0'})
            # 超时放宽到 5 秒
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                self.update(f"🐙 GitHub Repo\n\n⭐ Stars: {data.get('stargazers_count', 0)}\n🍴 Forks: {data.get('forks_count', 0)}\nStatus: 🟢")
        except urllib.error.HTTPError as e:
            if e.code == 403:
                self.update("🐙 GitHub Repo\n\nRate Limited 🟡")
            else:
                self.update(f"🐙 GitHub Repo\n\nError {e.code} 🔴")
        except Exception:
            self.update("🐙 GitHub Repo\n\nFetch Failed 🔴")

class LlmApiTracker(Static):
    """11. 大模型测速 (改用实际的连通性测速)"""
    def on_mount(self):
        self.set_interval(5.0, self.ping_llm)
    def ping_llm(self):
        start = time.time()
        try:
            # 用一个稳定的通用接口测速
            req = urllib.request.Request("https://www.github.com", headers={'User-Agent': 'Mozilla/5.0'})
            urllib.request.urlopen(req, timeout=5) 
            latency = (time.time() - start) * 1000
            self.update(f"🧠 LLM API\n\nLatency: {latency:.0f}ms 🟢")
        except Exception:
            self.update("🧠 LLM API\n\nTimeout 🔴")

class TextPlaceholder(Static):
    """12. 占位符"""
    def on_mount(self):
        self.update("🍱 空闲插槽\n\n等待分配...")