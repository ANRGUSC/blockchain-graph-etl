from neo4j import GraphDatabase
import json

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
            return transactions

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

        print("test########")
        insert_query_guest = '''
            MATCH (a:From_address)
            WITH collect({add: a.add, nodeType:'from'}) AS nodes RETURN nodes
            '''

        result = tx.run(insert_query_guest)
        for record in result:
            guest_node = json.dumps(dict(record))
            break

        guest_nodes = str(guest_node)[1:][:-2]

        insert_query_guest = '''
            MATCH (a:From_address)-[r:SEND_TO]->(b:To_address)
            WITH collect({source: a.add, target: b.add, value:r.value}) AS edges RETURN edges
            '''
        result = tx.run(insert_query_guest)
        for record in result:
            create_guest_edge = json.dumps(dict(record))
            break

        guest_edges = str(create_guest_edge)[1:]

        insert_query_guest = '''
            MATCH (a:To_address)
            WITH collect({add: a.add, nodeType:'to'}) AS nodes RETURN nodes
            '''

        result = tx.run(insert_query_guest)
        for record in result:
            create_event_node = json.dumps(record['nodes'])
            break

        event_node = str(create_event_node) + ']'

        graphjson = str(guest_nodes) + ', ' + str(event_node) + ',' + str(guest_edges)

        print(graphjson)

        return graphjson

    @staticmethod
    def get_trans_test(tx):
        print("get transactions")
        result = tx.run("""
                MATCH (n)-[r]->(m)
                RETURN n, r, m
                LIMIT 100
            """)
        return result

