from time import time
from collections import deque
from graph_io import load_graph
from branching import count_automorphisms
from automorphism import generate_automorphisms, order_computation

graphs = [
    # "Test/basicAut1.gr",
    # "Test/basicAut2.gr",
    "Sample/FastRefinementSample/threepaths1280.gr",
    # "Sample/BranchingSample/torus144.grl",
]

start = time()

for file in graphs:
    inter = time()
    print(file)
    print("Graph:", "Number of automorphisms:", sep='\t')

    if file.split(".")[1] == "gr":
        with open(file) as f:
            g = load_graph(f)

        with open(file) as f:
            h = load_graph(f)

        # ps = []
        # trivial = deque()
        # generate_automorphisms(g, h, [], [], trivial, ps, True)
        # result = order_computation(ps)
        result = count_automorphisms(g, h, [], [], True, False)
        print(0, result, sep='\t\t')

    else:
        with open(file) as f:
            g = load_graph(f, read_list=True)

        with open(file) as f:
            h = load_graph(f, read_list=True)

        for m in range(len(g[0])):
            # ps = []
            # trivial = deque()
            #
            # generate_automorphisms(g[0][m], h[0][m], [], [], trivial, ps, True)
            # result = order_computation(ps)
            result = count_automorphisms(g[0][m], h[0][m], [], [], True, False)
            print(m, result, sep='\t\t')

    print("Time:", time() - inter)
    print()

print("Total time:", time() - start)
