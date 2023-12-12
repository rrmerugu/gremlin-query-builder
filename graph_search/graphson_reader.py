#    Copyright 2021 Invana
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#     http:www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.
#
from gremlin_python.structure.io import graphsonV3d0
from gremlin_python.structure.graph import VertexProperty, Property
from gremlin_python.process.traversal import T, Direction
from .structure import RelationShip, Node, Path
import typing


def get_id(_id):
    if isinstance(_id, dict):
        if isinstance(_id.get('@value'), dict) and _id.get("@value").get('relationId'):
            return _id.get('@value').get('relationId')
        else:
            return _id.get('@value')
    return _id

def convert_vertex_properties_to_dict(properties: typing.List[VertexProperty]):
    data = {}
    for prop in properties:
        data[prop.label] = prop.value
    return data

def convert_edge_properties_to_dict(properties: typing.List[Property]):
    data = {}
    for prop in properties:
        data[prop.key] = prop.value
    return data


class InvanaMapType(graphsonV3d0.MapType):

    @staticmethod
    def create_node_object(dict_data):
        _ = dict_data.copy()
        node_id = get_id(_[T.id])
        node_label = _[T.label]
        del _[T.id]
        del _[T.label]
        return Node(node_id, node_label, properties=_)

    @staticmethod
    def create_relationship_object(dict_data):
        _ = dict_data.copy()
        node_id = get_id(_[T.id])
        node_label = _[T.label]
        inv = _[Direction.IN]
        outv = _[Direction.OUT]
        del _[T.id]
        del _[T.label]
        del _[Direction.IN]
        del _[Direction.OUT]
        return RelationShip(node_id, node_label, outv, inv, properties=_)

    @classmethod
    def objectify(cls, l, reader):
        new_dict = super(InvanaMapType, cls).objectify(l, reader)
        if T.id in new_dict and Direction.IN not in new_dict:
            return cls.create_node_object(new_dict)
        if T.id in new_dict and Direction.IN in new_dict:
            return cls.create_relationship_object(new_dict)
        return new_dict


class InvanaVertexDeserializer(graphsonV3d0.VertexDeserializer):

    @classmethod
    def objectify(cls, d, reader):
        properties = []
        for prop_key, prop_value in d.get("properties", {}).items():
            properties.extend(reader.to_object(prop_value))

        return Node(reader.to_object(get_id(d["id"])),
                    d.get("label", "vertex"),
                    properties=convert_vertex_properties_to_dict(properties))


class InvanaEdgeDeserializer(graphsonV3d0.EdgeDeserializer):

    @classmethod
    def objectify(cls, d, reader):
        properties = []
        for prop_key, prop_value in d.get("properties", {}).items():
            properties.append(reader.to_object(prop_value))

        return RelationShip(reader.to_object(get_id(d["id"])),
                            d.get("label", "edge"),
                            Node(reader.to_object(d["outV"]), d.get("outVLabel", "vertex")),
                            Node(reader.to_object(d["inV"]), d.get("inVLabel", "vertex")),
                            properties=convert_edge_properties_to_dict(properties))


class InvanaPathDeserializer(graphsonV3d0.PathDeserializer):

    @classmethod
    def objectify(cls, d, reader):
        return Path(reader.to_object(d["labels"]), reader.to_object(d["objects"]))


# class PropertyDeserializer(graphsonV3d0.PropertyDeserializer):
#
#     @classmethod
#     def objectify(cls, d, reader):
#         element = reader.to_object(d["element"]) if "element" in d else None
#         return Property(d["key"], reader.to_object(d["value"]), element)


INVANA_DESERIALIZER_MAP = {
    "g:Map": InvanaMapType,
    "g:Vertex": InvanaVertexDeserializer,
    "g:Edge": InvanaEdgeDeserializer,
    "g:Path": InvanaPathDeserializer,

    # "g:Property": InvanaEdgeDeserializer,
}
