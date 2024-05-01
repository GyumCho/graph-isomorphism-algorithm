from time import time
from graph_io import load_graph
from branching import count_automorphisms

graphs = [
    "Test/basicGI1.grl",
    "Test/basicGI2.grl",
    "Test/basicGI3.grl",
]

start = time()

for file in graphs:
    inter = time()
    print(file)
    print("Sets of isomorphic graphs:")

    with open(file) as f:
        g = load_graph(f, read_list=True)

    considered = [False] * len(g[0])
    for m in range(0, len(g[0]) - 1):
        if considered[m]:
            continue

        considered[m] = True
        temp = [m]
        num = 0

        for n in range(m + 1, len(g[0])):
            if considered[n]:
                continue

            result = count_automorphisms(g[0][m], g[0][n], [], [], False)

            if result != 0:
                considered[n] = True
                temp.append(n)

        print(temp)

    print("Time:", time() - inter)
    print()

print("Total time:", time() - start)
