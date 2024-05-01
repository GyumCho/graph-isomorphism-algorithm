"""
DELIVERY SESSION
"""
# Dario Capitani - s2754194
# Gyum Cho - s2113201
# Junseo Kim - s2648687

from os import listdir
from os.path import join
from time import time
from solve import solve_gi, solve_aut

if __name__ == "__main__":

    path = input("Folder: ")
    print()
    files = listdir(path)

    start = time()

    for f in files:
        if "GIAut" in f:
            solve_gi(join(path, f), True)
        elif "GI" in f:
            solve_gi(join(path, f), False)
        elif "Aut" in f:
            ext = f.split(".")[1]
            if ext == "gr":
                solve_aut(join(path, f), False)
            elif ext == "grl":
                solve_aut(join(path, f), True)

    print("Total time:", time() - start)
