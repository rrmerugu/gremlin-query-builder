from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection as _DriverRemoteConnection
from gremlin_python.process.anonymous_traversal import traversal
from .type_defs import GraphTraversalConfigType
from .traversals import  InvanaTraversalSource, InvanaTraversal, __
from .graphson_reader import INVANA_DESERIALIZER_MAP
from gremlin_python.structure.io.graphsonV3d0 import GraphSONReader, GraphSONWriter
from gremlin_python import __version__


class DriverRemoteConnection(_DriverRemoteConnection):

    @property
    def client(self):
        return self._client


class GraphSearch:

    def __init__(self, connection_url, transport_factory=None) -> None:
        self.connection_url = connection_url
        self.deserializer_map = INVANA_DESERIALIZER_MAP
        self.connection = DriverRemoteConnection(
            self.connection_url,  'g',
            graphson_reader=GraphSONReader(deserializer_map=self.deserializer_map),
            graphson_writer=GraphSONWriter(),
            transport_factory=transport_factory
        )
        print(f"Graphsearch is using gremlinpython=={__version__.version}")

    @property
    def graph(self) -> InvanaTraversal: # this will generate the `g`       
        return traversal(traversal_source_class=InvanaTraversalSource) \
                        .withRemote(self.connection)
 
    def search_graph(self, graph_traversal_config: GraphTraversalConfigType)-> InvanaTraversal:
        return self.graph.search_graph(**graph_traversal_config)
 