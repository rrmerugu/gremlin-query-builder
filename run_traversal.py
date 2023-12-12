from graph_search.graph_search import GraphSearch
import yaml
from graph_search.traversals import __
from gremlin_python.process.translator import Order


search = GraphSearch("ws://localhost:8182/gremlin")

example_configs = [
    # "examples/airport-dataset/oute_traversal.yml",
    # "examples/airport-dataset/simple_nodes_filters.yml",
    # "examples/airport-dataset/nodes_traversals_count_filters.yml",
    # "examples/airport-dataset/nodes_traversals_all_filters.yml",
    "examples/airport-dataset/nodes_traversals.yml"
]


for traversal_config_file in example_configs:
    traversal_config = yaml.safe_load(open(traversal_config_file))
    result = search.search_graph(traversal_config)
    bytecode =result.bytecode
    if "nodes_traversals_count_filters" in  traversal_config_file:
        print("====query", query)
        result = result.project('v','e').by(__.id()).by(__.outE().count())\
        .toList()  
        # result = result.toList()

        # .order().by("e", Order.desc) \
    elif "nodes_traversals_all_filters" in  traversal_config_file:
        # result = result.project('v','e').by(__.id()).by(__.outE().count())\
        # .toList()  
        # result = result.project('v','e').by(__.id()).by(__.outE())\
        # result = result.toList()  
        query = result.bytecode
        print("====query", query)
        # result = result.project('v','e').by(__.id()).by(__.outE().count())\
        # .toList()
        result = result.count()\
        .toList()
        # result = result.count().toList()  
    else:
        result = result.toList()
    print("\n\n\n")
    print(f"={traversal_config_file}============================================")
    for r in result:
        print("*",r, "\n------")
    print("=END=====total count", result.__len__(), "=============================")
    print("===query", bytecode)

search.connection.close()
