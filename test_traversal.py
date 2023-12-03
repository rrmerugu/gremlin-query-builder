# import sys
# sys.path.append("../")
from graph_search.graph_search import GraphSearch

search = GraphSearch("ws://localhost:8182/gremlin")

traversal_config = {
    "g": {
        "V": { # create orderede dictionary in order "filters", "traverse"
            "filters": {
                # filter by ids 
                # "ids": [],

                # filter by has key

                # filter on labels
                "labels": ["airport", "country"],

                # filter on properties
                "properties": {
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
                },

                # paginate
                "paginate": {
                    "page_size": 20, 
                    "page_number": 1
                }
            },
            # "traversals": {
            #     "oute": 
            # }
        }
    }

}

result = search.search_graph(traversal_config)
print("===result", result)