from flask import Flask, request
from neo4j import GraphDatabase, basic_auth
import logging
from neo4j.exceptions import ServiceUnavailable
from models import Transaction

app = Flask(__name__)


@app.route("/load")
def load_func():
    uri1 = "neo4j+s://34a4cf44.databases.neo4j.io"
    user1 = "neo4j"
    password1 = "Eds0XFkwVJGVvRuE8U9D907u1KQiLWVfj14L6ynD7iA"
    trans = Transaction(uri1, user1, password1)
    trans.load_csv()
    trans.close()
    return '''
                  load csv successfully'''

@app.route("/transactions")
def transaction_func():
    uri1 = "neo4j+s://34a4cf44.databases.neo4j.io"
    user1 = "neo4j"
    password1 = "Eds0XFkwVJGVvRuE8U9D907u1KQiLWVfj14L6ynD7iA"
    trans = Transaction(uri1, user1, password1)
    return trans.read_transactions()

@app.route("/cypher", methods=['GET', 'POST'])
def cypher_func():
    if request.method == 'POST':
        cypher = request.form.get('statement')
        uri1 = "neo4j+s://34a4cf44.databases.neo4j.io"
        user1 = "neo4j"
        password1 = "Eds0XFkwVJGVvRuE8U9D907u1KQiLWVfj14L6ynD7iA"
        trans = Transaction(uri1, user1, password1)
        result = trans.pass_cypher(cypher)
        print(result)
        return '''
                  <h1>The statement is: {}</h1>'''.format(cypher)
    return '''
              <form method="POST">
                  <div><label>Cypher: <input type="text" name="statement"></label></div>
                  <input type="submit" value="Submit">
              </form>'''

if __name__ == "__main__":
    app.run(port=8000, debug=True)





