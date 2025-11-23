#!/usr/bin/env python3
"""
Network Analyzer - 改进的网络分析模块

这是对原始 mst.py 的重构版本，展示了改进的代码结构和最佳实践。

作者: wsanalysis 项目
日期: 2025-11-23
"""

from igraph import Graph
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import logging
import colorsys


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NetworkAnalyzer:
    """
    网络分析器类 - 用于社区检测和网络分析

    这个类封装了常用的网络分析功能，包括：
    - 网络加载和预处理
    - 多种社区检测算法
    - 网络可视化
    - 统计信息计算
    """

    def __init__(self, network_file: str = None):
        """
        初始化网络分析器

        Args:
            network_file: 网络文件路径（Pajek 格式），如果为 None，需要后续手动加载
        """
        self.network_file = Path(network_file) if network_file else None
        self.graph: Optional[Graph] = None
        self.communities = None
        self.community_method = None

    def load_network(self, filepath: str = None) -> Graph:
        """
        加载网络文件

        Args:
            filepath: 网络文件路径，如果为 None 则使用初始化时的路径

        Returns:
            加载的图对象

        Raises:
            FileNotFoundError: 文件不存在
            ValueError: 文件格式错误
        """
        if filepath:
            self.network_file = Path(filepath)

        if not self.network_file:
            raise ValueError("No network file specified")

        if not self.network_file.exists():
            logger.error(f"Network file not found: {self.network_file}")
            raise FileNotFoundError(f"Network file not found: {self.network_file}")

        try:
            logger.info(f"Loading network from {self.network_file}")
            self.graph = Graph.Read_Pajek(str(self.network_file))

            # 简化图（移除自环和重复边）
            self.graph = self.graph.simplify()

            logger.info(f"Successfully loaded network with {self.graph.vcount()} vertices "
                       f"and {self.graph.ecount()} edges")
            return self.graph

        except Exception as e:
            logger.error(f"Failed to load network: {e}")
            raise ValueError(f"Failed to parse network file: {e}")

    def detect_communities_betweenness(self, directed: bool = True) -> Dict:
        """
        使用边介数算法检测社区

        这个算法通过迭代移除边介数最高的边来划分社区。
        边介数表示经过该边的最短路径数量。

        Args:
            directed: 是否将图视为有向图

        Returns:
            包含社区信息的字典
        """
        if self.graph is None:
            self.load_network()

        logger.info("Detecting communities using edge betweenness...")

        try:
            result = self.graph.community_edge_betweenness(directed=directed)
            self.communities = result.as_clustering()
            self.community_method = 'edge_betweenness'

            logger.info(f"Found {len(self.communities)} communities, "
                       f"modularity = {self.communities.modularity:.4f}")

            return {
                'method': 'edge_betweenness',
                'membership': self.communities.membership,
                'modularity': self.communities.modularity,
                'num_communities': len(self.communities),
                'sizes': self.communities.sizes()
            }

        except Exception as e:
            logger.error(f"Community detection failed: {e}")
            raise

    def detect_communities_eigenvector(self) -> Dict:
        """
        使用领先特征向量算法检测社区

        这个算法基于图的特征向量分解，速度较快，适合大型网络。

        Returns:
            包含社区信息的字典
        """
        if self.graph is None:
            self.load_network()

        logger.info("Detecting communities using leading eigenvector...")

        try:
            result = self.graph.community_leading_eigenvector()
            self.communities = result
            self.community_method = 'leading_eigenvector'

            logger.info(f"Found {len(self.communities)} communities, "
                       f"modularity = {self.communities.modularity:.4f}")

            return {
                'method': 'leading_eigenvector',
                'membership': self.communities.membership,
                'modularity': self.communities.modularity,
                'num_communities': len(self.communities),
                'sizes': self.communities.sizes()
            }

        except Exception as e:
            logger.error(f"Community detection failed: {e}")
            raise

    def detect_communities_walktrap(self, steps: int = 4) -> Dict:
        """
        使用随机游走算法检测社区

        Args:
            steps: 随机游走的步数

        Returns:
            包含社区信息的字典
        """
        if self.graph is None:
            self.load_network()

        logger.info(f"Detecting communities using walktrap (steps={steps})...")

        try:
            result = self.graph.community_walktrap(steps=steps)
            self.communities = result.as_clustering()
            self.community_method = 'walktrap'

            logger.info(f"Found {len(self.communities)} communities, "
                       f"modularity = {self.communities.modularity:.4f}")

            return {
                'method': 'walktrap',
                'membership': self.communities.membership,
                'modularity': self.communities.modularity,
                'num_communities': len(self.communities),
                'sizes': self.communities.sizes()
            }

        except Exception as e:
            logger.error(f"Community detection failed: {e}")
            raise

    def compare_algorithms(self, methods: List[str] = None) -> Dict[str, Dict]:
        """
        比较多种社区检测算法的结果

        Args:
            methods: 要比较的算法列表，可选值：
                    ['betweenness', 'eigenvector', 'walktrap']
                    如果为 None，则比较所有算法

        Returns:
            各算法的结果字典
        """
        if methods is None:
            methods = ['betweenness', 'eigenvector', 'walktrap']

        results = {}

        for method in methods:
            try:
                if method == 'betweenness':
                    results[method] = self.detect_communities_betweenness()
                elif method == 'eigenvector':
                    results[method] = self.detect_communities_eigenvector()
                elif method == 'walktrap':
                    results[method] = self.detect_communities_walktrap()
                else:
                    logger.warning(f"Unknown method: {method}")
                    results[method] = None

            except Exception as e:
                logger.error(f"Error with {method}: {e}")
                results[method] = None

        return results

    def visualize(
        self,
        output_file: str = None,
        layout: str = 'circle',
        vertex_size: int = 10,
        bbox: Tuple[int, int] = (800, 800)
    ):
        """
        可视化网络和社区结构

        Args:
            output_file: 输出文件路径（如果为 None 则直接显示）
            layout: 布局算法，可选：'circle', 'fr', 'kk', 'lgl'
            vertex_size: 节点大小
            bbox: 画布大小（宽度，高度）
        """
        if self.graph is None:
            self.load_network()

        logger.info(f"Visualizing network with layout={layout}")

        # 如果已检测社区，为节点着色
        if self.communities is not None:
            num_communities = len(self.communities)
            colors = self._generate_colors(num_communities)

            # 为每个节点分配颜色
            for vidx in range(self.graph.vcount()):
                community_id = self.communities.membership[vidx]
                self.graph.vs[vidx]['color'] = colors[community_id]

        # 设置可视化参数
        visual_style = {
            'vertex_size': vertex_size,
            'bbox': bbox,
            'margin': 50
        }

        # 设置布局
        if layout == 'fr':
            visual_style['layout'] = self.graph.layout_fruchterman_reingold()
        elif layout == 'circle':
            visual_style['layout'] = self.graph.layout_circle()
        elif layout == 'kk':
            visual_style['layout'] = self.graph.layout_kamada_kawai()
        elif layout == 'lgl':
            visual_style['layout'] = self.graph.layout_lgl()
        else:
            logger.warning(f"Unknown layout: {layout}, using default")
            visual_style['layout'] = self.graph.layout(layout)

        # 绘制或保存
        if output_file:
            from igraph import plot
            plot(self.graph, output_file, **visual_style)
            logger.info(f"Visualization saved to {output_file}")
        else:
            from igraph import plot
            plot(self.graph, **visual_style)

    def get_statistics(self) -> Dict:
        """
        获取网络的统计信息

        Returns:
            包含各种网络统计指标的字典
        """
        if self.graph is None:
            self.load_network()

        stats = {
            'num_vertices': self.graph.vcount(),
            'num_edges': self.graph.ecount(),
            'density': self.graph.density(),
            'is_connected': self.graph.is_connected(),
            'num_components': len(self.graph.components()),
            'avg_degree': sum(self.graph.degree()) / self.graph.vcount(),
        }

        # 直径只对连通图有意义
        if stats['is_connected']:
            stats['diameter'] = self.graph.diameter()
        else:
            stats['diameter'] = None

        # 如果已检测社区，添加社区相关统计
        if self.communities is not None:
            stats['num_communities'] = len(self.communities)
            stats['modularity'] = self.communities.modularity
            stats['community_sizes'] = self.communities.sizes()

        return stats

    @staticmethod
    def _generate_colors(n: int) -> List[str]:
        """
        生成 n 种视觉上可区分的颜色

        Args:
            n: 需要的颜色数量

        Returns:
            颜色列表（十六进制格式）
        """
        colors = []
        for i in range(n):
            hue = i / n
            saturation = 0.8
            value = 0.9
            rgb = colorsys.hsv_to_rgb(hue, saturation, value)
            hex_color = '#{:02x}{:02x}{:02x}'.format(
                int(rgb[0] * 255),
                int(rgb[1] * 255),
                int(rgb[2] * 255)
            )
            colors.append(hex_color)
        return colors


