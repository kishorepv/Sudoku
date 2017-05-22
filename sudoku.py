
import copy
from strategies import *
from utils import *
import sys
import argparse

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


def test_hidden_xs(values):
    values_copy=copy.deepcopy(values)
    values=hidden_twins(values)
    values_copy=hidden_xs(values_copy, 2)
    assert(values==values_copy)

def search(values):
    """
        DFS search over the simplified sudoku solution search space
    """
    strategies=[eliminate, only_choice, naked_twins, sub_group,hidden_twins]
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

def main(puzzle):
    """
        Solves and display puzzle solution.
    """
    problem=dict(zip(all_positions(), puzzle))
    solution=solve(puzzle)
    if solution:
        display_slowmo(problem, solution)
    else:
        print("The problem has no solution.")

def validate_input(inp):
    """
        Validates the input string
    """
    if len(inp)==81 and all([c in ".123456789" for c in inp]):
        return True
    else:
        return False


if __name__ =="__main__":
    parser=argparse.ArgumentParser(description="A Sudoku solver.")
    parser.add_argument("-p","--puzzle", dest="puzzle", help="Problem as a 64 character string with '.' for empty values")
    results=parser.parse_args()
    if validate_input(results.puzzle):
        main(results.puzzle)
    else:
        print("\nError: Invalid value for argument -p/--puzzle\n")
    # solve a sample problem
    #puzzles,solutions=problems()
    #puzzle=puzzles[0]
    #main(puzzle)
