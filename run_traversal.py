from graph_search.graph_search import GraphSearch
import yaml
from graph_search.traversals import __


search = GraphSearch("ws://localhost:8182/gremlin")

example_configs = [
    # "examples/airport-dataset/oute_traversal.yml",
    # "examples/airport-dataset/simple_nodes_filters.yml",
    "examples/airport-dataset/nodes_traversals_filters.yml"
]


for traversal_config_file in example_configs:
    traversal_config = yaml.safe_load(open(traversal_config_file))
    result = search.search_graph(traversal_config)\
        


    print("============================================")
    for r in result:
        print("*",r, "\n------")
    print("============================================")
    print("=====total count", result.__len__())
 