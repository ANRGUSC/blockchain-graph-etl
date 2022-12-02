from json import dumps
from flask_cors import CORS
import logging
import os

from flask import (
    Flask,
    g,
    request,
    Response,
)


from neo4j import (
    GraphDatabase,
    basic_auth,
)


app = Flask(__name__)
CORS(app)

url = "neo4j+s://34a4cf44.databases.neo4j.io"
username = "neo4j"
password = "Eds0XFkwVJGVvRuE8U9D907u1KQiLWVfj14L6ynD7iA"
neo4j_version = "4"
database = "neo4j"

driver = GraphDatabase.driver(url, auth=basic_auth(username, password))


def get_db():
    if not hasattr(g, "neo4j_db"):
        if neo4j_version >= "4":
            g.neo4j_db = driver.session(database=database)
        else:
            g.neo4j_db = driver.session()
    return g.neo4j_db


@app.route("/graph")
def get_graph():
    print("get_graph() func")
    def work(tx, limit):
        return list(tx.run(
            "MATCH (n)-[r]->(m) "
            "RETURN n AS from_add, r AS values, m AS to_add "
            "LIMIT $limit",
            {"limit": limit}
        ))

    db = get_db()
    results = db.read_transaction(work, request.args.get("limit", 100))
    nodes = []
    rels = []
    i = 0
    for record in results:
        print("--RECORD--")
        print(record)
        #print("from: " + record["from_add"]._properties["add"])
        nodes.append({"title": record["from_add"]._properties["add"], "label": "from_add"})
        target = i
        i += 1
        for name in record["to_add"]:
            # print("to: " + record["to_add"]._properties["add"])
            print("---VALUES---")
            print(record["values"])
            print(record["values"]._properties["value"])
            actor = {"title": record["to_add"]._properties["add"], "label": "to_add"}
            try:
                source = nodes.index(actor)
            except ValueError:
                nodes.append(actor)
                source = i
                i += 1
            rels.append({"source": source, "value": record["values"]._properties["value"] , "target": target})
    return Response(dumps({"nodes": nodes, "links": rels}),
                    mimetype="application/json")

@app.route("/cypher", methods=['GET', 'POST'])
def cypher_func():
    if request.method == 'POST':
        cypher = request.form.get('statement')
        print("get_cypher() func")

        def work(tx, limit):
            return list(tx.run(
                cypher +
                " LIMIT $limit",
                {"limit": limit}
            ))

        db = get_db()
        results = db.read_transaction(work, request.args.get("limit", 100))
        nodes = []
        rels = []
        i = 0
        for record in results:
            print("--RECORD--")
            print(record)
            #print("from: " + record["from_add"]._properties["add"])
            nodes.append({"title": record["from_add"]._properties["add"], "label": "from_add"})
            target = i
            i += 1
            for name in record["to_add"]:
                #print("to: " + record["to_add"]._properties["add"])
                print("---VALUES---")
                print(record["values"])
                print(record["values"]._properties["value"])
                actor = {"title": record["to_add"]._properties["add"], "label": "to_add"}
                try:
                    source = nodes.index(actor)
                except ValueError:
                    nodes.append(actor)
                    source = i
                    i += 1
                rels.append({"source": source, "value": record["values"]._properties["value"] , "target": target})
        return Response(dumps({"nodes": nodes,"links": rels}),
                        mimetype="application/json")
    return '''
                <form method="POST">
              <div><label>Cypher: <textarea name="statement" rows="4" cols="50"></textarea></label></div>
              <p></p >
              <input type="submit" value="Submit">
            </form>'''








if __name__ == "__main__":
    app.run(port=8000, debug=True)







