'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = kenken_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the KenKen puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only 
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only n-ary 
      all-different constraints for both the row and column constraints. 

3. kenken_csp_model (worth 20/100 marks) 
    - A model built using your choice of (1) binary binary not-equal, or (2) 
      n-ary all-different constraints for the grid.
    - Together with KenKen cage constraints.

'''
from cspbase import *
import itertools as it
import numpy as np
from copy import deepcopy

def binary_ne_grid(kenken_grid):
    # TODO! IMPLEMENT THIS!
    n = kenken_grid[0][0]
    const = []
    
    var = {}
    for row in range(1,n+1):
        for col in range(1,n+1):
            var_r_c = Variable('var'+str(row)+str(col),range(1,n+1))
            var['var'+str(row)+str(col)] = var_r_c
    
        
    #row constraints
    for row in range(1,n+1):
        for j in range(1,n+1):
            for k in range(j+1,n+1):
                c = Constraint('constraint'+str(row)+str(j)+'-'+str(row)+str(k),(var['var'+str(row)+str(j)],var['var'+str(row)+str(k)]))
                dom = list(range(1,n+1))
                sat_t = tuple(q for q in it.permutations(dom,2) if q[0] != q[1])
                c.add_satisfying_tuples(sat_t)
                const.append(c)
    
    #col constraints
    for col in range(1,n+1):
        for j in range(1,n+1):
            for k in range(j+1,n+1):
                c = Constraint('constraint'+str(j)+str(col)+'-'+str(k)+str(col),(var['var'+str(j)+str(col)],var['var'+str(k)+str(col)]))
                dom = list(range(1,n+1))
                sat_t = tuple(q for q in it.permutations(dom,2) if q[0] != q[1])
                c.add_satisfying_tuples(sat_t)
                const.append(c)

    csp = CSP('binary_grid',list(var.values()))
    const_list = const
    for i in range(len(const)):
        csp.add_constraint(const[i])
    
    var_list = list(var.values())
    var_list_organized = []
    #organize var variables
    cnt = 0
    for i in range(0,n):
        row = []
        for j in range(0,n):
            row.append(var_list[cnt])
            cnt += 1
        var_list_organized.append(row)
    
    
    return csp,var_list_organized


def nary_ad_grid(kenken_grid):
    # TODO! IMPLEMENT THIS!

    n = kenken_grid[0][0]
    const = []
    
    var = {}
    for row in range(1,n+1):
        for col in range(1,n+1):
            var_r_c = Variable('var'+str(row)+str(col),range(1,n+1))
            var['var'+str(row)+str(col)] = var_r_c
    
        
    #row constraint
    for row in range(1,n+1):
        var_list = []
        for j in range(1,n+1):
            var_list.append(var['var'+str(row)+str(j)])
        c = Constraint('constraint_row_'+str(row),tuple(var_list))
        sat_t = []
        dom = list(range(1,n+1))
        sat_t = tuple(q for q in it.permutations(dom,2) if q[0] != q[1])
        c.add_satisfying_tuples(sat_t)
        const.append(c)
    
    #col constraints
    for col in range(1,n+1):
        var_list = []
        for j in range(1,n+1):
            var_list.append(var['var'+str(j)+str(col)])
        c = Constraint('constraint_col_'+str(col),tuple(var_list))
        dom = list(range(1,n+1))
        sat_t = tuple(q for q in it.permutations(dom,2) if q[0] != q[1])
        c.add_satisfying_tuples(sat_t)
        const.append(c)
    
    csp = CSP('nary_grid',list(var.values()))
    const_list = const
    for i in range(len(const)):
        csp.add_constraint(const[i])
    
    var_list = list(var.values())
    var_list_organized = []
    #organize var variables
    cnt = 0
    for i in range(0,n):
        row = []
        for j in range(0,n):
            row.append(var_list[cnt])
            cnt += 1
        var_list_organized.append(row)
    
    
    return csp,var_list_organized
    

def kenken_csp_model(kenken_grid):
    # TODO! IMPLEMENT THIS!
    
    
    #make the binary constraints
    n = kenken_grid[0][0]
    const = []
    
    var = {}
    for row in range(1,n+1):
        for col in range(1,n+1):
            var_r_c = Variable('var'+str(row)+str(col),range(1,n+1))
            var['var'+str(row)+str(col)] = var_r_c
    
        
    #row constraints
    for row in range(1,n+1):
        for j in range(1,n+1):
            for k in range(j+1,n+1):
                c = Constraint('constraint'+str(row)+str(j)+'-'+str(row)+str(k),(var['var'+str(row)+str(j)],var['var'+str(row)+str(k)]))
                dom = list(range(1,n+1))
                sat_t = tuple(q for q in it.permutations(dom,2) if q[0] != q[1])
                c.add_satisfying_tuples(sat_t)
                const.append(c)
    
    #col constraints
    for col in range(1,n+1):
        for j in range(1,n+1):
            for k in range(j+1,n+1):
                c = Constraint('constraint'+str(j)+str(col)+'-'+str(k)+str(col),(var['var'+str(j)+str(col)],var['var'+str(k)+str(col)]))
                dom = list(range(1,n+1))
                sat_t = tuple(q for q in it.permutations(dom,2) if q[0] != q[1])
                c.add_satisfying_tuples(sat_t)
                const.append(c)

    grid = deepcopy(kenken_grid)
    
    ##add cage constraints
    grid.pop(0)
    i = 0
    for cage in grid:
        var_list = []
        if len(cage) == 2:
            target = cage.pop(-1)
            for cell in cage:
                row = int(cell/10)
                col = int(cell%10)                        
                var_list.append(var['var'+str(row)+str(col)])                            
            c = Constraint('constraint_cage_'+str(i),var_list)
            sat_tup = ((target,),)
            c.add_satisfying_tuples(sat_tup)
        else:
            operation = cage.pop(-1)
            target = cage.pop(-1)
            if (operation == 0):        #add
                for cell in cage:
                    row = int(cell/10)
                    col = int(cell%10)
                    var_list.append(var['var'+str(row)+str(col)])
                dom = range(1,n+1)
                c = Constraint('constraint_cage_'+str(i),tuple(var_list))
                sat_tup = tuple(q for q in it.product(dom,repeat=len(var_list)) if sum(q) == target)
                sat_tup_all = []
                for t in sat_tup:
                    sat_tup_all.extend([q for q in it.permutations(t)])
                c.add_satisfying_tuples(sat_tup_all)
            elif(operation == 1):       #subtract
                for cell in cage:
                    row = int(cell/10)
                    col = int(cell%10)
                    var_list.append(var['var'+str(row)+str(col)])
                dom = range(1,n+1)
                c = Constraint('constraint_cage_'+str(i),tuple(var_list))
                sat_tup = tuple(q for q in it.product(dom,repeat = len(var_list)) if q[0] - sum(q[1:]) == target)
                sat_tup_all = []
                for t in sat_tup:
                    sat_tup_all.extend([q for q in it.permutations(t)])
                c.add_satisfying_tuples(sat_tup_all)
            elif(operation == 2):       #division
                for cell in cage:
                    row = int(cell/10)
                    col = int(cell%10)
                    var_list.append(var['var'+str(row)+str(col)])
                dom = range(1,n+1)
                c = Constraint('constraint_cage_'+str(i),tuple(var_list))
                sat_tup = [q for q in it.product(dom,repeat = len(var_list)) if q[0] / np.prod(q[1:]) == target]            #find one tuple for each, permute all the combinations
                sat_tup_all = []
                for t in sat_tup:
                    sat_tup_all.extend([q for q in it.permutations(t)])
                c.add_satisfying_tuples(sat_tup_all)
            elif(operation == 3):       #multiplication
                for cell in cage:
                    row = int(cell/10)
                    col = int(cell%10)
                    var_list.append(var['var'+str(row)+str(col)])
                dom = range(1,n+1)
                c = Constraint('constraint_cage_'+str(i),tuple(var_list))
                sat_tup = tuple(q for q in it.product(dom,repeat = len(var_list)) if np.prod(q) == target)
                sat_tup_all = []
                for t in sat_tup:
                    sat_tup_all.extend([q for q in it.permutations(t)])
                c.add_satisfying_tuples(sat_tup_all)
        i += 1
        const.append(c)
    
    csp = CSP('kenken_model',list(var.values()))
    const_list = const
    for i in range(len(const)):
        csp.add_constraint(const[i])

    var_list = list(var.values())
    var_list_organized = []
    #organize var variables
    cnt = 0
    for i in range(0,n):
        row = []
        for j in range(0,n):
            row.append(var_list[cnt])
            cnt += 1
        var_list_organized.append(row)
    
    
    return csp,var_list_organized