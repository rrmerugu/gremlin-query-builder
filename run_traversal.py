from graph_search.graph_search import GraphSearch
import yaml
from graph_search.traversals import __
from gremlin_python.process.translator import Order


search = GraphSearch("ws://localhost:8182/gremlin")

example_configs = [
    # "examples/airport-dataset/oute_traversal.yml",
    # "examples/airport-dataset/simple_nodes_filters.yml",
    "examples/airport-dataset/nodes_traversals_count_filters.yml"
    # "examples/airport-dataset/nodes_traversals_all_filters.yml"
]


for traversal_config_file in example_configs:
    traversal_config = yaml.safe_load(open(traversal_config_file))
    result = search.search_graph(traversal_config)
    if "nodes_traversals_count_filters" in  traversal_config_file:
        query = result.bytecode
        print("====query", query)
        result = result.project('v','e').by(__.id()).by(__.outE().count())\
        .order().by("e", Order.desc).toList()  
    elif "nodes_traversals_all_filters" in  traversal_config_file:
        # result = result.project('v','e').by(__.id()).by(__.outE().count())\
        # .toList()  
        # result = result.project('v','e').by(__.id()).by(__.outE())\
        # result = result.toList()  
        result = result.outE().toList()
    else:
        result = result.toList()
    print("\n\n\n")
    print(f"={traversal_config_file}============================================")
    for r in result:
        print("*",r, "\n------")
    print("=END=====total count", result.__len__(), "=============================")
 
search.connection.close()
