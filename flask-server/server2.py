from json import dumps
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
    def work(tx, limit):
        return list(tx.run(
            "MATCH (n)-[r]->(m) "
            "RETURN n, r, m "
            "LIMIT $limit",
            {"limit": limit}
        ))

    db = get_db()
    results = db.read_transaction(work, request.args.get("limit", 100))
    return results


if __name__ == "__main__":
    app.run(port=8000, debug=True)
    # uri = "neo4j+s://34a4cf44.databases.neo4j.io"
    # user = "neo4j"
    # password = "Eds0XFkwVJGVvRuE8U9D907u1KQiLWVfj14L6ynD7iA"
    # trans = Transaction(uri, user, password)
    # trans.load_csv()
    # trans.read_transactions()
    # trans.close()
