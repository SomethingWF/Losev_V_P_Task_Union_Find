import networkx as nx
import matplotlib.pyplot as plt

# Глобальные переменные для фигуры и осей, чтобы переиспользовать их
_fig = None
_ax = None

def setup_visualization_figure(figsize=(12, 8)):
    """Инициализирует или переиспользует фигуру Matplotlib для визуализации."""
    global _fig, _ax
    if _fig is None or _ax is None:
        _fig, _ax = plt.subplots(figsize=figsize)
        plt.ion() # Включаем интерактивный режим для немедленного plt.draw()
    return _ax

def _get_node_positions(dsu_instance, G):
    """
    Рассчитывает позиции узлов для более иерархического отображения.
    Корни располагаются в верхнем ряду.
    """
    pos = {}
    roots = [node for node in G.nodes() if dsu_instance.parent.get(node) == node]
    other_nodes = [node for node in G.nodes() if node not in roots]

    # Располагаем корни
    root_y = 1.0
    for i, root in enumerate(roots):
        pos[root] = (i * 2.0, root_y) # Расстояние между корнями

    # Рекурсивная функция для расположения детей
    def position_children(parent_node, parent_x, current_y, x_spread_factor=0.7, y_step=-0.3):
        children = [child for child, p_candidate in dsu_instance.parent.items()
                    if p_candidate == parent_node and child != parent_node]
        
        num_children = len(children)
        if num_children == 0:
            return

        start_x = parent_x - ( (num_children -1) * x_spread_factor / 2.0 )

        for i, child in enumerate(children):
            if child not in pos: 
                child_x = start_x + i * x_spread_factor
                pos[child] = (child_x, current_y)
                position_children(child, child_x, current_y + y_step, x_spread_factor * 0.8, y_step)

    for root in roots:
        y_step=-0.3
        position_children(root, pos[root][0], root_y + y_step)

    current_x_fallback = (len(roots) + 1) * 2.0
    for node in other_nodes:
        if node not in pos:
            pos[node] = (current_x_fallback, 0.0) 
            current_x_fallback += 1.5
            
    if not pos and G.nodes(): 
        pos = nx.spring_layout(G, seed=42)
    elif len(pos) != len(G.nodes()): 
        remaining_nodes = [n for n in G.nodes() if n not in pos]
        if remaining_nodes:
            sub_graph = G.subgraph(remaining_nodes)
            if sub_graph.nodes(): 
                 pos_remaining = nx.spring_layout(sub_graph, center=pos.get(list(pos.keys())[0] if pos else (0,0) , (0,0)), seed=42)
                 pos.update(pos_remaining)
    
    if not pos and G.nodes(): 
        pos = nx.spring_layout(G, seed=42) 

    return pos


def visualize_dsu(dsu_instance, ax, title="", highlight_nodes=None, highlight_find_path=None, last_union_pair=None):
    """
    Визуализирует текущее состояние Системы непересекающихся множеств.
    """
    ax.clear()
    G = nx.DiGraph() 

    nodes_to_draw = list(dsu_instance.parent.keys())
    if not nodes_to_draw: 
        ax.set_title(title if title else "DSU is empty")
        ax.axis('off')
        plt.draw()
        # plt.pause(0.1) # Маленькая пауза все равно может быть полезна для обновления GUI
        return

    G.add_nodes_from(nodes_to_draw)

    edges = []
    for item, parent_item in dsu_instance.parent.items():
        if item != parent_item:  
            edges.append((item, parent_item)) 
    G.add_edges_from(edges)

    pos = _get_node_positions(dsu_instance, G)
    if not pos and G.nodes(): 
        pos = nx.spring_layout(G, k=1.5, iterations=50, seed=42)

    node_colors = []
    for node in G.nodes():
        is_root = (dsu_instance.parent.get(node) == node)
        if highlight_nodes and node in highlight_nodes:
            node_colors.append('orange')  
        elif highlight_find_path and node in highlight_find_path:
            node_colors.append('yellow') 
        elif last_union_pair and node in last_union_pair:
             node_colors.append('magenta') 
        elif is_root:
            node_colors.append('skyblue') 
        else:
            node_colors.append('lightgreen') 

    edge_colors = []
    edge_widths = []
    if G.number_of_edges() > 0:
        for u, v_target in G.edges(): 
            is_find_path_edge = highlight_find_path and u in highlight_find_path and v_target in highlight_find_path
            is_last_union_edge = False
            if last_union_pair:
                 if (u == last_union_pair[0] and v_target == last_union_pair[1]):
                     is_last_union_edge = True

            if is_find_path_edge:
                edge_colors.append('gold')
                edge_widths.append(2.5)
            elif is_last_union_edge:
                edge_colors.append('darkmagenta')
                edge_widths.append(2.5)
            else:
                edge_colors.append('gray')
                edge_widths.append(1.5)
    
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=700, edgecolors='black')
    if G.number_of_edges() > 0:
        nx.draw_networkx_edges(G, pos, ax=ax, edgelist=list(G.edges()), edge_color=edge_colors, width=edge_widths,
                               arrows=True, arrowstyle='-|>', arrowsize=20, connectionstyle='arc3,rad=0.1')
    
    labels = {node: f"{node}\n(r:{dsu_instance.rank.get(node,0)})" if dsu_instance.parent.get(node) == node else str(node) 
              for node in G.nodes()}
    nx.draw_networkx_labels(G, pos, ax=ax, labels=labels, font_size=9)

    ax.set_title(title)
    ax.axis('off')
    plt.draw() # Обновить отображение