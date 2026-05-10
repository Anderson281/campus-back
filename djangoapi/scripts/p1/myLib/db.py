import psycopg
from psycopg.rows import dict_row

from myLib import p1Settings as settings
class Db:
    def __init__(self, autoCommit=True, autoPrintResults=True, getRowsAsDicts=True):
        """Create a connection to the database
        autoCommit: if True, the connection will commit the
        changes automatically. If False, the connection will
        need to be committed manually
        autoPrintResults: if True, the connection will print the
        results of the query automatically. If False, the
        results will not be printed
        """
        self.getRowsAsDicts=getRowsAsDicts
        self.conn = psycopg.connect(
            dbname=settings.POSTGRES_DB,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT
        )
        self.autoPrintResults = autoPrintResults
        self.autoCommit = autoCommit

        if self.getRowsAsDicts:
            self.cursor = self.conn.cursor(row_factory=dict_row)
        else:
            self.cursor = self.conn.cursor()
        
        self.result = None
        print("Connected to database")

    def query(self, query, params=None):
        """
        Execute a query and return the results
            eg. query("SELECT * FROM table WHERE area > %s and owner
                like %s", [100], [’%Smith%’]))
        
        query: the query to execute. Use %s as a placeholder for
        
        parameters. Eg. "SELECT * FROM table WHERE area > %s
                and owner like %s"
            
        params: the parameters to pass to the query in a list.
                Eg. [100, ’%Smith%’]
        
        return: the results of the query in a list. Eg. [(1, ’
                Smith’, 200), (2, ’Smith’, 300)]
        """
        self.cursor.execute(query, params)
        if self.autoCommit:
            self.conn.commit()
        #insert or select put result in cursor.fetchall(),
        # but update and delete do not.
        #update and delete put something in cursor.rowcount
        # but insert or select do not
        #So we have to manage this:
        if "insert" in query.lower() or "select" in query.lower():
            self.result = self.cursor.fetchall()
        else:
        #operations update and delete
            self.result = self.cursor.rowcount
        if self.autoPrintResults:
            self.printResult()

    def disconnect(self):
        """Disconnect from the database
        Disconnect from the database. This should be called when
        the connection is no longer needed.
        There is a maximum number of connections that can be
        made to the database, so it is important to
        disconnect when the connection is no longer needed.
        """
        self.cursor.close()
        self.conn.close()
        print("Disconnected from database")
    
    def printResult(self):
        print(self.result)

    def __del__(self):
        """ Destructor. Disconnect from the database.
        On destruction of the object, disconnect from the
        database.
        This is automatically called when the object is deleted,
        eg. when the program ends.
        """
        self.cursor.close()
        self.conn.close()
        print("Disconnected from database")