from gremlin_python.process.graph_traversal import GraphTraversal, GraphTraversalSource
from gremlin_python.process.traversal import P, TextP, Bytecode, Cardinality
from gremlin_python.process.graph_traversal import __ as AnonymousTraversal
import copy
from .type_defs import NodeFiltersConfigType, RelationshipFiltersConfigType, \
      PropertyFilterType, GraphTraversalConfigType
from .constants import SearchTextPredicate, SearchPredicates
import typing


class InvanaTraversal(GraphTraversal):

    def __init__(self, graph, traversal_strategies, bytecode):
        super(InvanaTraversal, self).__init__(graph, traversal_strategies, bytecode)


    def clone(self):
        return InvanaTraversal(self.graph, self.traversal_strategies, copy.deepcopy(self.bytecode))


    # filter by properties 
    def filter_by_labels(self, *labels, _and: typing.List[str]=None,
                         _or=typing.List[str], _not=typing.List[str] ):
        if labels.__len__() == 1: # for single label
            self.bytecode.add_step("hasLabel", labels[0])
        else: # fore more than one labels
            args =[__.hasLabel(label) for label in labels]
            self.bytecode.add_step("or", *args)

    def filter_by_properties(self, _and: PropertyFilterType=None, 
                          _or: PropertyFilterType=None, 
                          _not: PropertyFilterType=None,
                          condition_type: typing.Literal["or", "and", "not",]= "and",
                          **kwargs: PropertyFilterType ):
        """
        Example usage 
        {
            "code": {
                "startingWith": "AUS"
            },
            "_or": {
                "code": {
                    "within": ["AUS", "ANC", "MCO"]
                },
                "icao": {
                    "eq": "KTPA"
                }
            }
            # _and
        }

        """


        """
        
def hasKey(*args):
    return __.hasKey(*args)


def hasLabel(*args):
    return __.hasLabel(*args)


def hasNot(*args):
    return __.hasNot(*args)


def hasValue(*args):
    return __.hasValue(*args)




        Raises:
            Exception: _description_
            Exception: _description_
        """
        if kwargs.keys().__len__() == 0 and _and is None and  _or is None and _not is None:
            raise Exception("filter_by_properties() should be used with kwargs or ['_and', '_or', '_not']")

        filters = []
        for property_name, property_filter in kwargs.items():
            for filter_key, filter_value in property_filter.items():
                if filter_key not in SearchTextPredicate.keys():
                     raise Exception(
                        f"'{filter_key}' not allowed in search_kwargs. "
                        f"Only {SearchTextPredicate.keys()} are allowed")
                
                if getattr(SearchTextPredicate, filter_key):
                    filters.append(__.has(property_name, getattr(TextP, filter_key)(filter_value) ))
                elif getattr(SearchPredicates, filter_key):
                    filters.append(__.has(property_name, getattr(P, filter_key)(filter_value) ))
        
        if filters.__len__() > 0:
            if condition_type == "or":
                self.or_(*filters)
            elif condition_type == "and":
                self.and_(*filters)
            elif condition_type == "not":
                self.not_(*filters)

        if _and:
            self.filter_by_properties(**_and, condition_type="and")
        
        if _or:
            self.filter_by_properties(**_or, condition_type="or")

        if _not:
            self.filter_by_properties(**_not, condition_type="not")

    def filter_edges(self, **kwargs: RelationshipFiltersConfigType):
        if kwargs.keys().__len__() == 0:
            raise Exception("filter_edges() should have kwargs")   
        property_filters = kwargs.get("properties")

        # filter by labels
        labels = kwargs.get("labels")
        if labels:
            self.filter_by_labels(*labels)
    
        # filter by properties
        if property_filters:
            self.filter_by_properties(**property_filters)

        # filter:pagination
        paginate_options = kwargs.get("paginate")
        if paginate_options:
            self.paginate(**paginate_options)

    def filter_nodes(self, **kwargs: NodeFiltersConfigType):
        if kwargs.keys().__len__() == 0:
            raise Exception("filter_nodes() should have kwargs")
        property_filters = kwargs.get("properties")

        # filter by labels
        labels = kwargs.get("labels")
        if labels:
            self.filter_by_labels(*labels)
    
        # filter by properties
        if property_filters:
            self.filter_by_properties(**property_filters)

        # filter:pagination
        paginate_options = kwargs.get("paginate")
        if paginate_options:
            self.paginate(**paginate_options)

        return self
    
    def search_graph(self, **graph_traversal_config: GraphTraversalConfigType):
        
        for traversal_type, traversal_option in graph_traversal_config['g'].items():
            if traversal_type == "V":
                if "filters" in traversal_option:
                    self.V().filter_nodes(**traversal_option['filters'])
                if "traversals" in traversal_option:
                    # TODO - detect outE based on the starting key 
                    for traversal_type, traversal_config in traversal_option['traversals'].items():
                        if traversal_type == "out_e":
                            if "filters" in traversal_config:
                                self.outE().filter_edges(**traversal_config['filters'])
        
        return self
    # def traverse_through(self, *edge_labels,  direction=None, **edge_search_kwargs):
    #     if direction not in ["in", "out", None]:
    #         raise Exception("valid directions are 'in' or 'out' or None")
    #     if direction == "in":
    #         self.inE(*edge_labels)
    #     elif direction == "out":
    #         self.outE(*edge_labels)
    #     elif direction is None:
    #         self.bothE(*edge_labels)
    #     # self.inV()            
    #     # if neighbor_labels:
    #     #     _.hasLabel(*neighbor_labels)
    #     # return _.path().by(__.elementMap())            
    #     return self

    def paginate(self, page_size:int = 10, page_number: int= 1):
        self.bytecode.add_step("limit", page_size)
        pagination_args = [(page_size * (page_number - 1)), (page_size * page_number)]
        self.bytecode.add_step("range", *pagination_args)
        return self

    def create_vertex(self, label, **properties):
        self.addV(label)
        for k, v in properties.items():
            self.property(k, v)
        return self

    def create_edge(self, label, from_vtx_id, to_vtx_id, **properties):
        self.addE(label).from_(__.V(from_vtx_id)).to(__.V(to_vtx_id))
        for k, v in properties.items():
            self.property(k, v)
        return self

    def update_properties(self, **properties):
        for k, v in properties.items():
            self.property(k, v)
        return self


