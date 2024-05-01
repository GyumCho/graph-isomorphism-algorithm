"""
Module for solving the graph isomorphism and count automorphism problems.
"""
# Dario Capitani - s2754194
# Gyum Cho - s2113201
# Junseo Kim - s2648687

from time import time
from collections import deque
from graph_io import get_graph
from branching import count_automorphisms
from automorphism import generate_automorphisms, order_computation


def solve_aut(file, multi):
    """
    Solve the count automorphism problem.
    :param file: Path of the instance
    :param multi: True to solve for a list of graphs
    """
    start = time()
    g = get_graph(file, multi)
    h = get_graph(file, multi)
    size = len(g) if multi else 1

    print(file)
    print("Graph:", "Number of automorphisms:", sep='\t')

    for m in range(size):
        ps = []
        trivial = deque()
        if multi:
            generate_automorphisms(g[m], h[m], [], [], trivial, ps, True)
        else:
            generate_automorphisms(g, h, [], [], trivial, ps, True)
        result = order_computation(ps)
        print(m, result, sep='\t')

    print("Time:", time() - start, '\n')


def solve_gi(file, aut):
    """
    Solve the graph isomorphism problem.
    :param file: Path of the instance
    :param aut: True to also solve the automorphism problem
    """
    start = time()
    g = get_graph(file, True)
    h = None

    print(file)

    if aut:
        h = get_graph(file, True)
        print("Sets of isomorphic graphs:", "Number of automorphisms:", sep='\t')
    else:
        print("Sets of isomorphic graphs:")

    considered = [False] * len(g)
    for m in range(0, len(g) - 1):
        if considered[m]:
            continue
        considered[m] = True
        temp = [m]

        for n in range(m + 1, len(g)):
            if considered[n]:
                continue
            result = count_automorphisms(g[m], g[n], [], [], False)
            if result != 0:
                considered[n] = True
                temp.append(n)

        if aut:
            ps = []
            trivial = deque()
            generate_automorphisms(g[temp[0]], h[temp[0]], [], [], trivial, ps, True)
            output = order_computation(ps)
            print(temp, output, sep='\t\t\t')
        else:
            print(temp)

    print("Time:", time() - start, '\n')
