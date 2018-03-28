'''
This file will contain different constraint propagators to be used within 
bt_search.

---
A propagator is a function with the following header
    propagator(csp, newly_instantiated_variable=None)

csp is a CSP object---the propagator can use this to get access to the variables 
and constraints of the problem. The assigned variables can be accessed via 
methods, the values assigned can also be accessed.

newly_instantiated_variable is an optional argument. SEE ``PROCESSING REQUIRED''
if newly_instantiated_variable is not None:
    then newly_instantiated_variable is the most
    recently assigned variable of the search.
else:
    propagator is called before any assignments are made
    in which case it must decide what processing to do
    prior to any variables being assigned. 

The propagator returns True/False and a list of (Variable, Value) pairs, like so
    (True/False, [(Variable, Value), (Variable, Value) ...]

Propagators will return False if they detect a dead-end. In this case, bt_search 
will backtrack. Propagators will return true if we can continue.

The list of variable value pairs are all of the values that the propagator 
pruned (using the variable's prune_value method). bt_search NEEDS to know this 
in order to correctly restore these values when it undoes a variable assignment.

Propagators SHOULD NOT prune a value that has already been pruned! Nor should 
they prune a value twice.

---

PROCESSING REQUIRED:
When a propagator is called with newly_instantiated_variable = None:

1. For plain backtracking (where we only check fully instantiated constraints)
we do nothing...return true, []

2. For FC (where we only check constraints with one remaining 
variable) we look for unary constraints of the csp (constraints whose scope 
contains only one variable) and we forward_check these constraints.

3. For GAC we initialize the GAC queue with all constaints of the csp.

When a propagator is called with newly_instantiated_variable = a variable V

1. For plain backtracking we check all constraints with V (see csp method
get_cons_with_var) that are fully assigned.

2. For forward checking we forward check all constraints with V that have one 
unassigned variable left

3. For GAC we initialize the GAC queue with all constraints containing V.

'''

def prop_BT(csp, newVar=None):
    '''
    Do plain backtracking propagation. That is, do no propagation at all. Just 
    check fully instantiated constraints.
    '''
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    # TODO! IMPLEMENT THIS!
    
    if not newVar:
        const_list = csp.get_all_cons()                         #list of all constraints
        prunes = []
        for constraint in const_list:
            if constraint.get_n_unasgn() != 1:                #not a unary constraint
                continue
            if (constraint.get_n_unasgn() > 0):                  #if there are unassigned variables left
                unassigned_var = constraint.get_unasgn_vars()[0] #get the only unassigned variable
                for d in unassigned_var.cur_domain():            #exhaust it's domain by assigning and checking
                    unassigned_var.assign(d)
                    vals = []
                    vars = constraint.get_scope()
                    for var in vars:
                        vals.append(var.get_assigned_value())
                    if not constraint.check(vals):              #this assignment falsified constraint
                        unassigned_var.unassign()               #unassign it
                        unassigned_var.prune_value(d)           #prune it
                        prunes.append((unassigned_var,d))
                    else:                                       #assignment actually works!
                        unassigned_var.unassign()               #unassign it, but don't prune it
    
                if unassigned_var.cur_domain_size() == 0:       #DWO
                    return False, prunes
                else:                                           #no DWO, can proceed
                    pass
                
        return True,prunes
    else:
        const_list = csp.get_cons_with_var(newVar)  #list of constraints that have newVar in them
        prunes = []
        for constraint in const_list:
            if constraint.get_n_unasgn() != 1:                 #not a unary constraint
                continue
            if (constraint.get_n_unasgn() > 0):                #if there are unassigned variables left
                unassigned_var = constraint.get_unasgn_vars()[0] #get the only unassigned variable
                for d in unassigned_var.cur_domain():           #exhaust it's domain by assigning and checking
                    unassigned_var.assign(d)
                    vals = []
                    vars = constraint.get_scope()
                    for var in vars:
                        vals.append(var.get_assigned_value())
                    if not constraint.check(vals):              #this assignment falsified constraint
                        unassigned_var.unassign()               #unassign it
                        unassigned_var.prune_value(d)           #prune it
                        prunes.append((unassigned_var,d))
                    else:                                       #assignment actually works!
                        unassigned_var.unassign()               #unassign it, but don't prune it
    
                if unassigned_var.cur_domain_size() == 0:         #DWO
                    return False, prunes
                else:                                           #no DWO, can proceed
                    pass
                
        return True,prunes

def prop_GAC(csp, newVar=None):
    '''
    Do GAC propagation. If newVar is None we do initial GAC enforce processing 
    all constraints. Otherwise we do GAC enforce with constraints containing 
    newVar on GAC Queue.
    '''
    # TODO! IMPLEMENT THIS!
    if not newVar:
        const_list = csp.get_all_cons()                         #list of all constraints
        prunes = []

        while len(const_list) != 0:                 #gac queue is not empty
            c = const_list.pop(0)                   #first constraint to examine
            for v in c.get_scope():                 #examine all the variables in constraint
                for d in v.cur_domain():            #examine all the values of the variable
                    if not c.has_support(v,d):      #if assignment does not have any support
                        v.prune_value(d)            #prune the value
                        prunes.append((v,d))
                        if v.cur_domain_size() == 0:    #if domain becomes empty -> DWO
                            const_list = [] 
                            return False,prunes
                        else:                       #else, for every prune, add the constraints that have v to the queue
                            const_have_v_in_scope = csp.get_cons_with_var(v)    #constraints that have v
                            for c_have_v in const_have_v_in_scope:
                                if c_have_v not in const_list and c_have_v != c:
                                    const_list.append(c_have_v)                     #add to queue
        return True, prunes
        
    else:

        const_list = csp.get_cons_with_var(newVar)  #list of constraints that have newVar in them
        prunes = []
        while len(const_list) != 0:                 #gac queue is not empty
            c = const_list.pop(0)                   #first constraint to examine
            for v in c.get_scope():                 #examine all the variables in constraint
                for d in v.cur_domain():            #examine all the values of the variable
                    if not c.has_support(v,d):      #if assignment does not have any support
                        v.prune_value(d)            #prune the value
                        prunes.append((v,d))
                        if v.cur_domain_size() == 0:    #if domain becomes empty -> DWO
                            const_list = [] 
                            return False,prunes
                        else:                       #else, for every prune, add the constraints that have v to the queue
                            const_have_v_in_scope = csp.get_cons_with_var(v)    #constraints that have v
                            for c_have_v in const_have_v_in_scope:
                                if c_have_v not in const_list and c_have_v != c:
                                    const_list.append(c_have_v)                     #add to queue
        return True, prunes