class __(AnonymousTraversal):
    graph_traversal: InvanaTraversal = InvanaTraversal

    @classmethod
    def filter_by_properties(cls, _and: PropertyFilterType=None, 
                          _or: PropertyFilterType=None, 
                          _not: PropertyFilterType=None,
                          condition_type: typing.Literal["or", "and", "not",]= "and",
                          **kwargs: PropertyFilterType ):
        return cls.graph_traversal(None, None, Bytecode()).filter_by_properties(
            _and=_and, _or=_or, _not=_not, condition_type=condition_type, **kwargs
        )

    @classmethod
    def filter_nodes(cls, **kwargs):
        return cls.graph_traversal(None, None, Bytecode()).filter_nodes(**kwargs)

    @classmethod
    def filter_edges(cls, **kwargs):
        return cls.graph_traversal(None, None, Bytecode()).filter_edges(**kwargs)

    @classmethod
    def search_graph(cls, **kwargs):
        return cls.graph_traversal(None, None, Bytecode()).search_graph(**kwargs)

    # @classmethod
    # def traverse_through(cls, *edge_labels,  direction=None, **edge_search_kwargs):
    #     return cls.graph_traversal(None, None, Bytecode()) \
    #         .traverse_through(*edge_labels,  direction=direction, **edge_search_kwargs)

    # @classmethod
    # def to(cls,  *vertex_labels, **vertex_search_kwargs):
    #     return cls.graph_traversal(None, None, Bytecode()) \
    #         .to( *vertex_labels, **vertex_search_kwargs)

    @classmethod
    def paginate(cls, *kwargs):
        return cls.graph_traversal(None, None, Bytecode()).paginate(*kwargs)

    @classmethod
    def create_vertex(cls, label, **properties):
        return cls.graph_traversal(None, None, Bytecode()).create_vertex(label, **properties)

    @classmethod
    def create_edge(cls, label, from_vtx_id, to_vtx_id, **properties):
        return cls.graph_traversal(None, None, Bytecode()).create_edge(label, from_vtx_id, to_vtx_id,
                                                                       **properties)
    @classmethod
    def update_properties(cls, **properties):
        return cls.graph_traversal(None, None, Bytecode()).update_properties(**properties)



class InvanaTraversalSource(GraphTraversalSource):
    def __init__(self, *args, **kwargs):
        super(InvanaTraversalSource, self).__init__(*args, **kwargs)
        self.graph_traversal = InvanaTraversal

    def get_graph_traversal(self) -> InvanaTraversal:
        return self.graph_traversal(self.graph, self.traversal_strategies, Bytecode(self.bytecode))

    def create_vertex(self, label, **properties):
        traversal = self.get_graph_traversal()
        traversal.create_vertex(label, **properties)
        return traversal

    def create_edge(self, label, from_vtx_id, to_vtx_id, **properties):
        traversal = self.get_graph_traversal()
        traversal.create_edge(label, from_vtx_id, to_vtx_id, **properties)
        return traversal
    
    def filter_nodes(self, **kwargs):
        traversal = self.get_graph_traversal()
        traversal.filter_nodes(**kwargs)
        return traversal

    def filter_edges(self, **kwargs: RelationshipFiltersConfigType):
        traversal = self.get_graph_traversal()
        traversal.filter_edges(**kwargs)
        return traversal
    
    def search_graph(self, **kwargs: GraphTraversalConfigType):
        traversal = self.get_graph_traversal()
        traversal.search_graph(**kwargs)
        return traversal
    
    def paginate(self, **kwargs):
        traversal = self.get_graph_traversal()
        traversal.paginate(**kwargs)
        return traversal
