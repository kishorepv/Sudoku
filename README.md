
## Sudoku puzzle solver.
![demo.gif](https://github.com/kishorepv/Sudoku/blob/master/demo.gif)

### Files

* `sudoku.py` - Main script invoked by the user.
* `strategies.py` - Strategies used to reduce the search space of the solution.  
  The implemented strategies are:  
   1. Single Possibility Rule  
   2. Only Choice Rule  
   3. Naked Twins Elimination Rule  
   4. Sub-Group Exclusion Rule  
   5. Hidden Twins Elimination Rule  
   6. Generalized version of "Hidden Twins Elimnation" rule to elimnate singlets/twins/.../nounplets

* `utils.py` - Helper functions for computation and visualization.
* `puzzles.txt` - Sample input file for batch solving
* `solutions.txt` - Sample output file after batch solving


### Usage
#### Solve a puzzle from cmdline
* $ `python sudoku.py --puzzle 2.............62....1....7...6..8...3...9...7...6..4...4....8....52............42`
#### Batch solve puzzles read from text file
* $ `python sudoku.py -f puzzles.txt`
#### Minimal output (-m) without slowmotion puzzle solving 
* $ `python sudoku.py -m --puzzle 2.............62....1....7...6..8...3...9...7...6..4...4....8....52............42`
#### Help
* $ `python sudoku.py --help`
