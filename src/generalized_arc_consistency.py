import itertools

def GAC(variables, domains, constraints):
    """
    Generalized arc consistency algorithm from the book 
    Artificial Inteligence: Foundations of computational agents
    Figure 4.3 p136

    Keyword arguments:
    variables -- a list of the variables
    domains -- a dictonary of domains for each variable. The variable is the key. The domain is the value.
    constraint -- a list of contraints. A constraint is a tuple consisting of the variables involved and a function

    returns a new set of reduced domains

    example usage:
    variables = ["A", "B", "C"]

    domains = {"A": [i for i in range(1,5)]),
               "B": [i for i in range(1,5)]),
               "C": [i for i in range(1,5)])
               }

    constraints = [(["A", "B"], lambda a, b: a < b),
                   (["B", "C"], lambda b, c: b < c)
    ]

    GAC(variables, domains, constraints)
    """

    #assign {<X,c>|c ∈ constraints and X ∈ scope(c)} to to_do
    to_do = []
    for constraint in constraints:
        for variable in constraint[0]:
            to_do.append((variable,constraint))
    
    def GAC2(variables, domains, constraints, to_do):
        processed_arcs = []
        while len(to_do) != 0:
            #select and remove <X,c> from to_do
            X_c = to_do.pop()

            X = X_c[0]
            constraint = X_c[1]

            #{Y_1,...Y_k} = scope(c\{X})
            scope_minus_X = [var for var in X_c[1][0] if var != X] 

            #ND = {x| x ∈ dom[X] and exists y_1 ∈ dom[Y_1]...y_k ∈ dom[Y_k] such that c(X=x Y_1=y_1,... Y_k = y_k)}
            ND = domains[X].copy()
            for x in domains[X]:
                var_list = [domains[var] if var != X else [x] for var in constraint[0]]
                var_comb = list(itertools.product(*var_list))
                if not any(map(constraint[1], *zip(*var_comb))):
                    ND.remove(x)
            

            #all of the previously consistent arcs that could, as a result of pruning X, 
            #have become inconsistent are placed back into the set to_do.
            #these are the arcs <Z,c'>, where c' is a constraint different from c that involves X, 
            #and Z is a variable involved in c' other than X
            if domains[X] != ND:
                for arc in processed_arcs:
                    #find all <Z,c'> and append them to to_do
                    if arc[0] != X_c[0] and arc[1] != X_c[1] and any(var in arc[1][0] for var in scope_minus_X):
                        to_do.append(arc)
                domains[X] = ND    
                
            processed_arcs.append(X_c) 

        return domains
    return GAC2(variables, domains, constraints, to_do)


if __name__ == '__main__':
    #Below is an example based on example 4.9 p.131
    variables = ["A", "B", "C", "D", "E"]
    domains = {"A": [i for i in range(1,5)],
               "B": [i for i in range(1,5)],
               "C": [i for i in range(1,5)],
               "D": [i for i in range(1,5)],
               "E": [i for i in range(1,5)],
               }
    
    constraints = [(["B"], lambda b: b != 3),
                   (["C"], lambda c: c != 2),
                   (["A", "B"], lambda a, b: a != b),
                   (["B", "C"], lambda b, c: b != c),
                   (["C", "D"], lambda c, d: c < d),
                   (["A", "D"], lambda a, d: a == d),
                   (["E", "A"], lambda e, a: e < a),
                   (["E", "B"], lambda e, b: e < b),
                   (["E", "C"], lambda e, c: e < c),
                   (["E", "D"], lambda e, d: e < d),
                   (["B", "D"], lambda b, d: b != d)
                ]


    print(GAC(variables, domains, constraints))