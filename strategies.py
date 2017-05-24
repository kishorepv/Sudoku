import itertools
from utils import *

def naked_twins(values):
    """
        Eliminate non-possible entries using "Naked Twins elimination" rule.
    """
    #finds all boxes with two possible values
    pairs=[k for k,v in values.items() if len(v)==2]
    for k in pairs:
        vv=values[k]
        row_p,col_p,sq_p=get_repeat_peers(k)
        # if naked twins are found, twin values are removed from corresponding row/column and
        # from the 3x3 square peers if the naked twins are in the same 3x3 sub-square
        for peer_group in [row_p,col_p]:
            peer_vals=[values[peer] for peer in set(peer_group)-set([k])]
            if vv in peer_vals: # naked twins exist
                twin_index=peer_vals.index(vv)
                values=remove_naked_ns(peer_group,vv,values)
                if twin_index in sq_p:
                    values=remove_naked_ns(sq_p,vv,values)
    return values

def naked_triplets(puzzle):
    """
        Eliminate non-possible entries using "Naked Triplets elimination" rule.
    """
    puzzle=naked_n(puzzle,3)
    return puzzle


def naked_n(puzzle, n):
    """
        This is a generalization of the "Naked Twins Elimnation" rule.
        Elimnates naked singlets/twins/triplets/.../nonuplets (specified by 'n').
    """
    x=max(1,min(n,9))
    all_n_tuples=[pos for pos,val in puzzle.items() if len(val)==n]
    for pos in all_n_tuples:
        vn=puzzle[pos]
        row_p,col_p,sq_p=get_repeat_peers(pos)
        for peer_group in [row_p,col_p]:
            peer_values=[puzzle[k] for k in set(peer_group)-set([pos])]
            if peer_values.count(vn)==(n-1): # naked n exist
                naked_ns=[k for k in peer_group if puzzle[k]==vn]
                puzzle=remove_naked_ns(peer_group, vn, puzzle)
                if all([each_naked in sq_p for each_naked in naked_ns]):
                    puzzle=remove_naked_ns(sq_p, vn, puzzle)
    return puzzle



def eliminate(values):
    """
        Eliminates single-valued-box value from its peers' possible entries.
    """
    originals_k=[k for k in values.keys() if len(values[k])==1]
    for k in originals_k: # reduce for only the original singleton units
        v=values[k]
        peers=get_self_and_peers(k)
        for peer in peers:
            if v in values[peer] and peer!=k:
                values[peer]=values[peer].replace(v, '')
    return values

def single_possibility(puzzle):
    """
        Eliminates non-possible values by applying "Single Possibility" rule, which is achieved by 'eliminate' function.
    """

def only_choice(values):
    """
        Eliminates non-possible entries by applying "Only Choice" rule
    """
    for k in values.keys():
        if len(values[k])==1: continue
        repeat_peers=get_repeat_peers(k)
        vals=list()
        for peerlist in repeat_peers:
                vals.append(''.join([values[peer] for peer in peerlist]))
        for v in values[k]:
            if 1 in [val.count(v) for val in vals]:
                values[k]=v
                break
    return values

def sub_group(puzzle):
    """
        Row and column subgroup elimination by use of "Sub-group exclusion" rule.
    """
    #index==0 for row subgroups, and index==1 for column subgroups
    for index,XY in enumerate(zip(["ABCDEFGHI", "123456789"], [["123","456", "789"], ["ABC", "DEF", "GHI"]])):
        X,Y=XY
        for r in X:
            for cols in Y:
                first_pos=cross(r, cols)[0] if index==0 else cross(cols,r)[0]
                row_p,col_p,sq_p=get_repeat_peers(first_pos)
                _3r_p=cross(r, cols) if index==0 else cross(cols, r)
                _6r_p=(set(row_p)-set(_3r_p)) if index==0 else (set(col_p)-set(_3r_p))
                for k in _3r_p:
                    vv=puzzle[k]
                    if len(vv)>1:
                        for v in vv:
                            if v not in [__ for _ in _6r_p for __ in puzzle[_]]:
                                for p in sq_p:
                                    if (not p in _3r_p) and len(puzzle[p])>1 and v in puzzle[p]:
                                        puzzle[p]=puzzle[p].replace(v, '')
    return puzzle

def hidden_xs(puzzle, x):
    """
        This is a generalization of the "Hidden Twins exclusion" rule.
        Elimnates hidden singlets/twins/triplets/.../nonuplets (specified by 'x').
    """
    x=max(1,min(x,9))
    explored=list()
    for index,XY in enumerate(zip(["ABCDEFGHI","123456789"],["ABCDEFGHI","123456789"][::-1])):
        X,Y=XY
        for r in X:
            poss=cross(r, Y) if index==0 else cross(Y,r)
            # itertools.combinations is better, but itertools.permutations takes care of problems with puzzle.values() not sorted ascending
            all_1_x_perms_poss=[(''.join(t),pos) for pos in poss for i in [1,x] for t in itertools.combinations(puzzle[pos],i) if t]
            all_x_perms=[perm for perm,pos in all_1_x_perms_poss if len(perm)==x]
            all_1_perms=[perm for perm,pos in all_1_x_perms_poss if len(perm)==1]
            for unique_p in set(all_x_perms):
                outside=all([all_1_perms.count(c)==x for c in unique_p])
                if  outside and all_x_perms.count(unique_p)==x:
                    hidden_xs=[pos for perm,pos in all_1_x_perms_poss if perm==unique_p]
                    assert(len(hidden_xs)==x)
                    for pos in hidden_xs:
                        if pos in explored: break
                        explored.append(pos)
                        if len(puzzle[pos])>x: puzzle[pos]=''.join(sorted(unique_p))
    return puzzle

def hidden_twins(puzzle):
    """
        Elimnates non-possible entries by applying "Hidden Twins exclusion" rule.
    """
    explored=list()
    for index,XY in enumerate(zip(["ABCDEFGHI","123456789"],["ABCDEFGHI","123456789"][::-1])):
        X,Y=XY
        for r in X:
            poss=cross(r, Y) if index==0 else cross(Y,r)
            # itertools.combinations is better, but itertools.permutations takes care of problems with puzzle.values() not sorted ascending
            all_1_2_perms_poss=[(''.join(x),pos) for pos in poss for i in range(1,3) for x in itertools.permutations(puzzle[pos],i) if x]
            all_2_perms=[perm for perm,pos in all_1_2_perms_poss if len(perm)==2]
            all_1_perms=[perm for perm,pos in all_1_2_perms_poss if len(perm)==1]
            for unique_p in set(all_2_perms):
                a,b=unique_p
                if  all_1_perms.count(a)==2 and all_1_perms.count(b)==2 and all_2_perms.count(unique_p)==2:
                    hidden_twins=[pos for perm,pos in all_1_2_perms_poss if perm==unique_p]
                    assert(len(hidden_twins)==2)
                    for twin in hidden_twins:
                        if twin in explored: break
                        explored.append(twin)
                        if len(puzzle[twin])>2: puzzle[twin]=''.join(sorted(unique_p))
    return puzzle
