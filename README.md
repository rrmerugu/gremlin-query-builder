# Query builder

The purpose of this project is to convert traversal config(filters and traversals)
to cypher and gremlin queries.



```
 

```




## Traversal 


# Invana Search Engine 

1. filter data
2. Create Traverals from the filtered data 



```yaml
# using traverseTo
g:
  V:
    properties:
      id
      first_name
    filters:
      labels:
        - Person
    traversals:
      oute:
        V: 
        
      labels:
        - Tweets
    limit: 10
    order:
      name: ASC

```



```yaml
# using traverseTo
g:
  filterV:
    labels:
      - Person
  traverseTo: # direction is to right side always 
    labels:
      - Tweets
    limit: 10
    order:
      name: ASC

```

```yaml
# using traverseVia
g:
  filterV:
    labels:
      - Person
  traverseVia:
    labels:
      - tweeted
    limit: 10
    to:
      labels:
        - Tweets
      order:
        name: ASC
    

```



```yaml
# using traverseVia
g:
  filterV:
    labels:
      - Person
  traverseVia:
    labels:
      - tweeted
    limit: 10
    out:
      labels:
        - Tweets
      order:
        name: ASC
    in:
      labels:
        - Person
    

```


```

g.filterV(labels=["Person"]).traverseTo()

g.filterV(labels=["Person"]).traverseVia(labels=["ACTED_IN"])

```


## traversal config example
```json

{
  "Actor": {
    "Properties": {
      "screen_name": true,
      "last_name": true,
      "first_name": true
    },
    "oute__ACTIN_IN": {
      "Id": true,
      "Label": true,
      "direction" : "OUT",
      "Properties": {
        "title": true,
        "published_date": true
      },
      "Movie": {
        "Id": true,
        "Label": true,
        "Properties": {
          "published_date": true,
          "title": true
        }
      }
    }
  }
}

```