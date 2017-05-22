import os
import time

def cross(X,Y):
    """
        Returns the Cartesian (cross) product of 'X' and 'Y'
    """
    return [x+y for x in X for y in Y]

def all_positions():
    """
        Returns all sudoku puzzle positions
    """
    return cross("ABCDEFGHI", "123456789")

def grid_values(grid):
    """
        Convert grid string into dictionary with "123456789" value for empty entries ('.' entries).
    """
    return {pos:c if c!='.' else "123456789" for pos,c in zip(cross("ABCDEFGHI", "123456789"),grid)}

def to_string(puzzle):
    """
        Converts a grid (output of 'grid_values' function to  string of puzzle entries from left to right, row-wise.
    """
    return ''.join([puzzle[pos] for pos in all_positions()])

def is_diagonal(values):
    """
        Checks if diagonal contraint is satisfied for puzzle
    """
    p_diagonal_vals=[z for x,y in zip("ABCDEFGHI", "123456789") for z in values[x+y]]
    o_diagonal_vals=[z for x,y in zip("ABCDEFGHI", "123456789"[::-1]) for z in values[x+y]]
    return set("123456789")==set(p_diagonal_vals)==set(o_diagonal_vals)


def get_repeat_peers(pos):
    """
        Returns row peers, column peers and box peers (10 each, including self)
    """
    row,col=pos
    row_peers=cross(row, "123456789")
    col_peers=cross("ABCDEFGHI", col)
    rows="ABCDEFGHI"
    sq_peers=cross( ''.join([rows[i+3*(int(rows.index(row)/3))] for i in range(0,3)]), ''.join([str(i+3*int((int(col)-1)/3)) for i in range(1,3+1)]))
    return [row_peers, col_peers, sq_peers]

def get_self_and_peers(pos):
    """
        Returns the 20 peers of position 'pos' along with 'pos'
    """
    row,col=pos
    # row peers with self
    row_peers=cross(row, "123456789")
    #column peers with self
    col_peers=cross("ABCDEFGHI", col)
    rows="ABCDEFGHI"
    #3x3 sub square peers with self
    sq_peers=cross( ''.join([rows[i+3*(int(rows.index(row)/3))] for i in range(0,3)]), ''.join([str(i+3*int((int(col)-1)/3)) for i in range(1,3+1)]))
    #return 20 peers + self
    return set(row_peers+col_peers+sq_peers)

def get_peers(pos):
    """
        Returns the unique 20 peers of a given box in the puzzle
    """
    return get_self_and_peers()-set([pos])

def remove_pair(peer_group,vv,values):
    """
        Removes any value of 'vv' from the puzzle (values) in all the 'peer_group' boxss
    """
    for  peer in peer_group:
        if values[peer]!=vv:
            for v in vv:
                if v in values[peer]:
                    values[peer]=values[peer].replace(v, '')
    return values


def create_row(row):
    """
        Creates a string for dipplaying one row of sudoko puzzle
    """
    r1="|   |   |   |"
    r2=" %s |"
    r3="|___|___|___|"
    R1=(r1*3)
    R3=(r3*3)
    R2="|"
    for index,box_val in enumerate(row,1):
        R2=R2+r2 %(box_val)+('' if index%3!=0 else '|')
    return "\n".join([R1,R2[:-1],R3])

def display(values):
    """
        Display the puzzle 'values' as a 2-D grid.
    """
    rows=list()
    for r in "ABCDEFGHI":
        rows.append(create_row([values[k] for k in cross(r,"123456789")]))
    c=3
    rows=['\n'.join(rows[r*c:(r+1)*c]) for r in range(3)]
    grid_string=(('\n'+(' '.join([' '.join(['']+['_'*3]*3)]*3))+'\n').join(['']+rows))+'\n'
    print(grid_string)
    return grid_string

def display_slowmo(puzzle, solution, delay=0.02):
    """
        Slow motion display of puzzle solution.
    """
    header_str=" SUDOKU SOLVER ".ljust(15+10, ' ').rjust(15+10*2, ' ')
    header_str="\n\n"+header_str+"\n"
    os.system("clear")
    #time.sleep(1)
    print(header_str)
    print("Problem: ")
    display(puzzle)
    time.sleep(2)
    for pos in all_positions():
        if puzzle[pos]=='.':
            puzzle[pos]=solution[pos]
            os.system("clear")
            print(header_str)
            print("Solution: ")
            display(puzzle)
            time.sleep(delay)
    print("\n")


def problems():
    """
        Sample puzzles with solutions.
    """
    puzzles=["723...1596..3.2..88...1...2.7.654.2...42.73...5.931.4.5...7...34..1.3..6932...714",
             "2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3", #has valid diagonal sudoku solution
             "...5.3.9.....6715..54921.3.84937.2..13.....79.75.194.3...65432..6.7329...2.198...", #has hidden twins
             ]
    solutions=["723846159615392478849715632378654921194287365256931847561479283487123596932568714",
               "239874156754316298681952374476128539312495687598637412143769825965283741827541963",
               "216583794398467152754921836849376215132845679675219483987654321561732948423198567",
               ]
    return puzzles,solutions
