'''
This file will contain different variable ordering heuristics to be used within
bt_search.

1. ord_dh(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the DH heuristic.
2. ord_mrv(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the MRV heuristic.
3. val_lcv(csp, var)
    - Takes in a CSP object (csp), and a Variable object (var)
    - Returns a list of all of var's potential values, ordered from best value 
      choice to worst value choice according to the LCV heuristic.

The heuristics can use the csp argument (CSP object) to get access to the 
variables and constraints of the problem. The assigned variables and values can 
be accessed via methods.
'''

import random
from copy import deepcopy

def ord_dh(csp):
    # TODO! IMPLEMENT THIS!
    remaining_vars = csp.get_all_unasgn_vars()
    max = None
    max_v = None
    for v in remaining_vars:
        size = len(csp.get_cons_with_var(v))
        if(max == None or max < size):
            max = size
            max_v = v
    return max_v

def ord_mrv(csp):
    # TODO! IMPLEMENT THIS!
    remaining_vars = csp.get_all_unasgn_vars()
    min = None
    min_v = None
    for v in remaining_vars:
        size = v.cur_domain_size()
        if(min == None or min > size):
            min = size
            min_v = v
    return min_v

def val_lcv(csp, var):
    # TODO! IMPLEMENT THIS!
    constraints = csp.get_cons_with_var(var)
    max = None
    max_d = None
    order = {}
    for d in var.cur_domain():
        var.assign(d)
        sum = 0
        for c in constraints:
            for v in c.get_unasgn_vars():
                for d2 in v.cur_domain():
                    if(c.has_support(v,d2)):
                        sum +=1
        var.unassign()
        order[d] = sum
        # if(max == None or max<sum):
        #     max = sum
        #     max_d = d
    
    ordered = sorted(order.items(), key=lambda x: x[1], reverse = True)
    ans = []
    for t in ordered:
        ans.append(t[0])
    
    return ans
