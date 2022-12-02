neo4j_cluster_alchemy
=====================

Alchemy.js Documentation
- Process begins with extracting data out of the Neo4j database. 
- You can build a cypher query by calling alchemy.plugins.neo4jBackend.buildQuery(input,queryType), where queryType is the key of the query template to use that is defined in the query key of the configuration. 
- This will return a cypher statement which you can then pass into alchemy.plugins.neo4jBackend.runQuery(cypherStatement [, callback] ).
- Passing in just a cypher statement and no callback will run your cypher query and update the alchemy graph with the results.
- If we wish to modify/view the date before updating the graph, you can pass a callback to which receive the returned graph.JSON for us to work with. 
- This all will stop automatic graphUpdating, hence afterwards we will need to call the alchemy.plugins.neo4jBackend.updateGraph()

Configuration 
- Url to neo4j can be configured with the “url” key in the configuration file.
- If it is running locally on some default port, then we do not have to configure anything explicitly.

Run Instructions
```
cd into directory
python -m SimpleHTTPServer
```

http://localhost:8000/graph.html
