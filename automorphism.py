"""
Module for working with automorphism groups.
"""
# Dario Capitani - s2754194
# Gyum Cho - s2113201
# Junseo Kim - s2648687

from collections import defaultdict, deque
from graph import Graph
from permv2 import permutation
from basicpermutationgroup import Orbit, Stabilizer, FindNonTrivialOrbit
from refinement import fast_refine


def generate_automorphisms(g: Graph, h: Graph, d: list, i: list, trivial: deque, ps: list, from_trivial: bool) -> bool:
    """
    Computes the generating set of the automorphism group of a graph.
    :param g: Selected graph
    :param h: Copy of selected graph
    :param d: Sequence of vertices of g
    :param i: Sequence of vertices of h
    :param trivial: Stack containing vertices chosen after a trivial mapping
    :param ps: Generating set containing the permutations of discrete colorings
    :param from_trivial: True if the previous mapping was trivial
    :return: True if the given mapping results in an isomorphism or all mappings have been considered
    """
    initial = {}  # get initial mapping based on d and i
    for index in range(len(d)):
        initial[d[index]] = index + 1
        initial[i[index]] = index + 1

    coloring = fast_refine([g, h], initial)

    g_label_unsorted = list(map(lambda a: coloring.get(a), g.vertices))
    h_label_unsorted = list(map(lambda a: coloring.get(a), h.vertices))
    g_label = sorted(g_label_unsorted)
    h_label = sorted(h_label_unsorted)

    max_color = 0
    g_color_vertex = defaultdict(list)
    h_color_vertex = defaultdict(list)
    for vertex, color in coloring.items():  # get color classes
        if vertex in g.vertices:
            g_color_vertex[str(color)].append(vertex)
        else:
            h_color_vertex[str(color)].append(vertex)

        if color > max_color:
            max_color = color

    stable = g_label == h_label  # check stable
    if not stable:
        return False

    discrete = len(g_label) == len(set(g_label))  # check discrete
    if discrete:
        label_mapping = []
        for label in g_label_unsorted:
            label_mapping.append(h_label_unsorted.index(label))
        ps.append(permutation(n=len(g_label_unsorted), mapping=label_mapping))  # add to permutation set
        return True

    vertices = [v for v in g_color_vertex.values() if len(v) > 1]
    color = min(vertices, key=len)  # get the smallest color class
    v_in_g = color[0]  # vertex in g
    v_in_h = h.vertices[g.vertices.index(v_in_g)]  # corresponding vertex in h

    if from_trivial:  # if previous mapping was trivial
        trivial.append(v_in_g)

    while trivial:  # until trivial queue is empty

        for vertex in h_color_vertex.get(str(coloring.get(v_in_g))):
            success = generate_automorphisms(g, h, d + [v_in_g], i + [vertex], trivial, ps, vertex == v_in_h)

            if success and (not trivial or v_in_g != trivial[-1]):
                return True

        trivial.pop()
        return True

    return True


def order_computation(ps: list) -> int:
    """
    Compute the order of the automorphism group of a graph given its generating set.
    :param ps: Generating set containing the permutations of discrete colorings
    :return: Order of the automorphism group
    """
    if len(ps) == 0 or (len(ps) == 1 and ps[0].istrivial()):  # only trivial mapping in generating set
        return 1

    el = FindNonTrivialOrbit(ps)
    orbit = Orbit(ps, el)
    stabilizer = Stabilizer(ps, el)

    return len(orbit) * order_computation(stabilizer)
