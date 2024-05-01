"""
Module for working with branching.
"""
# Dario Capitani - s2754194
# Gyum Cho - s2113201
# Junseo Kim - s2648687

from math import factorial, prod
from collections import defaultdict
from graph import Graph, Vertex
from refinement import refine, fast_refine


def count_automorphisms(g: Graph, h: Graph, d: list[Vertex], i: list[Vertex], count: bool, fast=True) -> int:
    """
    Count automorphisms of a pair of graphs. Either count just one or all automorphisms.
    :param g: First graph
    :param h: Second graph
    :param d: Sequence of vertices of g
    :param i: Sequence of vertices of h
    :param count: True to count all automorphisms
    :param fast: True to use fast color refinement
    :return: Number of automorphisms
    """
    alpha = {}  # make coloring A using D and I
    for index in range(len(d)):
        alpha[d[index]] = index + 1
        alpha[i[index]] = index + 1

    # get coloring B using A
    if fast:
        beta = fast_refine([g, h], alpha)
    else:
        beta = refine([g, h], alpha)

    g_colors = list(map(lambda b: beta.get(b), g.vertices))
    h_colors = list(map(lambda b: beta.get(b), h.vertices))

    g_colors.sort()
    h_colors.sort()

    if not g_colors == h_colors:  # check unbalanced
        return 0

    if len(set(g_colors)) == len(g_colors):  # check bijection
        return 1

    vertices_by_color = defaultdict(list)
    for vertex, color in beta.items():
        vertices_by_color[str(color)].append(vertex)

    vertices = [v for v in vertices_by_color.values() if len(v) > 2]

    color_class = max(vertices, key=len)  # get the largest color class

    for vg in color_class:
        if vg in g.vertices:  # for certain x of G in color class
            num = 0
            for vh in color_class:
                if vh in h.vertices:  # for all y of H in color class
                    num = num + count_automorphisms(g, h, d + [vg], i + [vh], count)
                    if not count and num > 0:
                        return 1  # finish if 1 automorphism is found
            return num


def detect_twins(g: Graph) -> int:
    """
    Detects true and false twins of a graph.
    :param g: Graph to analyze
    :return: Number of extra automorphisms
    """
    labeling = dict(zip(g.vertices, range(len(g.vertices))))
    mapping = {}

    for vertex in g.vertices:  # search for false twins
        neighbours = tuple(sorted(list(map(lambda a: labeling.get(a), vertex.neighbours))))

        if neighbours in mapping.keys():
            mapping[neighbours].append(vertex)
            g.del_vertex(vertex)
        else:
            mapping[neighbours] = [vertex]

    twins = [v for v in mapping.values() if len(v) >= 2]

    mapping.clear()

    for vertex in g.vertices:  # search for true twins
        neighbours = tuple(sorted(list(map(lambda a: labeling.get(a), vertex.neighbours + [vertex]))))

        if neighbours in mapping.keys():
            mapping[neighbours].append(vertex)
            g.del_vertex(vertex)
        else:
            mapping[neighbours] = [vertex]

    twins += [v for v in mapping.values() if len(v) >= 2]
    total = prod(list(map(lambda b: factorial(len(b)), twins)))

    return total - 1  # subtract the trivial automorphism
