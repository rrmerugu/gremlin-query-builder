# Gremlin Query Pattern Notes



```python
# generate path with `elementMap`
graph_search.graph.V().has('code', 'BNA').outE().inV().path().by(__.elementMap()).toList()
```

```python
# using `select` and `project`
graph_search.graph.V().limit(5).limit(100).dedup().as_('node') \
.project('id', 'label', 'properties', 'edges') \
.by(__.id()) \
.by(__.label()) \
.by(__.valueMap().by(__.unfold())) \
.by( \
    __.outE().project('id', 'from', 'to', 'label', 'properties') \
    .by(__.id()) \
    .by(__.select('node').id()) \
    .by(__.inV().id()) \
    .by(__.label()) \
    .by(__.valueMap().by(__.unfold())).fold() \
).toList()
```

```python
# 
graph_search.graph.V().limit(5).project('v','e').by().by(__.outE().count()).toList()
```