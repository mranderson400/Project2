import sqlite3

class SQLiteConnection:
    def __init__(self, db):
        self.connection = sqlite3.connect(db)
        self.connection.row_factory = sqlite3.Row 

    def query_db(self, query, data=None):
        with self.connection as conn:
            cursor = conn.cursor()
            try:
                query = query % data if data else query  
                print("Running Query:", query)

                cursor.execute(query)
                if query.lower().find("insert") >= 0:
                    conn.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    return cursor.fetchall()
                else:
                    conn.commit()
            except Exception as e:
                print("Something went wrong", e)
                return False

def connectToSQLite(db):
    return SQLiteConnection(db)
