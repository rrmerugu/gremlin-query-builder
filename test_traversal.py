# import sys
# sys.path.append("../")
from graph_search.graph_search import GraphSearch
import yaml

search = GraphSearch("ws://localhost:8182/gremlin")

# traversal_config = {
#     "g": {
#         "V": { # create orderede dictionary in order "filters", "traverse"
#             "filters": {
#                 # filter by ids 
#                 # "ids": [],

#                 # filter by has key
#                 # filter by has value

#                 # filter on labels
#                 "labels": ["airport", "country"],

#                 # filter on properties
#                 "properties": {
#                     # 
#                     "code": {
#                         "startingWith": "AUS"
#                     },
#                     "_or": {
#                         "code": {
#                             "within": ["AUS", "ANC", "MCO"]
#                         },
#                         "icao": {
#                             "eq": "KTPA"
#                         }
#                     }
#                     # _and
#                 },

#                 # filter based on relationships and relationships count 

#                 #

#                 # paginate
#                 "paginate": {
#                     "page_size": 20, 
#                     "page_number": 1
#                 }
#             },
#             "traversals": {
#                 # out_e, in_e, both_e, out_v, in_v, both_v, out, in
#                 "out_e": {
#                     "filters": {
#                         "labels": ["route"],
#                         "properties": {
#                             "dist": {
#                                 "between": (700, 900)
#                             },
#                             "_or": {
#                                 "dist": {
#                                     "between": (350, 600)
#                                 },
#                             }
#                         }
#                     }
               
#                 }
#             }
#         }
#     }

# }

traversal_config_str = """
---
g:
  V:
    filters:
      labels:
      - airport
      - country
      properties:
        code:
          startingWith: AUS
        _or:
          code:
            within:
            - AUS
            - ANC
            - MCO
          icao:
            eq: KTPA
      paginate:
        page_size: 20
        page_number: 1
    traversals:
      out_e:
        filters:
          labels:
          - route
          properties:
            dist:
              between: [300, 700]
            # _or:
            #   dist:
            #     between: 2

"""

traversal_config = yaml.safe_load(traversal_config_str)
result = search.search_graph(traversal_config)
print("===result", result)
print("=====count", result.__len__())

import ast

ast.parse