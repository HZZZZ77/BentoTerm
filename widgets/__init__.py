# 从当前目录的 monitors 文件中导入所有的类
from .monitors import (
    SysMonitor, BandwidthMonitor, LoadAndUptime, LocalPortSniffer,
    WorkingDirGitStatus, MicroDockerDashboard, LocalDbCacheProbe,
    LiveLogTailer, ApiHealthChecker, GithubRadar, LlmApiTracker, TextPlaceholder
)

# 统一对外暴露的组件注册表
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