

class SearchPredicates:

    within = "within"
    without = "without"
    inside = "inside"
    outside = "outside"
    between = "between"

    eq = "eq"
    neq = "neq"
    lt = "lt"
    lte = "lte"
    gt = "gt"
    gte = "gte"

    containing = "containing"
    startingWith = "startingWith"
    endingWith = "endingWith"

    test = "test"

    _and = "and"
    _or = "or"
    _not = "not"

    @classmethod
    def keys(cls):
        return [v for k, v in cls.__dict__.items() 
                if type(v) == str and v not in ["__main__", "graph_search.constants"]]

class SearchTextPredicate(SearchPredicates):

    containing = "containing"
    endingWith = "endingWith"
    notContaining = "notContaining"
    notEndingWith = "notEndingWith"
    notStartingWith = "notStartingWith"
    startingWith = "startingWith"

    @classmethod
    def keys(cls):
        parent_keys = SearchPredicates.keys()
        return list(parent_keys + [v for k, v in cls.__dict__.items() 
                    if type(v) == str and v not in ["__main__", "graph_search.constants"]])

