import yaml
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Grid

# 核心魔法：直接从我们重构好的 widgets 包里，导入注册表
from widgets import WIDGET_MAP

class BentoTermApp(App):
    """BentoTerm 核心调度引擎"""
    
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
        """解析 YAML 配置文件"""
        try:
            with open("config.yaml", "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {"widgets": [{"type": "text_placeholder"}]}
        except Exception:
            return {"widgets": [{"type": "text_placeholder"}]}

    def compose(self) -> ComposeResult:
        """渲染 UI 界面"""
        yield Header(show_clock=True)
        
        with Grid():
            # 遍历配置，从注册表中实例化对应的组件并渲染
            for widget_info in self.config.get("widgets", []):
                widget_type = widget_info.get("type")
                WidgetClass = WIDGET_MAP.get(widget_type, WIDGET_MAP["text_placeholder"])
                yield WidgetClass()
                
        yield Footer()

if __name__ == "__main__":
    app = BentoTermApp()
    app.run()