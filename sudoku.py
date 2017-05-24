from strategies import *
from utils import *

import sys
import argparse
import copy

def reduce_puzzle(values, strategies):
    """
        Apply strategies (from strategies.py) to repeatedly reduce the puzzle search space
    """
    stalled = False
    while not stalled:
        solved_values_before = len([k for k in values.keys() if len(values[k])==1])
        for strategy in strategies:
            values=strategy(values)
        # diagonal constraint check
        #if not is_diagonal(values):
        #    return False
        # hidden triplets elimnation
        #values=hidden_xs(values,3)
        solved_values_after = len([k for k in values.keys() if len(values[k])==1])
        stalled = solved_values_before == solved_values_after
        # sanity check
        if len([x for x in values.keys() if len(values[x])==0]):
            return False
    return values

def search(values):
    """
        DFS search over the simplified sudoku solution search space
    """
    strategies=[eliminate, only_choice, sub_group,hidden_twins, naked_twins,]# naked_triplets]
    values=reduce_puzzle(values, strategies)
    if values is False:
        return False
    boxes=cross("ABCDEFGHI", "123456789")
    if len([1 for k in values.keys() if len(values[k])==1])==81: return values #solved
    vals_len,k=min([(len(vals),k) for k,vals in values.items() if len(vals)>1])
    for v in values[k]:
        values2=values.copy()
        values2[k]=v
        trial=search(values2)
        if trial:
            return trial


def solve(grid):
    """
        Solves a Sudoku puzzle.
    """
    values=grid_values(grid)
    values=search(values)
    return values if values else False

def main(puzzle, minimal=False):
    """
        Solves and display puzzle solution.
    """
    problem=dict(zip(all_positions(), puzzle))
    solution=solve(puzzle)
    if solution:
        if not minimal: display_slowmo(problem, solution)
        return to_string(solution)
    else:
        print("The problem has no solution.")
        return False

def validate_input(inp):
    """
        Validates the input string
    """
    if len(inp)==81 and all([c in ".123456789" for c in inp]):
        return True
    else:
        print("Invalid puzzle problem.\n")
        return False


if __name__ =="__main__":
    parser=argparse.ArgumentParser(description="A Sudoku solver.")
    parser.add_argument("-p","--puzzle", dest="puzzle", help="Puzzle as a 64 character string with '.' for empty values")
    parser.add_argument("-f","--file", dest="filepath", help="File containing one puzzle string per line. Outputs to 'solutions.txt' puzzle string folowed by solution string.")
    parser.add_argument("-m","--minimal", dest="minimal", action="store_true", default=False, help="Disables slowmotion display of solution")
    results=parser.parse_args()
    if results.filepath:
        solutions=list()
        try:
            with open(results.filepath, 'r') as f:
                for puzzle_string in f:
                    puzzle_string=puzzle_string.strip()
                    solutions.append(puzzle_string)
                    if validate_input(puzzle_string):
                        solution=main(puzzle_string, results.minimal)
                        if solution:
                            solutions.append(solution)
                        else:
                            solutions.append("No solution.")
                    else:
                        solutions.append("Invalid puzzle string.")

            solutions=[solution.strip()+"\n" for solution in solutions]
            with open("solutions.txt", 'w') as f:
                f.writelines(solutions)
        except IOError as ioe:
            print("Error while reading/writing to file.")
    elif results.puzzle and validate_input(results.puzzle):
        solution=main(results.puzzle, results.minimal)
        if solution:
            print("Solution string: %s\n" %(solution))
    else:
        print("\nFor help: $python sudoku.py --help\n")
    # solve a sample problem
    #puzzles,solutions=problems()
    #puzzle=puzzles[0]
    #main(puzzle)