def main():
    """
    主函数 - 演示如何使用 NetworkAnalyzer 类

    这个示例复现了原始 mst.py 的功能，但使用了改进的代码结构。
    """
    # 获取项目根目录（假设脚本在 py/ 目录下）
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    net_dir = project_root / "net"

    # 指定网络文件
    network_file = net_dir / "camx.net"

    if not network_file.exists():
        logger.error(f"Network file not found: {network_file}")
        logger.info("请确保网络文件存在于 net/ 目录中")
        return

    # 创建分析器
    analyzer = NetworkAnalyzer(str(network_file))

    # 加载网络
    analyzer.load_network()

    # 打印网络统计信息
    stats = analyzer.get_statistics()
    print("\n" + "=" * 50)
    print("网络统计信息:")
    print("=" * 50)
    for key, value in stats.items():
        print(f"{key:<20}: {value}")

    # 检测社区（使用边介数算法）
    print("\n" + "=" * 50)
    print("社区检测 - 边介数算法:")
    print("=" * 50)
    result_betweenness = analyzer.detect_communities_betweenness(directed=True)
    print(f"模块度: {result_betweenness['modularity']:.4f}")
    print(f"社区数: {result_betweenness['num_communities']}")
    print(f"社区成员: {result_betweenness['membership'][:10]}...")  # 只显示前10个

    # 检测社区（使用特征向量算法）
    print("\n" + "=" * 50)
    print("社区检测 - 特征向量算法:")
    print("=" * 50)
    result_eigenvector = analyzer.detect_communities_eigenvector()
    print(f"模块度: {result_eigenvector['modularity']:.4f}")
    print(f"社区数: {result_eigenvector['num_communities']}")
    print(f"社区成员: {result_eigenvector['membership'][:10]}...")

    # 比较所有算法
    print("\n" + "=" * 50)
    print("算法比较:")
    print("=" * 50)
    comparison = analyzer.compare_algorithms()

    print(f"{'算法':<20} {'社区数':<10} {'模块度':<15}")
    print("-" * 50)
    for method, result in comparison.items():
        if result:
            print(f"{method:<20} {result['num_communities']:<10} "
                  f"{result['modularity']:<15.4f}")
        else:
            print(f"{method:<20} {'失败':<10}")

    # 可视化（使用圆形布局）
    print("\n正在生成可视化...")
    output_file = project_root / "community_visualization.pdf"
    analyzer.visualize(
        output_file=str(output_file),
        layout='circle',
        vertex_size=10
    )
    print(f"✓ 可视化已保存到: {output_file}")


if __name__ == "__main__":
    main()
