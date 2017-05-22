
# This program is a Sudoku puzzle solver.

### Code Files

* `sudoku.py` - Main script invoked by the user.
* `strategies.py` - Strategies used to reduce the search space of the solution.
                    The implemented strategies are:
                    1. Single Possibility Rule
                    2. Only Choice Rule
                    3. Naked Twins Elimination Rule
                    4. Sub-Group Exclusion Rule
                    5. Hidden Twins Elimination rule


* `utils.py` - Helper functions for computation and visualization.

### Usage

* $ python sudoku.py --puzzle 2.............62....1....7...6..8...3...9...7...6..4...4....8....52............42
* $ python sudoku.py --help
