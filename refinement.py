"""
Module for working with refinement.
"""
# Dario Capitani - s2754194
# Gyum Cho - s2113201
# Junseo Kim - s2648687

from collections import defaultdict, deque
from graph import Graph, Vertex
from dll import Node, DoublyLinkedList


def refine(graphs: list[Graph], initial: dict[Vertex, int] = None) -> dict[Vertex, int]:
    """
    Apply color refinement to a list of graphs.
    :param graphs: List of graphs
    :param initial: Optional initial coloring
    :return: Dictionary mapping of each vertex to a color
    """
    vertices = []
    for graph in graphs:  # combine vertices
        vertices += graph.vertices

    ax = {}
    ay = dict(zip(vertices, [0] * len(vertices)))  # default coloring

    mapping = {}  # neighbour combination to color
    offset = 0

    if initial is not None and len(initial) != 0:
        ay.update(initial)  # use initial coloring
        offset = max(initial.values())  # start with next highest color

    while ax != ay:  # until stable
        ax = ay
        ay = {}
        mapping.clear()
        c = offset + 1

        for vertex in ax:

            if initial is not None and vertex in initial:
                ay[vertex] = vertex.colornum = initial.get(vertex)  # maintain initial mapping
                continue

            n = []
            for neighbour in vertex.neighbours:  # get neighbour coloring
                n.append(ax.get(neighbour))

            n.sort()
            neighbour_set = tuple(n)

            if neighbour_set not in mapping:
                mapping[neighbour_set] = c
                c += 1

            ay[vertex] = vertex.colornum = mapping.get(neighbour_set)  # assign vertex coloring

    return ay


def fast_refine(graphs: list[Graph], initial: dict[Vertex, int] = None) -> dict[Vertex, int]:
    """
    Apply fast color refinement to a list of graphs.
    :param graphs: List of graphs
    :param initial: Optional initial coloring
    :return: Dictionary mapping of each vertex to a color
    """
    vertices = []
    for graph in graphs:  # combine vertices
        vertices += graph.vertices

    coloring = dict(zip(vertices, [0] * len(vertices)))  # default coloring

    if initial is not None:
        coloring.update(initial)  # maintain initial coloring

    color_class = defaultdict(DoublyLinkedList)  # map color to dll
    pointer = {}  # map vertex to dll node
    in_queue = {}

    max_color = 0
    for vertex, color in coloring.items():
        vertex.colornum = color
        node = Node(vertex)
        color_class[color].insert(node)
        pointer[vertex] = node
        if color > max_color:
            max_color = color

    queue = deque([])
    for color in color_class:
        queue.appendleft(color)
        in_queue[color] = True

    while queue:  # until empty queue
        color = queue.pop()
        in_queue[color] = False

        target = color_class.get(color).head  # get corresponding color class

        counter = defaultdict(int)  # map vertex to occurrence count
        incoming_states = defaultdict(set)  # map color to set of vertices

        while target is not None:  # loop through color class

            for neighbour in target.data.neighbours:
                counter[neighbour] += 1
                incoming_states[coloring.get(neighbour)].add(neighbour)

            target = target.next

        for incoming_color in incoming_states:
            vertices_by_count = defaultdict(list)  # map occurrence count to vertices

            for state in incoming_states.get(incoming_color):  # make partitions
                count = counter.get(state)
                vertices_by_count[str(count)].append(state)

            for partition in vertices_by_count.values():

                if len(partition) < color_class.get(incoming_color).length:  # check if splittable
                    new_color = max_color + 1
                    max_color += 1

                    for element in partition:  # update color
                        node = pointer.get(element)
                        color_class.get(incoming_color).delete(node)
                        color_class[new_color].insert(node)
                        coloring[element] = element.colornum = new_color

                    # update queue
                    if in_queue.get(incoming_color):
                        queue.appendleft(new_color)
                        in_queue[new_color] = True
                    else:
                        if len(partition) < color_class[incoming_color].length:  # add color of smallest partition
                            queue.appendleft(new_color)
                            in_queue[new_color] = True
                        else:
                            queue.appendleft(int(incoming_color))
                            in_queue[incoming_color] = True

    return coloring
