# from dataclasses import dataclass
# from gremlin_python.structure.graph import Vertex, Edge, Path


# @dataclass
# class Node:
#     data: Vertex = None

#     def __repr__(self) -> str:
#         id = self.data.id
#         return f"<Node {self.data.label}:{id}>"

# @dataclass
# class Relationship:
#     data: Edge = None

#     def __repr__(self) -> str:
#         id = self.data.id['@value']['relationId']
#         return f"<Relationship {self.data.label}:{id}>"
    
# # def create_graph_objects(result):
# #     result_ = []
# #     for res in result:
# #         if isinstance(res, Edge):
# #             result_.append(Relationship(res))
# #         elif isinstance(res, Vertex):
# #             result_.append(Node(res))
# #         else:
# #             raise Exception()
# #     return result_