"""
配置文件 - wsanalysis 项目

这个文件定义了项目的所有配置，包括路径、参数等。
使用配置文件可以避免硬编码路径和参数。
"""

from pathlib import Path
from typing import Dict


class Config:
    """项目配置类"""

    # 项目路径
    PROJECT_ROOT = Path(__file__).parent
    PY_DIR = PROJECT_ROOT / "py"
    R_DIR = PROJECT_ROOT / "R"
    NET_DIR = PROJECT_ROOT / "net"
    TRACE_DIR = PROJECT_ROOT / "trace"
    OUTPUT_DIR = PROJECT_ROOT / "output"

    # 常用网络文件
    NETWORKS = {
        'camx': NET_DIR / "camx.net",
        'ws100s': NET_DIR / "ws100s.net",
        'ws200s': NET_DIR / "ws200s.net",
        'ws300': NET_DIR / "ws300.net",
        'ws500': NET_DIR / "ws500.net",
        'ws': NET_DIR / "ws.net",
    }

    # 社区检测算法配置
    COMMUNITY_ALGORITHMS = {
        'walktrap': {
            'name': 'Random Walk',
            'params': {'steps': 4}
        },
        'eigenvector': {
            'name': 'Leading Eigenvector',
            'params': {}
        },
        'betweenness': {
            'name': 'Edge Betweenness',
            'params': {'directed': True}
        },
        'spinglass': {
            'name': 'Spinglass',
            'params': {'spins': 10}
        }
    }

    # 可视化配置
    VISUALIZATION = {
        'default_layout': 'fr',  # fruchterman-reingold
        'vertex_size': 10,
        'bbox': (800, 800),
        'margin': 50,
        'layouts': ['fr', 'circle', 'kk', 'lgl']
    }

    # 日志配置
    LOGGING = {
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'log_file': PROJECT_ROOT / 'wsanalysis.log'
    }

    @classmethod
    def get_network_path(cls, network_name: str) -> Path:
        """
        获取网络文件路径

        Args:
            network_name: 网络名称（例如 'camx', 'ws300'）

        Returns:
            网络文件的完整路径

        Raises:
            ValueError: 如果网络名称未定义
        """
        if network_name in cls.NETWORKS:
            return cls.NETWORKS[network_name]
        else:
            raise ValueError(f"Unknown network: {network_name}. "
                           f"Available: {list(cls.NETWORKS.keys())}")

    @classmethod
    def create_output_dir(cls) -> Path:
        """创建输出目录（如果不存在）"""
        cls.OUTPUT_DIR.mkdir(exist_ok=True)
        return cls.OUTPUT_DIR

    @classmethod
    def get_algorithm_config(cls, algorithm: str) -> Dict:
        """
        获取算法配置

        Args:
            algorithm: 算法名称

        Returns:
            算法配置字典
        """
        if algorithm in cls.COMMUNITY_ALGORITHMS:
            return cls.COMMUNITY_ALGORITHMS[algorithm]
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")


# 使用示例
if __name__ == "__main__":
    # 打印项目路径
    print("项目配置信息:")
    print(f"项目根目录: {Config.PROJECT_ROOT}")
    print(f"网络数据目录: {Config.NET_DIR}")
    print(f"输出目录: {Config.OUTPUT_DIR}")

    # 列出所有可用的网络
    print("\n可用的网络文件:")
    for name, path in Config.NETWORKS.items():
        exists = "✓" if path.exists() else "✗"
        print(f"  {exists} {name}: {path}")

    # 列出所有算法
    print("\n可用的社区检测算法:")
    for algo, config in Config.COMMUNITY_ALGORITHMS.items():
        print(f"  - {algo}: {config['name']}")
        print(f"    参数: {config['params']}")
