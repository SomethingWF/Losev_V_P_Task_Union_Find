import matplotlib.pyplot as plt
from dsu_model import DisjointSetUnionRank
from visualization import visualize_dsu, setup_visualization_figure

def wait_for_click_or_key(fig_to_wait_on):
    """Ожидает нажатия кнопки мыши или клавиши в окне фигуры."""
    if fig_to_wait_on and fig_to_wait_on.canvas.manager:
        return plt.waitforbuttonpress()
    else:
        print("Figure or canvas manager not available. Advancing automatically (or check GUI setup).")
        return False # Эмулируем нажатие клавиши, чтобы не зависнуть

def demo_step_by_step():
    """
    Пошаговая демонстрация работы DSU с визуализацией по клику мыши.
    """
    dsu = DisjointSetUnionRank()
    ax = setup_visualization_figure(figsize=(12, 8)) # Получаем оси для рисования
    fig = plt.gcf() # Получаем текущую фигуру для waitforbuttonpress

    print("--- Пошаговое демо СНМ ---")
    print("Нашмите на демонстрационное окно для породвижения вперед")

    elements_to_make = [0, 1, 2, 3, 4, "A", "B"]

    # 1. Создание множеств
    visualize_dsu(dsu, ax, "Исходная СНМ (пуста)")
    wait_for_click_or_key(fig)
    
    for i, elem in enumerate(elements_to_make):
        dsu.make_set(elem)
        visualize_dsu(dsu, ax, f"После make_set({elem}) - шаг {i+1}/{len(elements_to_make)}")
        wait_for_click_or_key(fig)
    
    visualize_dsu(dsu, ax, "Все элементы добавлены и образуют собственные множества")
    wait_for_click_or_key(fig)

    # 2. Операции Union
    unions_to_perform = [
        (0, 1, "Union(0, 1)"),
        (2, 3, "Union(2, 3)"),
        ("A", "B", "Union('A', 'B')"),
        (0, 2, "Union(0, 2) - слияние двух множеств"),
        (0, "A", "Union(0, 'A') - слияние множеств с разными типами элементов"),
    ]

    print("\n--- Демонстрания метода union ---")
    for u1, u2, title_suffix in unions_to_perform:
        print(f"Вызов {title_suffix}")
        
        root1 = dsu.find(u1)
        root2 = dsu.find(u2)
        union_occurred = dsu.union(u1, u2)
        
        if union_occurred:
            final_root_u1 = dsu.find(u1)
            joined_edge_info = None
            if dsu.parent.get(root1) == root2 : 
                 joined_edge_info = (root1, root2)
            elif dsu.parent.get(root2) == root1: 
                 joined_edge_info = (root2, root1)
            elif root1 == final_root_u1 and root2 != final_root_u1: 
                 joined_edge_info = (root2, root1)
            elif root2 == final_root_u1 and root1 != final_root_u1: 
                 joined_edge_info = (root1, root2)
            visualize_dsu(dsu, ax, f"После {title_suffix}", last_union_pair=joined_edge_info)
            print(f"{title_suffix}: успешно.")
        else:
            visualize_dsu(dsu, ax, f"После {title_suffix} (Уже были в одном множестве)")
            print(f"{title_suffix}: элементы уже находятся в одном множестве")
        wait_for_click_or_key(fig)
        if title_suffix == "Union(0, 2) - слияние двух множеств":
            visualize_dsu(dsu, ax, f"При слиянии множеств одинакового ранга ранг итогового множества увеличился на 1", highlight_find_path=[0])
            print(f"{title_suffix}: Акцент на ранге нового множества")
            wait_for_click_or_key(fig)

    # 3. Операции Find с демонстрацией сжатия путей
    print("\n--- Демонстрация метода find (Эвристика сжатия путей) ---")
    dsu.make_set(5)
    dsu.make_set(6)
    dsu.make_set(7)
    dsu.union(4,5)
    dsu.union(5,6)
    dsu.union(7,6)
    visualize_dsu(dsu, ax, "Добавление новых элементов и их объединение во множество")
    wait_for_click_or_key(fig)

    # Подсветка для первого сжатия
    find_element = 3
    print(f"При объединении множеств через union(3, 7) будет вызван find({find_element}), что продемонстрирует сжатие пути")
    
    parent_before_find = dsu.parent.get(find_element)
    path_to_highlight = []
    curr = find_element
    temp_parent_dict = dsu.parent.copy()
    while temp_parent_dict.get(curr) != curr and curr in temp_parent_dict:
        path_to_highlight.append(curr)
        if temp_parent_dict.get(curr) is None: break 
        curr = temp_parent_dict.get(curr)
    if curr is not None: path_to_highlight.append(curr)
    
    visualize_dsu(dsu, ax, f"При объединении множеств через union(3,7) будет вызван find({find_element})", highlight_find_path=path_to_highlight)
    wait_for_click_or_key(fig)

    root_of_3 = 0
    dsu.union(3,7)
    final_path_highlight = [find_element, root_of_3] if find_element != root_of_3 else [find_element]
    visualize_dsu(dsu, ax, f"После объединения неявно произошло сжатие пути", highlight_find_path=final_path_highlight)
    wait_for_click_or_key(fig)

    # Подсветка для второго сжатия
    visualize_dsu(dsu, ax, "Демонстрация явного сжатия: состояние СНМ перед find(7)") 
    wait_for_click_or_key(fig)

    find_element = 7
    print(f"Поиск представиля множества элемента {find_element} (будет произведено сжатие пути)")
    
    parent_before_find = dsu.parent.get(find_element)
    path_to_highlight = []
    curr = find_element
    temp_parent_dict = dsu.parent.copy()
    while temp_parent_dict.get(curr) != curr and curr in temp_parent_dict:
        path_to_highlight.append(curr)
        if temp_parent_dict.get(curr) is None: break 
        curr = temp_parent_dict.get(curr)
    if curr is not None: path_to_highlight.append(curr)
    
    visualize_dsu(dsu, ax, f"Путь до корня от узла {find_element} (перед сжатием)", highlight_find_path=path_to_highlight)
    wait_for_click_or_key(fig)

    root_of_7 = dsu.find(find_element)
    
    print(f"Представителем множества для {find_element} является {root_of_7}.")
    print(f"Родитель элемента {find_element} до find: {parent_before_find}, после find: {dsu.parent.get(find_element)}")
    
    final_path_highlight = [find_element, root_of_7] if find_element != root_of_7 else [find_element]
    visualize_dsu(dsu, ax, f"После find({find_element}) - путь был сжат", highlight_find_path=final_path_highlight)
    wait_for_click_or_key(fig)

    visualize_dsu(dsu, ax, f"Итоговок состояние СНМ")
    wait_for_click_or_key(fig)

    print("\nДемо окончено. Закройте  демострационное окно")
    plt.show() # Показываем финальный график и ждем закрытия окна в блокирующем режиме

if __name__ == "__main__":
    demo_step_by_step()