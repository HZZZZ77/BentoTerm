import yaml
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Grid

# 核心魔法：直接从我们重构好的 widgets 包里，导入注册表
from widgets import WIDGET_MAP

class BentoTermApp(App):
    """BentoTerm 核心调度引擎"""
    
    CSS = """
    /* 1. 苹果极简深色背景 */
    Screen {
        background: #000000; 
    }

    /* 设定 4列 x 3行 的底层网格骨架 */
    Grid {
        grid-size: 4 3; 
        grid-gutter: 1 2;
        padding: 1 2;
    }

    /* 2. 基础卡片样式 (Apple 1x1 Small Widget) */
    Static {
        background: #1c1c1e;   
        color: #f5f5f7;        
        border: round #3a3a3c; 
        height: 100%;
        content-align: center middle;
    }

    Static:hover {
        background: #2c2c2e;   
        border: round #0a84ff; 
    }

    /* 🍏 3. Apple 布局魔法：打破死板，引入大小卡片！ */
    
    /* 核心大面板 (2x2 Large Widget)：占据左上角主导地位 */
    SysMonitor {
        column-span: 2; 
        row-span: 2;    
    }

    /* 宽屏长条面板 (2x1 Medium Widget)：放在右侧上下排列 */
    BandwidthMonitor, GithubRadar {
        column-span: 2; 
    }
    /* 🍏 3. Apple 布局魔法：打破死板，引入大小卡片！ */
    
    /* 核心大面板 (2x2 Large Widget)：占据左上角主导地位 */
    SysMonitor {
        column-span: 2; 
        row-span: 2;    
        content-align: left middle; /* 文字靠左对齐，整体垂直居中 */
        padding-left: 4;            /* 左侧留出呼吸感空白 */
    }

    /* 宽屏长条面板 (2x1 Medium Widget)：放在右侧上下排列 */
    BandwidthMonitor, GithubRadar {
        column-span: 2; 
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