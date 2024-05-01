from time import time
from graph_io import load_graph
from refinement import refine, fast_refine
from branching import count_automorphisms

file = "Sample/FastRefinementSample/threepaths1280.gr"
print(file)

total = time()

with open(file) as f:
    g = load_graph(f)

with open(file) as f:
    h = load_graph(f)

# count_automorphisms(g, h, [], [], False, False)

refine([g])
# fast_refine([g])

print("Total time:", time() - total)
