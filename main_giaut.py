from time import time
from collections import deque
from graph_io import load_graph
from branching import count_automorphisms
from automorphism import generate_automorphisms, order_computation

graphs = [
    # "Test/basicGIAut1.grl",
    "Sample/BranchingSample/bigtrees1.grl",
]

start = time()

for file in graphs:
    inter = time()
    print(file)
    print("Sets of isomorphic graphs:", "Number of automorphisms:", sep='\t')

    with open(file) as f:
        g = load_graph(f, read_list=True)

    with open(file) as f:
        h = load_graph(f, read_list=True)

    considered = [False] * len(g[0])
    for m in range(0, len(g[0]) - 1):
        if considered[m]:
            continue

        considered[m] = True
        temp = [m]
        output = 0

        for n in range(m + 1, len(g[0])):
            if considered[n]:
                continue

            result = count_automorphisms(g[0][m], g[0][n], [], [], False)

            if result != 0:
                considered[n] = True
                temp.append(n)

        # ps = []
        # trivial = deque()
        # generate_automorphisms(g[0][temp[0]], h[0][temp[0]], [], [], trivial, ps, True)
        # output = order_computation(ps)
        output = count_automorphisms(g[0][temp[0]], h[0][temp[0]], [], [], True)
        print(temp, output, sep='\t\t\t\t')

    print("Time:", time() - inter)
    print()

print("Total time:", time() - start)
