from dataclasses import dataclass
import typing
# from graph_search.constants import SearchPredicates, SearchTextPredicate

 
ValidSearchPredicateTypes = str # typing.Literal[..., SearchTextPredicate.keys() ]

PropertyFilterType = typing.Dict[str, typing.Dict[
            ValidSearchPredicateTypes,
            typing.Union[str, int, float, typing.List[int], typing.List[str] ]
        ]
    ]


class NodeFiltersConfigType:
    labels: typing.List[str]
    properties: PropertyFilterType


class RelationshipFiltersConfigType:
    labels: typing.List[str]
    properties: typing.Dict[str, typing.Dict[
            ValidSearchPredicateTypes,
            typing.Union[str, int, float, typing.List[int], typing.List[str] ]]
        ]
    

class NodeTraversalType:
    filters: NodeFiltersConfigType


class RelationshipTraversalType:
    filters: RelationshipFiltersConfigType


class GraphTraversalOptionsType(typing.TypedDict):
    V : NodeTraversalType
    E : RelationshipTraversalType


class GraphTraversalConfigType:
    g : GraphTraversalOptionsType

