from neo4j import GraphDatabase


class Transaction:
    def __init__(self, uri, user, password):
        print("init")
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        print("close")
        self.driver.close()

    def load_csv(self):
        print("load csv")
        with self.driver.session() as session:
            greeting = session.execute_write(self._load)

    @staticmethod
    def _load(tx):
        print("load")
        result = tx.run("LOAD CSV WITH HEADERS FROM 'https://docs.google.com/spreadsheets/d/1vad0A3sJjP6WWv3_CGDJN9Oib8KuEpfHLvR66ikNkvE/gviz/tq?tqx=out:csv'"
                        " AS csvLine "
                        "WITH csvLine LIMIT 300 WHERE csvLine.from_address IS NOT NULL AND csvLine.to_address IS NOT NULL "
                        "MERGE (from_address:From_address {add: csvLine.from_address}) "
                        "MERGE (to_address:To_address {add: csvLine.to_address }) "
                        "MERGE (from_address)-[rel:SEND_TO {value: csvLine.value}]->(to_address)")
        return result.peek()

    def read_transactions(self):
        with self.driver.session() as session:
            transactions = session.execute_read(self._get_transactions)
            # for record in transactions:
            #     print(record["n"])

    @staticmethod
    def _get_transactions(tx):
        print("get transactions")
        result = tx.run("""
            MATCH (n)-[r]->(m)
            RETURN n, r, m
        """)
        peek = result.peek()
        print(peek["n"])
        print(peek["m"])
        print(peek["r"])
        return result.values()