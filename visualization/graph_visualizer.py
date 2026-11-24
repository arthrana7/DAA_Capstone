"""
visualization/graph_visualizer.py
Visualizes the delivery road network and the TSP delivery tour using Matplotlib and NetworkX.
Note: NetworkX is used strictly for graph layout rendering, NOT for algorithm calculations.
"""

from typing import Optional, List
import matplotlib.pyplot as plt
try:
    import networkx as nx
except ImportError:
    nx = None
from models.delivery_graph import DeliveryGraph
from algorithms.tsp import TSPResult


def plot_delivery_network(
    graph: DeliveryGraph,
    tsp_result: Optional[TSPResult] = None,
    save_path: Optional[str] = None,
    title: str = "SwiftRoute Logistics: Delivery Network & TSP Route"
) -> plt.Figure:
    fig, ax = plt.subplots(figsize=(11, 8))

    nodes = graph.get_nodes()
    pos = graph.coordinates if len(graph.coordinates) == len(nodes) else {n: (i * 2.0, (i % 3) * 3.0) for i, n in enumerate(nodes)}

    # 1. Draw base road edges
    for u in nodes:
        for v, w in graph.get_neighbors(u):
            if u < v or (v, u) not in [(x, y) for x in nodes for y, _ in graph.get_neighbors(x)]:
                p1, p2 = pos[u], pos[v]
                ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="#CBD5E1", lw=2.0, zorder=1)
                mid_x = (p1[0] + p2[0]) / 2.0
                mid_y = (p1[1] + p2[1]) / 2.0
                ax.text(
                    mid_x, mid_y, f"{w:.1f} km",
                    fontsize=8, color="#475569", ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#E2E8F0", alpha=0.9),
                    zorder=2
                )

    # 2. Categorize nodes: Warehouse, Delivery Stops, Other Network Nodes
    warehouse = tsp_result.warehouse if tsp_result else "Okhla Central Hub"
    visited_stops = tsp_result.route_sequence if tsp_result else []
    delivery_stops = [n for n in visited_stops if n != warehouse]
    other_nodes = [n for n in nodes if n != warehouse and n not in delivery_stops]

    if other_nodes:
        ox = [pos[n][0] for n in other_nodes]
        oy = [pos[n][1] for n in other_nodes]
        ax.scatter(ox, oy, s=600, color="#94A3B8", alpha=0.7, zorder=3)

    if delivery_stops:
        dx = [pos[n][0] for n in delivery_stops]
        dy = [pos[n][1] for n in delivery_stops]
        ax.scatter(dx, dy, s=800, color="#3B82F6", edgecolors="#1D4ED8", lw=2, zorder=4)

    if warehouse in nodes:
        wx, wy = pos[warehouse]
        ax.scatter([wx], [wy], s=1000, color="#10B981", marker="s", edgecolors="#047857", lw=2.5, zorder=5)

    # 3. Node labels
    for node in nodes:
        x, y = pos[node]
        if node == warehouse:
            ax.text(x, y - 0.35, f"★ {node}\n(DEPOT)", fontsize=8.5, fontweight="bold", color="#0F172A", ha="center", va="top", zorder=6)
        elif node in delivery_stops:
            order_indices = [str(i) for i, s in enumerate(visited_stops) if s == node]
            ax.text(x, y - 0.35, f"{node}\n[Stop #{','.join(order_indices)}]", fontsize=8.5, fontweight="bold", color="#0F172A", ha="center", va="top", zorder=6)
        else:
            ax.text(x, y - 0.35, node, fontsize=8.5, fontweight="bold", color="#0F172A", ha="center", va="top", zorder=6)

    # 4. Highlight TSP Tour path with directional arrows
    if tsp_result and tsp_result.detailed_legs:
        for idx, leg in enumerate(tsp_result.detailed_legs):
            leg_path = leg.path
            for i in range(len(leg_path) - 1):
                u_leg, v_leg = leg_path[i], leg_path[i + 1]
                p1, p2 = pos[u_leg], pos[v_leg]
                ax.annotate(
                    "",
                    xy=p2, xycoords="data",
                    xytext=p1, textcoords="data",
                    arrowprops=dict(
                        arrowstyle="-|>",
                        color="#EF4444",
                        lw=3.0,
                        ls="-",
                        shrinkA=15,
                        shrinkB=15,
                        mutation_scale=15
                    ),
                    zorder=7
                )

        total_km = tsp_result.total_distance_km
        ax.text(
            0.02, 0.02,
            f"Active TSP Tour: {' -> '.join(tsp_result.route_sequence)}\n"
            f"Total Driving Distance: {total_km:.2f} km | Stops: {len(delivery_stops)}",
            transform=ax.transAxes,
            fontsize=9.5,
            fontweight="semibold",
            bbox=dict(boxstyle="round,pad=0.5", fc="#FEF2F2", ec="#F87171", lw=1.5),
            zorder=8
        )

    ax.set_title(title, fontsize=14, fontweight="bold", pad=15)
    ax.axis("off")
    fig.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")

    return fig

