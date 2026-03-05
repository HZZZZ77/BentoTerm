import yaml
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Grid

# --- 1. 定义基础组件 (Widgets) ---

class SysMonitor(Static):
    """系统资源监控组件"""
    def on_mount(self) -> None:
        self.update("💻 System\n\nCPU: 12%\nRAM: 45%\nDisk: 60%")

class NetworkPing(Static):
    """网络延迟监控组件 (替换了原来的 Market)"""
    def on_mount(self) -> None:
        self.update("🌐 Network\n\nPing 1.1.1.1: 24ms\nPing github.com: 45ms\nStatus: 🟢 Online")

class AgentMonitor(Static):
    """本地 AI Agent 状态组件"""
    def on_mount(self) -> None:
        self.update("🤖 Local AI Agent\n\nOpenClaw (MacBook): RUNNING\nPort: 8080\nStatus: Ready")

class TextPlaceholder(Static):
    """默认占位组件"""
    def on_mount(self) -> None:
        self.update("🍱 自定义模块\n\n这是从 config.yaml 动态加载的")

# --- 2. 建立组件注册表 (核心魔法) ---
WIDGET_MAP = {
    "sys_monitor": SysMonitor,
    "network_ping": NetworkPing,  # 这里换成了新的网络组件
    "agent_monitor": AgentMonitor,
    "text_placeholder": TextPlaceholder
}

# --- 3. 主程序与布局 ---
class BentoTermApp(App):
    """BentoTerm 核心应用"""
    
    CSS = """
    Grid {
        grid-size: 2 2;
        grid-gutter: 1 2;
        padding: 1 2;
    }
    Static {
        border: solid green;
        height: 100%;
        content-align: center middle;
    }
    """
    
    BINDINGS = [("q", "quit", "退出 BentoTerm")]

    def __init__(self):
        super().__init__()
        self.dashboard_config = self.load_config()

    def load_config(self):
        """读取外部的 config.yaml 文件"""
        try:
            with open("config.yaml", "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
                if config is None:
                    return {"widgets": [{"type": "text_placeholder"}]}
                return config
        except FileNotFoundError:
            return {"widgets": [{"type": "text_placeholder"}]}

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        
        with Grid():
            widgets_config = self.dashboard_config.get("widgets", [])
            for widget_info in widgets_config:
                widget_type = widget_info.get("type")
                
                if widget_type in WIDGET_MAP:
                    WidgetClass = WIDGET_MAP[widget_type]
                    yield WidgetClass()
                else:
                    yield Static(f"❌ 配置错误\n\n找不到组件:\n{widget_type}", id="error")
            
        yield Footer()

if __name__ == "__main__":
    app = BentoTermApp()
    app.run()