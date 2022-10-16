from flask import Flask
from neo4j import GraphDatabase, basic_auth
import logging
from neo4j.exceptions import ServiceUnavailable
from models import Transaction

app = Flask(__name__)


@app.route("/test")
def try_func():
    print("try func")
    uri1 = "neo4j+s://34a4cf44.databases.neo4j.io"
    user1 = "neo4j"
    password1 = "Eds0XFkwVJGVvRuE8U9D907u1KQiLWVfj14L6ynD7iA"
    trans = Transaction(uri1, user1, password1)
    trans.load_csv()
    trans.read_transactions()
    trans.close()
    return {"members": ["1", "2", "3"]}


if __name__ == "__main__":
    # uri = "neo4j+s://34a4cf44.databases.neo4j.io"
    # user = "neo4j"
    # password = "Eds0XFkwVJGVvRuE8U9D907u1KQiLWVfj14L6ynD7iA"
    # trans = Transaction(uri, user, password)
    # trans.load_csv()
    # trans.read_transactions()
    # trans.close()
    app.run(port=8000, debug=True)





