import yaml
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Grid

# 核心魔法：直接从我们重构好的 widgets 包里，导入注册表
from widgets import WIDGET_MAP

class BentoTermApp(App):
    """BentoTerm 核心调度引擎"""
    
    CSS = """
    /* 1. 纯黑背景：模拟 OLED 屏幕的深邃感，极其干净 */
    Screen {
        background: #000000; 
    }

    Grid {
        grid-size: 4 3; 
        grid-gutter: 1 2;
        padding: 1 2;
    }

    /* 2. Apple Widget 风格：高级灰底色 + 极细的深色圆角边框 + 纯净的白字 */
    Static {
        background: #1c1c1e;   
        color: #f5f5f7;        
        border: round #3a3a3c; 
        height: 100%;
        content-align: center middle;
    }

    /* 3. 克制的交互：鼠标悬停时，背景微微提亮，边框亮起苹果标志性的科技蓝 */
    Static:hover {
        background: #2c2c2e;   
        border: round #0a84ff; 
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