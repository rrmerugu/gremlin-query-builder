from graph_search.graph_search import GraphSearch
import yaml


search = GraphSearch("ws://localhost:8182/gremlin")

# traversal_config_file = "examples/airport-dataset/oute_traversal.yml"
traversal_config_file = "examples/airport-dataset/simple_nodes_filters.yml"


traversal_config = yaml.safe_load(open(traversal_config_file))
result = search.search_graph(traversal_config)

print("============================================")
for r in result:
    print("*",r, "\n------")
print("============================================")
print("=====total count", result.__len__())
 