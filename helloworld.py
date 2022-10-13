from neo4j import GraphDatabase

class Transaction:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    '''
    Test writing to database

        def print_greeting(self, message):
            with self.driver.session() as session:
                greeting = session.execute_write(self._create_and_return_greeting, message)
                print(greeting)

        @staticmethod
        def _create_and_return_greeting(tx, message):
            result = tx.run("CREATE (a:Greeting) "
                            "SET a.message = $message "
                            "RETURN a.message + ', from node ' + id(a)", message=message)
            return result.single()[0]
    '''

    def load_csv(self):
        with self.driver.session() as session:
            greeting = session.execute_write(self._load)

    @staticmethod
    def _load(tx):
        result = tx.run("LOAD CSV FROM 'file:///transactions.csv' AS row "
                        "RETURN count(row)")
        
        # TODO: test if this works
        # result = tx.run("LOAD CSV WITH HEADERS FROM 'file:///transactions.csv' AS csvLine "
        #                 "WITH csvLine LIMIT 300 "
        #                 "MATCH (from_address:From_address {add: csvLine.from_address}) "
        #                 "MATCH (to_address:To_address {add: csvLine.to_address}) "
        #                 "MERGE (from_address)-[rel:SEND_TO {value: csvLine.value}]->(to_address)")

        print(result.peek())
        return result.peek()


    def read_transactions(self):
        with self.driver.session() as session:
            transactions = session.execute_read(self._get_transactions)
            # for record in transactions:
            #     print(record["n"])
    
    @staticmethod
    def _get_transactions(tx):
        result = tx.run("""
            MATCH (n)-[r]->(m)
            RETURN n, r, m
        """)
        peek = result.peek()
        print(peek)
        return result.values()

if __name__ == "__main__":
    greeter = Transaction("bolt://localhost:7687", "neo4j", "neo")
    # greeter.print_greeting("hello, world")
    greeter.load_csv()
    greeter.read_transactions()
    greeter.close()