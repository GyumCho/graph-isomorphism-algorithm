"""
Main program for the graph isomorphism and count automorphism problems.
"""
# Dario Capitani - s2754194
# Gyum Cho - s2113201
# Junseo Kim - s2648687

from solve import solve_gi, solve_aut

if __name__ == "__main__":

    while True:
        file_name = input("File: ")
        if file_name == "":
            break
        problem_type = input("Type [gi/aut/giaut]: ")
        if problem_type == "":
            break
        if problem_type != "gi" and problem_type != "aut" and problem_type != "giaut":
            continue
        print()
        try:
            ext = file_name.split(".")[1]
            if problem_type == "giaut" and ext == "grl":
                solve_gi(file_name, True)
            elif problem_type == "gi" and ext == "grl":
                solve_gi(file_name, False)
            elif problem_type == "aut":
                if ext == "gr":
                    solve_aut(file_name, False)
                elif ext == "grl":
                    solve_aut(file_name, True)
        except FileNotFoundError as error:
            pass
