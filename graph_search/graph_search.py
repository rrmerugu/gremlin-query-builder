from gremlin_python.process.traversal import TextP, P
# from gremlin_python.process.graph_traversal import __
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection as _DriverRemoteConnection
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.structure.graph import Graph
from gremlin_python.process.anonymous_traversal import traversal
from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
# from graph_search.elements import create_graph_objects
from .type_defs import GraphTraversalConfigType, NodeFiltersConfigType
from .traversals import  InvanaTraversalSource, InvanaTraversal, __
from .graphson_reader import INVANA_DESERIALIZER_MAP
from gremlin_python.structure.io.graphsonV3d0 import GraphSONReader


class DriverRemoteConnection(_DriverRemoteConnection):

    @property
    def client(self):
        return self._client


class GraphSearch:

    # https://github.com/apache/tinkerpop/blob/095718617e0f94f92545e0ac077ca0ab189d6b7f/docs/src/reference/gremlin-variants.asciidoc#domain-specific-languages-4
    #https://github.com/apache/tinkerpop/blob/095718617e0f94f92545e0ac077ca0ab189d6b7f/gremlin-python/src/main/python/gremlin_python/process/graph_traversal.py#L994
    def __init__(self, connection_url, ) -> None:
        self.connection_url = connection_url
        self.deserializer_map = INVANA_DESERIALIZER_MAP

        self.connection = DriverRemoteConnection(
            self.connection_url,  'g',
            graphson_reader=GraphSONReader(deserializer_map=self.deserializer_map),
        )

        self.g: InvanaTraversal = traversal(traversal_source_class=InvanaTraversalSource) \
                        .withRemote(self.connection)
 
    def search_graph(self, traversal_config: GraphTraversalConfigType):
        for traversal_type, traversal_option in traversal_config['g'].items():
            if traversal_type == "V":
                if "filters" in traversal_option:
                    g_ = self.g.V().filter_nodes(**traversal_option['filters'])

        _ = g_.toList()
        # _ = self.g.V().limit(1).outE().toList()
        # _ = g_.outE().limit(10).elementMap().toList()
# 
        self.connection.close()
        return _
        # return create_graph_objects(_)
   